import collections
import re


def neutrality_check():

    superlative_count = 0
    banned_words_dict = {}
    emotion_lexicon_dictionary = collections.defaultdict(list)
    emotion_words_text_dictionary = {}
    slur_count = 0
    total_word_number = 0

    # Read article text into list
    with open('cleanedTextFile.txt') as cleaned_text_file:
        article_paragraphs = cleaned_text_file.readlines()

    article_paragraphs = [paragraph.strip() for paragraph in article_paragraphs]

    # Read superlative text file into list
    with open('superlatives.txt') as superlatives:
        superlatives_list = superlatives.readlines()

    # Clean superlative list
    superlatives_list = [superlative.strip() for superlative in superlatives_list]
    superlatives_list = superlatives_list[1:]

    for i in range(len(superlatives_list)):
        superlatives_list[i] = (superlatives_list[i].split('\t'))[1]

    # print(superlatives_list)

    # Read Google banned words into list
    with open('google_banned_words_2021.txt') as banned_words:
        banned_words_list = banned_words.readlines()

    # Clean Google banned words list
    for i in range(len(banned_words_list)):
        banned_words_list[i] = (banned_words_list[i].split('\n'))[0]

    banned_words_set = set(banned_words_list)

    with open('NRC-Emotion-Lexicon-Wordlevel-v0.92.txt') as nrc_emotion_lexicon:
        emotion_lexicon = nrc_emotion_lexicon.readlines()

    for i in range(len(emotion_lexicon)):
        emotion_lexicon[i] = emotion_lexicon[i].strip('\n')
        emotion_lexicon[i] = emotion_lexicon[i].split('\t')

    for word in emotion_lexicon:
        if word.__contains__('1'):
            emotion_lexicon_dictionary[word[0]].append(word[1])
            #print(word)

    with open('racial_slurs.txt') as racial_slurs:
        racial_slur_list = racial_slurs.readlines()

    for i in range(len(racial_slur_list)):
        racial_slur_list[i] = racial_slur_list[i].strip("\n")

    for paragraph in article_paragraphs:
        words = paragraph.split()

        total_word_number += len(words)

        for i in range(len(words)):

            # Remove special characters from words (exception: hyphen)
            words[i] = re.sub('[.:;,!?(){}<>]', '', words[i])
            words[i] = words[i].replace('''”''', '')
            words[i] = words[i].replace('''“''', '')
            words[i] = words[i].replace('[', '')
            words[i] = words[i].replace(']', '')
            words[i] = words[i].lower()

        # print(words)

        # make string from list of words, append a whitespace before and after,
        # separate each word by whitespace
        cleaned_words = " " + " ".join(words) + " "

        # count number of superlatives
        for superlative in superlatives_list:
            superlative_count += count_overlapping(cleaned_words, superlative)

        # Count number of occurrence for each bad word in list, store count in dictionary
        # Some bad words appear in the list multiple times, as parts of expressions
        for banned_word in banned_words_set:
            banned_word_count_paragraph = count_overlapping(cleaned_words, " " + banned_word + " ")
            if banned_word_count_paragraph > 0:
                if banned_word not in banned_words_dict:
                    banned_words_dict[banned_word] = banned_word_count_paragraph
                else:
                    banned_words_dict[banned_word] += banned_word_count_paragraph

        # print(banned_words_dict)

        # Check if text contains words with emotional value (from EmoLex)
        # Count occurrences of emotional words for each emotion and the two valences
        for key in emotion_lexicon_dictionary:
            emotion_word_occurrence = count_overlapping(cleaned_words, " " + key + " ")
            if emotion_word_occurrence > 0:
                # print(key, emotion_lexicon_dictionary[key], emotion_word_occurrence)
                for value in emotion_lexicon_dictionary[key]:
                    if value not in emotion_words_text_dictionary:
                        emotion_words_text_dictionary[value] = 1
                    else:
                        emotion_words_text_dictionary[value] += 1

        for slur in racial_slur_list:
            slur_count += count_overlapping(cleaned_words, " " + slur.lower() + " ")

    # print(emotion_words_text_dictionary)

    # Check whether both a word and an expression containing it appear in the dictionary of bad word occurrences,
    # subtract number of occurrence in expressions from number of occurrence of word to avoid double counting
    for key1 in banned_words_dict:
        for key2 in banned_words_dict:
            if key1 in key2 and key1 != key2:
                banned_words_dict[key1] = banned_words_dict[key1] - banned_words_dict[key2]

    banned_words_final_count = banned_words_dict.copy()

    # Delete bad words which only appear as part of expressions from the dictionary
    # (their value is 0 because they don't appear alone)
    for key in banned_words_dict:
        if banned_words_dict[key] == 0:
            del banned_words_final_count[key]

    # for key in emotion_words_text_dictionary:
    #     if key != "negative" and key != "positive":
    #         print(emotion_words_text_dictionary[key], "instances of words corresponding to the emotion", key, "found")

    open("neutralityTestResults.txt", "w").close()

    neutrality_test_results = open("neutralityTestResults.txt", "a")

    # Copy the results of our neutrality check to the results file -> we will use it in the test cases
    line1_result = neutrality_test_results.write(str(superlative_count))
    line1_message = neutrality_test_results.write(' superlatives identified\n')

    line2_result = neutrality_test_results.write(str(len(banned_words_final_count)))
    line2_message = neutrality_test_results.write(' profanities found in ')
    line2_result2 = neutrality_test_results.write(str(sum(banned_words_final_count.values())))
    line2_message2 = neutrality_test_results.write(' instances\n')

    emotional_word_ratio = emotion_words_text_dictionary["positive"]/total_word_number + emotion_words_text_dictionary["negative"]/total_word_number
    if emotional_word_ratio >= 0.05:
        line3_result = neutrality_test_results.write("Unacceptable emotional word ratio\n")
    else:
        line3_result = neutrality_test_results.write("Acceptable emotional word ratio\n")

    # line4_result = neutrality_test_results.write(str(emotion_words_text_dictionary["negative"]/total_word_number))
    # line4_message = neutrality_test_results.write(' negative emotion word ratio\n')

    line4_result = neutrality_test_results.write(str(slur_count))
    line4_message1 = neutrality_test_results.write(' slurs identified\n')

# https://stackoverflow.com/questions/2970520/string-count-with-overlapping-occurrences
def count_overlapping(string, sub):
    count = start = 0
    while True:
        start = string.find(sub, start) + 1
        if start > 0:
            count+=1
        else:
            return count

neutrality_check()
