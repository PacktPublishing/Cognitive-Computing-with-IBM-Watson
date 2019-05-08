from watson_developer_cloud.visual_recognition_v3 import VisualRecognitionV3

visual_recognition = VisualRecognitionV3(api_key="unBcJ-zq5gaguq7g6rQnpu9K-1ue8yKvoclgqMf7wMLx", version="2018-03-19")

with open('./example_goldenretriever.jpg', 'rb') as images_file:
    classes = visual_recognition.classify(images_file, classifier_ids=["DogBreedClassifier_452959111"]).get_result()
    print json.dumps(classes, indent=2)
