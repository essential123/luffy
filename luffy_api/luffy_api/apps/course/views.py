from django.shortcuts import render

from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import RetrieveModelMixin,ListModelMixin
from utils.view import CommonListModelMixin
from .models import CourseCategory, Course, CourseChapter
from .serializer import CourseCategorySerializer, CourseSerializer, CourseChapterSerializer
from .page import CommonPageNumberPagination as PageNumberPagination
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

class CourseCategoryView(GenericViewSet, CommonListModelMixin):
    queryset = CourseCategory.objects.all().filter(is_delete=False, is_show=True).order_by('orders')
    serializer_class = CourseCategorySerializer


class CourseView(GenericViewSet, ListModelMixin, RetrieveModelMixin):
    queryset = Course.objects.all().filter(is_delete=False, is_show=True).order_by('orders')
    serializer_class = CourseSerializer
    pagination_class = PageNumberPagination
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    ordering_fields = ['orders', 'price', 'students']
    filterset_fields = ['course_category']


class CourseChapterView(GenericViewSet, ListModelMixin):
    queryset = CourseChapter.objects.all().filter(is_delete=False, is_show=True).order_by('orders')
    serializer_class = CourseChapterSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['course']


class CourseSearchView(GenericViewSet, ListModelMixin):
    queryset = Course.objects.all().filter(is_delete=False, is_show=True).order_by('orders')
    serializer_class = CourseSerializer
    pagination_class = PageNumberPagination
    filter_backends = [SearchFilter]
    ordering_fields = ['orders', 'price', 'students']
    search_fields = ['name']


# from rest_framework.viewsets import ViewSet
# from libs.alipay_common import alipay,GATEWAY
# from utils.response import APIResponse
# from rest_framework.decorators import action
# import uuid
# trade_no=str(uuid.uuid4())
# class PayView(ViewSet):
#     @action(methods=['GET'],detail=False)
#     def alipay(self,request):
#         res=alipay.api_alipay_trade_page_pay(
#             out_trade_no=trade_no,  # ?????????
#             total_amount=99,  # ???????????????
#             subject='??????',  # ???????????????????????????
#             return_url="https://example.com",  # # get????????????
#             notify_url="https://example.com/notify"  # ?????????????????????????????? notify url ???# post????????????
#         )
#         pay_url=GATEWAY+res
#         return APIResponse(pay_url=pay_url)