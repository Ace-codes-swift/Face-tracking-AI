import cv2

def select_camera():
    for i in range(1, 10):  # Adjust max_tested if necessary
        cap = cv2.VideoCapture(i, cv2.CAP_DSHOW)
        if cap.isOpened():
            print(f"External camera found at index {i}")
            cap.release()
            return i
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    if cap.isOpened():
        print("Using built-in camera (index 0)")
        cap.release()
        return 0
    print("Error: No cameras found.")
    return -1

def main():
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    camera_index = select_camera()
    if camera_index == -1:
        return
    cap = cv2.VideoCapture(camera_index, cv2.CAP_DSHOW)
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return
    cv2.namedWindow("Camera Feed", cv2.WINDOW_NORMAL)
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture frame.")
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 2)
            cv2.putText(frame, 'Face', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 255), 2)
        cv2.imshow("Camera Feed", frame)
        key = cv2.waitKey(1) & 0xFF
        if key in [27, ord(' ')]:  # ESC or space to quit
            break
        if cv2.getWindowProperty("Camera Feed", cv2.WND_PROP_AUTOSIZE) < 0:
            break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
