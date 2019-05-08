response = natural_language_understanding.analyze(
        html="Space/SpaceX and NASA Launch Is First Step to Renewed Human Spaceflight - The New York Times.html",
        features=Features(
                categories=CategoriesOptions(limit=4),
                concepts=ConceptsOptions(limit=10)),
        clean=False
    ).get_result()
