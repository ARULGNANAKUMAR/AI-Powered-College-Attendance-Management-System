import cv2
import pandas as pd
from datetime import datetime
import os

CASCADE_PATH = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
MODEL_PATH = r"D:\SVAC SKILL\smart_attendance\dataset\trainer.yml"
DATASET_ROOT = r"D:\SVAC SKILL\smart_attendance\dataset"
MASTER_FILE = r"D:\SVAC SKILL\smart_attendance\master_attendance.xlsx"

# Load master data - NO automatic datetime conversion
df = pd.read_excel(MASTER_FILE, dtype=str, date_parser=None)
if 'Roll number' not in df.columns or 'Name' not in df.columns:
    raise Exception("Master file must have columns 'Roll number' and 'Name'.")

# Get today's column name
today_col = datetime.now().strftime('%d-%m-%Y')
if today_col not in df.columns:
    df[today_col] = ''

# Build label mapping from dataset folders
label_map = {}
for i, folder in enumerate(sorted(os.listdir(DATASET_ROOT))):
    if os.path.isdir(os.path.join(DATASET_ROOT, folder)):
        parts = folder.split('_')
        roll = parts[0]
        name = '_'.join(parts[1:])
        label_map[i] = (roll, name)

# Load face recognizer and cascade
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read(MODEL_PATH)
face_cascade = cv2.CascadeClassifier(CASCADE_PATH)

# Track present students
present_rolls = set()
cap = cv2.VideoCapture(0)
print("Starting attendance marking. Press Q to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Camera error")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5)

    for (x, y, w, h) in faces:
        face_img = gray[y:y+h, x:x+w]
        label, confidence = recognizer.predict(face_img)
        if confidence < 90 and label in label_map:
            roll, name = label_map[label]
            present_rolls.add(str(roll))
            disp_text = f"{name} ({roll})"
            color = (0, 255, 0)
        else:
            disp_text = "Unknown"
            color = (0, 0, 255)
        cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
        cv2.putText(frame, disp_text, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

    cv2.imshow('Attendance System', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

# Mark attendance for today only - don't touch other columns
for i, row in df.iterrows():
    roll = str(row['Roll number']).strip()
    df.loc[i, today_col] = 'Present' if roll in present_rolls else 'Absent'

# Save the complete DataFrame - NO filtering or column removal
df.to_excel(MASTER_FILE, index=False)

print(f"Attendance marked for {today_col}. ALL previous columns preserved.")
print(f"Total columns in file: {len(df.columns)}")
print(f"Columns: {list(df.columns)}")
