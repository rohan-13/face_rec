import face_recognition
import cv2
import os

class Simple():

    def __init__(self, folder_path):
        self.folder_path = folder_path
        self.encodings = []
        self.known_faces_dict = {}
    
    def encode_image(self):
        for filename in os.listdir(self.folder_path):
            person_folder = os.path.join(self.folder_path, filename)
            if os.path.isdir(person_folder):
                self.known_faces_dict[filename] = []
                for filename in os.listdir(person_folder):


                    if filename.endswith(('.jpeg', '.jpg', 'webp', '.png', '.JPG', '.PNG')):
                        img_path = os.path.join(person_folder, filename)
                        img = cv2.imread(img_path)
                        rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                        encodings = face_recognition.face_encodings(rgb_img)
                        if encodings:
                            self.encodings.append(encodings[0])
                            name = os.path.splitext(person_folder)[0]
                            self.known_faces_dict[name] = encodings[0]
                        else:
                            print(f"No faces found in {filename}")
        print(len(self.encodings), "images have been encoded.")

    def compare_faces(self, encoding):
        results = face_recognition.compare_faces(self.encodings, encoding)
        return results

    def detect_known_faces(self, frame):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame)
        encodings = face_recognition.face_encodings(rgb_frame, face_locations)
        face_names = []
        
        for encoding in encodings:
            #name = self.compare_faces(encoding)
            #face_names.append(name)
            
            results = self.compare_faces(encoding)
            name = 'Unkown'
            for known_name, match in zip(self.known_faces_dict.keys(), results):
                if match:
                    name = known_name
                    break
            face_names.append(name)
            
        return face_locations, face_names



folder_path = "/Users/rohanpatel/Documents/Docs/VS/Python/face_rec/im2/"

simple = Simple(folder_path)
simple.encode_image()

'''

#image = face_recognition.load_image_file("download.jpeg")
#face_locations = face_recognition.face_locations(image)

#read in image -> covert to RBG -> enocde
    img = cv2.imread("/Users/rohanpatel/Documents/Docs/VS/Python/face_rec/im/EM.jpeg")

#convert img to RGB
    rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

#encode image
    img_encode = face_recognition.face_encodings(rgb_img)[0]

    img2 = cv2.imread("/Users/rohanpatel/Documents/Docs/VS/Python/face_rec/im/em2.jpeg")
    rgb_img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)
    img_encode2 = face_recognition.face_encodings(rgb_img2)[0]

    img3 = cv2.imread("/Users/rohanpatel/Documents/Docs/VS/Python/face_rec/im/DT.jpeg")
    rgb_img3 = cv2.cvtColor(img3, cv2.COLOR_BGR2RGB)
    img_encode3 = face_recognition.face_encodings(rgb_img3)[0]

    result = face_recognition.compare_faces([img_encode], img_encode2)
    #print("RESULT: ", result)

    #cv2.imshow("Img", rgb_img)
    #cv2.waitKey(0)

    '''
