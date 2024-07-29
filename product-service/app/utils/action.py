from ..model.models import Color, Product, ProductSize, ProductItem, Stock, ProductDetails, ProductItemDetails, SizeModelDetails, Review, ReviewModel, ProductReviewsDetails, UserReviewsDetails
from ..model.category_model import Category, Size, CategoryBaseModel
from fastapi import HTTPException, UploadFile, File, Form, Depends
from ..utils.admin_verify import get_current_active_admin_user
from ..utils.user_verify import get_current_active_user
from typing import List, Sequence, Annotated, Optional
from ..core.config import upload_files_in_s3
from ..model.authentication import Admin, Users
from ..core.db import DB_SESSION
from sqlmodel import select

# Create Categories
async def create_categories(category_input: CategoryBaseModel,
                            current_admin: Annotated[Admin, Depends(get_current_active_admin_user)],
                            session: DB_SESSION,
                            image: UploadFile = File(...)):
    if not current_admin:
        raise HTTPException(status_code=401, detail="Unauthorized Admin")
    category_image = await upload_files_in_s3(image)
    category = Category(**category_input.model_dump(), category_image=category_image)
    session.add(category)
    session.commit()
    session.refresh(category)
    return category

# Get Categories
async def get_categories(session: DB_SESSION):
    categories = session.exec(select(Category)).all()
    return {"data" : categories}

async def update_categories(category_id: str, 
                        category_input: CategoryBaseModel,
                        current_admin: Annotated[Admin, Depends(get_current_active_admin_user)],
                        session: DB_SESSION,
                        image: Optional[UploadFile] = None,
                        ):
    if not current_admin:
        raise HTTPException(status_code=401, detail="Unauthorized Admin")

    category = session.exec(select(Category).where(Category.id == category_id)).first()
    if not category:
            raise HTTPException(status_code=404, detail="Category not found")

    if not image:        
        category_data = category_input.model_dump()
    else:
        category_image = await upload_files_in_s3(image)
        category_data = category_input.model_dump()
        category_data["category_image"] = category_image

    for field, value in category_data.items():
        setattr(category, field, value)
    
    session.commit()
    session.refresh(category)

    return {"message" : "Update Categories Successfully!"}

# Create Size
async def create_sizes(size_input: Size,
                        current_admin: Annotated[Admin, Depends(get_current_active_admin_user)],
                        session: DB_SESSION):
    if not current_admin:
        raise HTTPException(status_code=401, detail="Unauthorized Admin")
    size = Size(**size_input.model_dump())
    session.add(size)
    session.commit()
    session.refresh(size)
    return size

# Get Sizes
async def get_sizies(session: DB_SESSION):
    sizes = session.exec(select(Size)).all()
    return {"data" : sizes}

# Update Colors
async def update_color(color_id: str,
                        color_details: Color,
                        current_admin: Annotated[Admin, Depends(get_current_active_admin_user)],
                        session: DB_SESSION):
    if not current_admin:
        raise HTTPException(status_code=401, detail="Unauthorized Admin")
    
    color = session.exec(select(Color).where(Color.id == color_id)).first()
    if not color:
        raise HTTPException(status_code=404, detail="Invalid color id")
    
    for field, value in color_details.model_dump().items():
        setattr(color, field, value)

    session.commit()
    session.refresh(color)

    return {"message" : "Update Color Successfully!"}

# Search Algorithm By Category
async def search_algorithm_by_category(input: str, session: DB_SESSION):
    """Search for categories that start with the given input."""
    categories = session.exec(select(Category).where(Category.category_name.startswith(input))).all()
    return categories

async def search_algorithm_by_category_type(product_id: str, session: DB_SESSION):
    product = session.exec(select(Product).where(Product.id == product_id)).first()
    
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    category = session.exec(select(Category).where(Category.id == product.category_id)).first()
    
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    categories = session.exec(select(Category).where(Category.category_type == category.category_type)).all()
    return categories

async def all_product_details(products: Sequence[Product], session: DB_SESSION):
    all_product_detail = []

    for product in products:
        product_items = session.exec(select(ProductItem).where(ProductItem.product_id == product.id)).all()
        product_items_table: List[ProductItemDetails] = []

        for item in product_items:
            product_sizes = session.exec(select(ProductSize).where(ProductSize.product_item_id == item.id)).all()
            product_sizes_table: List[SizeModelDetails] = []

            for product_size in product_sizes:
                size = session.exec(select(Size).where(Size.id == product_size.size)).first()
                if not size:
                    raise HTTPException(status_code=404, detail="Size not found")
                stock = session.exec(select(Stock).where(Stock.product_size_id == product_size.id)).first()
                if stock and stock.stock > 0:
                    size_model = SizeModelDetails(
                        product_size_id=product_size.id,
                        size=size.size,
                        price=product_size.price,
                        stock=stock.stock
                    )
                    product_sizes_table.append(size_model)

            if product_sizes_table:
                color = session.exec(select(Color).where(Color.id == item.color)).first()
                if not color:
                    raise HTTPException(status_code=404, detail="Color not found")

                product_item_model = ProductItemDetails(
                    product_item_id=item.id,
                    color_name=color.color_name,
                    color_value=color.color_value,
                    color=item.color,
                    image_url=item.image_url,
                    sizes=product_sizes_table
                )
                product_items_table.append(product_item_model)

        product_details = ProductDetails(
            product_id=product.id,
            product_name=product.product_name,
            product_desc=product.product_desc,
            featured=product.featured,
            category_id=product.category_id,
            product_item=product_items_table
        )
        all_product_detail.append(product_details)

    return all_product_detail


# Create Review function
async def create_review(review_details: ReviewModel,
                        session: DB_SESSION,
                        current_user: Annotated[Users, Depends(get_current_active_user)]
                        ):
    review = session.exec(select(Review).where(Review.user_id == current_user.id).where(Review.product_id == review_details.product_id)).one_or_none()
    if review is None:
        new_review = Review(**review_details.model_dump(), user_id=current_user.id)
        session.add(new_review)
        session.commit()
        session.refresh(new_review)
        return new_review.model_dump()
    else:
        raise HTTPException(status_code=400, detail="User already reviewed this product")


# Get Product Reviews
async def get_product_reviews_details(product_id: str, session: DB_SESSION):
    reviews = session.exec(select(Review).where(Review.product_id == product_id)).all()

    reviews_details: List[ProductReviewsDetails] = []

    for review in reviews:
        user = session.exec(select(Users).where(Users.id == review.user_id)).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        review_details = ProductReviewsDetails(
            review_id=review.id,
            rating=review.rating,
            review=review.review,
            username=user.username,
            email=user.email,
            imageUrl=user.imageUrl
        )
        reviews_details.append(review_details)
    
    return reviews_details

# User Reviews Details
async def get_user_reviews_details(session: DB_SESSION, 
                                current_user: Annotated[Users, Depends(get_current_active_user)]):
    reviews = session.exec(select(Review).where(Review.user_id == current_user.id)).all()

    reviews_details: List[UserReviewsDetails] = []

    for review in reviews:
        product = session.exec(select(Product).where(Product.id == review.product_id)).first()
        if not product:
            raise HTTPException(status_code=404, detail="User not found")
        
        review_details = UserReviewsDetails(
            review_id=review.id,
            rating=review.rating,
            review=review.review,
            product_id=product.id,
            product_name=product.product_name
        )
        reviews_details.append(review_details)
    
    return reviews_details