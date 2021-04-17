import json

def layoutCheck():
    with open('./Layout/report/1-layoutcheck.json', 'r') as layoutTest:
        data=layoutTest.read()
    layoutTest.close()

    obj = json.loads(data)
    galenCheckDict = {}

    galenCheckDict = ((((((((obj['report'])['nodes'])[0])['nodes'])[1])['nodes'])[0])['sections'])

    # print(galenCheckDict[0])

    layout_results = {
        'num_photos': 0,
        'video_present': False,
        'headline_font_size': False,
        'text_font_size': False,
        'headline_font_type': False,
        'text_font_type': False
    }

    for i in range(len(galenCheckDict)):
        if (galenCheckDict[i])['name'] == 'Picture check':
            pictureObjects = str((galenCheckDict[i])['objects'])
            layout_results['num_photos'] = pictureObjects.count('\'status\': \'info\'')
        if (galenCheckDict[i])['name'] == 'Video check':
            videoObjects = str((galenCheckDict[i])['objects'])
            if videoObjects.count('\'status\': \'info\'') == 1:
                layout_results['video_present'] = True
        if (galenCheckDict[i])['name'] == 'Font size check for headline':
            fontObjects = str((galenCheckDict[i])['objects'])
            if fontObjects.count('\'status\': \'info\'') > 0:
                layout_results['headline_font_size'] = True
        if (galenCheckDict[i])['name'] == 'Font size check for text':
            fontObjects = str((galenCheckDict[i])['objects'])
            if fontObjects.count('\'status\': \'info\'') > 0:
                layout_results['text_font_size'] = True
            if fontObjects.count('\"text\" is not visible on page') > 0:
                layout_results['text_font_size'] = 'not identified'
        if (galenCheckDict[i])['name'] == 'Font type check for headline':
            fontTypeObjects = str((galenCheckDict[i])['objects'])
            if fontTypeObjects.count('\'status\': \'info\'') == 0:
                layout_results['headline_font_type'] = True
        if (galenCheckDict[i])['name'] == 'Font type check for text':
            fontTypeObjects = str((galenCheckDict[i])['objects'])
            if fontTypeObjects.count('\'status\': \'info\'') == 0:
                layout_results['text_font_type'] = True
            if fontTypeObjects.count('\"text\" is not visible on page') > 0:
                layout_results['text_font_type'] = 'not identified'

    return(layout_results)

#layoutCheck()