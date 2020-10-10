import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pandas as pd


def sendmail(user, pwd, recipients, subject):
    try:
        df = pd.read_csv("output.csv")
        df_html = df.to_html()
        dfPart = MIMEText(df_html, "html")

        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = user
        msg["To1"] = recipients
        msg.attach(dfPart)

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(user, pwd)

        server.sendmail(user, recipients, msg.as_string())
        server.close()
        print("email sent")

    except Exception as e:
        print(str(e))
        print("Failed to send email;")
