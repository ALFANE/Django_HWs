from rest_framework.pagination import PageNumberPagination



class StudentPagination(PageNumberPagination):
    page_size = 20