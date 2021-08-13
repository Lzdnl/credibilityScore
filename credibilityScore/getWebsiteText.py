import sys

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import time

""" Because the HTML structure of each news website is different, we are taking the whole text of the page and writing
 it to a file to process later. The extension 'I don't care about cookies' removes the consent popups. """


def get_website_text(url):

    print("Fetching website properties...")

    # Create a Firefox profile to manipulate browser configuration
    profile = webdriver.FirefoxProfile()

    # Unfortunately, installing this extention doesn't work any more. Might be because of a Selenium update
    #profile.add_extension(extension='i_dont_care_about_cookies-3.3.1-an+fx.xpi')

    # Alternative: set browser to reject all cookies (removes cookie banner, but not for all websites)
    profile.set_preference("network.cookie.cookieBehavior", 2)

    # Start browser and request URL
    driver = webdriver.Firefox(firefox_profile=profile)
    driver.get(url)

    # It's better to wait until a certain element on the page has appeared. But this doesn't always work properly
    # Hard wait to make sure page is loaded
    wait = WebDriverWait(driver, 15)
    time.sleep(5)

    try:
        # Getting the text, title and author
        website_text = driver.find_element(By.XPATH, '//body').text
        website_title = driver.find_element(By.XPATH, '(//body//h1)[1]').text
        website_author = driver.find_elements(By.XPATH,
                                              '((//*[contains(@*, \'author\') or contains(@*, \'Byline\') or contains(@*, \'byline\')])[1] | (//meta[contains(@name, \'author\')])[1])[1]')

        # Getting the references
        ancestor_text=[]
        link_text=[]
        link_list=[]

        # Also getting the text of each URL and the text of its ancestor
        # Will be useful for getting rid of URLs from ads, buttons, etc
        for link in driver.find_elements(By.XPATH, '//h1/following::a[@href]'):
            ancestor = link.find_element(By.XPATH, 'ancestor::*[position()=1]')
            link_list.append(link.get_attribute('href'))
            if len(ancestor.text) != '':
                ancestor_text.append(ancestor.text)
            else:
                ancestor_text.append("null_ancestor_text")
            if link.text != '':
                link_text.append(link.text)
            else:
                link_text.append("null_link_text")
    except:
        print("Unexpected error:", sys.exc_info()[0])
        driver.close()

    # Create website properties dictionary.
    # This is passed from function to function and completed with relevant metrics and content
    # Add extracted properties to dictionary
    website_properties = {
        'all_text': website_text,
        'title': website_title,
        'url': url,
        'tran_author': False,
        'all_links': []
    }

    if len(website_author) == 1:
        website_properties['tran_author'] = True

    for i in range(len(link_list)):
        website_properties['all_links'].append(link_list[i] + "|" + link_text[i] + "|" + ancestor_text[i])

    driver.quit()

    return website_properties
