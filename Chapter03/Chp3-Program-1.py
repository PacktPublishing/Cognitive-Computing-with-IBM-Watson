def crop_face(original_image, face_name, watson_face_location):
    left = watson_face_location['left']
    top = watson_face_location['top']
    right = left + watson_face_location['width']
    bottom = top + watson_face_location['height']
    original_image.crop((left, top, right, bottom)).save(face_name)
