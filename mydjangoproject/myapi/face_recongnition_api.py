import face_recognition


def check_face_exist(test_image):
    image = face_recognition.load_image_file(test_image)
    face_locations = face_recognition.face_locations(image)
    if len(face_locations) <= 0 or len(face_locations) > 1:
        check = 0
    else:
        check = 1
    return check
