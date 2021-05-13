import cleanWebsiteText
from autocorrect import Speller
import re


def formality_check():

    marks_count_title = 0
    marks_count_text = 0
    consecutive_marks_count = 0
    all_caps_words_count = 0
    capitalized_words = []
    spelling_mistakes_count = 0
    incorrect_words = []
    title_spelling_mistakes_count = 0
    unique_words = set([])

    spell = Speller(lang='en')

    website_properties = cleanWebsiteText.clean_website_text()

    print("Formality check...")

    cleaned_text = website_properties['cleaned_text']

    article_paragraphs = [paragraph.strip() for paragraph in cleaned_text]

    # Check for exclamation or question marks in the title
    marks_count_title = website_properties['title'].count('!')
    marks_count_title += website_properties['title'].count('?')

    website_properties['form_num_marks_title'] = marks_count_title

    for paragraph in article_paragraphs:
        # Check for consecutive exclamation or question marks in each paragraph
        consecutive_marks_count += paragraph.count('!!')
        consecutive_marks_count += paragraph.count('??')
        # The literature says it also makes sense to count single instances of '?'
        marks_count_text += paragraph.count('?')

    website_properties['form_num_marks_text'] = marks_count_text

    # Check for CAPS LOCK usage, count how many words are written in caps lock
    for paragraph in article_paragraphs:
        words = paragraph.split(" ")
        for i in range(len(words)-1):
            if not words[i].isalpha() and not words[i].isnumeric():
                continue
            if words[i].isupper():
                if words[i+1].isupper() or words[i-1].isupper():
                    capitalized_words.append(words[i])
                    all_caps_words_count += 1
                    # print('Found word in all caps sequence: ', words[i])

        # Counting the number of unique words.

        for word in words:
            word = re.sub('[.,!?(){}<>]', '', word)
            if word.isalpha():
                if word.lower() not in unique_words:
                    unique_words.add(word.lower())

        # Check for spelling mistakes

        for i in range(len(words)):

            # Remove special characters from beginning and end of words
            words[i] = re.sub('[.:;,!?(){}<>"]', '', words[i])
            words[i] = words[i].replace('''”''', '')
            words[i] = words[i].replace('''“''', '')
            words[i] = words[i].replace('[', '')
            words[i] = words[i].replace(']', '')

            # exclude acronyms and common names by looking for words which begin with a majuscule
            # and are not at the beginning of a sentence
            if words[i] != '':
                if (words[i])[0].islower() or i == 0:
                    if words[i] != spell(words[i]):
                        if words[i] not in incorrect_words:
                            incorrect_words.append(words[i])
                        # print(words[i])
                elif (words[i])[0].isupper() and '.' in words[i-1] or '?' in words[i-1] or '!' in words[i-1]:
                    # TODO shouldn't this be words[i].lower?
                    if words[i] != spell(words[i]):
                        if words[i] not in incorrect_words:
                            incorrect_words.append(words[i])

    title_words = website_properties['title'].split(' ')

    for i in range(len(title_words)):
        title_words[i] = re.sub('[.:;,!?(){}<>]', '', title_words[i])
        title_words[i] = title_words[i].replace('''”''', '')
        title_words[i] = title_words[i].replace('''“''', '')
        title_words[i] = title_words[i].replace('[', '')
        title_words[i] = title_words[i].replace(']', '')

        if (title_words[i]) != spell(title_words[i]):
            title_spelling_mistakes_count += 1

    website_properties['form_num_spelling_errors'] = len(incorrect_words)
    website_properties['form_num_spelling_errors_title'] = title_spelling_mistakes_count
    website_properties['form_num_consecutive_marks'] = consecutive_marks_count
    website_properties['form_num_all_caps'] = all_caps_words_count
    website_properties['form_lexical_richness'] = len(unique_words)/website_properties['num_words']
    website_properties['form_misspelled_words'] = incorrect_words
    website_properties['form_capitalized_words'] = capitalized_words

    return website_properties


