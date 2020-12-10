""" Find a way to get rid of all the junk (ad texts, button texts, everything that is not part of the article
Solution for now: there is one comma and one end of sentence mark in each paragraph. Not 100% accurate.
Idea: compare each paragraph with what comes before and after to determine where the article starts/ends"""
#from gingerit.gingerit import GingerIt
from autocorrect import Speller
import re
import os

def spell_check():

    article_paragraphs = []
    marks_count_title = 0
    marks_count = 0
    consecutive_marks_count = 0
    all_caps_words_count = 0
    spelling_mistakes_count = 0
    title_spelling_mistakes_count = 0
    unique_words = set([])
    total_word_count = 0

    spell = Speller(lang='en')

    f = open('websiteText.txt', 'r')
    # Extract the actual text of the article from the website text (VIP) TODO: put this in separate file
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

    # print(article_paragraphs)

    # Count total number of words (will be used for normalization of spelling mistakes)
    for paragraph in article_paragraphs:
        words = paragraph.split(" ")
        total_word_count += len(words)


    # Check for exclamation or question marks in the title
    marks_count_title = article_paragraphs[0].count('!')
    marks_count_title += article_paragraphs[0].count('!')

    for paragraph in article_paragraphs:
        # Check for consecutive exclamation or question marks in each paragraph
        consecutive_marks_count += paragraph.count('!!')
        consecutive_marks_count += paragraph.count('??')
        # The literature say it also makes sense to count single instances of ! and ?
        marks_count += paragraph.count('!')
        marks_count += paragraph.count('?')

    # Check for CAPS LOCK usage, count how many words are written in caps lock
    for paragraph in article_paragraphs:
        words = paragraph.split(" ")
        for i in range(len(words)-1):
            if not words[i].isalpha() and not words[i].isnumeric():
                continue
            if words[i].isupper():
                if words[i+1].isupper() or words[i-1].isupper():
                    all_caps_words_count += 1
                    # print('Found word in all caps sequence: ', words[i])

        # Counting the number of unique words.
        # TODO: find out average vocabulary size of a credible article if exists

        for word in words:
            word = re.sub('[.,!?(){}<>]', '', word)
            if word.isalpha():
                if word.lower() not in unique_words:
                    unique_words.add(word.lower())

    # Check for spelling mistakes
    for paragraph in article_paragraphs:
        words = paragraph.split(' ')

        for i in range(len(words)-1):

            # Remove special characters from beginning and end of words
            words[i] = re.sub('[.:;,!?(){}<>]', '', words[i])
            words[i] = words[i].replace('''”''', '')
            words[i] = words[i].replace('''“''', '')
            words[i] = words[i].replace('[', '')
            words[i] = words[i].replace(']', '')

            # exclude acronyms and common names by looking for words which begin with a majuscule
            # and are not at the beginning of a sentence
            if (words[i])[0].islower() or i==0:
                if words[i] != spell(words[i]):
                    spelling_mistakes_count += 1
                    # print(words[i])
            elif (words[i])[0].isupper() and '.' in words[i-1] or '?' in words[i-1] or '!' in words[i-1]:
                if words[i] != spell(words[i]):
                    spelling_mistakes_count += 1
                    # print(words[i])

    title_words = article_paragraphs[0].split(' ')
    for i in range(len(title_words)-1):
        words[i] = re.sub('[.:;,!?(){}<>]', '', words[i])
        words[i] = words[i].replace('''”''', '')
        words[i] = words[i].replace('''“''', '')
        words[i] = words[i].replace('[', '')
        words[i] = words[i].replace(']', '')

        if (title_words[i]) != spell(title_words[i]):
            title_spelling_mistakes_count += 1
            # print(title_words[i])

    spelling_error_rate = (spelling_mistakes_count/total_word_count)*100
    lexical_density = len(unique_words)/total_word_count

    # Great grammar/spellchecker, but not free and also throws errors now
    # parser = GingerIt()
    # for paragraph in article_paragraphs:
    #     print(parser.parse(paragraph))
    #     spelling_mistakes_count += len((parser.parse(paragraph))['corrections'])

    # Clear the file if there's already something written in it
    open("formalityTestResults.txt", "w").close()

    formality_test_results = open("formalityTestResults.txt", "a")

    # Copy the results of our formality check to the results file -> we will use it in the test cases
    line1_result = formality_test_results.write(str(marks_count_title))
    line1_message = formality_test_results.write(' ! or ? in title\n')

    line2_result = formality_test_results.write(str(marks_count))
    line2_message = formality_test_results.write(' ! or ? in total\n')

    line3_result = formality_test_results.write(str(consecutive_marks_count))
    line3_message = formality_test_results.write(' consecutive ! or ? \n')

    line4_result = formality_test_results.write(str(all_caps_words_count))
    line4_message = formality_test_results.write( ' words in all caps found \n')

    line5_result = formality_test_results.write(str(title_spelling_mistakes_count))
    line5_message = formality_test_results.write(' spelling mistakes found in title \n')

    if spelling_error_rate >= 1:
        line6 = formality_test_results.write('Unacceptable error rate \n')
    else:
        line6 = formality_test_results.write('Acceptable error rate \n')

    if lexical_density > 0.4:
        line7 = formality_test_results.write('Higher than average lexical density')
    else:
        line7 = formality_test_results.write('Average or less than average lexical density')

    formality_test_results.close()



