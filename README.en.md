[Lao document version](https://github.com/xang555/face_recon/blob/master/README.md) | [English document version](https://github.com/xang555/face_recon/blob/master/README.en.md)

# face_recon

`face_recon` is a RESTful API implementing `face recognition` system developed with Python and Flask framework which can connect to IP camera that support RTSP protocol.

> Note: Still in development, several bugs may occurs

![demo](img/monitor.png)

## Concept

`face_recon` is a RESTful API managing data for identification, e.g. a picture with face. Using face verification principle to identify, retrieving person picture in database to compare with target picture by calculating distance between face embedding vector.

## Dashboard

`face_recon` has Web UI for easily use. Visit [facerecon_dashboard](https://github.com/xang555/facerecon_dashboard) for more information.

## Installation

### Requirements

+ Python 3
+ TensorFlow v2: [Install TensorFlow](https://www.tensorflow.org/install)
+ dlib: [How to install dlib from source on macOS or Ubuntu](https://gist.github.com/ageitgey/629d75c1baac34dfa5ca2a1928a7aeaf)
+ `face_reconition`: [How to Install face_recognition](https://github.com/ageitgey/face_recognition)
+ MTCNN: [Install mtcnn](https://github.com/ipazc/mtcnn)
+ `opencv-python`: [Install OpenCV For Python](https://pypi.org/project/opencv-python/)

Clone this repo and then run following command to install required dependencies:

```bash
pip3 install -r requirements.txt
```

## Usage

Start web server with following command:

```bash
python3 app.py
```

### Testing with Webcam

Assuming you don't have IP camera and you want to test via webcam, you can do so by editing `IpcameraStream.py`, change `url` to number or IO path of camera e.g. `0` or `/dev/video0` for Linux and macOS.

```python
class IpcameraStream:
    def __init__(self, uri):
        self.stream = cv2.VideoCapture(0) # Edit here
        self.stream.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.stream.set(cv2.CAP_PROP_BUFFERSIZE, 3)
        ....
```

## TODO

+ Change face reognition model to VGGFACE2
+ Optimize stream camera
+ Create production setup
+ Create Docker setup
+ Improve english readme (this doc)
+ Write test
+ Add support usb camera
+ Support store and calculate distance face embedding in database
