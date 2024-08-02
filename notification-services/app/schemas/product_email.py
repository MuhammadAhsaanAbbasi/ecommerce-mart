from ..utils.date import today_date

def product_schema(product_name: str, product_description: str, product_price: int, product_image: str):
    product_created_schema = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <meta http-equiv="X-UA-Compatible" content="ie=edge" />
    <title>Static Template</title>
    <link
        href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600&display=swap"
        rel="stylesheet"
    />
    <style>
        * {{
            box-sizing: border-box;
        }}
        body {{
            margin: 0;
            font-family: 'Poppins', sans-serif;
            background: #ffffff;
            font-size: 14px;
        }}
        .container {{
            max-width: 800px;
            margin: 0 auto;
            padding: 45px 30px 60px;
            background: #f4f7ff;
            background-image: url('https://hrk-boutique.s3.ap-south-1.amazonaws.com/emailTemplate/pawel-czerwinski-a7rDND-ns0M-unsplash.jpg');
            background-repeat: no-repeat;
            background-size: cover;
            background-position: top center;
            font-size: 14px;
        }}
        .header_table {{
            width: 100%;
        }}
        .main_content {{
            margin-top: 70px;
            padding: 20px;
            background: #ffffff;
            border-radius: 30px;
            text-align: center;
        }}
        .product_container {{
            display: flex;
            flex-direction: row;
            align-items: center;
            justify-content: center;
            gap: 10px;
            padding: 10px;
        }}
        .product_container img {{
            width: 200px;
            height: auto;
            border-radius: 10px;
        }}
        .product_details {{
            text-align: left;
            padding: 20px;
            gap: 10px;
        }}
        .product_details h2 {{
            font-size: 25px;
            font-weight: 600;
        }}
        .product_details p {{
            font-size: 20px;
            font-weight: 400;
        }}
        .v_button {{
            background-color: #2196F3;
            color: #fff;
            padding: 10px 20px;
            text-decoration: none;
            border-radius: 4px;
            display: inline-block;
            margin-top: 10px;
        }}
        .footer {{
            width: 100%;
            max-width: 490px;
            margin: 20px auto 0;
            text-align: center;
            border-top: 1px solid #e6ebf1;
        }}
        .footer img {{
            width: 36px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <table class="header_table"> 
                <tbody>
                    <tr style="height: 0;">
                        <td>
                            <img
                                alt=""
                                src="https://archisketch-resources.s3.ap-northeast-2.amazonaws.com/vrstyler/1663574980688_114990/archisketch-logo"
                                height="30px"
                            />
                        </td>
                        <td style="text-align: right;">
                            <span style="font-size: 16px; line-height: 30px; color: #000000;">
                                {today_date}
                            </span>
                        </td>
                    </tr>
                </tbody>
            </table>
        </header>
        <main>
            <div class="main_content">
                <h1 style="font-size: 40px; font-weight: 600; color: Black;">New Arrival</h1>
                <div class="product_container">
                    <img src={product_image} alt="Product" title="Product"/>
                    <div class="product_details display: flex; flex-direction: column; align-items: flex-start; text-align: left; width: 100%;">
                        <h2>{product_name}</h2>
                        <p>{product_description}</p>
                        <p>{product_price}</p>
                        <div>
                            <a href="https://hrk-boutique.com/products/" target="_blank" class="v_button">
                                <span><strong>Quick view</strong></span>
                            </a>
                        </div>
                    </div>
                </div>
                <div class="grid-container">
                    <div class="grid-item">
                        <img src="https://hrk-boutique.s3.ap-south-1.amazonaws.com/emailTemplate/image-17.png" alt="Icon" title="Icon"/>
                        <h4><strong>FREE SHIPPING</strong></h4>
                        <p>on order over $150.00</p>
                    </div>
                    <div class="grid-item">
                        <img src="https://hrk-boutique.s3.ap-south-1.amazonaws.com/emailTemplate/image-7.png" alt="Icon" title="Icon"/>
                        <h4><strong>FREE RETURNS</strong></h4>
                        <p>free 90 days return</p>
                    </div>
                    <div class="grid-item">
                        <img src="https://hrk-boutique.s3.ap-south-1.amazonaws.com/emailTemplate/image-6.png" alt="Icon" title="Icon"/>
                        <h4><strong>MEMBER DISCOUNT</strong></h4>
                        <p>free register</p>
                    </div>
                </div>
                <p style="max-width: 400px; margin: 0 auto; margin-top: 50px; text-align: center; font-weight: 500; color: #8c8c8c;">
                    Need help? Ask at
                    <a href="mailto:hrkBoutique@hotmail.com" style="color: #499fb6; text-decoration: none;">hrkBoutique@hotmail.com</a>
                    or visit our
                    <a href="" target="_blank" style="color: #499fb6; text-decoration: none;">Help Center</a>
                </p>
            </div>
        </main>
        <footer class="footer">
            <p style="margin: 0; margin-top: 40px; font-size: 16px; font-weight: 600; color: #434343;">
                HRK Boutique
            </p>
            <p style="margin: 0; margin-top: 8px; color: #434343;">
                Address 540, City, State.
            </p>
            <div style="margin: 0; margin-top: 16px;">
                <a href="" target="_blank" style="display: inline-block;">
                    <img alt="Facebook" src="https://archisketch-resources.s3.ap-northeast-2.amazonaws.com/vrstyler/1661502815169_682499/email-template-icon-facebook"/>
                </a>
                <a href="" target="_blank" style="display: inline-block; margin-left: 8px;">
                    <img alt="Instagram" src="https://archisketch-resources.s3.ap-northeast-2.amazonaws.com/vrstyler/1661504218208_684135/email-template-icon-instagram"/>
                </a>
                <a href="" target="_blank" style="display: inline-block; margin-left: 8px;">
                    <img alt="Twitter" src="https://archisketch-resources.s3.ap-northeast-2.amazonaws.com/vrstyler/1661503043040_372004/email-template-icon-twitter"/>
                </a>
                <a href="" target="_blank" style="display: inline-block; margin-left: 8px;">
                    <img alt="Youtube" src="https://archisketch-resources.s3.ap-northeast-2.amazonaws.com/vrstyler/1661503195931_210869/email-template-icon-youtube"/>
                </a>
            </div>
            <p style="margin: 0; margin-top: 16px; color: #434343;">
                Copyright © 2024 Company. All rights reserved.
            </p>
        </footer>
    </div>
</body>
</html>
"""


# ============================================================================================================

# update_product_item_size_schema


# ============================================================================================================