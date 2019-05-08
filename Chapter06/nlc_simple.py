import json
from ibm_watson import NaturalLanguageClassifierV1

service = NaturalLanguageClassifierV1(url='https://gateway.watsonplatform.net/natural-language-classifier/api', iam_apikey='JieYHJwBRgrd5Rl9R4q63d5DWvAuffdrRIj1jKhkfoAH')

classes = service.classify('8a423bx518-nlc-1830', 'Air Canada lost my luggage twice in the same month, delayed my flight, and didn\'t care about my stopover!').get_result()
print(json.dumps(classes, indent=2))
