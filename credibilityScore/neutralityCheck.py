import re

def neutrality_check():

    superlative_count = 0
    superlatives_list = []

    # Read article text into list
    with open('cleanedTextFile.txt') as cleaned_text_file:
        article_paragraphs = cleaned_text_file.readlines()

    article_paragraphs = [paragraph.strip() for paragraph in article_paragraphs]

    # Read superlative text file into list
    with open('superlatives.txt') as superlatives:
        superlatives_list = superlatives.readlines()

    superlatives_list = [superlative.strip() for superlative in superlatives_list]
    superlatives_list = superlatives_list[1:]

    for i in range(len(superlatives_list)):
        superlatives_list[i] = (superlatives_list[i].split('\t'))[1]

    for paragraph in article_paragraphs:
        words = paragraph.split(' ')
        for i in range(len(words)):

            # Remove special characters from words (exception: hyphen)
            words[i] = re.sub('[.:;,!?(){}<>]', '', words[i])
            words[i] = words[i].replace('''”''', '')
            words[i] = words[i].replace('''“''', '')
            words[i] = words[i].replace('[', '')
            words[i] = words[i].replace(']', '')

            # attempt at superlative detection
        for superlative in superlatives_list:
            superlative_count += paragraph.lower().count(superlative)

    print(superlative_count, "superlatives found")



neutrality_check()