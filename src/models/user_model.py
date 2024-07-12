from pydantic import BaseModel
class UserModel(BaseModel):
    __tablename__ = "user_account"

