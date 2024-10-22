# import threading
# import time
# from datetime import timedelta
# from django.utils import timezone
# from django.core.mail import send_mail
# from django.conf import settings
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from .models import UserData
# import logging
# from django.utils.dateformat import format
# import pytz

# # Set up logging
# logger = logging.getLogger(__name__)

# # Global variable to track if the reminder thread is running
# reminder_thread_running = False

# def send_expiration_reminder():
#     global reminder_thread_running
#     reminder_thread_running = True
#     while True:
#         current_time = timezone.now()
#         upcoming_expiries = UserData.objects.filter(
#             expiry_date__gt=current_time,
#             expiry_date__lte=current_time + timedelta(minutes=1),  # Check for the next minute
#             email_sent=False
#         )

#         for instance in upcoming_expiries:
#             try:
#                 expiry_date_local = instance.expiry_date.astimezone(pytz.timezone('Asia/Kolkata'))
#                 formatted_expiry_date = format(expiry_date_local, 'Y-m-d H:i:s T')
#                 send_mail(
#                     subject='Expiry Reminder',
#                     message=f'Your data with License Number: {instance.licence_no} will expire on {formatted_expiry_date}.',
#                     from_email=settings.EMAIL_HOST_USER,
#                     recipient_list=[instance.email],
#                     fail_silently=False,
#                 )
#                 logger.info(f"Sent email to {instance.email} about licence {instance.licence_no}")

#                 # Mark as email sent
#                 instance.email_sent = True
#                 instance.save(update_fields=['email_sent'])  # Only save the email_sent field
#             except Exception as e:
#                 logger.error(f"Failed to send email to {instance.email}: {str(e)}")

#         time.sleep(60)  # Check every minute

# def start_reminder_thread():
#     global reminder_thread_running
#     if not reminder_thread_running:
#         threading.Thread(target=send_expiration_reminder, daemon=True).start()

# # Flag to prevent recursion
# updating_user_data = False

# @receiver(post_save, sender=UserData)
# def start_reminder_on_userdata_creation(sender, instance, created, **kwargs):
#     global updating_user_data
#     if updating_user_data:
#         return  # Prevent recursion

#     # Check if the expiry date needs to trigger a reminder
#     current_time = timezone.now()
#     needs_reminder = instance.expiry_date > current_time and instance.expiry_date <= current_time + timedelta(minutes=1)

#     if created or not instance.email_sent or needs_reminder:  # Check if newly created or email not sent
#         logger.info("Creating or updating UserData instance, starting reminder thread.")
        
#         # Prevent recursion when saving the instance
#         updating_user_data = True
#         instance.email_sent = False  # Reset email_sent to False
#         instance.save(update_fields=['email_sent'])  # Only save the email_sent field
#         updating_user_data = False  # Reset the flag

#         start_reminder_thread()



import threading
import time
from datetime import timedelta
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import UserData
import logging
from django.utils.dateformat import format
import pytz

# Set up logging
logger = logging.getLogger(__name__)

# Global variable to track if the reminder thread is running
reminder_thread_running = False

def send_expiration_reminder():
    global reminder_thread_running
    reminder_thread_running = True
    while True:
        current_time = timezone.now()
        
        # Check for reminders 30 days before expiry
        thirty_days_reminders = UserData.objects.filter(
            expiry_date__gt=current_time,
            expiry_date__lte=current_time + timedelta(days=30),
            email_sent=False
        )

        # Check for reminders 24 hours before expiry
        twenty_four_hours_reminders = UserData.objects.filter(
            expiry_date__gt=current_time,
            expiry_date__lte=current_time + timedelta(hours=24),
            email_sent=False
        )

        for instance in thirty_days_reminders:
            try:
                expiry_date_local = instance.expiry_date.astimezone(pytz.timezone('Asia/Kolkata'))
                formatted_expiry_date = format(expiry_date_local, 'Y-m-d H:i:s T')
                send_mail(
                    subject='30-Day Expiry Reminder',
                    message=f'Your data with License Number: {instance.licence_no} will expire in 30 days on {formatted_expiry_date}.',
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[instance.email],
                    fail_silently=False,
                )
                logger.info(f"Sent 30-day reminder email to {instance.email} about licence {instance.licence_no}")

                # Mark as email sent
                instance.email_sent = True
                instance.save(update_fields=['email_sent'])
            except Exception as e:
                logger.error(f"Failed to send 30-day reminder email to {instance.email}: {str(e)}")

        for instance in twenty_four_hours_reminders:
            try:
                expiry_date_local = instance.expiry_date.astimezone(pytz.timezone('Asia/Kolkata'))
                formatted_expiry_date = format(expiry_date_local, 'Y-m-d H:i:s T')
                send_mail(
                    subject='24-Hour Expiry Reminder',
                    message=f'Your data with License Number: {instance.licence_no} will expire in 24 hours on {formatted_expiry_date}.',
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[instance.email],
                    fail_silently=False,
                )
                logger.info(f"Sent 24-hour reminder email to {instance.email} about licence {instance.licence_no}")

                # Mark as email sent
                instance.email_sent = True
                instance.save(update_fields=['email_sent'])
            except Exception as e:
                logger.error(f"Failed to send 24-hour reminder email to {instance.email}: {str(e)}")

        time.sleep(60)  # Check every minute

def start_reminder_thread():
    global reminder_thread_running
    if not reminder_thread_running:
        threading.Thread(target=send_expiration_reminder, daemon=True).start()

# Flag to prevent recursion
updating_user_data = False

@receiver(post_save, sender=UserData)
def start_reminder_on_userdata_creation(sender, instance, created, **kwargs):
    global updating_user_data
    if updating_user_data:
        return  # Prevent recursion

    # Check if the expiry date needs to trigger a reminder
    current_time = timezone.now()
    needs_reminder = instance.expiry_date > current_time and (instance.expiry_date <= current_time + timedelta(days=30) or instance.expiry_date <= current_time + timedelta(hours=24))

    if created or not instance.email_sent or needs_reminder:  # Check if newly created or email not sent
        logger.info("Creating or updating UserData instance, starting reminder thread.")
        
        # Prevent recursion when saving the instance
        updating_user_data = True
        instance.email_sent = False  # Reset email_sent to False
        instance.save(update_fields=['email_sent'])  # Only save the email_sent field
        updating_user_data = False  # Reset the flag

        start_reminder_thread()
