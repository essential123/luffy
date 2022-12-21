from rest_framework.response import Response


class APIResponse(Response):
    def __init__(self, code=100, msg='ok', status=None, headers=None, **kwargs):
        data = {'code': code, 'msg': msg}
        if kwargs:
            data.update(kwargs)
        super().__init__(data=data, status=status, headers=headers)
