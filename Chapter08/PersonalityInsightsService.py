from ibm_watson import PersonalityInsightsV3

def initPI():
    return PersonalityInsightsV3(
        version='2017-10-13',
        iam_apikey='W9i5QuJlAuEtngktBVbzOzVur5q-8Pxuti1ljSjpbZAc')

def getProfile(text, session=initPI()):
    return session.profile(text, 'application/json').get_result()

def prettyPrintProfile(profile):
    pretty_string = ""
    def processTraits(traits):
        pstring = ""
        for trait in traits:
            pstring += trait["name"] + ": " + str(round(trait["percentile"] * 100)) + "%" + "\n"
        return pstring
    pretty_string += "\n" + "Personality:" + "\n"
    pretty_string += processTraits(profile["personality"])
    pretty_string += "\n" + "Needs:" + "\n"
    pretty_string += processTraits(profile["needs"])
    pretty_string += "\n" + "Values:" + "\n"
    pretty_string += processTraits(profile["values"])
    return pretty_string