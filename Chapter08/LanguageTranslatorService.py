from ibm_watson import LanguageTranslatorV3

languages = {
    "English": "en",
    "French": "fr",
    "Spanish": "es",
    "German": "de"
}

API_key = 'ujft9Uu2E6jFCcaYAiUxIKfs4w6DnFnX3C_hac2IDr_N'

def initLT():
    return LanguageTranslatorV3(
        version = '2018-05-01',
        iam_apikey = API_key)

def translate(text, target, source=None, service=initLT()):
    if target not in languages.values():
        target = languages[target]
    if source is None:
        source = service.identify(text).get_result()["languages"][0]["language"].split("-")[0]
    else:
        if source not in languages.values():
            source = languages[source]
    return service.translate(text=text, model_id=source + "-" + target).get_result()["translations"][0]["translation"]
