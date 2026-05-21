from django.core.mail import send_mail
from django.conf import settings

from accounts.models import RoleChoices, User

from .models import Notification


def notify_onboarding_completed(instance) -> None:
    """Email employee and HR when onboarding reaches 100%."""
    employee = instance.employee
    subject = f'Онбординг завершён: {instance.program.name}'
    body = (
        f'Сотрудник {employee.get_full_name() or employee.username} '
        f'завершил программу «{instance.program.name}».'
    )

    recipients = [employee]
    hr_users = User.objects.filter(
        company=employee.company,
        role__in=(RoleChoices.HR, RoleChoices.ADMIN),
        is_active=True,
    )
    recipients.extend(hr_users)

    seen = set()
    for user in recipients:
        if user.id in seen:
            continue
        seen.add(user.id)
        Notification.objects.create(
            recipient=user,
            subject=subject,
            body=body,
            is_sent=False,
        )
        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            [user.email] if user.email else [],
            fail_silently=True,
        )
        Notification.objects.filter(recipient=user, subject=subject).update(is_sent=True)
