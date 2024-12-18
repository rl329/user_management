import smtplib
from email.mime.text import MIMEText

# Email details
sender = "your_email@example.com"
recipient = "recipient@example.com"
subject = "Test Email from Python"
body = "This is a test email sent from Python."

# Create the email
msg = MIMEText(body)
msg["Subject"] = subject
msg["From"] = sender
msg["To"] = recipient

# SMTP Server Configuration (Mailtrap example)
smtp_server = "sandbox.smtp.mailtrap.io"
smtp_port = 2525
username = "f861aa274666e4"
password = "c75889b1328989"

try:
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(username, password)
        server.sendmail(sender, [recipient], msg.as_string())
        print("Email sent successfully!")
except Exception as e:
    print(f"Error: {e}")
