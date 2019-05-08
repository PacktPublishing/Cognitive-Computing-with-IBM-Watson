import json
from ibm_watson import AssistantV1

def BankBot():

    # Create session with the Watson Assistant
    assistant = AssistantV1(
            iam_apikey='PrLJLVykZG4V-FQrADLiZG91oOKcJN0UZWEUAo0HxW8Q',
            version='2018-09-20')

    # Pull the first prompt from the Dialog
    response = assistant.message(
            workspace_id='3e86c7a1-b071-4e6a-ada2-a8ac616e6aa6').get_result()

    # Continue prompting the user and getting their input, until they indicate
    # it's time to quit
    while True:

        # Get the text of the prompt
        prompt = response.get("output").get("text")
  
        # Display all of the text provided in the prompt
        for text in prompt:
            print(text)
 
        # Get the user's next utterance
        utterance = input("==> ")

        # Invoke Watson to assess the intent of the utterance and determine how
        # to respond to the user
        response = assistant.message(
                workspace_id='3e86c7a1-b071-4e6a-ada2-a8ac616e6aa6',
                input={'text': utterance},
                context=response.get("context")).get_result()

        # Ensure there are intents in the response.
        if len(response.get("intents")) > 0:
            
            #Check whether the dialog indicates an end to the conversation
            if response["intents"][0]["intent"] == "General_Ending":
                if len(response.get("output").get("text")) > 0:
                    # If there are any remaining messages in the response then
                    # print them out.
                    print(response.get("output").get("text")[0] + '\n')
                    # And terminate the conversation.
                    break

            # If there are other intents that need processing, that logic can
            # go here


BankBot()
