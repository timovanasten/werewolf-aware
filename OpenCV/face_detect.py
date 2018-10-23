import cv2
import sys

casc_path_face = "haarcascade_frontalface_default.xml"
casc_path_body = "haarcascade_upper_body.xml"
faceCascade = cv2.CascadeClassifier(casc_path_face)
bodyCascade = cv2.CascadeClassifier(casc_path_body)

video_capture = cv2.VideoCapture("J:\TU Delft\SSP\data_set_wolf_2\wolf_2_C_E.avi")

# print(dir(cv2))

while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )

    bodies = bodyCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )

    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        print('[x,y,w,h] : ', '[',x,',',y,',',w,',',h,']')
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 255, 0), 2)
        cv2.circle(frame, (int((x+(w/2))), int((y+(h/2)))), 5, (255, 0, 0), 2)

    for (x, y, w, h) in bodies:
        print('[x,y,w,h] : ', '[',x,',',y,',',w,',',h,']')
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.circle(frame, (int((x+(w/2))), int((y+(h/2)))), 5, (255, 0, 0), 2)    	

    # Display the resulting frame
    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()