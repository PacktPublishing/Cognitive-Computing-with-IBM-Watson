response = natural_language_understanding.analyze(
        url=resource_link,
        features=Features(
                categories=CategoriesOptions(limit=10),
                concepts=ConceptsOptions(limit=50),
                emotion=EmotionOptions(document=True),
                entities=EntitiesOptions(limit=100, mentions=True, sentiment=True, \
                        emotion=True, model=Model_key),
                keywords=KeywordsOptions(limit=100, sentiment=True, emotion=True),
                metadata=MetadataOptions(),
                relations=RelationsOptions(),
                semantic_roles=SemanticRolesOptions(limit=50, keywords=True, \
                        entities=True),
                sentiment=SentimentOptions(['Rockets', 'Space', 'Mars'])),
        return_analyzed_text=True
    ).get_result()
