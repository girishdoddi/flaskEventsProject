import smtplib
import random
from uuid import uuid4

from interfaces.send_email import ChangePassword, SendEmail, VerifyOtp, LoginUser
from interfaces.jwt_tokens import JWTManagement


def add_details_and_get_otp(username, email, password):
    return SendEmail().send_otp_to_email(email_id= email,
            user_name=username, user_password=password)


def verify_otp_from_db(id, otp):
    return VerifyOtp().verify_otp(id, otp)

def login_user(username, password):
    return LoginUser().log_user(username, password)

def forget_password_func(email):
    return SendEmail().forget_password(email)

def verify_otp_change_password(id, otp, password):
    data = VerifyOtp().verify_otp(id, otp, True)
    print(data)
    if data != "User Successfully Verified":
        return "Invalid OTP"
    return ChangePassword().change_password(id, password)


def get_payload_from_token(token):
    payload = JWTManagement().decode_token(token)
    return payload

def delete_user_account(email):
    