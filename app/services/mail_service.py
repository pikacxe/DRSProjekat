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
    # Read the HTML content from a file
    with open('transaction_complete.html') as template_file:
        html_content = template_file.read().decode('utf-8')

    # Replace placeholders with actual values
    html_content = html_content.format(transaction_id=t.id)

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
    # Read the HTML content from a file
    with open('user_registered.html') as template_file:
        html_content = template_file.read().decode('utf-8')

    # Replace placeholders with actual values
    html_content = html_content.format(user_email=u.email, user_password=u.password)

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
    # Read the HTML content from a file
    with open('verify_user.html') as template_file:
        html_content = template_file.read().decode('utf-8')
    # Set the HTML content directly
    msg.html = html_content

    # Send the email
    mail.send(msg)
    return True