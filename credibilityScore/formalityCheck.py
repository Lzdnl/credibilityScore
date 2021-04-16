from autocorrect import Speller
import re


def formality_check():

    marks_count_title = 0
    marks_count = 0
    consecutive_marks_count = 0
    all_caps_words_count = 0
    capitalized_words = []
    spelling_mistakes_count = 0
    incorrect_words = []
    title_spelling_mistakes_count = 0
    unique_words = set([])
    total_word_count = 0
    formality_results = {}

    spell = Speller(lang='en')

    with open('cleanedTextFile.txt') as cleaned_text_file:
        article_paragraphs = cleaned_text_file.readlines()

    article_paragraphs = [paragraph.strip() for paragraph in article_paragraphs]

    # Count total number of words (will be used for normalization of spelling mistakes)
    for paragraph in article_paragraphs:
        words = paragraph.split(" ")
        total_word_count = total_word_count + len(words)

    wProp = open("websiteProperties.txt", "a")
    wProp.writelines(str(total_word_count) + "\n")
    wProp.close()

    # Check for exclamation or question marks in the title
    marks_count_title = article_paragraphs[0].count('!')
    marks_count_title += article_paragraphs[0].count('?')

    for paragraph in article_paragraphs:
        # Check for consecutive exclamation or question marks in each paragraph
        consecutive_marks_count += paragraph.count('!!')
        consecutive_marks_count += paragraph.count('??')
        # The literature say it also makes sense to count single instances of '?'
        marks_count += paragraph.count('?')

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
    for paragraph in article_paragraphs:
        words = paragraph.split(' ')

        for i in range(len(words)):

            # Remove special characters from beginning and end of words
            words[i] = re.sub('[.:;,!?(){}<>]', '', words[i])
            words[i] = words[i].replace('''”''', '')
            words[i] = words[i].replace('''“''', '')
            words[i] = words[i].replace('[', '')
            words[i] = words[i].replace(']', '')

            # exclude acronyms and common names by looking for words which begin with a majuscule
            # and are not at the beginning of a sentence
            if words[i] != '':
                if (words[i])[0].islower() or i==0:
                    if words[i] != spell(words[i]):
                        if words[i] not in incorrect_words:
                            incorrect_words.append(words[i])
                        # print(words[i])
                elif (words[i])[0].isupper() and '.' in words[i-1] or '?' in words[i-1] or '!' in words[i-1]:
                    if words[i] != spell(words[i]):
                        if words[i] not in incorrect_words:
                            incorrect_words.append(words[i])

    title_words = article_paragraphs[0].split(' ')

    for i in range(len(title_words)):
        title_words[i] = re.sub('[.:;,!?(){}<>]', '', title_words[i])
        title_words[i] = title_words[i].replace('''”''', '')
        title_words[i] = title_words[i].replace('''“''', '')
        title_words[i] = title_words[i].replace('[', '')
        title_words[i] = title_words[i].replace(']', '')

        if (title_words[i]) != spell(title_words[i]):
            title_spelling_mistakes_count += 1
            # print(title_words[i])

    formality_results['num_spelling_errors'] = len(incorrect_words)
    formality_results['num_spelling_errors_title'] = title_spelling_mistakes_count
    formality_results['num_consecutive_marks'] = consecutive_marks_count
    formality_results['num_marks_title'] = marks_count_title
    formality_results['num_marks_text'] = marks_count - marks_count_title
    formality_results['num_all_caps'] = all_caps_words_count
    formality_results['lexical_richness'] = len(unique_words)/total_word_count
    formality_results['misspelled_words'] = incorrect_words
    formality_results['capitalized_words'] = capitalized_words

    # Clear the file if there's already something written in it
    #open("formalityTestResults.txt", "w").close()

    #formality_test_results = open("formalityTestResults.txt", "a")

    # Copy the results of our formality check to the results file -> we will use it in the test cases
    #line1_result = formality_test_results.write(str(marks_count_title))
    #line1_message = formality_test_results.write(' ! or ? in title\n')

    #line2_result = formality_test_results.write(str(marks_count))
    #line2_message = formality_test_results.write(' ? in total\n')

    #line3_result = formality_test_results.write(str(consecutive_marks_count))
    #line3_message = formality_test_results.write(' consecutive ! or ? \n')

    #line4_result = formality_test_results.write(str(all_caps_words_count))
    #line4_message = formality_test_results.write( ' words in all caps found \n')

    #line5_result = formality_test_results.write(str(title_spelling_mistakes_count))
    #line5_message = formality_test_results.write(' spelling mistakes found in title \n')

    #if spelling_error_rate >= 1:
    #    line6 = formality_test_results.write('Unacceptable error rate \n')
    #else:
    #    line6 = formality_test_results.write('Acceptable error rate \n')

    #if lexical_richness > 0.4:
    #    line7 = formality_test_results.write('Higher than average lexical density')
    #else:
    #    line7 = formality_test_results.write('Average or less than average lexical richness')

    #formality_test_results.close()

    return formality_results

#formality_check()

