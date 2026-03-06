import cv2                                  #for accessing camera
import math                                 #for distance calulation
import mediapipe as mp                      #mediapipe google ai pipeline/model for image recognition
from mediapipe.tasks import python          #for BaseOptions 
from mediapipe.tasks.python import vision   #mediapipe tasks has three model vision,audio and nlp vision is used for facial recognition

def run_face_analysis():  #fxn to run in app.py

    base_options = python.BaseOptions(model_asset_path = "ai/face_landmarker.task")     #the model asset file face_landmarker.task need to download it differntly and placed in same folder it contain the tensorflow lite model created by google also store graph configuration, the BaseOptions fxn create a object base_options which store the information about model

    options = vision.FaceLandmarkerOptions(
            base_options = base_options,      #tell mediapipe which model file to use
            running_mode = vision.RunningMode.IMAGE,      #tell running mode, 3 possible mode are there IMAGE,VIDEO,LIVESTREAM
            output_face_blendshapes = False,     #model will not return facial expression
            output_facial_transformation_matrixes = False,   #no 3d matrix will be given
            num_faces = 1    #track only one face
            )
    #here we created a option object which has configuration going to be set for model how model should run,what outputs return

    detector = vision.FaceLandmarker.create_from_options(options) #here the model is loaded into ram

    def calculate_dist(a,b):        #fxn to calculate distance b/w point
        return math.hypot(a.x - b.x, a.y - b.y)

    def analyze_frame(results):     #fxn to calculate vatta,pitta,kappha

        if not results.face_landmarks:      #if no landmarks
            print("No face detected")
            return None

        landmarks = results.face_landmarks[0]   #get one face from all faces

        top = landmarks[10]             #mannualy decided the position of face marks
        chin = landmarks[152]           #each face has 468 landmarks means landmarks has 468 indexes
        l_cheek = landmarks[234]        #each index represent a specific location   
        r_cheek = landmarks[454]        #each has x,y,z relative postion to top corner(0,0)
        face_height = calculate_dist(top, chin)
        face_width  = calculate_dist(l_cheek, r_cheek) #simple calucalated the face height and width

        hw_ratio = face_height/face_width if face_width != 0 else 0 #ratio of face h/w

        res = {"Vata":0,"Pitta":0,"Kapha":0}  #dictonary containg prakriti information

        if hw_ratio > 1.5:      # simple calculation for prakriti information
            res["Vata"] = 70
            res["Pitta"] = 20
            res["Kapha"] = 10
        elif hw_ratio < 1.2:
            res["Kapha"] = 70
            res["Pitta"] = 20
            res["Vata"] = 10
        else:
            res["Pitta"] = 70
            res["Vata"] = 15
            res["Kapha"] = 15

        return res
    
    cap = cv2.VideoCapture(0)  #turn on the camera 0 for default
    
    text = None #empty object used later
    
    while True:
        
        ret,frame = cap.read()
        if not ret:
            break

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format = mp.ImageFormat.SRGB, data = rgb_frame)

        result = detector.detect(mp_image)

        if result.face_landmarks:

            text = analyze_frame(result)

            for face in result.face_landmarks:
                h, w, _ = frame.shape

                for lm in face:
                     x = int(lm.x * w)
                     y = int(lm.y * h)
                     cv2.circle(frame, (x,y), 1, (0,255,0), -1)

        if text:
            y_pos = 40
            for key,value in text.items():
                cv2.putText(
                        frame,
                        f"{key}: {value}%",
                        (30,y_pos),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.8,
                        (0,255,0),
                        2
                        )
                y_pos += 30

        cv2.imshow("MASHAR", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
