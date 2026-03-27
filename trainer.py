import os
import numpy as np
import cv2
from PIL import Image

CASCADE_PATH = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
DATASET_ROOT = 'D:\\SVAC SKILL\\smart_attendance\\dataset'  # Should match the dataset folder used previously

def get_images_and_labels(dataset_root):
    face_cascade = cv2.CascadeClassifier(CASCADE_PATH)
    faces = []
    labels = []
    label_map = {}
    label_counter = 0

    for person_dir in os.listdir(dataset_root):
        folder_path = os.path.join(dataset_root, person_dir)
        if not os.path.isdir(folder_path):
            continue
        # Assign integer label
        label_map[person_dir] = label_counter
        label = label_counter
        label_counter += 1

        for image_filename in os.listdir(folder_path):
            image_path = os.path.join(folder_path, image_filename)
            img = Image.open(image_path).convert('L')
            img_np = np.array(img, 'uint8')
            # Detect face in image
            face_rects = face_cascade.detectMultiScale(img_np, scaleFactor=1.1, minNeighbors=5)
            for (x, y, w, h) in face_rects:
                faces.append(img_np[y:y+h, x:x+w])
                labels.append(label)

    return faces, labels

def main():
    faces, labels = get_images_and_labels(DATASET_ROOT)
    print(f"Total faces: {len(faces)}, Total unique labels: {len(set(labels))}")

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.train(faces, np.array(labels))
    recognizer.save("D:/SVAC SKILL/smart_attendance/dataset/trainer.yml")
    print("Model trained and saved as trainer.yml.")

if __name__ == "__main__":
    main()
