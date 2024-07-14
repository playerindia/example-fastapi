from fastapi import FastAPI,Response,status, HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session
from .. import models,schemas,utils
from .. database import get_db


router = APIRouter(  prefix ='/users',
                    tags =['Users']
                   )

@router.post("/",status_code = 201,response_model =schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
  

    hashed_password = utils.hash(user.password)
    user.password = hashed_password 
    new_user= models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user    


@router.get("/{id}",response_model =schemas.UserOut)
def get_post(id:int,db: Session = Depends(get_db)):
   
    #  cursor.execute(""" SELECT * FROM posts WHERE id = (%s)  """,(str(id)))
    #  posts = cursor.fetchone()

    #  insted of first if you use all you get list 
     user = db.query(models.User).filter(models.User.id == id).first()

     if not user:
      raise HTTPException(status_code=404, detail="Item not found.")
    


     return user 