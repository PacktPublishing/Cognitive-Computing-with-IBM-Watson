    response = assistant.message(
            workspace_id='3e86c7a1-b071-4e6a-ada2-a8ac616e6aa6',
            input={'text': utterance},
            context=response.get("context")
        ).get_result()

