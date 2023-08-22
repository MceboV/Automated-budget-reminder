from datetime import datetime
import pandas
import smtplib

MY_EMAIL = "cebovilaz@gmail.com"
MY_PASSWORD = "riosvwlomaydvxhi"

today = datetime.now()
today_tuple = (today.month, today.day)

data = pandas.read_csv("clients_info.csv")
information_dict = {(data_row["month"], data_row["day"]): data_row for (index, data_row) in data.iterrows()}
if today_tuple in information_dict:
    budget_person = information_dict[today_tuple]
    file_path = f"email_template/email_reminder.txt"
    with open(file_path) as email_file:
        contents = email_file.read()
        contents = contents.replace("[NAME]", budget_person["name"])

    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(MY_EMAIL, MY_PASSWORD)
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs=budget_person["email"],
            msg=f"Subject:Budget Reminder!\n\n{contents}"
        )
