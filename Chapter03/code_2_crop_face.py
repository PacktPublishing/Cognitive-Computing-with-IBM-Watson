import json
from watson_developer_cloud import VisualRecognitionV3
from PIL import Image

def crop_face(original_image, face_name, watson_face_location):
    left = watson_face_location['left']
    top = watson_face_location['top']
    right = left + watson_face_location['width']
    bottom = top + watson_face_location['height']
    original_image.crop((left, top, right, bottom)).save(face_name)

visual_recognition = VisualRecognitionV3(
    '2018-03-19',
    iam_apikey='unBcJ-zq5gaguq7g6rQnpu9K-1ue8yKvoclgqMf7wMLx')

with open('./rob_and_tanmay.jpg', 'rb') as images_file:
    faces = visual_recognition.detect_faces(images_file).get_result()
    for (faceID, face) in enumerate(faces['images'][0]['faces']):
        filename = str(faceID) + "_" + str(face['age']['min']) + '_' + str(face['age']['max']) + '_' + face['gender']['gender'] + ".png"
        crop_face(Image.open('./rob_and_tanmay.jpg'), filename, face['face_location'])
