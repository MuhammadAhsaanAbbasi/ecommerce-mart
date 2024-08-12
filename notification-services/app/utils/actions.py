from ..core.config import send_email_via_ses
from datetime import datetime, timedelta
from ..schemas.order_emails import order_schema
from ..schemas.product_email import product_schema
from .date import today_date
import numpy as np

# Generate Otp
def generate_otp():
    """
    Generate a random OTP using numpy.
    """
    return ''.join(np.random.choice([str(i) for i in range(10)], size=6))