# type: ignore
from ..model.product import Product, ProductItem, ProductSize, Stock, SizeModel, ProductItemFormModel, ProductFormModel, Size
from ..model.order import Order, OrderItem, OrderItemDetail, OrderDetail
from openai.types.shared_params.function_definition import FunctionDefinition
from ..utils.admin_verify import get_current_active_admin_user
from ..utils.actions import all_product_details, single_product_details
from ..utils.user_verify import get_current_active_user
from fastapi import Depends, HTTPException, Query
from ..model.authentication import Users, Admin
from typing import Annotated, Optional, List, Sequence
from ..core.db import DB_SESSION
from openai.types.chat import ChatCompletionMessage
from ..setting import OPENAI_API_KEY
from datetime import datetime, timedelta
from dotenv import load_dotenv, find_dotenv
from sqlmodel import select
from openai import OpenAI
import json

_ = load_dotenv(find_dotenv())

client: OpenAI = OpenAI()

async def get_all_product_details(session: DB_SESSION):
    products = session.exec(select(Product)).all()

    product_details = await all_product_details(products, session)

    return product_details

async def get_features_product(session: DB_SESSION):
    # Get all features Product which create 14 days ago from now
    current_date = datetime.now()
    two_weeks_ago = current_date - timedelta(days=14)
    
    if not Product.created_at:
        raise HTTPException(status_code=400, detail="Products date not found")

    products = session.exec(
        select(Product)
        .where(Product.featured == True)
        .where(Product.created_at >= two_weeks_ago)
    ).all()

    if not products:
        raise HTTPException(status_code=404, detail="No featured products found")

    product_details = await all_product_details(products, session)
    return product_details

# Get Order By Id
async def get_orders_by_tracking_id(
                    session: DB_SESSION,
                    tracking_id: str,
                    ):
    order = session.exec(select(Order).where(Order.tracking_id == tracking_id)).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    try:
        order_items = session.exec(select(OrderItem).where(OrderItem.order_id == order.id)).all()
        order_items_detail = []

        for order_item in order_items:
            product = session.exec(select(Product).where(Product.id == order_item.product_id)).first()
            product_item = session.exec(select(ProductItem).where(ProductItem.id == order_item.product_item_id)).first()
            product_size = session.exec(select(ProductSize).where(ProductSize.id == order_item.product_size_id)).first()
            stock = session.exec(select(Stock).where(Stock.product_size_id == order_item.product_size_id)).first()

            if product and product_item and product_size and stock:
                size = session.exec(select(Size).where(Size.id == product_size.size)).first()
                if not size:
                    raise HTTPException(status_code=404, detail="Size not found")

                order_item_detail = OrderItemDetail(
                    product=product.product_name,
                    product_item={
                        'color': product_item.color,
                        'image_url': product_item.image_url
                    },
                    size=size.size,
                    price=product_size.price,
                    quantity=order_item.quantity,
                    stock=stock.stock,
                )
                order_items_detail.append(order_item_detail)

        order_detail = OrderDetail(
                order_id=order.id,
                order_address=order.order_address,
                phone_number=order.phone_number,
                order_payment=order.order_payment,
                total_price=order.total_price,
                order_status=order.order_status,
                tracking_id=order.tracking_id,
                delivery_date=order.delivery_date,
                order_date=order.order_date,
                order_items=order_items_detail
            )

        return order_detail
    except HTTPException as e:
        raise e


async def get_openai_shop_assistant(input: str, session: DB_SESSION):
    get_all_product_details_tool: FunctionDefinition = {
                "name": "single_product_details",
                "description": "Get all product details & Product Description",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "product" : {
                            "type": "string",
                            "description": "Product name just like Saree, Shalwar Kameez"
                        }
                    },
                    "required": []
                }
            }

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant design the JSON output that you’d like to convert into a more interactive and readable message?"},
            {"role": "user", "content": input}
        ],
    tools=[
        {"type": "function", "function": get_all_product_details_tool},
    ]
    )

    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls
    if tool_calls:
        available_functions = {
            "single_product_details": single_product_details,
        }
        messages = []
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_to_call = available_functions.get(function_name)
            messages.append(response_message)
            if function_to_call:
                function_args = json.loads(tool_call.function.arguments)
                product = function_args.get("product")
                function_response = await function_to_call(session=session, product_name=product)
                messages.append(
                    {
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": function_name,
                        "content": str(function_response),
                    }
                )
        second_response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
        )
        return second_response
    else:
        return response_message.content
