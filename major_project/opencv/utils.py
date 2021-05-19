import csv
import os
import base64
import pandas as pd
from PIL import Image
import numpy as np
import requests
import json
import sqlalchemy
from sqlalchemy import create_engine
from datetime import date
from datetime import datetime

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
    image.save(os.path.join(workpath, 'image.jpg'))
    value=image_request(os.path.join(workpath,"image.jpg"))
    
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
        elif(i.isdigit() and k<=8 and flag==True):
            str1=str1+i
            k+=1
        elif(i=="m"):
            flag=False   
            
    """
    final_digits=[]
    for i in description:
        if(i.isdigit()):
            final_digits.append(i)
    print(final_digits)  
    print("Recognized Digits") 
    #gas1 final_digits[10:18]
    #gas2 final_digits[25:33]    
    #str1=''.join(final_digits[10:18])  
    str1=''.join(final_digits[25:33])  
    """
    print(str1) 
     
    customer_no="01222345"
    value=db.execute("select meter_reading,date from meter_readings where consumer_no="+f"'{customer_no}'")
    print(value)
    value1=list(value)
    print(value1)
    flag1=False
    if(len(value1)>0):
        list1=[]
        
        print(value)
        for i in value1:
            list1.append(list(i))
        print(list1)
        print(int(list1[-1][0]),int(str1))
        check=[]
        check.append(list1[-1][0])
        check.append(str1)
        print(check[0][0:5],check[1][0:5])
        if(int(check[0][0:5])>=int(check[1][0:5])):
            flag1=True
    if(flag1==False):

        meter_reading=str1
        print(meter_reading)
        date1=date.today()
        timestamp=int(datetime.timestamp(datetime.now()))
        timestamp= datetime.fromtimestamp(timestamp)
        db.execute("insert into"+" meter_readings("+'"consumer_no",'+'"meter_reading",'+'"date",'+'"timestamp"'+") "+f"values('{customer_no}','{meter_reading}','{date1}','{timestamp}')")
        value=db.execute("select meter_reading,date from meter_readings where consumer_no="+f"'{customer_no}'")
        list1=[]
        for i in value:
            list1.append(list(i))
        if(len(list1)>1):
            meter=[]
            print(list1[-1])
            print(list1[-2])
            meter.append((list1[-2][0]))
            meter.append((list1[-1][0]))
            date_value=(list1[-1][1]-list1[-2][1])
            print(date_value)
            if int(str(date_value)[0])==0:
                date_value=1
            else:
                date_value=int(str(date_value)[0])
            print(meter)
            ans=int(meter[1][0:5])-int(meter[0][0:5]) 
            print(ans)
            scmd=ans/date_value
            if(scmd<=0.60):
                value=scmd*date_value
                value=value*21.96
            elif(0.61<=scmd<=1.50):
                value1=0.60*date_value
                value1=value1*21.96
                scmd=scmd-0.60
                value=scmd*date_value
                value=value*26.01 
                value=value1+value
            elif(scmd>1.51):
                value1=0.60*date_value
                value1=value1*21.96
                scmd=scmd-0.60
                value2=0.90*date_value
                scmd=scmd-0.90
                value2=value2*26.01
                value=scmd*date_value
                value=value*33.36
                value=value+value1+value2
            print("Billing:",value)
            date1=date.today()
            db.execute(f"insert into billing(\"consumer_no\",\"pc_scmd\",\"bill_amount\",\"date\") values('{customer_no}',{scmd},{value},'{date1}');")
    else:
        print("Sorry the meter reading is faulty")    


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