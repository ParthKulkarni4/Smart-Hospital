from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import date, timedelta
from django.core.mail import send_mail
from .models import Donor

# 1️⃣ Thank-you email + update next eligible date when donation recorded
@receiver(post_save, sender=Donor)
def donor_thank_you_and_update(sender, instance, created, **kwargs):

    # If donor is newly created → no email
    if created:
        return
    
    # If donor has no last donation date → skip
    if not instance.last_donation_date:
        return
    
    # Calculate next eligible date (90 days)
    next_eligible = instance.last_donation_date + timedelta(days=90)

    # THANK YOU Email (sent immediately after new donation date is saved)
    if instance.last_donation_date == date.today():
        if instance.email:
            send_mail(
                "Thank You for Donating Blood!",
                f"Dear {instance.name},\n\nThank you for your generous blood donation!",
                "hospital@gmail.com",
                [instance.email],
                fail_silently=True,
            )

    # Save the next eligible date (optional: only if you add field)
    # instance.next_eligible_date = next_eligible
    # instance.save()


# 2️⃣ Eligibility email when donor becomes eligible again (90+ days)
@receiver(post_save, sender=Donor)
def donor_eligibility_check(sender, instance, **kwargs):

    if not instance.last_donation_date:
        return

    days = (date.today() - instance.last_donation_date).days

    # Eligible again after 90 days
    if days >= 90:

        if instance.email:
            send_mail(
                "You Are Eligible to Donate Blood Again!",
                f"Dear {instance.name},\n\n"
                "You are now eligible to donate blood again (90 days passed).",
                "hospital@gmail.com",
                [instance.email],
                fail_silently=True,
            )
