import asyncio
from playwright.async_api import async_playwright

playwright_path = r'C:\path\to\playwright'  # Change this to your Playwright installation path
url = 'https://www.trip.com/'

async def scrape_urls(location,browser):
        url = f"https://www.trip.com/hotels/list?city=58&cityName={location}"
        page = await browser.new_page()
        await page.goto(url)
        while not await page.query_selector('.nothing'):
            await page.evaluate('window.scrollBy(0, 1000)')
            break
        elements = await page.query_selector_all('.compressmeta-hotel-wrap-v8')
        urls = [f"https://www.trip.com/hotels/detail/?hotelId={await element.get_attribute('id')}" for element in elements]
       
        return urls

async def scrape_page(url,browser):
        page = await browser.new_page()
        await page.goto(url)
        stars_selector = 'div[class^="headInit_headInit_left"] .u-icon-ic_new_star'
        names_selector = 'h1[class^="headInit_headInit-title_name"]'
        address_selector = '[class^="headInit_headInit-address_text"]'

        star = len(await page.query_selector_all(stars_selector))
        print(star)
        name = await page.query_selector(names_selector)
        name=await name.text_content()
        address = await page.query_selector(address_selector)
        address=await address.text_content()
        review_button = await page.query_selector('[class^="reviewSwiper_reviewSwiper-moreReviewButtonText"]')
        await review_button.click()
        pages = await page.query_selector_all('[class^="reviewPagination_reviewPagination-number"]')
        for page in pages:
            await page.click()
            await page.wait_for_timeout(4000)
            reviews = await page.query_selector_all('[class^="minNoise_reviewCard-container"]')
            review_data = []
            for review in reviews:
                name = await (await review.query_selector('[class^="class="reviewCard_reviewCard-userName"]')).text_content()
                rating =await (await review.query_selector('[class^="class="reviewCard_reviewHead-currentScore"]')).text_content()
                details = await review.query_selector_all('[class^="reviewCard_reviewCard-userDetailItem"] span')
                details = [await (await item).text_content() for item in details]
                review_data.append([name, rating, details])
        await browser.close()
        print([name, star, address, review_data])    
        return [name, star, address, review_data]

async def main():
  async with async_playwright() as p:
    browser = await p.chromium.launch(headless=False)
    urls = await scrape_urls("Hong KOng",browser)
    print(urls)
    for url in urls:
        try:
         data = await scrape_page(url,browser)
        except Exception as e:
            print(e)
            input()
        print(data)

asyncio.run(main())
