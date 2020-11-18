from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

""" Because the HTML structure of each news website is different, we are taking the whole text of the page and writing
 it to a file to process later. The extension 'I don't care about cookies' removes the consent popups. """
def get_website_text(url):
    profile = webdriver.FirefoxProfile()
    profile.add_extension(extension='i_dont_care_about_cookies-3.2.4-an+fx.xpi')
    driver = webdriver.Firefox(firefox_profile=profile)

    driver.get(url)

    wait = WebDriverWait(driver, 10)

    # Getting the text
    website_text = driver.find_element(By.XPATH, '//body').text

    website_text_file = open("websiteText.txt", "w")
    n = website_text_file.write(website_text)
    website_text_file.close()

    driver.quit()