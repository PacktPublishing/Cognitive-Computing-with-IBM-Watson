voice_model = text_to_speech.create_voice_model(
        'First Model',
        'en-US',
        'First custom voice model'
    ).get_result()

customization_id = voice_model.get("customization_id")
