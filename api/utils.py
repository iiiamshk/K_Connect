from django.core.mail import send_mail
from django.template.loader import render_to_string
from .models import *
from django.shortcuts import get_object_or_404

def send_otp_mail(otp, user_email):
    # send otp to email
    html_message = render_to_string('otp_email_template.html', {
        'OTP': otp,
        'CurrentYear': 2025
    })

    try:
        mail = send_mail(
            subject="Your OTP Code",
            message="Your OTP is " + otp,
            from_email="otp@kconnect.in",
            recipient_list=[user_email],
            html_message=html_message,
            fail_silently=False,
        )
        return mail
    except Exception as e:
        print(e)
        return False
    


def add_group_member(group, members):
    for member_id in members:
        user = get_object_or_404(User, id=member_id)
        if not Group_member.objects.filter(group=group, user=user).exists():
            Group_member.objects.create(group=group, user=user)



