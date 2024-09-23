import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
from fake_useragent import UserAgent

# Function to fetch data from eBay
def fetch_ebay_data(pages=1):
    ebay_url = "https://www.ebay.com/b/Small-Kitchen-Appliances/20667/bn_2311275?_pgn={}"
    ua = UserAgent()
    headers = {
        "User-Agent": ua.random,
        "Connection": "keep-alive",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US;q=0.9",
        "Referer": "https://www.google.com/",
        "DNT": "1"
    }

    data_list = []
    sponsored_count = 0  # Counter for sponsored items

    for page in range(1, pages + 1):
        try:
            url = ebay_url.format(page)
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                print(f"Successfully scraped {url}")

                soup = BeautifulSoup(response.text, 'html.parser')
                ul = soup.find("ul", class_="b-list__items_nofooter")
                listings = ul.find_all('li', class_='s-item s-item--large')
                print(f"Found {len(listings)} listings on page {page}")

                for listing in listings:
                    try:
                        # Debugging: Print the listing's HTML for analysis
                        print(listing.prettify())  # This prints the full HTML structure of each listing

                        # Sponsored Check
                        sponsored_tag = listing.find('span', {'class': 's-item__pl'})
                        is_sponsored = True if sponsored_tag else False

                        # Title
                        title_tag = listing.find('h3', class_='s-item__title')
                        title_text = title_tag.get_text(strip=True) if title_tag else 'N/A'

                        # Price
                        price_tag = listing.find('span', class_='s-item__price')
                        price_text = price_tag.get_text(strip=True) if price_tag else 'N/A'

                        # Shipping
                        shipping_element = listing.find("span", class_="s-item__shipping s-item__logisticsCost")
                        shipping = shipping_element.text.strip() if shipping_element else "N/A"

                        product_url = listing.find("a", class_="s-item__link")["href"]

                        # Add item to the data list
                        data_list.append({
                            'Product URL': product_url,
                            'Title': title_text,
                            'Price': price_text,
                            'Shipping Fee': shipping
                        })

                        if is_sponsored:
                            sponsored_count += 1  # Increment sponsored count
                            print(f"Skipping sponsored item: {listing}")  # Log the skipped item for further analysis

                    except Exception as e:
                        print(f"Error parsing listing: {e}")

            else:
                print(f"Failed to scrape {url}, Status Code: {response.status_code}")

        except Exception as e:
            print(f"Error fetching page {page}: {e}")

    print(f"Total products scraped: {len(data_list)}")
    print(f"Total sponsored products skipped: {sponsored_count}")  # Debug statement for sponsored count

    # Create CSV
    df = pd.DataFrame(data_list)
    df.to_csv("ebay_data.csv", index=False)
    df.to_excel("ebay_data.xlsx", index=False)
    # Write to JSON
    with open('ebay_data.json', 'w', encoding='utf-8') as json_file:
        json.dump(data_list, json_file, ensure_ascii=False, indent=4)

    print("--------")
    print("Excel File created")
    print("--------")
    print("Json file created")
    print("----------")
    print("Excel File also created")

# Call the function with the number of pages
fetch_ebay_data(pages=150)
