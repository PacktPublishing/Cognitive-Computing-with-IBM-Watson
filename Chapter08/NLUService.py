import urllib
import json
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 import *

API_key = '32AZltOLLv83-m0n-UqU28YFUTeOpPKOGj2Q7DeNtvej'
Model_key = None

def initNLU():
    return NaturalLanguageUnderstandingV1(
        version = '2018-11-16',
        iam_apikey = API_key,
        url = 'https://gateway.watsonplatform.net/natural-language-understanding/api')

def getEntities(url, session=initNLU(), limit=20, mentions=True, sentiment=True, emotion=True, model=Model_key):
    return session.analyze(
            url=url,
            features=Features(
                entities=EntitiesOptions(limit=limit, mentions=mentions, sentiment=sentiment, emotion=emotion, model=model))
            ).get_result()["entities"]

def preprocessEntities(entities):
    e = []
    for entity in entities:
        new_entity = {}
        new_entity["text"] = entity["text"]
        new_entity["synonyms"] = list(set([x["text"] for x in entity["mentions"]]))
        new_entity["sentiment"] = {"score": int(round(entity["sentiment"]["score"] * 100)), "label": entity["sentiment"]["label"]}
        if "disambiguation" in entity.keys():
            if "dbpedia_resource" in entity["disambiguation"].keys():
                new_entity["dbpedia"] = entity["disambiguation"]["dbpedia_resource"]
        e.append(new_entity)
    return e

def dbpedia2wikidata(url):
    json_url = url.replace("//dbpedia.org/resource", "//dbpedia.org/data") + ".json"
    dbpedia_response = json.loads(urllib.request.urlopen(json_url).read())[url]
    same_as = dbpedia_response["http://www.w3.org/2002/07/owl#sameAs"]
    wikidata_url = [x for x in same_as if "http://www.wikidata.org/entity" in x["value"]]
    if len(wikidata_url) == 0:
        return None
    return wikidata_url[0]["value"]

def wikidata2twitter(url):
    json_url = url + ".json"
    wikidata_response = json.loads(urllib.request.urlopen(json_url).read())["entities"]
    wikidata_response = wikidata_response[list(wikidata_response.keys())[0]]
    claims = wikidata_response["claims"]
    if "P2002" not in claims.keys():
        return None
    return claims["P2002"][0]["mainsnak"]["datavalue"]["value"]

def entity2twitter(entity):
    if "dbpedia" not in entity.keys():
        return None
    dbpedia_url = entity["dbpedia"]
    wikidata_url = dbpedia2wikidata(dbpedia_url)
    if wikidata_url == None:
        return None
    twitter_handle = wikidata2twitter(wikidata_url)
    if twitter_handle == None:
        return None
    return twitter_handle

def entityWithName(name, entities):
    return [x for x in entities if x["text"] == name][0]

def disambiguateEntity(entity, entities):
    relevant = [x["text"] for x in entities if (entity in x["synonyms"]) or (entity == x["text"])]
    if len(relevant) == 0:
        return None
    if len(relevant) == 1:
        return entityWithName(relevant[0], entities)
    for (eI, e) in enumerate(relevant):
        print(str(eI + 1) + ". " + e)
    try:
        entity_index = int(raw_input("Which entity are you referring to? ")) - 1
    except NameError:
        entity_index = int(input("Which entity are you referring to? ")) - 1
    return entityWithName(relevant[entity_index], entities)

def getCategories(url, session=initNLU()):
    return session.analyze(
            url=url,
            features=Features(categories=CategoriesOptions())).get_result()["categories"]

def getText(url, session=initNLU()):
    return session.analyze(
            url=url,
            features=Features(metadata=MetadataOptions()),
            return_analyzed_text=True).get_result()["analyzed_text"]
