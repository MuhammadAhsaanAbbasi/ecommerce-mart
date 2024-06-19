from fastapi import APIRouter

router = APIRouter()

@router.get("/create_product")
async def get_product():
    return {"message": "Get Product Details"}

# Additional routes...
