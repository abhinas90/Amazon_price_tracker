import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import pandas as pd


def sendmail(user, pwd, recipients, subject, df, outputfile):
    try:
        df = df
        df_html = df.to_html()
        dfPart = MIMEText(df_html, "html")

        msg = MIMEMultipart("alternative")
        msg["Subject"] = f'Scapared at {outputfile.replace(".csv","")}'

        msg["From"] = user
        msg["To"] = recipients
        msg.attach(dfPart)

        filename = outputfile
        attachment = open(filename, 'rb')
        part = MIMEBase('application', 'octet-stream')
        part.set_payload((attachment).read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition',
                        "attachment; filename= " + filename)
        msg.attach(part)
        text = msg.as_string()

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(user, pwd)

        server.sendmail(user, recipients, msg.as_string())
        server.quit()
        print("email sent")

    except Exception as e:
        print(str(e))
        print("Failed to send email;")
