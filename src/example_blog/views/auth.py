from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from example_blog.dependencies import get_db
from example_blog.services import UserService

router = APIRouter()

user_service = UserService()


@router.post('/token')
def login(
        form_data: OAuth2PasswordRequestForm = Depends(),
        session: Session = Depends(get_db)
):
    return user_service.auth_for_access_token(session, form_data.username, form_data.password)
