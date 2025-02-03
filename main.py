import face_recognition
import cv2
import time
from simple import Simple


#Encode all faces from folder
path = "/Users/rohanpatel/Documents/Docs/VS/Python/face_rec/im2/"
sf = Simple(path)
sf.encode_image()



cap = cv2.VideoCapture(1, cv2.CAP_AVFOUNDATION)



if not cap.isOpened():
    print("Error: Could not open video device.")
    exit()

# Set the desired frame rate and resolution
desired_fps = 30  # You can adjust this value
cap.set(cv2.CAP_PROP_FPS, desired_fps)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  # Adjust the width
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)  # Adjust the height

ret, frame = cap.read()
if not ret:
    print("Error: Camera opened but cannot deliver frames.")
    cap.release()
    exit()
else:
    print("Camera is delivering frames successfully.")

frame_count = 0
process_every_n_frames = 3  # Process every 3rd frame
fps_start_time = time.time()
fps_frame_count = 0

while True:
    start_time = time.time()

    # Capture frame-by-frame
    ret, frame = cap.read()

    # Mirror the frame
    frame = cv2.flip(frame, 1)
    
    # Detect the face location
    face_locations, face_names = sf.detect_known_faces(frame)
    for face_loc, name in zip(face_locations, face_names):
        y1, x1, y2, x2 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]
        #print(face_loc)

        cv2.putText(frame, name, (x1, y1 - 10), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 0), 2)
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
    
        frame_count += 1
        fps_frame_count += 1

    # Calculate and display FPS over multiple frames
    if fps_frame_count >= 30:  # Update FPS every 30 frames
        fps_end_time = time.time()
        fps = fps_frame_count / (fps_end_time - fps_start_time)
        fps_start_time = fps_end_time
        fps_frame_count = 0
        cv2.putText(frame, f"FPS: {fps:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    

    if not ret:
        print("Error: Could not read frame.")
        break
    
    
    # Display the resulting frame
    cv2.imshow('Frame', frame)

    # Press 'q' to exit the video window
    key = cv2.waitKey(1)
    if key & 0xFF == ord('q'):
        break

    # Add a small delay to manage frame rate
    time.sleep(1 / desired_fps)

# Release the capture and close any OpenCV windows
cap.release()
cv2.destroyAllWindows()