import cv2
import os

# Path to Haar Cascade Face Detector included with OpenCV
CASCADE_PATH = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'

# Directory to save all face datasets
DATASET_ROOT = r'D:\SVAC SKILL\smart_attendance\dataset'
SAMPLES_PER_STUDENT = 50 

def create_output_dir(student_id, student_name):
    dir_name = f"{student_id}_{student_name.replace(' ', '_')}"
    save_path = os.path.join(DATASET_ROOT, dir_name)
    os.makedirs(save_path, exist_ok=True)
    return save_path

def main():
    # Input: Student Details
    student_id = input("Enter student ID: ").strip()
    student_name = input("Enter student Name: ").strip()
    save_folder = create_output_dir(student_id, student_name)
    
    face_cascade = cv2.CascadeClassifier(CASCADE_PATH)
    cap = cv2.VideoCapture(0)
    
    sample_count = 0
    print("Starting image capture. Look towards the webcam...")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to open camera.")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

        for (x, y, w, h) in faces:
            face_img = frame[y:y + h, x:x + w]
            file_path = os.path.join(
                save_folder, f"{student_id}_{student_name.replace(' ', '_')}_{sample_count+1}.jpg"
            )
            cv2.imwrite(file_path, face_img)
            sample_count += 1

            # Draw a rectangle around the face
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        cv2.imshow('Capturing Faces - Press Q to Quit', frame)

        if sample_count >= SAMPLES_PER_STUDENT:
            print(f"Collected {sample_count} face images for {student_name}.")
            break

        # Exit if Q is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Capture interrupted by user.")
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
