from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import datetime as dt


def get_articles(search_term):

    # set up options for headless browsing
    options = webdriver.FirefoxOptions()
    options.add_argument('--headless')
    # create a new instance of the Firefox driver with the headless option
    driver = webdriver.Firefox(options=options)
    # navigate to the URL of the page you want to scrape
    driver.get(f"https://www.pabliq.se/sokresultat?q={search_term}")
    # wait for the table to appear on the page
    wait = WebDriverWait(driver, 10)
    table = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[3]/div/div[2]/div/table")))
    # use pandas to read the HTML table into a DataFrame
    df = pd.read_html(table.get_attribute('outerHTML'))[0]
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    # close the browser
    driver.quit()
    df.columns = ['Upphandling', 'Beställare', 'Publicerat', 'Senast_svar', 'Länk']
    # df['Publicerat'] = pd.to_datetime(df['Publicerat'])
    # df['Publicerat'] = df['Publicerat'].dt.date
    df = df[df['Publicerat'] > '2023-01-01']
    # print(df)
    # print(df.columns)
    return df


if __name__ == '__main__':
    df = get_articles('vibration')
    # print(df)
    # print(df.columns)