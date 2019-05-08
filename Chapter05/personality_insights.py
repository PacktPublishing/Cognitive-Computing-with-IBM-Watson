from watson_developer_cloud import PersonalityInsightsV3

personality_insights = PersonalityInsightsV3(version='2017-10-13', iam_apikey='W73kz6O3XR1pkIQVn2RYbrrtIU2o0IvNYuqiMICwSwro')

profile_text = open("personality.txt").read()

profile = personality_insights.profile(profile_text, "text/plain").get_result()

needs = profile["needs"]
values = profile["values"]
personality = profile["personality"]

def print_traits(traits_category_name, traits):
    print(traits_category_name + ":")
    for trait in traits:
        print(trait["name"] + ": {:.3f}%".format(trait["percentile"] * 100))
    print("\n")

print_traits("Needs", needs)
print_traits("Values", values)
print_traits("Personality", personality)
