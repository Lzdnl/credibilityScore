import getWebsiteText


def clean_website_text():

    article_paragraphs = []
    num_words = 0
    num_sentences = 0

    # Get properties dictionary returned by getWebsiteText.py
    website_properties = getWebsiteText.get_website_text(input("Enter URL: "))

    # Split website text into paragraphs
    paragraphs = str(website_properties['all_text']).split("\n")

    # Paragraph analysis by number of words, presence of punctuation, presence of disclaimer content
    # Meant to eliminate text from ads, disclaimers, footers, page buttons etc
    for i in range(len(paragraphs)):
        num_words = paragraphs[i].count(' ')+1
        if num_words > 15:
            if '.' in paragraphs[i] or '!' in paragraphs[i] or '?' in paragraphs[i]:
                if not paragraphs[i].lower().__contains__('cookie policy'):
                    if not paragraphs[i].lower().__contains__('all rights reserved'):
                        article_paragraphs.append(paragraphs[i])

    # The remaining paragraphs are analyzed. Refinement to eliminate text of ads.
    # Meant to eliminate all text detected after the first advertisement (these are usually below the article)
    for i in range(int(len(paragraphs)/2), len(paragraphs)):
        if paragraphs[i] in article_paragraphs:
            if paragraphs[i+1] not in article_paragraphs and paragraphs[i+2] not in article_paragraphs and \
                    paragraphs[i+3] not in article_paragraphs:
                article_paragraphs = article_paragraphs[:(article_paragraphs.index(paragraphs[i]))]
        break

    # Adding cleaned text to properties dictionary
    website_properties['cleaned_text'] = article_paragraphs

    # Counting number of words and sentences and adding them to the properties dictionary
    for paragraph in article_paragraphs:
        words = paragraph.split()
        num_words += len(words)
        num_sentences += paragraph.count(".")
        num_sentences += paragraph.count("!")
        num_sentences += paragraph.count("?")

    website_properties['num_words'] = num_words
    website_properties['num_sentences'] = num_sentences

    return website_properties
