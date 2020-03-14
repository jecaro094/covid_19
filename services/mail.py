# https://aiosmtplib.readthedocs.io/en/latest/overview.html#quickstart
import asyncio as aio
import aiosmtplib
from email.mime.text import MIMEText
from services import logger
import html2text


fromaddr = 
pwd = 
user = 
hostname = 

debug = True

class Mail():
    def __init__(self, loop):
        self.cn = self.__class__.__name__
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

    async def sendmail(self, key, message, participant, hostname, par_type):
        if key not in self.smtp:
            await self.connect(key)
        # NOTE Considered tags in message
        for key_ in participant.keys():
            # NOTE ...as long as there is a value assigned to the key_
            if participant[key_] != None: 
                tag = f'<{key_}>'
                if tag in message:
                    message = message.replace(tag, participant[key_])

        # NOTE Considered link in message
        if '<link>' in message:
            link_id = participant['id']
            link_message = f'{hostname}/participant?{par_type}={link_id}'
            message = message.replace('<link>', link_message )

        # NOTE Signature included in message sent, as an example
        h = html2text.HTML2Text()
        h.ignore_links = False
        signature = f"""\
        <html>
        <head></head>
        <body>
            <br>
            <br>
            <p>Hi!<br>
                This is an example of signature for email<br>
            </p>
        </body>
        </html>
        """
        signature = h.handle(signature)

        # NOTE Message to send
        final_message = message + signature
        logger.log(lvl="INFO", msg=f"Final message: {final_message}", orig=self.cn)

        final_message = MIMEText(final_message)
        final_message["From"] = fromaddr
        final_message["To"] = participant['email']
        final_message["Subject"] = 'subject'
        logger.log(lvl="INFO", msg=f"Sending message... ({par_type})", orig=self.cn)
        if debug:
            print("debug mode,do not send...")
            return
        await self.smtp[key].send_message(final_message)
        logger.log(lvl="INFO", msg=f"Message sent! ({par_type})", orig=self.cn)
        self.smtp[key].close()
        self.smtp.pop(key)


