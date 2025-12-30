from fastapi import APIRouter ,Depends,HTTPException,status
from sqlalchemy.orm import Session
from .. import schemas  , models
from .. import database
from ..core.hashing import hash
from ..core import security


router=APIRouter(tags=['User'])


@router.post("/register")
def create_user(request:schemas.UserData ,db:Session= Depends(database.get_db)):
    hashed_pwd=hash.get_hash_password(request.password)
    new_user=models.Users( email=request.email ,hashed_password=hashed_pwd)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/get/user/{user_id}" , response_model=schemas.UserResponse)
def get_user(user_id:int ,db:Session= Depends(database.get_db)):
    user=db.query(models.Users).filter(models.Users.id==user_id).first()

    if not  user:
       raise HTTPException (status_code=status.HTTP_404_NOT_FOUND) 
    return user


@router.get("/get/users/all", response_model=list[schemas.UserResponse])  #Protected Route to Test
def get_all_users(
    db: Session = Depends(database.get_db),
    current_user: models.Users = Depends(security.get_current_user)
    ):
    users = db.query(models.Users).all() 
    
    if not users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='No users exist'
        )
    return users
    