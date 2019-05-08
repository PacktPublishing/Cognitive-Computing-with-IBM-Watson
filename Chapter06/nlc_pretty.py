import json
from ibm_watson import NaturalLanguageClassifierV1

service = NaturalLanguageClassifierV1(url='https://gateway.watsonplatform.net/natural-language-classifier/api', iam_apikey='JieYHJwBRgrd5Rl9R4q63d5DWvAuffdrRIj1jKhkfoAH')

user_tweet = input("Give me a tweet: ")
classes = service.classify('8a423bx518-nlc-1830', user_tweet).get_result()

for sentiment in classes["classes"]:
    print(sentiment["class_name"] + " sentiment: " + str(round(sentiment["confidence"] * 100)) + "% confidence")
