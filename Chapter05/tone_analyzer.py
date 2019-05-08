from watson_developer_cloud import ToneAnalyzerV3

service = ToneAnalyzerV3(iam_apikey="NaPe5R7RNR-e38IRR1jT5k_ictmN1SalGmt64aTC5-f8", version="2017-09-21")

text = "The Tone Analyzer service is very interesting, I hope it works."
service_response = service.tone({'text': text}, 'application/json').get_result()

for tone in service_response['document_tone']['tones']:
    print("Tone:\t'" + tone['tone_name'] + "'")
    print("Score:\t" + str(tone['score']), end="\n\n")

utterances = [
  {
    "text": "Hi. My computer won't turn on. This is really annoying because I just got it 2 weeks ago, and I'm travelling at the moment.", 
    "user": "customer"
  }, 
  {
    "text": "Hello. I'm sorry to hear you're having this issue. Could I have your computer's serial number?", 
    "user": "agent"
  }, 
  {
    "text": "Alright, it's [serial].", 
    "user": "customer"
  }, 
  {
    "text": "Thank you. Could you try running an SMC Reset? Hold down \"option\", \"control\", and \"command\" with the power button until your computer reboots. Ensure it's plugged into power.", 
    "user": "agent"
  }, 
  {
    "text": "Alright, but you should really make this information more accessible!", 
    "user": "customer"
  }, 
  {
    "text": "It's working now, thank you!", 
    "user": "customer"
  }
]

service.tone_chat(utterances).get_result()

for utterance in result['utterances_tone']:
    print("Utterance: " + utterance['utterance_text'])
    if len(utterance['tones']) == 0:
            print("No tones detected.")
    for tone in utterance['tones']:
            print("Tone: " + tone['tone_name'])
            print("Score: " + str(tone['score']))
    print("\n")
