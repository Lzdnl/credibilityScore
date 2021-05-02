import layoutCheck


def calculate_score():

    website_properties = layoutCheck.layoutCheck()

    print("Calculating score...\n")

    for key in website_properties.keys():
        if key.__contains__('tran') or key.__contains__('neut') or key.__contains__('form') or key.__contains__('lay'):
            print(key + ": " + str(website_properties[key]))

    print("num_sentences: " + str(website_properties['num_sentences']))
    print("num_words: " + str(website_properties['num_words']))

    print("___________________________________________________________________________")
    print("___________________________________________________________________________")

    title_length = website_properties['title'].count(" ")

    # ________________________________ Formality Score _________________________________________________________
    form_score_spelling = 1 - (website_properties['form_num_spelling_errors_title']/title_length +
                               website_properties['form_num_spelling_errors']/website_properties['num_words'])

    if website_properties['form_num_consecutive_marks'] > 0:
        score_consecutive_marks = 0
    else:
        score_consecutive_marks = 1

    if website_properties['form_num_marks_title'] > 0:
        score_marks_title = 0
    else:
        score_marks_title = 1

    score_marks_text = 1 - (website_properties['form_num_marks_text']/website_properties['num_sentences'])

    form_score_punctuation = (score_consecutive_marks + score_marks_title + score_marks_text) / 3

    if website_properties['form_num_all_caps'] > 0:
        form_score_capitalization = 0.0
    else:
        form_score_capitalization = 1.0

    # Fake news are semantically more complex than real news
    # Real news are syntactically more complex than fake news
    form_score_semantic_complexity = 1 - website_properties['form_lexical_richness']
    form_score_syntactic_complexity = 1 - website_properties['num_sentences']/website_properties['num_words']
    form_score_complexity = (form_score_syntactic_complexity + form_score_semantic_complexity) / 2

    print("form_score_spelling: ", form_score_spelling)
    print("form_score_punctuation: ", form_score_punctuation)
    print("form_score_capitalization", form_score_capitalization)
    print("form_score_complexity: ", form_score_complexity)

    score_formality = (form_score_spelling + form_score_punctuation + form_score_capitalization +
                       form_score_complexity)

    print("\nscore_formality: ", score_formality, "\n")

    # ______________________________________ Neutrality Score ______________________________________________________

    neut_score_superlatives = 1 - website_properties['neut_num_superlatives']/website_properties['num_words']

    # If the article is marked as opinion, it's OK to use emotional words
    neut_score_emotional = 1- website_properties['neut_num_emotional']/website_properties['num_words']
    if website_properties['tran_marked_as_opinion'] == True:
        neut_score_emotional = 1
    neut_score_banned = 1 - int(website_properties['neut_num_banned_words'])/int(website_properties['num_words'])

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

    tran_score_citations = (tran_score_references + tran_score_direct_quotes) / website_properties['num_sentences']

    tran_score_external_references = website_properties['tran_num_refs_external'] / website_properties['tran_num_refs']
    tran_score_broken_links = 1- (website_properties['tran_num_broken_links'] / website_properties['tran_num_refs'])

    if website_properties['tran_author'] == True:
        tran_score_author = 1
    else:
        tran_score_author = 0

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

    if website_properties['lay_video_present'] == True:
        lay_score_video = 1
    else:
        lay_score_video = 0

    if website_properties['lay_headline_font_size'] == True:
        lay_score_headline_size = 1
    else:
        lay_score_headline_size = 0

    if website_properties['lay_text_font_size'] == True or website_properties['lay_text_font_size'] == 'not identified':
        lay_score_text_size = 1
    else:
        lay_score_text_size = 0

    lay_score_font_size = (lay_score_headline_size + lay_score_text_size) / 2

    if website_properties['lay_headline_font_type'] == True:
        lay_score_headline_type = 1
    else:
        lay_score_headline_type = 0

    if website_properties['lay_text_font_type'] == True or website_properties['lay_text_font_type'] == 'not identified':
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


calculate_score()
