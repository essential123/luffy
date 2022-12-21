from rest_framework.pagination import PageNumberPagination


class CommonPageNumberPagination(PageNumberPagination):
    page_size = 2  # 每页显示的条数
    page_query_param = 'page'  # /books/?page=3  页面查询参数，查询第几页的参数
    page_size_query_param = 'size'  # page_size_query_param：表示 url 中每页数量参数
    max_page_size = 5  # 限制通过size查询，最大的条数
