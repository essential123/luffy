#依赖镜像名称和ID
FROM python:3.8
#指定镜像创建者信息
MAINTAINER xxx
#切换工作目录
RUN mkdir /soft
WORKDIR /soft
COPY ./requestment.txt /soft/requestment.txt
RUN pip install -r requirements.txt -i https://pypi.doubanio.com/simple
#CMD ["uwsgi", "-x", "./luffy.xml"]
CMD ["uwsgi", "./luffy.ini"]
#CMD ["python", "manage_pro.py", "runserver"]