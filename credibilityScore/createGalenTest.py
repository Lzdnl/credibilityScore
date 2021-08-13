import transparencyCheck
import os


def create_galen_test():

    # Get properties dictionary from transparencyCheck.py
    website_properties = transparencyCheck.transparency_check()

    # Get URL of article
    website_url = website_properties['url']

    # We need to create the Galen test file at runtime because the URL is hardcoded into the test file
    # No dynamic URL passing possible with Galen
    galenTest = open("./Layout/layoutCheck.test", "w")
    galenTest.write("layoutCheck\n    jsfactory ./Layout/mydriver.js " + website_url + " 768x576\n" + "        wait 10s\n        check ./Layout/layoutCheck.gspec --include \"all\"")
    galenTest.close()

    # Starting the Galen layout test with hardcoded command
    print("Running layout tests...")
    os.system('command galen test ./Layout/layoutCheck.test --htmlreport "./Layout/report" >/dev/null 2>&1')

    return website_properties
