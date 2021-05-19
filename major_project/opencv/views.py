from django.contrib import auth
from django.shortcuts import render
from .forms import ImageForm
from .models import Upload
import sqlalchemy
from sqlalchemy import create_engine
from datetime import date
from datetime import datetime
from twilio.rest import Client
from django.shortcuts import redirect
from django.contrib.auth import logout,login,authenticate
from django.contrib.auth.decorators import login_required
list2=[]
engine=sqlalchemy.create_engine("postgresql://bgnnchtclsosex:13f25d52cbda8621b0ecee9dea4bfa691e9022a98f134c4a96e2658d62711d1a@ec2-107-22-83-3.compute-1.amazonaws.com:5432/d2phjkie6l3btf")
db=engine.connect()
# Create your views here.
import os
import math,random
digits = "0123456789"
otp=""

for i in range(5) :
   otp+= digits[math.floor(random.random() * 10)]
print(int(otp))

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
path=os.path.join(BASE_DIR,'templates')
path1=os.path.join(path,'home.html')
path2=os.path.join(path,'index.html')
path3=os.path.join(path,'otp.html')
with open(os.path.join(BASE_DIR,"cred.txt"),"w") as file:
   file.write("False")
def logout1(request):
   with open(os.path.join(BASE_DIR,"cred.txt"),"w") as file:
      file.write("False")
   return redirect("/")
list1=[]
img=[]
def home(request):
 
 with open(os.path.join(BASE_DIR,"cred.txt"),"r") as file:
   value=file.read()
   print(value,request.method)
   request.method="POST"
   if(value=="True"):
      print("in")
      if request.method == "POST":
         form = ImageForm(request.POST, request.FILES)
         if form.is_valid():
            form.save()
         form = ImageForm()
         
      
      
         return render(request, path1, {'img':img,'form':form})
   else:
      return render(request, path2)     

def second(request):
   
   message=""
   if request.method=="POST":
      otp1=[]
      otp1.append(request.POST.get("first"))
      otp1.append(request.POST.get("second"))
      otp1.append(request.POST.get("third"))
      otp1.append(request.POST.get("fourth"))
      otp1.append(request.POST.get("fifth"))
      print("This is otp1",otp1)
      otp1="".join(otp1)
      if(otp==otp1):
         
         with open(os.path.join(BASE_DIR,"cred.txt"),"w") as file:
            file.write("True")
         return redirect("/uploads")   
      else:
         with open(os.path.join(BASE_DIR,"cred.txt"),"w") as file:
            file.write("False")
         message="Incorrect OTP" 
   return render(request, path3,{"message":message})
  
        



def first(request):
   message1=" "
   
   if request.method=="POST":
      consumer_no=request.POST.get("consumer")
      list2.append(consumer_no)
      print("This is the consumer no:",consumer_no)
      value=db.execute("select consumer_no,mobile_no from customer where consumer_no="+f"'{consumer_no}'")
      value1=list(value)
      print(value1)
      if(len(value1)>0):
         with open(os.path.join(BASE_DIR,"open.txt"),"r") as file:
            list1=file.read().split(" ")
         print(list1)   
         account_sid = list1[0]
         auth_token = list1[1]
         client = Client(account_sid, auth_token)
         print("This is:",otp)
         '''
         message = client.messages.create(
                              body=otp,
                              from_='+12542740980',
                              to=f"+91{value1[0][1]}"
                          )
         '''
         #print(message.sid)
         request.method="GET"
         message1=""
         return redirect("/otp")
         
      else:
         message1="Sorry you are not registered"


      
   return render(request, path2,{"message":message1})

      


