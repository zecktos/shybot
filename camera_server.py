from flask import Flask, render_template, Response
import cv2

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

def gen():
    camera = cv2.VideoCapture(0)
    camera.set(3, 640)
    camera.set(4, 480)
    faceFrontCascade = cv2.CascadeClassifier("haarcascades/haarcascade_frontalface_default.xml")

    if camera.isOpened() :
        print("camera opend")
    else : 
        raise RuntimeError('Could not start camera.')

    while True :
        rt, frame = camera.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = faceFrontCascade.detectMultiScale(
                gray,
                scaleFactor = 1.2,
                minNeighbors = 1,
                minSize = (150, 150)
        )
        for (x, y, w, h ) in faces :
            cv2.rectangle(frame, (x, y), (x + w, y + h), (220, 99, 255), 2)
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = frame[y:y+h, x:x+w]

        frame = cv2.imencode(".jpg", frame)[1].tobytes()
        yield (b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n")

@app.route("/video_feed")
def video_feed():
    return Response(gen(),
                    mimetype = "multipart/x-mixed-replace; boundary=frame")

if __name__ == "__main__" :
    app.run(host="0.0.0.0")

