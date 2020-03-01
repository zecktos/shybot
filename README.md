# Shybot

Shybot is a little shy robot. If it recognizes a human face it turns away, because, well, it is very shy.
It is driven by two servo motors controlled from a raspberry pi.
Image processing is done with opencv.
  
## Setup

`sudo apt install pigpiod python3-opencv python3-flask python3-pigpio`  
in directory '/haarcascades' do :  
`wget https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/haarcascade_frontalface_default.xml`

## Usage

run `python3 shybot.py` for the main loop  
run `python3 camera_server.py` to start a flask server streaming the camera video

![shybot](./img/shybot.gif)
