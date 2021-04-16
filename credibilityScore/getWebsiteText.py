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


    # Getting the text, title and author
    website_text = driver.find_element(By.XPATH, '//body').text
    website_title = driver.find_element(By.XPATH, '(//body//h1)[1]').text
   # website_subtitle = driver.find_element(By.XPATH, '(//body//h2)[1]').text
    website_author = driver.find_elements(By.XPATH, '(//*[contains(@*, \'author\')])[1]')
    opinion_section_exists = driver.find_elements(By.XPATH, '//h1/preceding::*[text() = \'Opinion\']')

    # Getting the references
    ancestor_text=[]
    link_text=[]
    link_list=[]

    #for ancestor in driver.find_elements(By.XPATH, '//h1/following::a/ancestor::*[position()=1]', ):
    #    if ancestor.text != '':
    #        ancestor_text.append(ancestor.text)
    #    else:
    #        ancestor_text.append("null_ancestor_text")

    #print(len(ancestor_text))
    #print(ancestor_text)

    for link in driver.find_elements(By.XPATH, '//h1/following::a[@href]'):
        ancestor = link.find_element(By.XPATH, 'ancestor::*[position()=1]')
        ancestor_text.append(ancestor.text)
        if link.text != '':
            link_text.append(link.text)
        else:
            link_text.append("null_link_text")
        link_list.append(link.get_attribute('href'))

    website_text_file = open("websiteText.txt", "w")
    website_text_write = website_text_file.write(website_text)
    website_text_file.close()

    website_title_file = open("websiteTitle.txt", "w")
    website_title_write = website_title_file.write(website_title)
    website_title_file.close()

    website_reference_file = open("allLinks.txt", "w")
    for i in range(len(link_list)):
        website_reference_file_write = website_reference_file.write(link_list[i] + "|" + link_text[i] + "|" + ancestor_text[i] + "\n")
    website_reference_file.close()

    website_properties = open("websiteProperties.txt", "w")
    website_properties_url = website_properties.write(url)
    if len(website_author) == 1:
        website_properties_author = website_properties.write("\nAuthor found \n")
    if len(website_author) == 0:
        website_properties_author = website_properties.write("\nNo author found \n")
    if len(opinion_section_exists) > 0:
        website_properties_opinion_section = website_properties.write("True\n")
    if len(opinion_section_exists) == 0:
        website_properties_opinion_section = website_properties.write("False\n")
    website_properties.close()

   # website_subtitle_file = open("websiteSubTitle.txt", "w")
   # website_subtitle_write = website_subtitle_file.write(website_subtitle)
   # website_subtitle_file.close()

    driver.quit()