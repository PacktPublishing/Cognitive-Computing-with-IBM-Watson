import json
from threading import Thread

import ibm_watson
from ibm_watson.websocket import RecognizeCallback, AudioSource

from StreamSpeechService import *
from TextSpeechService import *
from NLUService import *
from LanguageTranslatorService import *
from PersonalityInsightsService import *
from TwitterService import *

def BankBot(research_URL=None):
    
    def speakAndPrint(text):
        print("Watson: {}".format(text))
        textSpeech(text=text, voice=voice, session=speechSession)
    
    # Create session with the Watson Assistant
    assistant = ibm_watson.AssistantV1(
            iam_apikey='PrLJLVykZG4V-FQrADLiZG91oOKcJN0UZWEUAo0HxW8Q',
            version='2018-09-20')
    workspace_id = "beb32203-c974-46dd-997f-f91f0968acf5"
    
    # Get a session to NLU
    nluSession = initNLU()
    
    # Prep speech output
    speechSession = initTextSpeech()
    voice = 'en-US_AllisonVoice'

    # Prep voice input
    confidence_threshold = 50   # Watson must be greater than this confidence to accept the voice input
    # Create a control object
    SPEECH_CONTROL = StreamSpeechControl()
    
    # Prepare a thread to recognize the input from the microphone input
    recognize_thread = Thread(target=recognizeUsingWebsocket, args=(SPEECH_CONTROL,))
    recognize_thread.start()
    
    # Prep working session
    document_of_interest = ""
    entity_of_interest = ""
    
    # Pull the first prompt from the Dialog
    response = assistant.message(workspace_id).get_result()

    # Get the text of the prompt
    prompt = response.get("output").get("text")
    context = response.get("context")
        
    # Display and Say all of the text provided in the prompt
    for text in prompt:
        speakAndPrint(text)
    
    # Continue prompting the user and getting their input, until they indicate
    # it's time to quit
    while True:

        # Get the user's next utterance
        # First test for voice input
        
        # Get instances of the needed microphone stream
        microphoneStream = SPEECH_CONTROL.initAudio()

        # Wait for the speech service to transcribe input from the user
        while not SPEECH_CONTROL.MYCALLBACK.isTextTranscribed():
            pass

        # Process the transcribed input
        transcript = SPEECH_CONTROL.MYCALLBACK.getTranscription(True)

        # Turn off the microphone while the transcribed text is being processed
        SPEECH_CONTROL.terminateAudio(microphoneStream)
    
        # Figure out the confidence of the resulting text
        confidence = int(round(100*transcript[0].get("confidence")))
        utterance = transcript[0].get("transcript")
        print("You: " + utterance)

        if confidence < confidence_threshold:
            print("Watson had poor confidence in what you said.")
            utterance = "Garbage"

        # Invoke Watson to assess the intent of the utterance and determine how
        # to respond to the user
        response = assistant.message(
                workspace_id,
                input={'text': utterance},
                context=context).get_result()

        # Get the text and context of the response
        response_text = response.get("output").get("text")
        context = response.get("context")


        # Display and Say all of the text provided in the response
        for text_line in response_text:
            speakAndPrint(text_line)

        
        # Ensure there are intents in the response.
        if len(response.get("intents")) > 0:
            
            # Check whether the dialog indicates an end to the conversation
            if response["intents"][0]["intent"] == "Done":
                # Terminate the conversation.
                break

            # Otherwise, process the other intents that may have been expressed

            # Process the #Document-Of-Interest intent
            elif (response["intents"][0]["intent"] == "Document-Of-Interest") and (context.get("research_document")):
                document_of_interest = response.get("context").get("research_document")
            
            # Process the #Document-Of-Interest intent and prompt for the document URL if needed
            elif (response["intents"][0]["intent"] == "Document-Of-Interest"):
                try:
                    research_URL = raw_input("What URL do you want to research? ==> ")
                except NameError:
                    research_URL = input("What URL do you want to research? ==> ")
                utterance = "Let's do research on the document at: " + research_URL
                response = assistant.message(
                        workspace_id,
                        input={'text': utterance},
                        context=context).get_result()
                # Get the text and context of the response
                response_text = response.get("output").get("text")
                context = response.get("context")
                # Display and Say all of the text provided in the response
                for text_line in response_text:
                    speakAndPrint(text_line)

            # Summarize the document
            elif (response["intents"][0]["intent"] == "Summarize-Document") and (context.get("research_document")):
                # Enumrate the article content
                article_text = getText(research_URL, session=nluSession)
                print(article_text)
                # Enumerate the enties found in the document
                entities = preprocessEntities(getEntities(research_URL, limit=5, session=nluSession))
                if len(entities) > 0:
                    speakAndPrint("The following entities were found:")
                    text_line = ''
                    for i in range(len(entities)-1):
                        text_line = text_line + entities[i].get("text") + ", "
                    if len(entities) > 1:
                        text_line = text_line + "and "
                        text_line = text_line + entities[len(entities)-1].get("text")
                    speakAndPrint(text_line)
                else:
                    speakAndPrint("No entites were mentioned in the document")
                # Enumerate the document categories
                categories = getCategories(research_URL, session=nluSession)
                speakAndPrint("The article spoke about these concepts:")
                for concept in categories:
                    speakAndPrint(concept.get("label"))
            
            # Process the #Entity-Of-Interest intent
            elif (response["intents"][0]["intent"] == "Entity-Of-Interest") and (context.get("research_entity")):
                entity_of_interest = disambiguateEntity(response.get("context").get("research_entity"), entities)

            # Process the #Entity-Personality intent
            elif response["intents"][0]["intent"] == "Entity-Personality":
                entity_twitter = entity2twitter(entity_of_interest)
                if entity_twitter == None:
                    speakAndPrint("Sorry, I couldn't find a twitter handle for " + entity_twitter["text"])
                else:
                    speakAndPrint("Here's a twitter-based personality analysis for " + entity_twitter["text"])
                    print(prettyPrintProfile(getProfile(tweets(entity_twitter))))

           # Process the #Entity-Tone intent
            elif response["intents"][0]["intent"] == "Entity-Tone":
                speakAndPrint("The sentiment of " + entity_of_interest["text"] + " is " + entity_of_interest["sentiment"]["label"] + " with an intensity of " + str(entity_of_interest["sentiment"]["score"]))

            # Process the #Classify-Text intent
            elif response["intents"][0]["intent"] == "Classify-Text":
                categories = getCategories(research_URL, session=nluSession)
                speakAndPrint("The document generally falls into the following categories:")
                for (category_index, category) in enumerate(categories):
                    speakAndPrint("Category " + str(category_index) + " : " + category["label"])

            # Process the #Translate-Research intent
            elif (response["intents"][0]["intent"] == "Translate-Research") and (context.get("translation_language")):
                article_text = getText(research_URL, session=nluSession)
                translated_article = translate(article_text, response.get("context").get("translation_language"))
                speakAndPrint("I've translated your document to " + context.get("translation_language"))
                print(translated_article)

                    
        if SPEECH_CONTROL.SESSION_ENDED == True:
            # The speech session ended prematurely
            break
                
                
    # Shut down the input to the SpeechSocket
    SPEECH_CONTROL.AUDIO.terminate()
    SPEECH_CONTROL.AUDIO_SOURCE.completed_recording()


BankBot()
