from ..model.models import ProductFormModel, ProductDetails
from ..model.authentication import SubscribeEmail
from ..core.config import send_email_via_ses
from ..schemas.product_email import product_schema
from ..core.db import DB_SESSION
from sqlmodel import select

async def send_product_email(product_form: ProductFormModel, session: DB_SESSION):
    subscribe_email = session.exec(select(SubscribeEmail)).all()
    for email in subscribe_email:
        message = product_schema(product_name=product_form.product_name,
                                product_description=product_form.product_desc if product_form.product_desc else "",
                                product_price=product_form.product_item[0].sizes[0].price,
                                product_image=product_form.product_item[0].image_url if product_form.product_item[0].image_url  else ""
                                )
        await send_email_via_ses(email.email, message, subject="Product Details Notification")
