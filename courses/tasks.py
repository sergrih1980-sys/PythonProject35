from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings


@shared_task
def send_email_task(subject, body, to_email):
    send_mail(
        subject=subject,
        message=body,
        from_email='from@example.com',
        recipient_list=[to_email],
    )
    return f"Sent to {to_email}"


@shared_task
def send_course_update_notification(course_id, course_title, updated_fields):
    from courses.models import Course, Subscription
    from users.models import User

    # Получаем курс
    try:
        course = Course.objects.get(pk=course_id)
    except Course.DoesNotExist:
        return

    # Находим активных подписчиков именно на этот курс
    subscribers = Subscription.objects.filter(
        course=course,
        is_active=True
    ).select_related('user')

    if not subscribers.exists():
        return

    subject = f"Обновление курса: {course_title}"
    body = (
        f"Курс «{course_title}» был обновлён.\n\n"
        f"Изменённые поля: {', '.join(updated_fields) or 'все данные'}\n\n"
        "Перейдите в личный кабинет, чтобы посмотреть новые материалы."
    )

    for sub in subscribers:
        if not sub.user.email:
            continue
        send_mail(
            subject=subject,
            message=body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[sub.user.email],
            fail_silently=False,
        )