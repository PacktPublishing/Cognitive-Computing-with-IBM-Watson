response = natural_language_understanding.analyze(
        text="SpaceX sent the Crew Dragon to various waypoints outside of the station early Sunday morning, to test the vehicle's docking capability. Using its onboard thrusters, the capsule periodically approached the ISS and then held its position over the course of two and a half hours. The capsule even backed away at one point to test the spacecraft's capability of retreating in case of an emergency.",
        features=Features(
                categories=CategoriesOptions(limit=4),
                concepts=ConceptsOptions(limit=10))
    ).get_result()
