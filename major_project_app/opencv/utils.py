import cv2
import matplotlib.pyplot as plt
import easyocr
import cv2 as cv
import matplotlib.pyplot as plt
import csv
import boto3
import os
import base64
import pandas as pd
from django.contrib.staticfiles import finders
from PIL import Image
import numpy as np
import requests
import json
import sqlalchemy
from sqlalchemy import create_engine
engine=sqlalchemy.create_engine("postgresql://bgnnchtclsosex:13f25d52cbda8621b0ecee9dea4bfa691e9022a98f134c4a96e2658d62711d1a@ec2-107-22-83-3.compute-1.amazonaws.com:5432/d2phjkie6l3btf")
db=engine.connect()
url = "https://vision.googleapis.com/v1/images:annotate"
workpath=os.path.dirname(os.path.abspath(__file__))
c=open(os.path.join(workpath,"api_key.txt"),"r")
api_key=c.read()
querystring={"key":api_key}
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read())
def image_request(image_path):
    
    payload = '{  \"requests\":[    {      \"image\":{        \"content\":\"'+encode_image(image_path).decode("utf-8")+'"      },      \"features\":[        {          \"type\":\"TEXT_DETECTION\" }      ]    }  ]}'
    response = requests.request("POST", url, data=payload, params=querystring)

    return response.text  
def get_filtered_image(image,action):
    image.save(os.path.join(workpath, 'image.jpeg'))
    value=image_request(os.path.join(workpath,"image.jpeg"))
    
    with open(os.path.join(workpath,"value.txt"),"w") as file:
        file.write(value)
    with open(os.path.join(workpath,"value.txt"),"r") as file:
        read=json.loads(file.read()) 
    value=read.get("responses")
    value1=dict(value[0])
    text_annot=value1["textAnnotations"]
    value2=dict(text_annot[0])
    description=value2["description"]
    k=0
    str1=""
    flag=False
    for i in description:
        print(i)
        if(i=='r'):
            flag=True
        if(i.isdigit() and k<=8 and flag==True):
            str1=str1+i
            k+=1
        if(i=="m"):
            flag=False   
    print(str1)        
    customer_no="01222345"
    meter_reading=int(str1)
    date1=date.today()
    timestamp=int(datetime.timestamp(datetime.now()))
    timestamp= datetime.fromtimestamp(timestamp)
    db.execute("insert into"+" meter_readings("+'"consumer_no",'+'"meter_reading",'+'"date",'+'"timestamp"'+") "+f"values('{customer_no}',{meter_reading},'{date1}','{timestamp}')")


    """
    print("This is image array",image)
   
    
    os.environ["AWS_DEFAULT_REGION"]='us-west-2'
    workpath = os.path.dirname(os.path.abspath(__file__))
    c = open(os.path.join(workpath, 'new_user_credentials.csv'), 'r')
    next(c)
    reader=csv.reader(c)
    
    

    print("This is csv",reader)
    for line in reader:
        aws_key_id=line[2]
        secret_access_key=line[3]
        print("AWS_KEY",aws_key_id,"AWS SECRET key",secret_access_key)
    client=boto3.client("rekognition",aws_access_key_id=aws_key_id,aws_secret_access_key=secret_access_key)
    
    
    image.save(os.path.join(workpath, 'image.png'))
    with open(os.path.join(workpath, 'image.png'),"rb") as image:
        source_bytes=image.read()
    response=client.detect_text(Image={"Bytes":source_bytes})
    for i in response['TextDetections']:
        for j,k in i.items():
            if(j=="DetectedText"):
                if(len(k)>=5  and k.isdigit()==True):
                    print(k)  
    """                 

    """
    reader=easyocr.Reader(['en'])
    
    
    def digit_recognition():
        output1=[]
        k=0
        for m in range(1,9,1):
            img=cv.imread(f"{m}.png")
            #Capture 6 120 resize 
            #Capture 5 300 resize
            #Capture 4 300 resize
            #Capture 3 100 resize
            #Capture 2 100 resize 
            #Capture 100 resize 
            #gas_meter 220 resize
            img=cv.resize(img,(180,180),cv.INTER_AREA)
            
            output=reader.readtext(img,allowlist="0123456789")
            k=0
            cv.waitKey(0)
            for i in output:
                for j in i:
                    k=k+1
                    if k==2:
                        if(len(j)>1):
                            val=list(j)
                            final_digits.append(int(val[0]))
                            print(val[0])
                        elif (j!=''):
                            final_digits.append(int(j))
                            print(j)
                    
    def digit_extraction(img):
        x=0
        w=75
        y=0
        h=100
        #Capture image 6 values x=5 w=28 y=5 h=40
        #Capture image 6 values x=5 w=45 y=5 h=50
        #Capture image 5 values x=5 w=45 y=0 h=50
        #Capture image 4 values x=28 w=25 y=0 h=35
        #Capture image 3 values x=0 w=25 y=0 h=40
        #Capture image 2 values x=0 w=20 y=0 h=20
        #Capture x=0 w=17 y=0 h=15
        #meter.jpg x=2 w=30 y=9 h=25
        #gas_mter.jpeg x=0 w=75 #y=9 #h=100
        #gas_meter1.jpeg x=0 w=60 #y=0 #h=100
        #gas_meter_2.jpeg x=0 w=60 #y=0 #h=100




        
        for i in range(1,9,1):
            
            roi = img[y:y + h, x:x + w]
            x=x+w
            cv.imwrite(str(i) + '.png', roi)
        digit_recognition()  

    def image_crop():
        
        img=open_cv_image[365:440,237:834]
        #img=cv.imread("gas_mter.jpeg")
        #img=img[360:450,220:1000]
       
        #img=img[52:78,30:200]Capture6
        #img=img[90:140,56:343]Capture5
        #img=img[70:110,70:280]Capture 4
        #img=img[70:110,80:280]Capture3
        #img=img[70:90,80:180]Capture2
        #plt.imshow(img[90:130,25:175]) meter.jpg
        #img=img[90:130,25:175]
        #img=img[350:450,220:1000] gas_meter.jpeg
        #gas_meter1 img=img[360:450,220:1000]
        #gas_meter_2 img=img[359:468,237:834]
        
        digit_extraction(img)
    final_digits=[]
    image_crop()
    with open('data.txt', 'a') as f:
        f.write(str(final_digits))    
    """    

    
    if action=='NO_FILTER':
        filtered=image
    return filtered    