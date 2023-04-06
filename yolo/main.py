import sys
import os
import time
from pathlib import Path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import torch
from time import sleep
from config.mqtt import topicPub
from config.drive import currentdayImagePath
from yolo.helper import TakeImage, ResultsParser, GetDeviceTopic
from yolo.mqtt import connectMqtt

try: 
  mqttClient = connectMqtt()
except:
  print("failed to connect mqtt as sender")

model = torch.hub.load('ultralytics/yolov5', 'yolov5n')
model.multi_label = False
model.classes = [0]
model.max_det = 1
model.cpu()

def ImageProcess(uniqueName):
  begin = time.time()
  img = Path(f"{currentdayImagePath}/{uniqueName}.bmp")
  rawResult = model(img)
  print(f"time run ImageProcess is {round(time.time() - begin, 1)} seconds")
  return ResultsParser(rawResult)

def PredictImage():
  beginImage = time.time()
  commandArr = ["servo360:45", "servo360:135", "servo180:90", "servo360:45", "servo360:135"]
  deviceTopic = GetDeviceTopic()
  for command in commandArr:
    mqttClient.publish(deviceTopic, command)
    sleep(1)
    TakeImage()
    print("Take a picture now")
  mqttClient.publish(deviceTopic, "requestResetServo")
  print(f"time run ImageCapture is {round(time.time() - beginImage, 1)} seconds")

  if not len(os.listdir(currentdayImagePath)) == 0:
    for file in os.listdir(currentdayImagePath):
      result = ImageProcess(file[:file.index(".")])
      if result != "0": 
        mqttClient.publish(topicPub, "1")
        return
    mqttClient.publish(topicPub, "0")
  else: 
    print("No file to detect")