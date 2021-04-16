""" Find a way to get rid of all the junk (ad texts, button texts, everything that is not part of the article
Solution for now: there is one comma and one end of sentence mark in each paragraph. Not 100% accurate.
Idea: compare each paragraph with what comes before and after to determine where the article starts/ends"""

def clean_website_text():
    article_paragraphs = []

    f = open('websiteText.txt', 'r')
    # Extract the actual text of the article from the website text (VIP)
    paragraphs = f.read().split('\n')
    # print(paragraphs)

    # print(len(paragraphs))

    for i in range(len(paragraphs)):
        # print(paragraphs[i])
        num_words = paragraphs[i].count(' ')+1
        # print(num_words)
        if num_words > 10:
            if '.' in paragraphs[i] or '!' in paragraphs[i] or '?' in paragraphs[i]:
                if not paragraphs[i].lower().__contains__('cookie policy' and 'all rights reserved'):
                    article_paragraphs.append(paragraphs[i])

    for i in range(int(len(paragraphs)/2), len(paragraphs)):
        if paragraphs[i] in article_paragraphs:
            if paragraphs[i+1] not in article_paragraphs and paragraphs[i+2] not in article_paragraphs and paragraphs[i+3] not in article_paragraphs:
                article_paragraphs = article_paragraphs[:(article_paragraphs.index(paragraphs[i]))+1]
            break

    #for i in range(len(article_paragraphs)):
    #    print(i, article_paragraphs[i])

    f.close()

    t = open('websiteTitle.txt', 'r')

    # Add the title
    title = t.read()
    if title not in article_paragraphs[0]:
        article_paragraphs.insert(0, title)

    t.close()

    st = open('websiteSubTitle.txt', 'r')

    # Add the subtitle
    subtitle = st.read()
    if subtitle not in article_paragraphs[1]:
        article_paragraphs.insert(1, subtitle)

    with open("cleanedTextFile.txt", "w") as cleaned_text_file:
        for paragraph in article_paragraphs:
            cleaned_text_file.write(paragraph + "\n")

    cleaned_text_file.close()