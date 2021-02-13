import re


def neutrality_check():

    superlative_count = 0
    banned_words_dict = {}

    # Read article text into list
    with open('./test/cleanedTextFile2.txt') as cleaned_text_file:
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
    with open('google_banned_words_2021_01_18.txt') as banned_words:
        banned_words_list = banned_words.readlines()

    # Clean Google banned words list
    for i in range(len(banned_words_list)):
        banned_words_list[i] = (banned_words_list[i].split('\n'))[0]

    banned_words_set = set(banned_words_list)

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

        # print(words)

        # make string from list of words, append a whitespace before and after,
        # separate each word by whitespace
        cleaned_words = " " + " ".join(words) + " "

        # count number of superlatives
        for superlative in superlatives_list:
            superlative_count += cleaned_words.count(superlative)

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

    print(superlative_count, "superlatives found")
    print(len(banned_words_final_count), "profanities found in a total of",
          sum(banned_words_final_count.values()), "instances")

def count_overlapping(string, sub):
    count = start = 0
    while True:
        start = string.find(sub, start) + 1
        if start > 0:
            count+=1
        else:
            return count

neutrality_check()
