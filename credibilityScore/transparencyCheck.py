def transparency_check():

    with open('allLinks.txt') as all_links:
        links_with_info = all_links.readlines()

    articleLinks = []
    articleText = []

    # Keeping only relevant links - links which are surrounded by text of the article.
    # Excluding links where the text and the surrounding text are the exact same
    # Excluding links from disclaimers
    for link_with_info in links_with_info:
        link_info = link_with_info.split("|")
        if(len(link_info)>2 and link_info[2].__contains__(".") and len(link_info[2].split())>15):
            if not (link_info[2].lower().__contains__("all rights reserved")):
                if(link_info[1].strip() != link_info[2].strip()):
                    # print(link_info[1])
                    # print(link_info[2])
                    articleLinks.append(link_info[0])
                    articleText.append(link_info[1])

    # Total number of references
    numReferences = len(articleLinks)
    print("Total number of references:", numReferences)

    # Number of internal references

    internal_reference_count = 0

    with open('websiteURL.txt') as wURL:
        websiteURL = wURL.readlines()[0]
        urlComponents = websiteURL.split("/")
        for component in urlComponents:
            if component.count(".") >= 2:
                baseDomain = component.split(".")[1] + "." + component.split(".")[2]
                break

    for link in articleLinks:
        if link.__contains__(baseDomain):
            internal_reference_count += 1

    print("Number of external references:", numReferences-internal_reference_count)
    print("Number of internal references:", internal_reference_count)


neutrality_check()