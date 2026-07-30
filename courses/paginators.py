from rest_framework.pagination import PageNumberPagination

class StandardResultsSetPagination(PageNumberPagination):
    """
    Стандартная пагинация для списков курсов и уроков.
    """
    page_size = 10  # количество элементов на странице по умолчанию
    page_size_query_param = 'page_size'  # параметр запроса для изменения размера страницы
    max_page_size = 50  # максимальный размер страницы