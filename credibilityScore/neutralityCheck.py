import formalityCheck
import collections
import re


def neutrality_check():

    # Initiating relevant variables for this category
    superlative_count = 0
    superlatives_found = []
    banned_words_dict = {}
    banned_words_found = set([])
    emotion_lexicon_dictionary = collections.defaultdict(list)
    emotion_words_text_dictionary = {}
    emotion_words_found = set([])
    slur_count = 0
    slurs_found = set([])

    # Getting properties dictionary from formalityCheck.py
    website_properties = formalityCheck.formality_check()

    # Splitting cleaned text into paragraphs
    article_paragraphs = [paragraph.strip() for paragraph in website_properties['cleaned_text']]

    # Read superlative text file into list
    with open('./Lexicons/superlatives.txt') as superlatives:
        superlatives_list = superlatives.readlines()

    # Clean superlative list
    superlatives_list = [superlative.strip() for superlative in superlatives_list]
    superlatives_list = superlatives_list[1:]

    for i in range(len(superlatives_list)):
        superlatives_list[i] = (superlatives_list[i].split('\t'))[1]

    # Read Google banned words into list
    with open('./Lexicons/google_banned_words_2021.txt') as banned_words:
        banned_words_list = banned_words.readlines()

    # Clean Google banned words list
    for i in range(len(banned_words_list)):
        banned_words_list[i] = (banned_words_list[i].split('\n'))[0]

    banned_words_set = set(banned_words_list)

    # Read emotional word list into list
    with open('./Lexicons/NRC-Emotion-Lexicon-Wordlevel-v0.92.txt') as nrc_emotion_lexicon:
        emotion_lexicon = nrc_emotion_lexicon.readlines()

    # Clean emotional word list
    for i in range(len(emotion_lexicon)):
        emotion_lexicon[i] = emotion_lexicon[i].strip('\n')
        emotion_lexicon[i] = emotion_lexicon[i].split('\t')

    for word in emotion_lexicon:
        if word.__contains__('1'):
            emotion_lexicon_dictionary[word[0]].append(word[1])

    # Read slurs into list
    with open('./Lexicons/racial_slurs_cleaned.txt') as racial_slurs:
        racial_slur_list = racial_slurs.readlines()

    # Clean slurs list
    for i in range(len(racial_slur_list)):
        racial_slur_list[i] = racial_slur_list[i].strip("\n")

    for paragraph in article_paragraphs:
        words = paragraph.split()

        for i in range(len(words)):

            # Remove special characters from words (exception: hyphen)
            words[i] = re.sub('[.:;,!?(){}<>]', '', words[i])
            words[i] = words[i].replace('''”''', '')
            words[i] = words[i].replace('''“''', '')
            words[i] = words[i].replace('[', '')
            words[i] = words[i].replace(']', '')
            words[i] = words[i].lower()

        # Make string from list of words, append a whitespace before and after,
        # separate each word by whitespace
        cleaned_words = " " + " ".join(words) + " "

        # count number of superlatives
        for superlative in superlatives_list:
            superlative_count += count_overlapping(cleaned_words, superlative)
            if superlative in cleaned_words:
                superlatives_found.append(superlative)

        # Count number of occurrence for each bad word in list, store count in dictionary
        # Some bad words appear in the list multiple times, as parts of expressions
        for banned_word in banned_words_set:
            banned_word_count_paragraph = count_overlapping(cleaned_words, " " + banned_word + " ")
            if banned_word_count_paragraph > 0:
                if banned_word not in banned_words_dict:
                    banned_words_dict[banned_word] = banned_word_count_paragraph
                else:
                    banned_words_dict[banned_word] += banned_word_count_paragraph

        # Check if text contains words with emotional value (from EmoLex)
        # Count occurrences of emotional words for each emotion and the two valences
        for key in emotion_lexicon_dictionary:
            if " " + key + " " in cleaned_words:
                emotion_words_found.add(key)
            emotion_word_occurrence = count_overlapping(cleaned_words, " " + key + " ")
            if emotion_word_occurrence > 0:
                for value in emotion_lexicon_dictionary[key]:
                    if value not in emotion_words_text_dictionary:
                        emotion_words_text_dictionary[value] = 1
                    else:
                        emotion_words_text_dictionary[value] += 1

        # Count number of slurs
        for slur in racial_slur_list:
            slur_count += count_overlapping(cleaned_words, " " + slur.lower() + " ")
            if " " + slur.lower() + " " in cleaned_words:
                slurs_found.add(slur)

    # Check whether both a word and an expression containing it appear in the dictionary of bad word occurrences,
    # subtract number of occurrence in expressions from number of occurrence of word to avoid double counting
    for key1 in banned_words_dict:
        for key2 in banned_words_dict:
            if key1 in key2 and key1 != key2:
                banned_words_dict[key1] = banned_words_dict[key1] - banned_words_dict[key2]

    banned_words_final_count = banned_words_dict.copy()

    for key in banned_words_final_count.keys():
        banned_words_found.add(key)

    # Delete bad words which only appear as part of expressions from the dictionary
    # (their value is 0 because they don't appear alone)
    for key in banned_words_dict:
        if banned_words_dict[key] == 0:
            del banned_words_final_count[key]

    # Add relevant metrics to properties dictionary
    website_properties['neut_num_superlatives'] = superlative_count
    website_properties['neut_num_banned_words'] = str(sum(banned_words_final_count.values()))
    website_properties['neut_num_emotional'] = emotion_words_text_dictionary["positive"] + emotion_words_text_dictionary["negative"]
    website_properties['neut_num_emotion_positive'] = emotion_words_text_dictionary["positive"]
    website_properties['neut_num_emotion_negative'] = emotion_words_text_dictionary["negative"]
    website_properties['neut_num_slurs'] = slur_count
    website_properties['neut_superlatives_found'] = superlatives_found
    website_properties['neut_banned_words_found'] = list(banned_words_found)
    website_properties['neut_emotional_words_found'] = list(emotion_words_found)
    website_properties['neut_slurs_found'] = list(slurs_found)

    return website_properties


# https://stackoverflow.com/questions/2970520/string-count-with-overlapping-occurrences
def count_overlapping(string, sub):
    count = start = 0
    while True:
        start = string.find(sub, start) + 1
        if start > 0:
            count+=1
        else:
            return count
