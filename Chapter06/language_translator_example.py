from watson_developer_cloud import LanguageTranslatorV3

language_translator = LanguageTranslatorV3(version="2018-05-01", iam_apikey="rvE894AVGJQ_t_ZNuUoQrclWWQwvpFB0_78jr9pvtjIl")

print "Enter a sentence in English:"
eng_sent = raw_input()
translation = language_translator.translate(text=eng_sent, model_id="en-fr").get_result()["translations"][0]["translation"]
print "Your sentence in French is:\n" + translation
