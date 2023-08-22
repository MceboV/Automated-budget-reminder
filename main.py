from datetime import datetime
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Set your email and password here
MY_EMAIL = "cebovilaz@gmail.com"
MY_PASSWORD = "riosvwlomaydvxhi"


def get_today_tuple():
    today = datetime.now()
    return today.month, today.day


def read_client_info(file_path):
    data = pd.read_csv(file_path)
    return {(row["month"], row["day"]): row for _, row in data.iterrows()}


def read_email_template(template_path):
    with open(template_path, "r") as email_file:
        return email_file.read()


def send_email(subject, to_email, message):
    msg = MIMEMultipart()
    msg['From'] = MY_EMAIL
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))

    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(MY_EMAIL, MY_PASSWORD)
        connection.sendmail(MY_EMAIL, to_email, msg.as_string())


def main():
    today_tuple = get_today_tuple()

    client_info = read_client_info("clients_info.csv")
    if today_tuple in client_info:
        budget_person = client_info[today_tuple]
        template_contents = read_email_template("email_template/email_reminder.txt")
        message = template_contents.replace("[NAME]", budget_person["name"])

        subject = "Budget Reminder!"
        send_email(subject, budget_person["email"], message)


if __name__ == "__main__":
    main()
