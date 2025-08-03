from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..database import get_db
from ..security.rate_limit import limiter, RateLimits
from ..security.password_validator import password_validator

router = APIRouter(
    prefix="/users",
    tags=["users"],
)

@router.post("/", response_model=schemas.User)
@limiter.limit(RateLimits.AUTH_STRICT)
def create_user(request: Request, user: schemas.UserCreate, db: Session = Depends(get_db)):
    # パスワード強度チェック
    password_validator.validate_or_raise(user.password)
    
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)
