""" Find a way to get rid of all the junk (ad texts, button texts, everything that is not part of the article
Solution for now: there is one comma and one end of sentence mark in each paragraph. Not 100% accurate.
Idea: compare each paragraph with what comes before and after to determine where the article starts/ends"""
from autocorrect import Speller

def spell_check():
    f = open("websiteText.txt", "r")

    # Extract the actual text of the article from the website text (VIP)
    article_paragraphs = []
    consecutive_marks_count = 0
    all_caps_words_count = 0
    spelling_mistakes_count = 0

    spell = Speller(lang='en')

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

    # print(article_paragraphs)

    f.close()

    # Check for consecutive exclamation or question marks in each paragraph
    for paragraph in article_paragraphs:
        if '!!' in paragraph or '??' in paragraph:
            consecutive_marks_count += 1
    print(consecutive_marks_count, 'paragraphs with consecutive exclamation or question marks found')

    # Check for CAPS LOCK usage, count how many words are written in caps lock (VIP)
    for paragraph in article_paragraphs:
        words = paragraph.split(" ")
        for i in range(len(words)-1):
            if not words[i].isalpha() and not words[i].isnumeric():
                continue
            if words[i].isupper():
                if words[i+1].isupper() or words[i-1].isupper():
                    all_caps_words_count += 1
            # exclude acronyms and common names -> problem: also excludes all capitalized words at the beginning of a sentence
            if (words[i])[0].islower() or i==0:
                if words[i] != spell(words[i]):
                    # print(words[i])
                    spelling_mistakes_count += 1
            elif (words[i])[0].isupper() and '.' in words[i-1] or '?' in words[i-1] or '!' in words[i-1]:
                if words[i] != spell(words[i]):
                    # print(words[i])
                    spelling_mistakes_count += 1


    print(all_caps_words_count, 'words in all caps found')
    print(spelling_mistakes_count, 'spelling mistakes found')


spell_check()