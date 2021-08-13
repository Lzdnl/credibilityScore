import credibilityScore.calculateScore as calculateScore
import sys
from io import StringIO
from csv import DictWriter

# Function for calculating credibility score of large number of articles
# Goes through dataset one by one and runs the calculateScore function
# Stores score results in csv file
def for_testing_calculate_score():

    all_scores = []

    with open('fake_news_collection.txt') as fn:
        fake_news = fn.readlines()

    for i in range(len(fake_news)):
        fake_news[i] = (fake_news[i].split('\n'))[0]

    for i in range(len(fn)):
        try:
            sys.stdin = StringIO(fake_news[i])
            score_elements = calculateScore.calculate_score()
            score_elements['url'] = fake_news[i]
            all_scores.append(score_elements)
            with open('fake_news_collection_scores2.csv', 'w') as outfile:
                writer = DictWriter(outfile,
                                    ('form_score_spelling', 'form_score_punctuation', 'form_score_capitalization',
                                     'form_score_complexity', 'neut_score_superlatives', 'neut_score_emotional',
                                     'neut_score_banned', 'neut_score_slurs', 'tran_score_citations',
                                     'tran_score_external_references', 'tran_score_broken_links', 'tran_score_author',
                                     'lay_score_photos', 'lay_score_video', 'lay_score_font_size',
                                     'lay_score_font_type', 'score_formality', 'score_neutrality', 'score_transparency',
                                     'score_layout', 'credibility_score', 'credibility_score_weighted', 'url'))
                writer.writeheader()
                writer.writerows(all_scores)
        except:
            print("An error has occurred. Moving on to the next article.")

for_testing_calculate_score()
