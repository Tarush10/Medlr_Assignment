from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd


def scrape_netmeds_data(MAX_COUNT):
    
    letters_to_search = ['b', 'f']

    all_names = []
    all_prices = []
    all_links = []


    for starting_letter in letters_to_search:
        names_list = []
        prices_list = []
        links_list = []

        link = f'https://www.netmeds.com/catalogsearch/result/{starting_letter}/all'

        driver = webdriver.Chrome()
        driver.get(link)

        time.sleep(2)
        height = driver.execute_script("return document.body.scrollHeight")

        count = 0

        while count < MAX_COUNT:
            driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            time.sleep(3)
            new_height = driver.execute_script("return document.body.scrollHeight")

            if height == new_height:
                break
            height = new_height

            names = driver.find_elements(By.CLASS_NAME, 'clsgetname')
            prices = driver.find_elements(By.CLASS_NAME, 'price-box')
            med_links = driver.find_elements(By.CLASS_NAME, 'category_name')
            
            # categories = driver.find_elements(By.CLASS_NAME,'cate_filter')
            # for category in categories:
            #     cat_first = category.find_element(By.CSS_SELECTOR,'a:nth-child(2)')
            #     title_val = cat_first.get_attribute('title')
            #     print(cat_first.text)

            for name, price, med_link in zip(names, prices, med_links):
                names_list.append(name.text)
                prices_list.append(price.text)
                links_list.append(med_link.get_attribute('href'))

                count += 1

                if count >= MAX_COUNT:
                    break

        driver.quit()

        # Create a DataFrame for each letter
        data = {'Name': names_list, 'Price': prices_list, 'URL': links_list}
        df_letter = pd.DataFrame(data)

        # Append to the lists for final concatenation
        all_names.append(df_letter['Name'])
        all_prices.append(df_letter['Price'])
        all_links.append(df_letter['URL'])

    # Concatenate the DataFrames for both letters
    final_data = {'Name': pd.concat(all_names, ignore_index=True),
                'Price': pd.concat(all_prices, ignore_index=True),
                'URL': pd.concat(all_links, ignore_index=True)}

    df_combined = pd.DataFrame(final_data)

    # Drop duplicates from the combined DataFrame
    df_no_duplicates = df_combined.drop_duplicates()

    # Save DataFrame to CSV file
    df_no_duplicates.to_csv('output_combined.csv', index=False)

    print("Combined CSV file created successfully.")
