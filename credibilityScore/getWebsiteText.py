from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import time
from selenium.webdriver.support import expected_conditions as EC

""" Because the HTML structure of each news website is different, we are taking the whole text of the page and writing
 it to a file to process later. The extension 'I don't care about cookies' removes the consent popups. """
def get_website_text(url):
    profile = webdriver.FirefoxProfile()
    profile.add_extension(extension='i_dont_care_about_cookies-3.2.4-an+fx.xpi')
    driver = webdriver.Firefox(firefox_profile=profile)

    driver.get(url)

    # TODO get rid of sleep by making the wait work properly
    wait = WebDriverWait(driver, 15)
    time.sleep(5)


    # Getting the text
    website_text = driver.find_element(By.XPATH, '//body').text
    website_title = driver.find_element(By.XPATH, '(//body//h1)[1]').text
    website_subtitle = driver.find_element(By.XPATH, '(//body//h2)[1]').text

    website_text_file = open("websiteText.txt", "w")
    website_text_write = website_text_file.write(website_text)
    website_text_file.close()

    website_title_file = open("websiteTitle.txt", "w")
    website_title_write = website_title_file.write(website_title)
    website_title_file.close()

    website_subtitle_file = open("websiteSubTitle.txt", "w")
    website_subtitle_write = website_subtitle_file.write(website_subtitle)
    website_subtitle_file.close()

    driver.quit()

get_website_text('https://www.foxnews.com/politics/new-york-cuomo-sexual-harassment-leading-liberal-women')