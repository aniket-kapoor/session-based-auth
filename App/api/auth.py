from fastapi import APIRouter , HTTPException , status
from .. import schemas , models
from .. import database
from fastapi import Depends, Response
from sqlalchemy.orm import Session
from ..core.hashing import hash
import uuid
from datetime import timedelta, datetime , timezone
from ..core.security import cookie_scheme


router=APIRouter()


@router.post('/login')
def login(data:schemas.UserData, response:Response,
          db:Session=Depends(database.get_db)):
    
    user=db.query(models.Users).filter(models.Users.email==data.email).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED ,
                             detail="Invalid Credentials")
    
    if not hash.verify_password( data.password , user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail='Wrong Password',
                            headers={"WWW-Authenticate": "Bearer"})

    session_id = str(uuid.uuid4())
    expiry_date = datetime.now(timezone.utc) + timedelta(days=1)
   

    session=models.Session(session_id=session_id, user_id=user.id , expires_at=expiry_date  , )

    db.add(session)
    db.commit()
    
    response.set_cookie( 
        key="session_id",
        value=session_id,
        httponly=True,  #Prevents JavaScript access
        samesite="lax",  # CSRF protection
        secure=True,  # HTTPS only (use True in production!)
        max_age=86400)
    
    return {"message": "Login successful"}


@router.post('/logout')
def logout(
    response: Response,
    db: Session = Depends(database.get_db),
    session_id: str | None = Depends(cookie_scheme)
):
   
    if session_id:
       
        session = db.query(models.Session).filter(
            models.Session.session_id == session_id
        ).first()
        
        if session:
            db.delete(session)
            db.commit()
    
   
    response.delete_cookie(key="session_id")
    
    return {"message": "Logout successful"}





    


    
    

