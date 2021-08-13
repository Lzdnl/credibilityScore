import neutralityCheck
import requests
import re


def transparency_check():

    # Get properties dictionary from neutralityCheck.py
    website_properties = neutralityCheck.neutrality_check()

    article_text = website_properties['cleaned_text']

    article_links = []
    link_text = []
    broken_links = []
    internal_reference_count = 0

    # Keeping only relevant links - looking for whether URL text is in cleaned text of article
    for link_with_info in website_properties['all_links']:
        link_info = link_with_info.split("|")
        # This excludes links from ads and disclaimers. Leaving it here, might be useful
        # if not link_info[0].__contains__("taboola" or "outbrain" or "@"):
        #    if not link_info[2].lower().__contains__("all rights reserved" or "privacy policy"):
        #        if link_info[0].count(".") > 1:
        if link_info[2] in article_text:
            article_links.append(link_info[0])
            link_text.append(link_info[1])

    # Total number of references
    num_references = len(article_links)

    # Getting base domain of each URL to check for internal references
    url_components = website_properties['url'].split("/")

    for component in url_components:
        if component.count(".") >= 2:
            base_domain = component.split(".")[1] + "." + component.split(".")[2]
            break
        if component.count(".") == 1:
            base_domain = component.split(".")[0] + "." + component.split(".")[1]
            break

    # Number of internal references
    for link in article_links:
        if link.__contains__(base_domain):
            internal_reference_count += 1

    print("Checking for broken links. This might take a while...")
    # Check for broken links, not doing it with Selenium because it would slow the program down too much
    # https://stackoverflow.com/questions/1140661/what-s-the-best-way-to-get-an-http-response-code-from-a-url
    for link in article_links:
        try:
            r = requests.head(link, timeout = 10)
            if r.status_code >= 400:
                broken_links.append(link)
        except:
            print("Connection error, moving on to the next link")

    # Number of direct quotes
    quotes_count = 0

    for text_block in article_text:
        text_block.strip("\n")
        text_block = re.sub("[«»„“〞〟＂”]", "\"", text_block)
        quotes_count += int(text_block.count("\"")/2)

    # Opinion tag presence
    if website_properties['url'].__contains__('opinion'):
        website_properties['tran_marked_as_opinion'] = True
    else:
        website_properties['tran_marked_as_opinion'] = False

    # Add relevant metrics to properties dictionary
    website_properties['tran_num_refs'] = num_references
    website_properties['tran_num_refs_external'] = num_references-internal_reference_count
    website_properties['tran_num_refs_internal'] = internal_reference_count
    website_properties['tran_num_broken_links'] = len(broken_links)
    website_properties['tran_num_direct_quotes'] = quotes_count
    website_properties['tran_ref_links'] = article_links
    website_properties['tran_broken_links'] = broken_links

    return website_properties

