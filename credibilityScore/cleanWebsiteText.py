""" Find a way to get rid of all the junk (ad texts, button texts, everything that is not part of the article
Solution for now: there is one comma and one end of sentence mark in each paragraph. Not 100% accurate.
Idea: compare each paragraph with what comes before and after to determine where the article starts/ends"""

def clean_website_text():
    article_paragraphs = []

    f = open('websiteText.txt', 'r')
    # Extract the actual text of the article from the website text (VIP)
    paragraphs = f.read().split('\n')
    for paragraph in paragraphs:
        comma_count = paragraph.count(',')
        if comma_count >= 1:
            if '.' in paragraph:
                article_paragraphs.append(paragraph)
            if '?' in paragraph and paragraph not in article_paragraphs:
                article_paragraphs.append(paragraph)
            if '!' in paragraph and paragraph not in article_paragraphs:
                article_paragraphs.append(paragraph)

    f.close()

    t = open('websiteTitle.txt', 'r')

    # Add the title
    title = t.read()
    article_paragraphs.insert(0, title)

    t.close()

    with open("cleanedTextFile.txt", "w") as cleaned_text_file:
        for paragraph in article_paragraphs:
            cleaned_text_file.write(paragraph + "\n")

    cleaned_text_file.close()
