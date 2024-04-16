from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import pandas as pd


def main():

    with sync_playwright() as p: 
        
        url_ = 'https://www.booking.com/searchresults.html?ss=Atlanta%2C+United+States+of+America&ssne=Paris&ssne_untouched=Paris&label=gen173nr-1FCAQoggI46wdIMVgEaJUCiAEBmAExuAEXyAEM2AEB6AEB-AEDiAIBqAIDuALDi_ewBsACAdICJDlmZjJkYTQ1LTJkMmQtNDJlNC1iZjg2LTdkOTI0YWM3NTAwNtgCBeACAQ&aid=304142&lang=en-us&sb=1&src_elem=sb&src=searchresults&dest_id=20024809&dest_type=city&checkin=2024-04-15&checkout=2024-04-16&group_adults=1&no_rooms=1&group_children=0'
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(url_, timeout=100000)
        hotels = page.locator('xpath=(//div[@aria-label="Property"])').all()
        
        print(f'There are: {len(hotels)} hotels.')

        hotels_list = []

        for hotel in hotels:
            hotel_dict = {}

            hotel_dict['hotel'] = hotel.locator('//div[@data-testid="title"]').inner_text()
            hotel_dict['price'] = hotel.locator('//span[@data-testid="price-and-discounted-price"]').inner_text()
            hotel_dict['score'] = hotel.locator('//div[@data-testid="review-score"]/div[1]').inner_text()
            hotel_dict['avg review'] = hotel.locator('//div[@data-testid="review-score"]/div[2]/div[1]').inner_text()
            hotel_dict['reviews count'] = hotel.locator('//div[@data-testid="review-score"]/div[2]/div[2]').inner_text().split()[0]

            hotels_list.append(hotel_dict)

            df = pd.DataFrame(hotels_list)
            df.to_excel('hotels_list.xlsx', index=False) 
            df.to_csv('hotels_list.csv', index=False) 

        

        browser.close()

if __name__ == '__main__':
    main()




