""" Find a way to get rid of all the junk (ad texts, button texts, everything that is not part of the article
Solution for now: there is one comma and one end of sentence mark in each paragraph. Not 100% accurate.
Idea: compare each paragraph with what comes before and after to determine where the article starts/ends"""
from autocorrect import Speller
from gingerit.gingerit import GingerIt
import re
import os

def spell_check():
    f = open("websiteText.txt", "r")

    # Extract the actual text of the article from the website text (VIP)
    article_paragraphs = []
    consecutive_marks_count = 0
    all_caps_words_count = 0
    spelling_mistakes_count = 0
    unique_words = set([])

    #spell = Speller(lang='en')

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

    #print(article_paragraphs)

    f.close()

    # Check for consecutive exclamation or question marks in each paragraph
    for paragraph in article_paragraphs:
        consecutive_marks_count += paragraph.count('!!')
        consecutive_marks_count += paragraph.count('??')

    # Check for CAPS LOCK usage, count how many words are written in caps lock (VIP)
    for paragraph in article_paragraphs:
        words = paragraph.split(" ")
        for i in range(len(words)-1):
            if not words[i].isalpha() and not words[i].isnumeric():
                continue
            if words[i].isupper():
                if words[i+1].isupper() or words[i-1].isupper():
                    all_caps_words_count += 1
                    print('Found word in all caps sequence: ', words[i])
        # Counting the number of unique words. TODO: find out average vocabulary size of a credible article if exists
        for word in words:
            word = re.sub('[.,!?(){}<>]', '', word)
            if word.isalpha():
                if word.lower() not in unique_words:
                    unique_words.add(word.lower())

            # Check for spelling mistakes in the same loop
            # exclude acronyms and common names -> problem: also excludes all capitalized words at the beginning of a sentence
            #if (words[i])[0].islower() or i==0:
            #    if words[i] != spell(words[i]):
            #        # print(words[i])
            #        spelling_mistakes_count += 1
            #        print(words[i])
            #elif (words[i])[0].isupper() and '.' in words[i-1] or '?' in words[i-1] or '!' in words[i-1]:
            #    if words[i] != spell(words[i]):
            #        # print(words[i])
            #        spelling_mistakes_count += 1
            #        print(words[i])

    # Nice way to check for spelling/grammar mistakes
    # parser = GingerIt()
    # for paragraph in article_paragraphs:
    #    spelling_mistakes_count += len((parser.parse(paragraph))['corrections'])


    # print(consecutive_marks_count, 'occurrences of consecutive exclamation or question marks found')
    # print(all_caps_words_count, 'words in all caps found')
    # print(spelling_mistakes_count, 'spelling mistakes found')
    # print(len(unique_words), 'unique words in article')

    # Clear the file if there's already something written in it
    open("formalityTestResults.txt", "w").close()

    formality_test_results = open("formalityTestResults.txt", "a")

    # Copy the results of our formality check to the results file -> we will use it in the test cases
    line1_result = formality_test_results.write(str(consecutive_marks_count))
    line1_message = formality_test_results.write(' consecutive ! or ? \n')

    line2_result = formality_test_results.write(str(all_caps_words_count))
    line2_message = formality_test_results.write( ' words in all caps found \n')

    line3_result = formality_test_results.write(str(spelling_mistakes_count))
    line3_message = formality_test_results.write(' spelling mistakes found \n')

    line4_result = formality_test_results.write(str(len(unique_words)))
    line4_message = formality_test_results.write(' unique words in article \n')

    formality_test_results.close()


spell_check()

