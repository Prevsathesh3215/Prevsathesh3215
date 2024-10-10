import smtplib
import get_emails


class NotificationManager:
    def __init__(self, data):
        print(data)
        self.__my_email = "shabadabadingdongprevin@gmail.com"
        self.__password = "lowx lxcx wacg kmgq"
        text = f"Subject:CHEAP FLIGHT NOTICE:\n\n-Low Price Alert! Only:"

        if len(data) > 1:
            for i in range(len(data)):
                if i == len(data) - 1:
                    template = f'and RM {data[i][1]}.00 to fly from KUL to {data[i][0]}.'
                    text += '\n' + template

                else:
                    template = f'RM {data[i][1]}.00 to fly from KUL to {data[i][0]},'
                    text += '\n' + template

        else:
            template = f'RM {data[1]}.00 to fly from KUL to {data[0]},'
            text += '\n' + template

        print(text)
        emails = get_emails.Emails()

        if len(emails.data) > 1:
            print('this code is run')
            for i in range(len(emails.data)):
                self.send_email(text, emails.data[i])

        else:
            self.send_email(text, emails.data[0])


    def send_email(self, text, receiver_email):
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=self.__my_email, password=self.__password)
            connection.sendmail(from_addr=self.__my_email, to_addrs=receiver_email,
                                msg=text)

