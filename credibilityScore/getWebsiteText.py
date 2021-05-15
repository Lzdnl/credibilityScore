from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import time
from selenium.webdriver.support import expected_conditions as EC

""" Because the HTML structure of each news website is different, we are taking the whole text of the page and writing
 it to a file to process later. The extension 'I don't care about cookies' removes the consent popups. """


def get_website_text(url):

    print("Fetching website properties...")

    profile = webdriver.FirefoxProfile()
    profile.add_extension(extension='i_dont_care_about_cookies-3.2.4-an+fx.xpi')
    driver = webdriver.Firefox(firefox_profile=profile)

    driver.get(url)

    # TODO get rid of sleep by making the wait work properly
    wait = WebDriverWait(driver, 15)
    time.sleep(5)


    # Getting the text, title and author
    website_text = driver.find_element(By.XPATH, '//body').text
    website_title = driver.find_element(By.XPATH, '(//body//h1)[1]').text
    website_author = driver.find_elements(By.XPATH, '(//*[contains(@*, \'author\')])[1] | (//*[contains(@*, \'byline-prefix\')])[1]')
    opinion_section_exists = driver.find_elements(By.XPATH, '//h1/preceding::*[text() = \'Opinion\']')

    # Getting the references
    ancestor_text=[]
    link_text=[]
    link_list=[]

    for link in driver.find_elements(By.XPATH, '//h1/following::a[@href]'):
        ancestor = link.find_element(By.XPATH, 'ancestor::*[position()=1]')
        ancestor_text.append(ancestor.text)
        if link.text != '':
            link_text.append(link.text)
        else:
            link_text.append("null_link_text")
        link_list.append(link.get_attribute('href'))

    website_properties = {
        'all_text': website_text,
        'title': website_title,
        'url': url,
        'tran_author': False,
        'tran_marked_as_opinion': False,
        'all_links': []
    }

    if len(website_author) == 1:
        website_properties['tran_author'] = True
    if len(opinion_section_exists) > 0:
        website_properties['tran_marked_as_opinion'] = True

    for i in range(len(link_list)):
        website_properties['all_links'].append(link_list[i] + "|" + link_text[i] + "|" + ancestor_text[i])

    driver.quit()

    return website_properties
