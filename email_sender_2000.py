"""
    Python function used to send bulk emails with HTML content
    and pdf attachment. All using Gmail SMPT servers

    Author: https://github.com/doxxedd
    Date:   Feb 9, 2022
"""
import ssl
import smtplib
from email import encoders
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase


def email_sender_2000(sender_email, sender_email_pwd, target_email,
                      html_content, text_content):
    """Email sender function
    NOTE: "LESS SECURE APPS" MUST BE TURNED ON IN GMAIL SETTINGS
    https://support.google.com/accounts/answer/6010255?hl=en#zippy=

    :param sender_email: String, email(s) are sent from this address
    :param sender_email_pwd: String
    :param target_email: String, email(s) are being sent to this address
    :param html_content: String
    :param text_content: String, in case HTML can't be rendered on receiver end
    """

    # Credentials entered
    print(f'\n{sender_email=}')
    print(f'{sender_email_pwd=}')
    print(f'{target_email=}')

    smpt_server = "smtp.gmail.com"

    message = MIMEMultipart("alternative")
    message["Subject"] = "<enter email subject here>"
    message["From"] = sender_email
    message["To"] = target_email
    message["Bcc"] = target_email

    # Turning our content to MIMEText objects
    plain_text_obj = MIMEText(text_content, "plain")
    html_obj = MIMEText(html_content, "html")

    # Attaching both pieces of content to MIMEMultipart message
    # The receiver client will try to render in the HTML first
    message.attach(plain_text_obj)
    message.attach(html_obj)

    # PDF attaching. If you don't need pdf attaching, comment this section out
    attachment = "pdf_name.pdf"  # Must be in the same directory as this script
    binary_pdf = open(attachment, 'rb')
    part = MIMEBase('application', 'octet-stream', Name=attachment)
    part.set_payload(binary_pdf.read())

    encoders.encode_base64(part)  # Encoding the binary_pdf to base64
    part.add_header('Content-Decomposition', 'attachment', filename=attachment)
    message.attach(part)
    # PDF attaching ends here

    context = ssl.create_default_context()  # Creating SSL context

    # Sending the email after logging in to smpt_server
    try:
        server = smtplib.SMTP(smpt_server, 587)
        server.ehlo()
        # Notifies smpt_server to encrypt content
        server.starttls(context=context)
        server.ehlo()
        server.login(sender_email, sender_email_pwd)
        server.sendmail(sender_email, target_email, message.as_string())
        server.quit()
        print("\nEmail(s) sent successfully!")
    except Exception as error:
        print(f'{error}\n\n Sending the email failed successfully.')


def main():
    sender_email = "<Your sender email here>"
    sender_email_pwd = "<Your sender email password>"
    target_email = "<Your receiver email here>"

    # Sample Content
    text_content = """\
    Yo what up dawg. Welcome to email_sender_2000.
    Your boys gitty is down here:
    https://github.com/doxxedd
    """
    html_content = """\
    <html>
      <body>
        <p>
            Yo,<br>
            What up dawg? Welcome to email_sender_2000<br>
            Checkout yo boy <a href="https://github.com/doxxedd"> here</a><br>
            Thanks fam no kizzy on a stack fr.<br>
            Sent using email_sender_2000
        </p>
      </body>
    </html>
    """

    email_sender_2000(sender_email, sender_email_pwd, target_email,
                      html_content, text_content)


if __name__ == '__main__':
    main()
