from fastapi import FastAPI,Response,status, HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session
from typing import List,Optional
from sqlalchemy import func
from .. import models,schemas,oauth2 
from .. database import get_db

router = APIRouter(
    prefix ='/post',
    tags =['Posts']
)

@router.get("/",response_model =List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db),current_user:int=Depends(oauth2.get_current_user),limit:int=10,skip:int=0,search: Optional[str]=""):

    # cursor.execute("""select * from posts """)
    # posts = cursor.fetchall()

    # post = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    post = db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(
        models.Vote,models.Vote.post_id==models.Post.id,isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()


    return post   

    

#user_id:int=Depends(oauth2.get_current_user) this is used for jwt token validation
#
#
#
#
@router.post("/",status_code = 201,response_model =schemas.Post)
def create_posts(post:schemas.PostCreate,db: Session = Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    # cursor.execute("""INSERT into posts (title, content, published) VALUES (%s,%s,%s) RETURNING * """,
    #                (post.title,post.content,post.published))
    # new_post = cursor.fetchone()
    # conn.commit()

    print(current_user.email)
    new_post= models.Post(owner_id=current_user.id,**post.dict())
    db.add(new_post)
    db.commit() 
    db.refresh(new_post)

    return new_post    

@router.get("/{id}",response_model =schemas.PostOut)
def get_post(id:int,db: Session = Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
   
    #  cursor.execute(""" SELECT * FROM posts WHERE id = (%s)  """,(str(id)))
    #  posts = cursor.fetchone()

    #  insted of first if you use all you get list 
     posts = db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(
        models.Vote,models.Vote.post_id==models.Post.id,isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()

     if not posts:
      raise HTTPException(status_code=404, detail="Item not found.")
     
    
    


     return posts 

@router.delete("/{id}",status_code =204)
def delete_post(id:int,db: Session = Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    # cursor.execute(""" DELETE FROM posts WHERE id = (%s)  returning *""",(str(id)))
    # deleted_posts = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post == None:
      raise HTTPException(status_code=404, detail="Item not found.")
    

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Not allowed")
    
    post_query.delete(synchronize_session =False)
    db.commit()

    return Response(status_code=204)


@router.put("/{id}",response_model =schemas.Post)
def update_post(id:int,updated_post:schemas.PostCreate,db: Session = Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    #   cursor.execute(""" UPDATE posts SET title = %s ,content = %s,published = %s WHERE id = %s RETURNING *""",(post.title,post.content,post.published,str(id)))
    #   updated_post = cursor.fetchall()
    #   conn.commit()


      post_query = db.query(models.Post).filter(models.Post.id == id)
      post = post_query.first()

      if post == []:
         raise HTTPException(status_code=404, detail="Item not found.")
      
      if post.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Not allowed")
      
      post_query.update(updated_post.dict(),synchronize_session =False)
      db.commit()
       
      return post_query.first() 



# users apis