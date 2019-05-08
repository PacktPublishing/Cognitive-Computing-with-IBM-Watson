import json
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 import *

# Create a connection to the NLU service
natural_language_understanding = NaturalLanguageUnderstandingV1(
        version='2018-11-16',
        iam_apikey='w02JlNpjSbT6OBJSjT1dd3Fe4ebXETJz4yp0etEEFmrU',
        url='https://gateway.watsonplatform.net/natural-language-understanding/api'
    )

# Invoke NLU to analyze the text at the specified URL
response = natural_language_understanding.analyze(
        url="https://en.wikipedia.org/wiki/SpaceX",     # URL of the page to analyze
        features=Features(                              # Indicate what features to look for
                categories=CategoriesOptions(limit=4),      # Look for up to 4 categories
                concepts=ConceptsOptions(limit=10)          # Look for up to 10 concepts
            )
    ).get_result()                                      # Get the results of the analysis

print
print("=======================================================================")
print
print(json.dumps(response, indent=2))
