from flask import Flask, request


from interfaces.request_validations import SignUpValidator, Token, ValidationError
from interfaces.request_validations import VerifyOtp, SignIn, PasswordChange,VerifyOtpChangePassword
from interfaces.users_process import add_details_and_get_otp, forget_password_func, get_payload_from_token, verify_otp_change_password, verify_otp_from_db
from interfaces.users_process import login_user
app = Flask(__name__)



@app.route('/')
def check_working():
    return "Working"

@app.route('/signup', methods = ["POST"])
def sign_up():
    try:
        data = request.get_json()
        signup_data = SignUpValidator(**data)
        username = signup_data.username
        email = signup_data.email
        password = signup_data.password
    except ValidationError as e:
        print(e)
        return "Validation Exception Occured"
    except Exception as e:
        print(e)
        return "Exception Occured"
    data = add_details_and_get_otp(username, email, password)
    if isinstance(data, int):
        return {"user_id" : data, "status" : "If the Email is Valid you will get the otp"}
    return {"status" : "Failed", "description" : data}


@app.route('/verify_otp', methods = ["POST"])
def verify_otp():
    try:
        request_data = request.get_json()
        parsed_data = VerifyOtp(**request_data)
        id = parsed_data.id
        otp = parsed_data.otp
    except ValidationError as e:
        print(e)
        return "Input Validation Error"
    except Exception as e:
        print(e)
        return "JSON Parsing Went Wrong"
    
    response = verify_otp_from_db(id, otp)
    return {"status" : response}

@app.route('/signin', methods = ["POST"])
def get_signin():
    try:
        request_data = request.get_json()
        validated_data = SignIn(**request_data)
        user_name = validated_data.username
        password = validated_data.password
    except ValidationError as e:
        print(e)
        return "Invalid Input"
    except Exception as e:
        print(e)
        return "Something Went Wrong, might me json parsing!!"
    token = login_user(user_name, password)
    return {"jwt_token" : token}

@app.route('/change_password', methods = ["POST"])
def password_change():
    try:
        input_body = request.get_json()
        input_body_obj = PasswordChange(**input_body)
    except ValidationError as e:
        print(e)
        return "Invalid Input"
    except Exception as e:
        print(e)
        return "Got Exception in input json converter"
    token = input_body_obj.token
    email = get_payload_from_token(token)
    print(email)
    if email == "Invalid Token" or email == "Signature verification failed":
        return "Invalid Token, please login"
    email = input_body_obj.email
    response = forget_password_func(email)
    return {"Status" : response}
    

@app.route('/verify_otp_change_password', methods = ["POST"])
def verify_otp_password():
    try:
        request_data = request.get_json()
        parsed_data = VerifyOtpChangePassword(**request_data)
        id = parsed_data.id
        otp = parsed_data.otp
        password = parsed_data.password
    except ValidationError as e:
        print(e)
        return "Input Validation Error"
    except Exception as e:
        print(e)
        return "JSON Parsing Went Wrong"
    token = parsed_data.token
    email = get_payload_from_token(token)
    if email == "Invalid Token" or email == "Signature verification failed":
        return "Invalid Token, please login"
    response = verify_otp_change_password(id, otp, password)
    return {"status" : response}


@app.route('/delete_account', methods = ["POST"])
def delete_account():
    try:
        input_body = request.get_json()
        parsed_input = Token(input_body)
    except ValidationError as e:
        print(e)
        return "Invalid Input from User"
    except Exception as e:
        print(e)
        return "Failed during parsing the request bosy to JSON"
    
    token = parsed_input.token
    email = get_payload_from_token(token)
    if email == "Invalid Token" or email == "Signature verification failed":
        return "Invalid Token, please login"
    
    response = delete_user_account()
    return {"Status" : response}


if __name__ == "__main__":
    app.run(debug= True)