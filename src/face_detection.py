import cv2
import face_recognition
import os
import numpy as np
import pandas as pd

class InfluencerDetector:
    def __init__(self, video_dir='data/raw/videos'):
        self.video_dir = video_dir
        self.known_faces = {}

    def extract_faces(self, video_path, max_frames=10):
        video = cv2.VideoCapture(video_path)
        frame_count = 0
        unique_faces = []

        while frame_count < max_frames:
            ret, frame = video.read()
            if not ret:
                break

            face_locations = face_recognition.face_locations(frame)
            face_encodings = face_recognition.face_encodings(frame, face_locations)

            for encoding in face_encodings:
                is_new_face = True
                for known_face in unique_faces:
                    if face_recognition.compare_faces([known_face], encoding)[0]:
                        is_new_face = False
                        break
                
                if is_new_face:
                    unique_faces.append(encoding)

            frame_count += 1

        video.release()
        return unique_faces

    def process_videos(self):
        influencers = []
        
        for video_file in os.listdir(self.video_dir):
            video_path = os.path.join(self.video_dir, video_file)
            faces = self.extract_faces(video_path)
            
            for face_encoding in faces:
                influencers.append({
                    'video': video_file,
                    'face_encoding': face_encoding
                })
        
        return pd.DataFrame(influencers)