from fastapi import APIRouter,UploadFile,File,Depends,HTTPException,Query,BackgroundTasks
from fastapi.responses import JSONResponse
from sqlmodel import Session
from app.core.database import get_session
from app.services.catalog_service import process_csv_stream
from app.repositories.product_repo import ProductRepository

router=APIRouter()

@router.post("/upload")
async def upload(file:UploadFile=File(...),session:Session=Depends(get_session)):
    if file.content_type not in("text/csv","application/vnd.ms-excel","text/plain"):
        raise HTTPException(status_code=400,detail="Invalid file type, must be CSV")
    result=process_csv_stream(file.file,session)
    return JSONResponse(result)

@router.get("/products")
def list_products(page:int=Query(1,ge=1),limit:int=Query(20,ge=1,le=200),session:Session=Depends(get_session)):
    repo=ProductRepository(session)
    return repo.list_products(page=page,limit=limit)

@router.get("/products/search")
def search_products(brand:str=None,color:str=None,minPrice:float=None,maxPrice:float=None,page:int=Query(1,ge=1),limit:int=Query(20,ge=1,le=200),session:Session=Depends(get_session)):
    repo=ProductRepository(session)
    return repo.search(brand=brand,color=color,min_price=minPrice,max_price=maxPrice,page=page,limit=limit)
