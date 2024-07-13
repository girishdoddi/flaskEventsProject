import smtplib
import random
from uuid import uuid4
from hashlib import md5
from database.connect_database import session
from database.table_models import Users, OTP
from constants import USER_EXISTS, DB_ERROR, SECRET_KEY
from datetime import datetime, timedelta

import jwt

from interfaces.jwt_tokens import JWTManagement

class SendEmail():
    def __init__(self) -> None:
        self.sender_email = "girishdoddi055@gmail.com"
        self.password = "pojtrzbidcbzgxwf"


    def generate_random_otp(self):
        otp = ""
        for i in range(4):
            otp += str(random.randint(0,9))
        return otp
    
    def send_otp_to_email_core(self, email_id, user_name, otp):
        
        message = f"Hey {user_name} here is you otp for email verification --> {otp}, Kudos!"
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(self.sender_email, password=self.password)
        print("Login success")

        #send otp via mail to verify
        server.sendmail(self.sender_email, email_id, message)
        server.quit()


    def send_otp_to_email(self,email_id, user_name, user_password):
        otp = self.generate_random_otp()
        user_password = md5(user_password.encode("utf-8")).hexdigest()
        try:
            check_user = session.query(Users).filter_by(email = email_id).first()
        except Exception as e:
            print(e)
            return DB_ERROR
        user_id = 0
        print("*****************************************************************************")
        if check_user and check_user.is_verified:
            return USER_EXISTS
        if check_user:
            #if user exists and he is not verified yet.
            user_id = check_user.id
            check_user.password = user_password
            session.commit()
        else:
            #If no user exists add a new user
            user = Users(name = user_name, password = user_password, email = email_id, createdat = datetime.now(), is_verified = False)
            session.add(user)
            session.commit()
            user_id = user.id
        otp_data_check = session.query(OTP).filter_by(user_id=user_id).first()
        if otp_data_check:
            otp_data_check.otp = otp
            otp_data_check.created_at = datetime.now()
            session.commit()
        else:
            otp_row = OTP(user_id = user_id, otp = otp, created_at=datetime.now())
            session.add(otp_row)
            session.commit()
        # server.debuglevel(1)
        # server.timeout = 10
        #send otp to Email via SMTP service.
        self.send_otp_to_email_core(email_id, user_name, otp)
        print("Email Sent successfuly")
        return user_id
        
    def forget_password(self, email_id):
        #Generating OTP
        otp = self.generate_random_otp()

        #Storing OTP in DB
        user = session.query(Users).filter_by(email = email_id).first()
        if not user or not user.is_verified:
            return "User Does Not Exists or Yet To Be verified"
        user_name = user.name
        id = user.id
        otp_row = session.query(OTP).filter_by(user_id = id).first()
        if not otp_row:
            otp_obj = OTP(user_id = id, otp = otp, created_at = datetime.now())
            session.add(otp_obj)
        else:
            otp_row.otp = otp
        session.commit()

        self.send_otp_to_email_core(email_id, user_name, otp)
        return id

            

class VerifyOtp:
    def __init__(self) -> None:
        pass



    def verify_otp(self, id, otp, password_change_bool = False):
        user_data_otp = session.query(OTP).filter_by(user_id = id).first()
        user_data = session.query(Users).filter_by(id=id).first()
        if not user_data:
            return "User Doesent Exist"
        if not user_data_otp:
            return "OTP Either Expired or Not Sent To Email"
        if user_data_otp and user_data.is_verified and not password_change_bool:
            return "User Already Verified! please login"
        if user_data_otp and user_data_otp.otp != otp:
            return "OTP Is INVALID, Please Enter the Valid OTP"
        user_data.is_verified = True
        session.delete(user_data_otp)
        session.commit()
        return "User Successfully Verified"
    
class LoginUser:
    def __init__(self) -> None:
        self.jwt_managment = JWTManagement()

    def log_user(self, username, password):
        user_data = session.query(Users).filter_by(email= username).first()
        password = md5(password.encode('utf-8')).hexdigest()
        if not user_data:
            return "User Doesn't Exsist"
        if user_data and user_data.password != password:
            return "Invalid Password"
        
        if user_data and not user_data.is_verified:
            return "Invalid Username/Password"
        
        payload = {
            "user_id" : user_data.email,
            "exp" : datetime.now() + timedelta(minutes= 30)
        }

        token = JWTManagement().encode_payload(payload)

        return token
        

class ChangePassword():
    def __init__(self) -> None:
        pass


    def change_password(self, user_id, password):
        check_email_id = session.query(Users).filter_by(id = user_id).first()
        if not check_email_id:
            return "Invalid User"
        
        check_email_id.password = md5(password.encode('utf-8')).hexdigest()
        session.commit()

        return "Password Changed Successfully"


            

