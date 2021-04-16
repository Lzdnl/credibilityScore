import createGalenTest
import getWebsiteText
import cleanWebsiteText
import formalityCheck
import neutralityCheck
import transparencyCheck

getWebsiteText.get_website_text(input("Enter URL: "))
cleanWebsiteText.clean_website_text()
formalityCheck.formality_check()
neutralityCheck.neutrality_check()
transparencyCheck.transparency_check()
createGalenTest.createGalenTest()
#run galen test
#layoutCheck.py
