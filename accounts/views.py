from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

# Import model and Generic Methods 
from accounts.models import User
from accounts.serializers import * 
from portals.GM2 import GenericMethodsMixin
from django.core.exceptions import ObjectDoesNotExist

from django.contrib.auth.hashers import check_password
from random import randint
from django.db import transaction
from portals.email_utility import send_email_async
from portals.services import generate_token


import requests
def send_otp_to_phone(phone_number,otp) :
    try : 
        api_key  = "bcbc6fc9-14d9-11ef-8b60-0200cd936042"
        new_key = "841a5c5f-8159-11ef-8b17-0200cd936042"
        url    = f'https://2factor.in/API/V1/{api_key}/SMS/{phone_number}/{otp}/'
        response = requests.get(url)
        return otp
    except Exception as e :
        return None

class UserAPI(GenericMethodsMixin,APIView):
    model = User
    serializer_class = UserSerializer1
    lookup_field = "id"
    
class CustomerAPI(GenericMethodsMixin,APIView):
    model = User
    serializer_class = UserSerializer1
    lookup_field = "id"

class RegisterUserApi(APIView):
    def post(self,request,*args, **kwargs):
        try : 
            with transaction.atomic():
                print(request.data)
                mobile_number = request.data.get('mobile_number')
                serializer = UserSerializer(data=request.data)
                sms_otp   = randint(100000,999999)
                request.POST._mutable = True
                request.data['sms_otp']  = sms_otp 
                otp = send_otp_to_phone(mobile_number,sms_otp) 
                print(otp)
                if  serializer.is_valid():
                    user = serializer.save()
                    token = generate_token(user.mobile_number)
                    return Response({"message" : "User Created Successfully" , "data" : UserSerializer1(user).data , "token" : token},status=status.HTTP_201_CREATED)
                error_list = [serializer.errors[error][0] for error in serializer.errors]
                return Response({"error": True, "message": error_list}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e :
            return Response({"error" : True , "message" : str(e) , "status_code" : 400},status=status.HTTP_400_BAD_REQUEST,)

class VerifyOTPApi(APIView):
    def post(self, request, *args, **kwargs):
        try : 
            mobile_number = request.data.get('mobile_number')
            sms_otp = request.data.get('sms_otp')
            # sms_otp = request.data.get('sms_otp')
            print(mobile_number,sms_otp)
            if not mobile_number or not sms_otp :
                return Response({"error": True, "message": "Mobile Number, and SMS OTP are required."}, status=status.HTTP_400_BAD_REQUEST)
            try:
                user = User.objects.get(mobile_number=mobile_number)
                print(user.mobile_number,user.sms_otp)
            except ObjectDoesNotExist:
                return Response({"error": True, "message": "User not found."}, status=status.HTTP_404_NOT_FOUND)
            if user.sms_otp == sms_otp:
                print(mobile_number,sms_otp)
                token = generate_token(user.mobile_number)
                return Response({"error": False, "message": "OTP verified successfully.","token" : token , "user_role" : user.user_role }, status=status.HTTP_200_OK)
            return Response({"error": True, "message": "Invalid OTP for Mobile Number."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e :
            return Response({"error" : True , "message" : str(e) ,"status_code" : 400},status=status.HTTP_400_BAD_REQUEST,)

class ResendOTPApi(APIView):
    def post(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                mobile_number     = request.data.get('mobile_number')
                user              = User.objects.get(mobile_number=mobile_number)
                sms_otp           = randint(100001,999999)
                otp               = send_otp_to_phone(mobile_number,sms_otp)
                user.sms_otp      = sms_otp
                user.save()
                return Response({"error": False, "message": "OTP Sent successfully." , "sms-otp" : sms_otp}, status=status.HTTP_200_OK)
        except Exception as e :
            return Response({"error" : True , "message" : str(e) , "status_code" : 400},status=status.HTTP_400_BAD_REQUEST,)

class LoginAPI(APIView):
    def post(self,request,*args,**kwargs):
        try :
            mobile_number     = request.data.get('mobile_number')
            user              = User.objects.get(mobile_number=mobile_number)
            sms_otp           = randint(100001,999999)
            user.sms_otp      = sms_otp
            otp = send_otp_to_phone(mobile_number,sms_otp)
            user.save()
            return Response({"error" : False, "message" : "OTP send Successfully" , "otp" : user.sms_otp},status=status.HTTP_200_OK)
        except Exception as e :
            return Response({"error" : True , "message" : str(e) , "status_code" : 400},status=status.HTTP_400_BAD_REQUEST,)

 
class LoginWithUsernamePassword(APIView):
    def post(self,request,*args, **kwargs):
        try : 
            username       = request.data.get('username')
            password       = request.data.get('password')
            user           = User.objects.filter(username=username).first()
            if user is None : 
             return Response({"error" : False,"message" : "User Not Exists"},status=status.HTTP_400_BAD_REQUEST)
            token = generate_token(user.mobile_number)
            password_match = check_password(password,user.password)
            serializer = UserSerializer2(user)
            print(serializer.data,"------------------------")
            # data = {"error" : False, "message": "User logged in successfully","user_info": serializer.data,"token" : token}
            if password == user.password  or password_match:
                return Response({"error" : False, "message" : "User logged in successfully",token : token , "data" : serializer.data},status=status.HTTP_200_OK)
            return Response({"error" : True, "message" : "Password is not Matched"},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e :
            return Response({"error" : True, "message" : str(e)},status=status.HTTP_400_BAD_REQUEST)

class ChangePasswordApi(APIView):
    def post(self,request,*args, **kwargs):
        try : 
            serializer = ChangePasswordSerializer(data=request.data,context={'request': self.request})
            if serializer.is_valid():
                serializer.save()
                return Response({"Success": "Password updated successfully"},status=status.HTTP_202_ACCEPTED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e :
                return Response({"error" : True, "message" : str(e)},status=status.HTTP_400_BAD_REQUEST)


class UserProfileAPI(APIView):
    def get(self,request,*args,**kwargs):
        try :
            user_data = User.objects.get(id=request.thisUser.id)
            serializer = UserSerializer2(user_data)
            return Response({"error" : False, "data" : serializer.data},status=status.HTTP_200_OK)
        except Exception as e :
            return Response({"error" : True , "message" : str(e)},status=status.HTTP_400_BAD_REQUEST)
