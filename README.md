# face_recon

`face_recon` ຄື restful api ທີ່ implement `face recognition` system ພັດທະນາໂດຍໃຊ້ `Python` ແລະ `Flask` http framework 

> Note: ຍັງຢູ່ໃນຊ່ວງພັດທະນາ ອາດມີຂໍ້ຜິດພາດຫຼາຍຈຸດ

# Installation

### requirements

ກ່ອນທີ່ຈະ run project ຕ້ອງໄດ້ຕິດຕັ້ງ environment ແລະ library ລຸ່ມນີ້ເສຍກ່ອນ

+ python3
+ tensorflow v2
+ dlib 
+ face_recognition face recognition library
+ mtcnn  deep learning face detection
+ opencv for python

 ການຕິດຕັ້ງແມ່ນໃຊ້ `pip3` ຫຼັງຈາກນັ້ນເຂົ້າໄປທີ່ `root` project ແລ້ວໃຊ້ຄຳສັ່ງ

 ```command
 $ pip3 install -r requirements.txt
 ```

# Usage

start web server ໂດຍໃຊ້ຄຳສັ່ງ

```command
$ python3 app.py
```

ສາມາດເຂົ້າໃຊ້ງານ API ຈາກ URL [http://localhost:8080/api/v1](http://localhost:8080/api/v1)

API Documents [face_recon api docs](asset/face_recon_api_docs.json)

# TODO

+ change face reognition model to VGGFACE2
+ optimize stream camera
+ create production setup
+ create Docker setup