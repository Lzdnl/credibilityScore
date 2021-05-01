""" Find a way to get rid of all the junk (ad texts, button texts, everything that is not part of the article
Solution for now: there is one comma and one end of sentence mark in each paragraph. Not 100% accurate.
Idea: compare each paragraph with what comes before and after to determine where the article starts/ends"""
import getWebsiteText


def clean_website_text():

    article_paragraphs = []
    num_words = 0
    num_sentences = 0

    website_properties = getWebsiteText.get_website_text(input("Enter URL: "))

    print("Cleaning article text...")

    paragraphs = str(website_properties['all_text']).split("\n")

    for i in range(len(paragraphs)):
        num_words = paragraphs[i].count(' ')+1
        if num_words > 15:
            if '.' in paragraphs[i] or '!' in paragraphs[i] or '?' in paragraphs[i]:
                if not paragraphs[i].lower().__contains__('cookie policy'):
                    if not paragraphs[i].lower().__contains__('all rights reserved'):
                        article_paragraphs.append(paragraphs[i])

    for i in range(int(len(paragraphs)/2), len(paragraphs)):
        if paragraphs[i] in article_paragraphs:
            if paragraphs[i+1] not in article_paragraphs and paragraphs[i+2] not in article_paragraphs and paragraphs[i+3] not in article_paragraphs:
                article_paragraphs = article_paragraphs[:(article_paragraphs.index(paragraphs[i]))+1]
            break

    website_properties['cleaned_text'] = article_paragraphs

    for paragraph in article_paragraphs:
        words = paragraph.split()
        num_words += len(words)
        num_sentences += paragraph.count(".")
        num_sentences += paragraph.count("!")
        num_sentences += paragraph.count("?")

    website_properties['num_words'] = num_words
    website_properties['num_sentences'] = num_sentences

    return website_properties
