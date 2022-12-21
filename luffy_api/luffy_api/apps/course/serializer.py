from .models import CourseCategory, Course, Teacher, CourseChapter, CourseSection
from rest_framework import serializers
from django.conf import settings


class CourseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseCategory
        fields = ['id', 'name']


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ['id', 'name', 'role', 'title', 'signature', 'image', 'brief']


class CourseSerializer(serializers.ModelSerializer):
    # 方式三：子序列化：通过老师的序列化类来实现序列化
    teacher = TeacherSerializer()

    class Meta:
        model = Course
        fields = ['id', 'name', 'course_img',
                  'price',  # 课程价格
                  'students',  # 学生数量
                  'pub_sections',  # 发布了多少课时
                  'sections',  # 总课时数量
                  # 课程详情也用这个序列化类（brief，attachment_path）
                  'brief',  # 课程介绍
                  'attachment_path',  # 课程课件地址

                  'period',  # 建议学习周期

                  'course_type_name',  # 课程类型名字，表中没有这个字段，表模型中重写方法
                  'level_name',  # 级别名字
                  'status_name',  # 状态名字

                  # 'teacher_detail',  # 老师  {name:xx,title:xxx}
                  'teacher',
                  'section_list',  # 课时 最多4个课时 [{},{},{},{}]
                  ]  # 要序列化更多字段：图片，有多少课时，更新了多少，学生数量，价格。。。   teacher字段:{name:xx,title:asdf}   章节下的课时，最多四个课时

    # 指定序列化的字段：三种方式
    # 方式一：在表模型中写
    # 方式二：序列化类中写
    # teacher = serializers.SerializerMethodField()

    # def get_teacher(self, obj):
    #     # obj 是当前序列化的对象(课程对象)
    #     return {'name': obj.teacher.name, 'image': settings.HOST_URL + '/media/' + str(obj.teacher.image),
    #             'title': obj.teacher.title}


class CourseSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseSection
        fields = '__all__'


class CourseChapterSerializer(serializers.ModelSerializer):
    # 一个章节下，有很多课时，课时是多条，子序列化时，不要忘了many=True
    coursesections =CourseSectionSerializer(many=True)

    class Meta:
        model = CourseChapter
        fields = ['id', 'name', 'chapter', 'summary', 'coursesections']

