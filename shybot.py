import cv2
import time
import pigpio

# set up camera
camera = cv2.VideoCapture(0)
camera.set(cv2.CAP_PROP_BUFFERSIZE,1)
camera.set(3, 640)
camera.set(4, 480)
faceFrontCascade = cv2.CascadeClassifier("haarcascades/haarcascade_frontalface_default.xml")

# servo range is between 3 and 13 
center = int(9 * 10000)
step0 = (int(5.8 * 10000), int(5 * 10000))
step1 = (int(8 * 10000), int(5 * 10000))
step2 = (int(8 * 10000), int(7.8 * 10000))

def setupHead(servoX, servoY, init_pos, freq) :
    pi = pigpio.pi()
    pi.hardware_PWM(servoX, freq, init_pos)
    pi.hardware_PWM(servoY, freq, init_pos)
    return (servoX, servoY, freq, pi)

def moveHead(config, dest, timeout) :
    pos = [config[3].get_PWM_dutycycle(config[0]), config[3].get_PWM_dutycycle(config[1]) ]

    while dest[0] != pos[0] or dest[1] != pos[1] :
        for i, v in enumerate(pos) :
            if v < dest[i] :
                pos[i] = v + 100
            if v > dest[i] :
                pos[i] = v - 100
            config[3].hardware_PWM(config[i], config[2], pos[i])
            time.sleep(timeout)

def headGetPosition(config) :
    pos = (config[3].get_PWM_dutycycle(config[0]), config[3].get_PWM_dutycycle(config[1]) )
    return pos




if camera.isOpened() :
    print("camera opend")
else :
    raise RuntimeError(" Could not start camera ")
    pass

print(" setup servos ...")
conf = setupHead(19, 18, center, 50)
time.sleep(1)

timer = 0 

print("enter main loop")
while True :

    rt, frame = camera.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = faceFrontCascade.detectMultiScale(
                gray,
                scaleFactor = 1.2,
                minNeighbors = 1,
                minSize = (150, 150)
    )

    if faces is not () :
        print("oh no a face ! ")
        print(faces)
        moveHead(conf, step0,0)
        camera.grab()
        time.sleep(5)

    if headGetPosition(conf) == step0 :
        moveHead(conf,step1,0.004)
        time.sleep(3)

    if headGetPosition(conf) == step1 :
        moveHead(conf, step2,0.003)
        time.sleep(2)

    if headGetPosition(conf) == step2 :
        moveHead(conf, (center, center) ,0.001)
        

