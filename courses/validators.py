import re
from django.core.exceptions import ValidationError
from urllib.parse import urlparse

ALLOWED_DOMAIN = 'youtube.com'


def validate_only_youtube_com(value: str) -> None:
    """
    Проверяет, что в тексте нет ссылок на сторонние ресурсы.
    Разрешён ТОЛЬКО домен youtube.com (точно, без поддоменов и youtu.be).

    Если в value есть хоть одна ссылка не на youtube.com — выбрасывает ValidationError.
    """
    if not value:
        return

    # Регулярка для поиска URL (протокол + домен + путь)
    url_pattern = re.compile(
        r'https?://'  # http или https
        r'(?:[a-zA-Z0-9-]+\.)?'  # опциональный поддомен (один сегмент)
        r'[a-zA-Z0-9-]+\.[a-zA-Z]{2,}'  # домен.зона
        r'(?:/[^\s"\')>\]]*)?',  # путь (до пробела или кавычки)
        re.IGNORECASE
    )

    found_urls = url_pattern.findall(value)

    for url in found_urls:
        parsed = urlparse(url)
        domain = parsed.netloc.lower()

        # Убираем порт, если есть (например, :80)
        if ':' in domain:
            domain = domain.split(':', 1)[0]

        # Сравниваем домен строго с ALLOWED_DOMAIN
        if domain != ALLOWED_DOMAIN:
            raise ValidationError(
                f"Ссылки на сторонние ресурсы запрещены. Обнаружена ссылка на '{domain}'. "
                "Разрешён только домен youtube.com."
            )