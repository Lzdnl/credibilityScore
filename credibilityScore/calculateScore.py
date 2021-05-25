import layoutCheck


def calculate_score():

    website_properties = layoutCheck.layoutCheck()

    print("Calculating score...\n")

    for key in website_properties.keys():
        if key.__contains__('tran') or key.__contains__('neut') or key.__contains__('form') or key.__contains__('lay'):
            print(key + ": " + str(website_properties[key]))

    print("num_sentences: " + str(website_properties['num_sentences']))
    print("num_words: " + str(website_properties['num_words']))
    print("num_unique_words: " + str(website_properties['num_unique_words']))

    print("___________________________________________________________________________")
    print("___________________________________________________________________________")

    title_length = website_properties['title'].count(" ") + 1

    # ________________________________ Formality Score _________________________________________________________
    MIN_FORMALITY = 0.8
    MIN_COMPLEXITY = 0.2
    MAX_COMPLEXITY = 0.45

    spelling_error_rate = 1 - (website_properties['form_num_spelling_errors_title']/title_length +
                               website_properties['form_num_spelling_errors']/website_properties['num_unique_words'])/2

    form_score_spelling = max(0, (spelling_error_rate - MIN_FORMALITY) / (1 - MIN_FORMALITY))

    if website_properties['form_num_consecutive_marks'] or website_properties['form_num_marks_title'] > 0:
        form_score_punctuation = 0
    else:
        score_marks_text = 1 - (website_properties['form_num_marks_text']/website_properties['num_sentences'])
        form_score_punctuation = max(0, (score_marks_text - MIN_FORMALITY) / (1 - MIN_FORMALITY))

    all_caps_error_rate = 1 - website_properties['form_num_all_caps']/website_properties['num_words']
    form_score_capitalization = max(0, (all_caps_error_rate - MIN_FORMALITY) / (1 - MIN_FORMALITY))

    # Fake news are semantically more complex than real news
    # Real news are syntactically more complex than fake news
    form_score_semantic_complexity = 1 - website_properties['form_lexical_richness']
    form_score_syntactic_complexity = website_properties['num_sentences']/website_properties['num_words']
    complexity_rate = (form_score_syntactic_complexity + form_score_semantic_complexity) / 2
    form_score_complexity = max(0, (complexity_rate - MIN_COMPLEXITY) / (MAX_COMPLEXITY - MIN_COMPLEXITY))
    form_score_complexity = min(form_score_complexity, 1)

    print("form_score_spelling: ", form_score_spelling)
    print("form_score_punctuation: ", form_score_punctuation)
    print("form_score_capitalization", form_score_capitalization)
    print("form_score_complexity: ", form_score_complexity)

    score_formality = (form_score_spelling + form_score_punctuation + form_score_capitalization +
                       form_score_complexity)

    print("\nscore_formality: ", score_formality, "\n")

    # ______________________________________ Neutrality Score ______________________________________________________

    MIN_NEUTRALITY = 0.8

    superlative_rate = 1 - website_properties['neut_num_superlatives']/website_properties['num_words']
    neut_score_superlatives = max(0, (superlative_rate - MIN_NEUTRALITY) / (1 - MIN_NEUTRALITY))

    # If the article is marked as opinion, it's OK to use emotional words
    emotional_rate = 1 if website_properties['tran_marked_as_opinion'] else \
        1- website_properties['neut_num_emotional']/website_properties['num_words']
    neut_score_emotional = max(0, (emotional_rate - MIN_NEUTRALITY) / (1 - MIN_NEUTRALITY))

    banned_rate = 1 - int(website_properties['neut_num_banned_words'])/int(website_properties['num_words'])
    neut_score_banned = max(0, (banned_rate - MIN_NEUTRALITY) / (1 - MIN_NEUTRALITY))

    if website_properties['neut_num_slurs'] > 0:
        neut_score_slurs = 0
    else:
        neut_score_slurs = 1

    score_neutrality = neut_score_superlatives + neut_score_emotional + neut_score_banned + neut_score_slurs

    print("neut_score_superlatives: ", neut_score_superlatives)
    print("neut_score_emotional: ", neut_score_emotional)
    print("neut_score_banned: ", neut_score_banned)
    print("neut_score_slurs: ", neut_score_slurs)

    print ("\nscore_neutrality: ", score_neutrality, "\n")

    # ___________________________________ Transparency Score _______________________________________________________

    tran_score_references = website_properties['tran_num_refs']
    tran_score_direct_quotes = website_properties['tran_num_direct_quotes']

    tran_score_citations = min(1, (tran_score_references + tran_score_direct_quotes) / website_properties['num_sentences'])

    if website_properties['tran_num_refs'] == 0:
        tran_score_external_references = 0
        tran_score_broken_links = 0
    else:
        tran_score_external_references = website_properties['tran_num_refs_external'] / website_properties['tran_num_refs']
        tran_score_broken_links = 1 - (website_properties['tran_num_broken_links'] / website_properties['tran_num_refs'])

    if website_properties['tran_author']:
        tran_score_author = 1
    else:
        tran_score_author = 0

    if website_properties['tran_marked_as_opinion'] and website_properties['tran_author']:
        tran_score_citations = 1
        tran_score_external_references = 1
        tran_score_broken_links = 1

    score_transparency = tran_score_citations + tran_score_external_references + tran_score_broken_links + \
                         tran_score_author

    print("tran_score_citations: ", tran_score_citations)
    print("tran_score_external_references: ", tran_score_external_references)
    print("tran_score_broken_links: ", tran_score_broken_links)
    print("tran_score_author: ", tran_score_author)

    print("\nscore_transparency: ", score_transparency, "\n")

    # ______________________________________ Layout Score __________________________________________________________

    if website_properties['lay_num_photos'] == 0:
        lay_score_photos = 0
    if 0 < website_properties['lay_num_photos'] <= 2:
        if website_properties['num_words'] <= 500:
            lay_score_photos = 1
        else:
            lay_score_photos = 0.5
    if 2 < website_properties['lay_num_photos'] <= 7:
        if website_properties['num_words'] <= 500:
            lay_score_photos = 0.5
        else:
            lay_score_photos = 1
    if website_properties['lay_num_photos'] > 7:
        if website_properties['num_words'] <= 500:
            lay_score_photos = 0.25
        else:
            lay_score_photos = 0.75

    if website_properties['lay_video_present']:
        lay_score_video = 1
    else:
        lay_score_video = 0

    if website_properties['lay_headline_font_size']:
        lay_score_headline_size = 1
    else:
        lay_score_headline_size = 0

    if website_properties['lay_text_font_size'] or website_properties['lay_text_font_size'] == 'not identified':
        lay_score_text_size = 1
    else:
        lay_score_text_size = 0

    lay_score_font_size = (lay_score_headline_size + lay_score_text_size) / 2

    if website_properties['lay_headline_font_type']:
        lay_score_headline_type = 1
    else:
        lay_score_headline_type = 0

    if website_properties['lay_text_font_type'] or website_properties['lay_text_font_type'] == 'not identified':
        lay_score_text_type = 1
    else:
        lay_score_text_type = 0

    lay_score_font_type = (lay_score_headline_type + lay_score_text_type) / 2

    score_layout = lay_score_photos + lay_score_video + lay_score_font_size + lay_score_font_type

    print("lay_score_photos: ", lay_score_photos)
    print("lay_score_video: ", lay_score_video)
    print("lay_score_font_size: ", lay_score_font_size)
    print("lay_score_font_type: ", lay_score_font_type)

    print("\nscore_layout: ", score_layout, "\n")

    credibility_score = (score_formality + score_neutrality + score_transparency + score_layout) * 10 / 16

    print("credibility_score: ", credibility_score)

    if website_properties['tran_marked_as_opinion']:
        print("This article is an opinion piece. Language emotionality and presence of references are not taken into "
              "account.")

    score_elements = {
        'form_score_spelling': form_score_spelling,
        'form_score_punctuation': form_score_punctuation,
        'form_score_capitalization': form_score_capitalization,
        'form_score_complexity': form_score_complexity,
        'neut_score_superlatives': neut_score_superlatives,
        'neut_score_emotional': neut_score_emotional,
        'neut_score_banned': neut_score_banned,
        'neut_score_slurs': neut_score_slurs,
        'tran_score_citations': tran_score_citations,
        'tran_score_external_references': tran_score_external_references,
        'tran_score_broken_links': tran_score_broken_links,
        'tran_score_author': tran_score_author,
        'lay_score_photos': lay_score_photos,
        'lay_score_video': lay_score_video,
        'lay_score_font_size': lay_score_font_size,
        'lay_score_font_type': lay_score_font_type
    }

    score_weights = {
        'form_score_spelling': 0.2,
        'form_score_punctuation': 0.3,
        'form_score_capitalization': 0.1,
        'form_score_complexity': 0.3,
        'neut_score_superlatives': 0.2,
        'neut_score_emotional': 0.2,
        'neut_score_banned': 0.1,
        'neut_score_slurs': 0.1,
        'tran_score_citations': 0.2,
        'tran_score_external_references': 0.1,
        'tran_score_broken_links': 0.1,
        'tran_score_author': 0.2,
        'lay_score_photos': 0.1,
        'lay_score_video': 0.1 if lay_score_video == 1 else 0.0,
        'lay_score_font_size': 0.05,
        'lay_score_font_type': 0.05
    }

    credibility_score_weighted = 0

    for key in score_elements.keys():
        credibility_score_weighted += score_elements[key] * score_weights[key]
        #print(credibility_score_weighted)

    credibility_score_weighted = credibility_score_weighted / 2.4 if lay_score_video == 1 else credibility_score_weighted / 2.3

    print("Weighted credibility score:", credibility_score_weighted)
    
    score_elements['score_formality'] = score_formality
    score_elements['score_neutrality'] = score_neutrality
    score_elements['score_transparency'] = score_transparency
    score_elements['score_layout'] = score_layout
    score_elements['credibility_score'] = credibility_score
    score_elements['credibility_score_weighted'] = credibility_score_weighted

    return score_elements

#calculate_score()
