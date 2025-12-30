from .. import database
from sqlalchemy.orm import Session
from fastapi import Depends , Cookie , HTTPException,status
from fastapi.security import APIKeyCookie
from datetime import datetime, timezone
from .. import models

#This is the get_current_user dependency function

#This creates the security scheme for Swagger UI


cookie_scheme = APIKeyCookie(name="session_id", auto_error=False)



def get_current_user( session_id: str | None = Depends(cookie_scheme),
                     db:Session=Depends(database.get_db)):
    
    if not session_id :
        raise HTTPException(status_code=401 , 
                            detail="Not Authenticated")
    
    session=db.query(models.Session).filter(
        models.Session.session_id==session_id).first()

    if not session:
        raise HTTPException(status_code=401, detail="Invalid Session")
    
    if session.expires_at < datetime.now(timezone.utc):
        db.delete(session)
        db.commit()
        raise HTTPException(status_code=401 , detail="Session Expired")
    
    user=db.query(models.Users).filter(
        models.Users.id==session.user_id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User doesn't exist")
    
    return user
    


