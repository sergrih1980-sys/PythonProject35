from celery import shared_task
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from users.models import User

@shared_task
def deactivate_inactive_users():
    """
    Блокирует пользователей, у которых last_login старше 30 дней.
    Учитываются только активные пользователи. last_login может быть None — таких не трогаем.
    """
    cutoff_date = timezone.now() - timedelta(days=30)

    # Важно: last_login__lte, и last_login не NULL
    users_to_deactivate = User.objects.filter(
        is_active=True,
        last_login__isnull=False,
        last_login__lte=cutoff_date
    )

    count = users_to_deactivate.count()
    if count == 0:
        return {"status": "no_changes", "count": 0}

    users_to_deactivate.update(is_active=False)

    return {
        "status": "done",
        "count": count,
        "cutoff_date": cutoff_date.isoformat(),
    }