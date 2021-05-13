import neutralityCheck
import time
import requests
import re


def transparency_check():

    website_properties = neutralityCheck.neutrality_check()

    print("Transparency check...")

    article_links = []
    link_text = []
    broken_links = []
    internal_reference_count = 0

    # Keeping only relevant links - links which are surrounded by text of the article.
    # Excluding links where the text and the surrounding text are the exact same
    # Excluding links from disclaimers
    for link_with_info in website_properties['all_links']:
        link_info = link_with_info.split("|")
        if len(link_info)>2 and link_info[2].__contains__(".") and len(link_info[2].split())>15:
            if not (link_info[2].lower().__contains__("all rights reserved")):
                if link_info[1].strip() != link_info[2].strip():
                    # print(link_info[1])
                    # print(link_info[2])
                    article_links.append(link_info[0])
                    link_text.append(link_info[1])

    # Total number of references
    num_references = len(article_links)

    # Number of internal references
    url_components = website_properties['url'].split("/")

    for component in url_components:
        if component.count(".") >= 2:
            base_domain = component.split(".")[1] + "." + component.split(".")[2]
            break
        if component.count(".") == 1:
            base_domain = component.split(".")[0] + "." + component.split(".")[1]
            break

    for link in article_links:
        if link.__contains__(base_domain):
            internal_reference_count += 1

    print("Checking for broken links. This might take a while...")
    # Check for broken links, not doing it with Selenium because it would slow the program down too much
    # https://stackoverflow.com/questions/1140661/what-s-the-best-way-to-get-an-http-response-code-from-a-url
    for link in article_links:
        print("Checking status code for " + str(link))
        try:
            r = requests.head(link, timeout = 10)
            if r.status_code >= 400:
                broken_links.append(link)
        except requests.ConnectionError:
            print("failed to connect")
        except requests.exceptions.InvalidSchema:
            print(link, "is invalid")

    article_text = website_properties['cleaned_text']

    quotes_count = 0

    for text_block in article_text:
        text_block.strip("\n")
        text_block = re.sub("[«»„“〞〟＂”]", "\"", text_block)
        quotes_count += int(text_block.count("\"")/2)

    if website_properties['url'].__contains__('opinion'):
        website_properties['tran_marked_as_opinion'] = True

    website_properties['tran_num_refs'] = num_references
    website_properties['tran_num_refs_external'] = num_references-internal_reference_count
    website_properties['tran_num_refs_internal'] = internal_reference_count
    website_properties['tran_num_broken_links'] = len(broken_links)
    website_properties['tran_num_direct_quotes'] = quotes_count
    website_properties['tran_ref_links'] = article_links
    website_properties['tran_broken_links'] = broken_links

    return(website_properties)
