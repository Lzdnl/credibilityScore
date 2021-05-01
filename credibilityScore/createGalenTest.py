import transparencyCheck
import os


def createGalenTest():

    website_properties = transparencyCheck.transparency_check()

    website_url = website_properties['url']

    galenTest = open("./Layout/layoutCheck.test", "w")
    galenTest.write("layoutCheck\n    jsfactory ./Layout/mydriver.js " + website_url + " 768x576\n" + "        wait 1s\n        check ./Layout/layoutCheck.gspec --include \"all\"")
    galenTest.close()

    print("Running layout tests...")
    os.system('command galen test ./Layout/layoutCheck.test --htmlreport "./Layout/report" >/dev/null 2>&1')

    return website_properties
