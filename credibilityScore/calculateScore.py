import formalityCheck
import neutralityCheck
import transparencyCheck
import layoutCheck

def calculateScore():

    print(formalityCheck.formality_check())
    print(neutralityCheck.neutrality_check())
    print(transparencyCheck.transparency_check())
    print(layoutCheck.layoutCheck())

calculateScore()