from ..utils.date import today_date

def verified_user_schema(user_name:str):
    verified_notification_schema = f"""
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
                </head>
                <body
                    style="
                    margin: 0;
                    font-family: 'Poppins', sans-serif;
                    background: #ffffff;
                    font-size: 14px;
                    "
                >
                    <div
                    style="
                        max-width: 680px;
                        margin: 0 auto;
                        padding: 45px 30px 60px;
                        background: #f4f7ff;
                        background-image: url('https://hrk-boutique.s3.ap-south-1.amazonaws.com/emailTemplate/pawel-czerwinski-a7rDND-ns0M-unsplash.jpg'); /* Update URL to a direct link */
                        background-repeat: no-repeat;
                        background-size: 800px 452px;
                        background-position: top center;
                        font-size: 14px;
                    "
                    >
                    <header>
                        <table style="width: 100%;">
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
                                <span
                                style="font-size: 16px; line-height: 30px; color: #000000;"
                                >{today_date}</span
                                >
                            </td>
                            </tr>
                        </tbody>
                        </table>
                    </header>

                    <main>
                        <div
                        style="
                            margin: 0;
                            margin-top: 70px;
                            padding: 92px 30px 115px;
                            background: #ffffff;
                            border-radius: 30px;
                            text-align: center;
                        "
                        >
                            <div style="width: 100%; max-width: 489px; margin: 0 auto;">
                            <img
                                alt=""
                                src="https://hrk-boutique.s3.ap-south-1.amazonaws.com/emailTemplate/check.png"
                                height="90px"
                                />
                            <h1
                                style="
                                margin: 0;
                                font-size: 24px;
                                font-weight: 500;
                                color: #1f1f1f;
                            "
                            >
                            Hey {user_name}
                            </h1>
                            <p
                                style="
                                margin: 0;
                                margin-top: 17px;
                                font-weight: 500;
                                letter-spacing: 0.56px;
                            "
                            >
                                Congratulations on successfully verifying your email address. 
                                <span style="font-weight: 600; color: #1f1f1f;">Thank you for being a part of our community!</span>.
                                We are thrilled to have you with us!
                            </p>
                            </div>
                        </div>

                        <p
                            style="
                            max-width: 400px;
                            margin: 0 auto;
                            margin-top: 90px;
                            text-align: center;
                            font-weight: 500;
                            color: #8c8c8c;
                        "
                        >
                            Need help? Ask at
                            <a
                            href="mailto:hrkBoutique@hotmail.com"
                            style="color: #499fb6; text-decoration: none;"
                            >hrkBoutique@hotmail.com</a
                            >
                            or visit our
                            <a
                            href=""
                            target="_blank"
                            style="color: #499fb6; text-decoration: none;"
                            >Help Center</a
                        >
                        </p>
                    </main>

                    <footer
                        style="
                            width: 100%;
                            max-width: 490px;
                            margin: 20px auto 0;
                            text-align: center;
                            border-top: 1px solid #e6ebf1;
                        "
                        >
                        <p
                            style="
                            margin: 0;
                            margin-top: 40px;
                            font-size: 16px;
                            font-weight: 600;
                            color: #434343;
                        "
                        >
                            HRK Boutique
                        </p>
                        <p style="margin: 0; margin-top: 8px; color: #434343;">
                            Address 540, City, State.
                        </p>
                        <div style="margin: 0; margin-top: 16px;">
                            <a href="" target="_blank" style="display: inline-block;">
                            <img
                                width="36px"
                                alt="Facebook"
                                src="https://archisketch-resources.s3.ap-northeast-2.amazonaws.com/vrstyler/1661502815169_682499/email-template-icon-facebook"
                            />
                            </a>
                            <a
                            href=""
                            target="_blank"
                            style="display: inline-block; margin-left: 8px;"
                        >
                            <img
                                width="36px"
                                alt="Instagram"
                                src="https://archisketch-resources.s3.ap-northeast-2.amazonaws.com/vrstyler/1661504218208_684135/email-template-icon-instagram"
                            /></a>
                            <a
                            href=""
                            target="_blank"
                            style="display: inline-block; margin-left: 8px;"
                        >
                            <img
                                width="36px"
                                alt="Twitter"
                                src="https://archisketch-resources.s3.ap-northeast-2.amazonaws.com/vrstyler/1661503043040_372004/email-template-icon-twitter"
                            />
                            </a>
                            <a
                            href=""
                            target="_blank"
                            style="display: inline-block; margin-left: 8px;"
                            >
                            <img
                                width="36px"
                                alt="Youtube"
                                src="https://archisketch-resources.s3.ap-northeast-2.amazonaws.com/vrstyler/1661503195931_210869/email-template-icon-youtube"
                            /></a>
                        </div>
                        <p style="margin: 0; margin-top: 16px; color: #434343;">
                            Copyright © 2024 Company. All rights reserved.
                        </p>
                        </footer>
                    </div>
                    </body>
                </html>
        """
    return verified_notification_schema


