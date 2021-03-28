import requests

def transparency_check():

    with open('allLinks.txt') as all_links:
        links_with_info = all_links.readlines()

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

    print(article_links)

    # Total number of references
    num_references = len(article_links)
    print("Total number of references:", num_references)

    # Number of internal references

    internal_reference_count = 0

    with open('websiteURL.txt') as wURL:
        website_url = wURL.readlines()[0]
        url_components = website_url.split("/")
        for component in url_components:
            if component.count(".") >= 2:
                base_domain = component.split(".")[1] + "." + component.split(".")[2]
                break

    for link in article_links:
        if link.__contains__(base_domain):
            internal_reference_count += 1

    print("Number of external references:", num_references-internal_reference_count)
    print("Number of internal references:", internal_reference_count)

    # Check for broken links, not doing it with Selenium because it would slow the program down too much
    # https://stackoverflow.com/questions/1140661/what-s-the-best-way-to-get-an-http-response-code-from-a-url
    for link in article_links:
        try:
            r = requests.head(link)
            if r.status_code >= 400:
                broken_links.append(link)
        except requests.ConnectionError:
            print("failed to connect")

    print("Number of broken links:", len(broken_links))

    # Check for direct quotes
    with open('cleanedTextFile.txt') as cleanedTextFile:
        article_text = cleanedTextFile.readlines()

    quotes_count = 0
    for text_block in article_text:
        text_block.strip("\n")
        quotes_count += int(text_block.count("\"")/2)

    print("Instances of direct quoting:", quotes_count)


transparency_check()