import time
import requests
import re


def transparency_check():

    with open('allLinks.txt') as all_links:
        links_with_info = all_links.readlines()
    all_links.close()

    article_links = []
    link_text = []
    broken_links = []

    # Keeping only relevant links - links which are surrounded by text of the article.
    # Excluding links where the text and the surrounding text are the exact same
    # Excluding links from disclaimers
    for link_with_info in links_with_info:
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
    internal_reference_count = 0

    with open('websiteProperties.txt') as wProp:
        website_url = wProp.readlines()[0]
        url_marked_as_opinion = website_url.__contains__('opinion')
        url_components = website_url.split("/")
        for component in url_components:
            if component.count(".") >= 2:
                base_domain = component.split(".")[1] + "." + component.split(".")[2]
                break
    wProp.close()

    with open('websiteProperties.txt') as wProp:
        author_found = wProp.readlines()[1]
    wProp.close()

    for link in article_links:
        if link.__contains__(base_domain):
            internal_reference_count += 1

    # Check for broken links, not doing it with Selenium because it would slow the program down too much
    # https://stackoverflow.com/questions/1140661/what-s-the-best-way-to-get-an-http-response-code-from-a-url
    for link in article_links:
        try:
            r = requests.head(link)
            if r.status_code >= 400:
                broken_links.append(link)
        except requests.ConnectionError:
            print("failed to connect")

    # Check for direct quotes
    with open('cleanedTextFile.txt') as cleanedTextFile:
        article_text = cleanedTextFile.readlines()

    quotes_count = 0

    for text_block in article_text:
        text_block.strip("\n")
        text_block = re.sub("[«»„“〞〟＂”]", "\"", text_block)
        quotes_count += int(text_block.count("\"")/2)

    with open('websiteProperties.txt') as wProp:
        opinion_section_exists = wProp.readlines()[2]
    wProp.close()

    marked_as_opinion = url_marked_as_opinion or opinion_section_exists

    open("transparencyTestResults.txt", "w").close()

    transparency_test_results = open("transparencyTestResults.txt", "a")
    line1_result = transparency_test_results.write(str(num_references))
    line1_message = transparency_test_results.write(' references in total\n')

    line2_result = transparency_test_results.write(str(num_references-internal_reference_count))
    line2_message = transparency_test_results.write(' external references\n')

    line3_result = transparency_test_results.write(str(internal_reference_count))
    line3_message = transparency_test_results.write(' internal references\n')

    line4_result = transparency_test_results.write(str(len(broken_links)))
    line4_message = transparency_test_results.write(' broken links\n')

    line5_result = transparency_test_results.write(str(quotes_count))
    line5_message = transparency_test_results.write(' instances of direct quoting\n')

    line6_result = transparency_test_results.write(str(author_found))

    line7_message = transparency_test_results.write('Article marked as opinion: ')
    line7_result = transparency_test_results.write(str(marked_as_opinion))

    transparency_test_results.close()


#transparency_check()