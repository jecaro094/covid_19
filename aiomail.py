# https://aiosmtplib.readthedocs.io/en/latest/overview.html#quickstart
import asyncio as aio
import aiosmtplib
from email.mime.text import MIMEText


fromaddr = 
pwd = 
user = 
hostname = 

# TODO Create new file with this class info, at /services/mail.py
# TODO Change prints with logger messages.
# NOTE Class with capitals, file/object with non capitals
class Mail():
    def __init__(self, loop):
        self.loop = loop
        self.smtp = {}

    async def connect(self, key):
        if key in self.smtp:
            if self.smtp[key].is_connected:
                print("allready connected")
        else:
            self.smtp[key] = aiosmtplib.SMTP(hostname=hostname, port=587, loop=self.loop) 
            await self.smtp[key].connect()
            await self.smtp[key].starttls()
            await self.smtp[key].login(user, pwd)
            print("connected")

    async def sendmail(self, key, message, return_adress, name):
        if key not in self.smtp:
            await self.connect(key)
        message = MIMEText(message)
        message["From"] = fromaddr
        message["To"] = fromaddr
        message["Subject"] = "message by %s: %s" % (name, return_adress)
        await self.smtp[key].send_message(message)
        self.smtp[key].close()
        self.smtp.pop(key)


# TODO Change e-mail address for testing and loop (the one that already exists at app.py)
if __name__ == "__main__":
    loop = aio.get_event_loop()
    mail = Mail(loop)
    f3 = mail.sendmail(1234, "test", "jesus.caballero@quantecdc.es", "oli")
    f4 = mail.sendmail(7890, "test", "jesus.caballero@quantecdc.es", "oli")
    loop.run_until_complete(aio.gather(f3, f4))


