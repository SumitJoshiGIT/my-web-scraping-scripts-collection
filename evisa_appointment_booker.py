#evisa.py

import asyncio
from playwright.async_api import async_playwright, TimeoutError
from playwright_stealth import stealth_async
import datetime
import json
import urllib
import pydub
from speech_recognition import Recognizer, AudioFile
import random
import os
from pydub import AudioSegment

# If ffmpeg is not in your PATH
AudioSegment.ffmpeg = "ffmpeg.exe"
AudioSegment.ffprobe = "ffprobe.exe"

configs = {
    'CHROME_BUNDLE': '/home/binit/driver/chrome-linux/chrome',
    'HEADLESS': 'false',
}

args = [
        '--deny-permission-prompts',
        '--no-default-browser-check',
        '--no-first-run',
        '--deny-permission-prompts',
        '--disable-popup-blocking',
        '--ignore-certificate-errors',
        '--no-service-autorun',
        '--password-store=basic',
        '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
        '--window-size=640,480',
        '--disable-audio-output'
    ]
 

class SolveCaptcha:#solves captcha 
    def __init__(self, page):
        self.page = page
        self.main_frame = None
        self.recaptcha = None

    async def delay(self):
        await self.page.wait_for_timeout(random.randint(1, 3) * 1000)

    async def presetup(self):
        name = await self.page.locator(
            "//iframe[@title='reCAPTCHA']").get_attribute("name")
        print(name)
        self.recaptcha =  self.page.frame(name=name)

        await self.recaptcha.click("//div[@class='recaptcha-checkbox-border']")
        await self.delay()
        s = self.recaptcha.locator("//span[@id='recaptcha-anchor']")
        if await s.get_attribute("aria-checked") != "false":  # solved already
            return

        self.main_frame = self.page.frame(name=await self.page.locator(
            'iframe[title^="o"]').get_attribute("name"))
        await self.main_frame.click("id=recaptcha-audio-button")

    async def start(self):
        await self.presetup()
        tries = 0
        while (tries <= 5):
            await self.delay()
            try:
                await self.solve_captcha()
            except Exception as e:
                print(e)
                await self.main_frame.click("id=recaptcha-reload-button")
            else:
                s = self.recaptcha.locator("//span[@id='recaptcha-anchor']")
                if await s.get_attribute("aria-checked") != "false":
                    await self.page.click("id=recaptcha-demo-submit")
                    await self.delay()
                    break
            tries += 1

    async def solve_captcha(self):
        await self.main_frame.click(
            "//button[@aria-labelledby='audio-instructions rc-response-label']")
        href = await self.main_frame.locator(
            "//a[@class='rc-audiochallenge-tdownload-link']").get_attribute("href")
        print(href)
        urllib.request.urlretrieve(href, "audio.mp3")

        sound = pydub.AudioSegment.from_mp3(
            "audio.mp3").export("audio.wav", format="wav")

        recognizer = Recognizer()

        recaptcha_audio = AudioFile("audio.wav")
        with recaptcha_audio as source:
            audio = recognizer.record(source)

        text = recognizer.recognize_google(audio)
        print(text)
        await self.main_frame.fill("id=audio-response", text)
        await self.main_frame.click("id=recaptcha-verify-button")
        await self.delay()

    def __del__(self):
        os.remove("audio.mp3")
        os.remove("audio.wav")


async def Solve(page):
        try:
            captcha_solver = SolveCaptcha(page)
            await captcha_solver.start()
            del captcha_solver
        except Exception as e:
            print(e)
       #some issue with downloading the audio sample  for the captcha 
       #but the gist of it is to download the audio sample for captcha and then use speech recognition to  recognize the answer

class Evisa():
 def __init__(self,usern,passw):
        self.username =usern   # Replace with your actual username
        self.password =passw   # Replace with your actual password
        self.url=r"https://pedidodevistos.mne.gov.pt"   

 async def save_cookies(self,browser):
    with open('cookies.json', 'r') as f:
        cookies = json.load(f)
        await browser.add_cookies(cookies)

 async def login_form(self):
    url = self.url+r"/VistosOnline/Authentication.jsp"
    username_selector = "input[name='username']"  # Replace with the actual selector for the username input
    password_selector = "input[name='password']"  # Replace with the actual selector for the password input
    submit_button_selector = "button[id='loginFormSubmitButton']"  # Replace with the actual selector for the submit button

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await stealth_async(page)
        await page.goto(url)
        await page.type(username_selector, self.username,delay=30)
        await page.type(password_selector, self.password,delay=30)
        await asyncio.sleep(3)
        await Solve(page)
        await page.click(submit_button_selector)
        
        cookies = await browser.cookies()
        with open('cookies.json', 'w') as f:
            import json
            f.write(json.dumps(cookies))
 async def book_appointments(self,browser):
   await browser.close()

ins=Evisa("2023maria","Rodrigues 2023@")
asyncio.run(ins.login_form())
