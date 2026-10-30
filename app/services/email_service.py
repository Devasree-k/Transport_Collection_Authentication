
import logging
import smtplib
import asyncio

from email.message import EmailMessage
from email.utils import formatdate

from app.core.config import (
    EMAIL_SENDER,
    EMAIL_PASSWORD,
    ADMIN_EMAIL,
)

logger = logging.getLogger(__name__)

class EmailService:

    def send_email(self, subject: str, body: str) -> bool:

        if not EMAIL_SENDER or not EMAIL_PASSWORD or not ADMIN_EMAIL:
            logger.error("Email configuration is missing")
            return False

        try:
            message = EmailMessage()

            message["Subject"] = subject
            message["From"] = EMAIL_SENDER
            message["To"] = ADMIN_EMAIL
            message["Date"] = formatdate(localtime=True)

            message.set_content(body)

            with smtplib.SMTP_SSL( "smtp.gmail.com",465,timeout=15) as smtp:
                
                smtp.login(EMAIL_SENDER, EMAIL_PASSWORD)
                smtp.send_message(message)
            logger.info("Admin notification email sent successfully")

            return True

        except (smtplib.SMTPException, OSError):
            logger.exception("Failed to send admin notification email")
            return False

    # Notification 1: New driver registered
    def send_driver_notification(self, driver_name: str, phone: str | None, license_number: str | None) -> bool:
        subject = "New Driver Registered - Transport Collection System"

        body = f"""
            Hello Admin,

            A new driver has been registered in the Transport Collection System.

            Driver Details
            --------------

            Driver Name: {driver_name}
            Phone Number: {phone or "Not provided"}
            License Number: {license_number or "Not provided"}

            Please log in to the system to view the complete driver details.

            Regards,
            Transport Collection System
        """

        return self.send_email(subject, body)


    async def send_driver_notification_async(self, driver_name: str, 
                phone: str | None,
                license_number: str | None) -> bool:  

        return await asyncio.to_thread(
            self.send_driver_notification,
            driver_name,
            phone,
            license_number,
        )
        

