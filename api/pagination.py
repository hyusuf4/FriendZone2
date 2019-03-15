from rest_framework.pagination import PageNumberPagination


class DefaultPageNumberPagination(PageNumberPagination):
    page_size=2
    page_size_query_param= 'page'
    max_page_size=50
