import json
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 \
    import Features, CategoriesOptions, ConceptsOptions, EntitiesOptions

natural_language_understanding = NaturalLanguageUnderstandingV1(
        version = '2018-11-16',
        iam_apikey = '32AZltOLLv83-m0n-UqU28YFUTeOpPKOGj2Q7DeNtvej',
        url = 'https://gateway.watsonplatform.net/natural-language-understanding/api')

response = natural_language_understanding.analyze(
        url = "https://en.wikipedia.org/wiki/SpaceX",
        features=Features(
            entities=EntitiesOptions(limit=100, mentions=True, sentiment=True, emotion=True)
       )
    ).get_result()

print
print("=======================================================================")
print
print(json.dumps(response, indent=2))
