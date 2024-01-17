from flask_mail import Message
from app.models.transaction import Transaction
from app.repos.user_repo import UserRepo
from app.extensions import mail
from app.models.user import User
import os 

class MailService:
  def __init__(self) -> None:
    pass

  def send_mail_transaction(t:Transaction)->bool:
    sender=UserRepo.get_user_by_id(t.sender_id)
    if not sender:
      return False
    msg=Message()
    msg.recipients.append(t.recipient_email)
    msg.recipients.append(sender.email)
    msg.subject=f"Transaction {t.id} completed."
    html_content="""
    <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Transaction Completed</title>
    <style>
        /* Add your custom styles here */
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f4;
            color: #333;
            padding: 20px;
        }

        .container {
            max-width: 600px;
            margin: 0 auto;
            background-color: #fff;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }

        h1 {
            color: #007BFF;
        }

        p {
            margin-bottom: 20px;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }

        th, td {
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }

        th {
            background-color: #007BFF;
            color: white;
        }

        .footer {
            text-align: center;
            margin-top: 20px;
            color: #777;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Transaction Completed</h1>
        <p>Hello dear customer,</p>
        <p>We are pleased to inform you that your transaction with ID <strong>{ transaction_id }</strong> has been successfully completed.</p>
        <h2>Transaction</h2>
        <table>
            <tr>
                <th>Field</th>
                <th>Value</th>
            </tr>
            <tr>
                <td>Transaction ID</td>
                <td>{ transaction_id }</td>
            </tr>
            <tr>
                <td>Sender ID</td>
                <td>{ sender_id }</td>
            </tr>
            <tr>
                <td>Sender Card Number</td>
                <td>{ sender_card_number }</td>
            </tr>
            <tr>
                <td>Currency</td>
                <td>{ currency }</td>
            </tr>
            <tr>
                <td>Amount</td>
                <td>{ amount }</td>
            </tr>
            <tr>
              <td>Recipient mail</td>
              <td>{ recipient_mail }</td>
            </tr>

        </table>

        <p>Thank you for choosing our service. If you have any questions or concerns, please feel free to contact our support team.</p>
        <div class="footer">
            <p>Best Regards,<br>Your bank</p>
        </div>
    </div>
</body>
</html>
    """.format(transaction_id=t.id, sender_id=t.sender_id, sender_card_number=t.sender_card_number, currency=t.currency, amount=t.amount, recipient_mail=t.recipient_email)

    # Set the HTML content directly
    msg.html = html_content

    # Send the email
    mail.send(msg)
    return True

  def send_mail_register(u:User)->bool:
    if not u:
      return False
    msg=Message()
    msg.recipients.append(u.email)
    msg.subject=f"Your registration is complete."
    html_content="""
    <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Welcome to our bank</title>
    <style>
        /* Add your custom styles here */
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f4;
            color: #333;
            padding: 20px;
        }

        .container {
            max-width: 600px;
            margin: 0 auto;
            background-color: #fff;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }

        h1 {
            color: #007BFF;
        }

        p {
            margin-bottom: 20px;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }

        th, td {
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }

        th {
            background-color: #007BFF;
            color: white;
        }

        .footer {
            text-align: center;
            margin-top: 20px;
            color: #777;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Welcome to our bank</h1>
        <p>Hello,</p>
        <p>Your account has been successfully registered. Below are your login details:</p>

        <table>
            <tr>
                <th>Field</th>
                <th>Value</th>
            </tr>
            <tr>
                <td>Email</td>
                <td>{ user_email }</td>
            </tr>
            <tr>
                <td>Password</td>
                <td>{ user_password }</td>
            </tr>
        </table>

        <p>Make sure to keep your login details secure. You can now log in to our website using the provided credentials.</p>

        <p>Thank you for joining us. If you have any questions or need assistance, please feel free to contact our support team.</p>
        
        <div class="footer">
            <p>Best Regards,<br>Your bank</p>
        </div>
    </div>
</body>
</html>
    """.format(user_email=u.email, user_password=u.password)
    # Set the HTML content directly
    msg.html = html_content

    # Send the email
    mail.send(msg)
    return True

  def send_mail_verification(u:User)->bool:
    if not u:
      return False
    msg=Message()
    msg.recipients.append(u.email)
    msg.subject=f"Your account is verified."
    html_content="""
    <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Account Verification Successful</title>
    <style>
        /* Add your custom styles here */
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f4;
            color: #333;
            padding: 20px;
        }

        .container {
            max-width: 600px;
            margin: 0 auto;
            background-color: #fff;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }

        h1 {
            color: #28a745; /* Green color */
        }

        p {
            margin-bottom: 20px;
        }

        .footer {
            text-align: center;
            margin-top: 20px;
            color: #777;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Account Verification Successful</h1>
        <p>Hello,</p>
        <p>Your account has been successfully verified. You can now log in and access all the features of our website.</p>
        <p>Thank you for verifying your account. If you have any questions or need assistance, please feel free to contact our support team.</p>
        <div class="footer">
            <p>Best Regards,<br>Your bank</p>
        </div>
    </div>
</body>
</html>
    """
    # Set the HTML content directly
    msg.html = html_content

    # Send the email
    mail.send(msg)
    return True