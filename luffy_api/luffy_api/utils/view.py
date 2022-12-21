from utils.response import APIResponse
from rest_framework.mixins import ListModelMixin


class CommonListModelMixin(ListModelMixin):
    def list(self, request, *args, **kwargs):
        res = super().list(request, *args, **kwargs)
        print(res)
        return APIResponse(result=res.data)
