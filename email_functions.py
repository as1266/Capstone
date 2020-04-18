import email, smtplib, ssl

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

def SendEmail(customer_email, file_name, unlock_code):
    unlock_code = str(unlock_code)
    subject = "SRS Distribution Order Confirmation"
    body = "Your order is ready for pick up.\n Enter the code or scan the qr code at the pickup location.\n" + unlock_code
    sender_email = "srs.locker@gmail.com"
    receiver_email = customer_email
    password = "Yo moms a hoe1"

    # Create a multipart message and set headers
    message = MIMEMultipart('related')
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    #message["Bcc"] = receiver_email  # Recommended for mass emails

    # Add body to email
    message.attach(MIMEText(body, "plain"))

    filename = str(file_name)+".png"  # In same directory as script

    # Record the MIME types.
    #msgHtml = MIMEText(html, 'html')

    img = open(file_name, 'rb').read()
    msgImg = MIMEImage(img, 'png')
    msgImg.add_header('Content-ID', '<image1>')
    msgImg.add_header('Content-Disposition', 'inline', filename=file_name)
    #img.close()

    message.attach(msgImg)

    text = message.as_string()

    # Log in to server using secure context and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, text)
