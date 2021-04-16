def createGalenTest():

    with open('websiteProperties.txt', 'r') as wProp:
        website_url=wProp.readlines()[0].strip("\n")
    wProp.close()

    galenTest = open("./Layout/layoutCheck.test", "w")
    galenTest.write("layoutCheck\n    jsfactory ./Layout/mydriver.js " + website_url + " 768x576\n" + "        wait 1s\n        check ./Layout/layoutCheck.gspec --include \"all\"")
    galenTest.close()

createGalenTest()