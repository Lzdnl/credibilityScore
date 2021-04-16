import json

def layoutCheck():
    with open('./Layout/report/1-layoutcheck.json', 'r') as layoutTest:
        data=layoutTest.read()
    layoutTest.close()

    obj = json.loads(data)
    galenCheckDict = {}

    galenCheckDict = ((((((((obj['report'])['nodes'])[0])['nodes'])[1])['nodes'])[0])['sections'])

    # print(galenCheckDict[0])

    for i in range(len(galenCheckDict)):
        if (galenCheckDict[i])['name'] == 'Picture check':
            pictureObjects = str((galenCheckDict[i])['objects'])
            print(pictureObjects.count('\'status\': \'info\''), "pictures found in article")
        if (galenCheckDict[i])['name'] == 'Video check':
            videoObjects = str((galenCheckDict[i])['objects'])
            if videoObjects.count('\'status\': \'info\'') == 1:
                print("Video found")
            else:
                print("No video found")
        if (galenCheckDict[i])['name'] == 'Font size check for headline':
            fontObjects = str((galenCheckDict[i])['objects'])
            if fontObjects.count('\'status\': \'info\'') > 1:
                print("Balanced font size for headline")
            else:
                print("Unbalanced font size for headline")
        if (galenCheckDict[i])['name'] == 'Font size check for text':
            fontObjects = str((galenCheckDict[i])['objects'])
            if fontObjects.count('\'status\': \'info\'') > 1:
                print("Balanced font size for text")
            else:
                print("Unbalanced font size for text")
        if (galenCheckDict[i])['name'] == 'Font type check for headline':
            fontTypeObjects = str((galenCheckDict[i])['objects'])
            if fontTypeObjects.count('\'status\': \'info\'') == 0:
                print("Serif fonts used in headline")
            else:
                print("Sans-serif fonts used in headline")
        if (galenCheckDict[i])['name'] == 'Font type check for text':
            fontTypeObjects = str((galenCheckDict[i])['objects'])
            if fontTypeObjects.count('\'status\': \'info\'') == 0:
                print("Serif fonts used in text")
            else:
                print("Sans-serif fonts used in text")

layoutCheck()