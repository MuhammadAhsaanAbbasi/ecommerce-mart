from ..utils.date import today_date

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
        .header-table {{
            width: 100%;
        }}
        .main-content {{
            margin-top: 70px;
            padding: 20px;
            background: #ffffff;
            border-radius: 30px;
            text-align: center;
        }}
        .grid-container {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 10px;
            padding: 10px;
        }}
        .grid-item {{
            padding: 10px;
        }}
        .grid-item img {{
            width: 150px;
            height: auto;
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
        @media screen and (max-width: 768px) {{
            .grid-container {{
                grid-template-columns: repeat(2, 1fr);
            }}
        }}
        @media screen and (max-width: 480px) {{
            .grid-container {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <table class="header-table">
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
            <div class="main-content">
                <div class="grid-container">
                    <div class="grid-item">
                        <img align="center" border="0" src="https://hrk-boutique.s3.ap-south-1.amazonaws.com/emailTemplate/image-17.png" alt="Icon" title="Icon"/>
                        <h4><strong>FREE SHIPPING</strong></h4>
                        <p>on order over $150.00</p>
                    </div>
                    <div class="grid-item">
                        <img align="center" border="0" src="https://hrk-boutique.s3.ap-south-1.amazonaws.com/emailTemplate/image-7.png" alt="Icon" title="Icon"/>
                        <h4><strong>FREE RETURNS</strong></h4>
                        <p>free 90 days return</p>
                    </div>
                    <div class="grid-item">
                        <img align="center" border="0" src="https://hrk-boutique.s3.ap-south-1.amazonaws.com/emailTemplate/image-6.png" alt="Icon" title="Icon"/>
                        <h4><strong>MEMBER DISCOUNT</strong></h4>
                        <p>free register</p>
                    </div>
                </div>
                <h4><strong>FEATURED PRODUCTS</strong></h4>
                <div class="grid-container">
                    <div class="grid-item">
                        <img align="center" border="0" src="https://hrk-boutique.s3.ap-south-1.amazonaws.com/emailTemplate/image-20.jpeg" alt="Product" title="Product"/>
                        <h4><strong>Grouped Product</strong></h4>
                        <p>$500.00</p>
                        <div align="center">
                            <a href="https://unlayer.com/" target="_blank" class="v-button">
                                <span><strong>Quick view</strong></span>
                            </a>
                        </div>
                    </div>
                    <div class="grid-item">
                        <img align="center" border="0" src="https://hrk-boutique.s3.ap-south-1.amazonaws.com/emailTemplate/image-8.jpeg" alt="Product" title="Product"/>
                        <h4><strong>Premium Quality</strong></h4>
                        <p>$600.00</p>
                        <div align="center">
                            <a href="https://unlayer.com/" target="_blank" class="v-button">
                                <span><strong>Quick view</strong></span>
                            </a>
                        </div>
                    </div>
                    <div class="grid-item">
                        <img align="center" border="0" src="https://hrk-boutique.s3.ap-south-1.amazonaws.com/emailTemplate/image-13.jpeg" alt="Product" title="Product"/>
                        <h4><strong>Simple product</strong></h4>
                        <p>$450.00</p>
                        <div align="center">
                            <a href="https://unlayer.com/" target="_blank" class="v-button">
                                <span><strong>Quick view</strong></span>
                            </a>
                        </div>
                    </div>
                </div>
                <p style="max-width: 400px; margin: 0 auto; margin-top: 90px; text-align: center; font-weight: 500; color: #8c8c8c;">
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