# ============================================================================================================

# update_user_schema
def update_user_schema(user_name:str):
    schema = f"""
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
                </head>
                <body
                    style="
                    margin: 0;
                    font-family: 'Poppins', sans-serif;
                    background: #ffffff;
                    font-size: 14px;
                    "
                >
                    <div
                    style="
                        max-width: 680px;
                        margin: 0 auto;
                        padding: 45px 30px 60px;
                        background: #f4f7ff;
                        background-image: url('https://hrk-boutique.s3.ap-south-1.amazonaws.com/emailTemplate/pawel-czerwinski-a7rDND-ns0M-unsplash.jpg'); /* Update URL to a direct link */
                        background-repeat: no-repeat;
                        background-size: 800px 452px;
                        background-position: top center;
                        font-size: 14px;
                    "
                    >
                    <header>
                        <table style="width: 100%;">
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
                                <span
                                style="font-size: 16px; line-height: 30px; color: #000000;"
                                >{today_date}</span
                                >
                            </td>
                            </tr>
                        </tbody>
                        </table>
                    </header>

                    <main>
                        <div
                        style="
                            margin: 0;
                            margin-top: 70px;
                            padding: 92px 30px 115px;
                            background: #ffffff;
                            border-radius: 30px;
                            text-align: center;
                        "
                        >
                            <div style="width: 100%; max-width: 489px; margin: 0 auto;">
                            <img
                                alt=""
                                src="https://hrk-boutique.s3.ap-south-1.amazonaws.com/emailTemplate/updated.png"
                                height="90px"
                                />
                            <h1
                                style="
                                margin: 0;
                                font-size: 24px;
                                font-weight: 500;
                                color: #1f1f1f;
                            "
                            >
                            Hey {user_name}
                            </h1>
                            <p
                                style="
                                margin: 0;
                                margin-top: 17px;
                                font-weight: 500;
                                letter-spacing: 0.56px;
                            "
                            >
                                Your account details have been successfully updated.  
                                <span style="font-weight: 600; color: #1f1f1f;">If you did not make this change,</span>.
                                please contact our support team immediately.
                            </p>
                            </div>
                        </div>

                        <p
                            style="
                            max-width: 400px;
                            margin: 0 auto;
                            margin-top: 90px;
                            text-align: center;
                            font-weight: 500;
                            color: #8c8c8c;
                        "
                        >
                            Need help? Ask at
                            <a
                            href="mailto:hrkBoutique@hotmail.com"
                            style="color: #499fb6; text-decoration: none;"
                            >hrkBoutique@hotmail.com</a
                            >
                            or visit our
                            <a
                            href=""
                            target="_blank"
                            style="color: #499fb6; text-decoration: none;"
                            >Help Center</a
                        >
                        </p>
                    </main>

                    <footer
                        style="
                            width: 100%;
                            max-width: 490px;
                            margin: 20px auto 0;
                            text-align: center;
                            border-top: 1px solid #e6ebf1;
                        "
                        >
                        <p
                            style="
                            margin: 0;
                            margin-top: 40px;
                            font-size: 16px;
                            font-weight: 600;
                            color: #434343;
                        "
                        >
                            HRK Boutique
                        </p>
                        <p style="margin: 0; margin-top: 8px; color: #434343;">
                            Address 540, City, State.
                        </p>
                        <div style="margin: 0; margin-top: 16px;">
                            <a href="" target="_blank" style="display: inline-block;">
                            <img
                                width="36px"
                                alt="Facebook"
                                src="https://archisketch-resources.s3.ap-northeast-2.amazonaws.com/vrstyler/1661502815169_682499/email-template-icon-facebook"
                            />
                            </a>
                            <a
                            href=""
                            target="_blank"
                            style="display: inline-block; margin-left: 8px;"
                        >
                            <img
                                width="36px"
                                alt="Instagram"
                                src="https://archisketch-resources.s3.ap-northeast-2.amazonaws.com/vrstyler/1661504218208_684135/email-template-icon-instagram"
                            /></a>
                            <a
                            href=""
                            target="_blank"
                            style="display: inline-block; margin-left: 8px;"
                        >
                            <img
                                width="36px"
                                alt="Twitter"
                                src="https://archisketch-resources.s3.ap-northeast-2.amazonaws.com/vrstyler/1661503043040_372004/email-template-icon-twitter"
                            />
                            </a>
                            <a
                            href=""
                            target="_blank"
                            style="display: inline-block; margin-left: 8px;"
                            >
                            <img
                                width="36px"
                                alt="Youtube"
                                src="https://archisketch-resources.s3.ap-northeast-2.amazonaws.com/vrstyler/1661503195931_210869/email-template-icon-youtube"
                            /></a>
                        </div>
                        <p style="margin: 0; margin-top: 16px; color: #434343;">
                            Copyright © 2024 Company. All rights reserved.
                        </p>
                        </footer>
                    </div>
                    </body>
                </html>
    """
    return schema

# ============================================================================================================