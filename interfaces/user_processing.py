from database.connect_database import session
from database.table_models import Users

class DeleteUser():
    def __init__(self) -> None:
        pass


    def delete_user_account(self, email):
        user_data = session.query(Users).filter_by(email = email).first()
        if not user_data or not user_data.is_verified:
            return "User Does Not Exist or Nor Verified"
        
        session.delete(user_data)
        session.commit()

        return "User Successfully Deleted"
    

