from django.db import models

from utils.models import BaseModel
from django.conf import settings


# 课程分类，课程，老师，章节，课时

class CourseCategory(BaseModel):
    """分类"""
    name = models.CharField(max_length=64, unique=True, verbose_name="分类名称")

    class Meta:
        db_table = "luffy_course_category"
        verbose_name = "分类"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "%s" % self.name


class Course(BaseModel):
    """课程"""
    course_type = (
        (0, '付费'),
        (1, 'VIP专享'),
        (2, '学位课程')
    )
    level_choices = (
        (0, '初级'),
        (1, '中级'),
        (2, '高级'),
    )
    status_choices = (
        (0, '上线'),
        (1, '下线'),
        (2, '预上线'),
    )
    name = models.CharField(max_length=128, verbose_name="课程名称")
    # blank 后台管理录入可以为空，null存到数据库字段可以为空
    course_img = models.ImageField(upload_to="courses", max_length=255, verbose_name="封面图片", blank=True, null=True)
    # 课程付费类型
    course_type = models.SmallIntegerField(choices=course_type, default=0, verbose_name="付费类型")
    # TextField 大文本， 存html
    brief = models.TextField(max_length=2048, verbose_name="详情介绍", null=True, blank=True)
    # 难度等级
    level = models.SmallIntegerField(choices=level_choices, default=0, verbose_name="难度等级")
    # 发布日期
    pub_date = models.DateField(verbose_name="发布日期", auto_now_add=True)
    # 建议学习周期
    period = models.IntegerField(verbose_name="建议学习周期(day)", default=7)
    # 课件路径
    attachment_path = models.FileField(upload_to="attachment", max_length=128, verbose_name="课件路径", blank=True,
                                       null=True)
    status = models.SmallIntegerField(choices=status_choices, default=0, verbose_name="课程状态")
    # 优化字段
    students = models.IntegerField(verbose_name="学习人数", default=0)
    # 课程一边录，一边传
    sections = models.IntegerField(verbose_name="总课时数量", default=0)
    pub_sections = models.IntegerField(verbose_name="课时更新数量", default=0)
    price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="课程原价", default=0)

    # 关联字段
    # ForeignKey的on_delete的选择：
    # models.CASCADE    级联删除，用的少，除非真的要删除
    # models.SET_NULL   关联字段设为空   null=True
    # models.SET_DEFAULT 关联字段设为默认值 defalut='asfasd'
    # models.DO_NOTHING  什么都不做， 不用强外键关联
    # models.SET()       放一个函数内存地址，关联字段删除时，执行这个函数

    # 外键关联的好处和坏处
    #     -好处在于 插入修改数据，有校验，能够保证数据不会错乱，不会出现脏数据
    #     -坏处在于 有校验，速度慢，数量越大，越慢，咱们可以通过程序控制不加入脏数据
    # 公司内部为了效率，一般不建立外键关联，关系在 ，只是没有那条线了

    # 在django中不建立外键关联，只是不创建外键，关联关系还在【关联查询】，也是使用ForeignKey，只是加一个参数，加了之后，没有约束，但你们关系还在
    teacher = models.ForeignKey("Teacher", on_delete=models.DO_NOTHING, null=True, blank=True, verbose_name="授课老师",
                                db_constraint=False)
    course_category = models.ForeignKey("CourseCategory", on_delete=models.SET_NULL, db_constraint=False, null=True,
                                        blank=True, verbose_name="课程分类")

    class Meta:
        db_table = "luffy_course"
        verbose_name = "课程"
        verbose_name_plural = "课程"

    def __str__(self):
        return "%s" % self.name

    def course_type_name(self):
        # 通过数字映射对应的文字
        return self.get_course_type_display()

    def level_name(self):
        return self.get_level_display()

    def status_name(self):
        return self.get_status_display()

    # 序列化teacher的方法
    # def teacher_detail(self):
    #     # self是当前课程对象
    #     return {'name': self.teacher.name, 'image': settings.HOST_URL+'/media/'+str(self.teacher.image), 'title': self.teacher.title}

    # 序列化section_list的方法
    def section_list(self):
        section_list = []
        # 先根据课程取出所有章节，循环每个章节，取出所有课时，拼接到列表中，当列表长度等于四，就结束
        # 取到所有章节   原来是   表名小写_set.all()
        # course_chapter_list=self.coursechapter_set.all()
        # 一个课程有多个章节，一对多外键字段在章节，所以章节查课程是正向查询,反之反向查询
        course_chapter_list = self.coursechapters.all()
        for chapter in course_chapter_list:
            course_section = chapter.coursesections.all()  # 原来是   表名小写_set.all()
            for section in course_section:
                section_list.append({'id': section.id,
                                     'name': section.name,
                                     'section_link': section.section_link,
                                     'duration': section.duration,
                                     'free_trail': section.free_trail,
                                     })
            if len(section_list) >= 4:  # 最多4条
                return section_list
        return section_list  # 不足4条


class Teacher(BaseModel):
    """导师"""
    role_choices = (
        (0, '讲师'),
        (1, '导师'),
        (2, '班主任'),
    )
    name = models.CharField(max_length=32, verbose_name="导师名")
    role = models.SmallIntegerField(choices=role_choices, default=0, verbose_name="导师身份")
    title = models.CharField(max_length=64, verbose_name="职位、职称")
    signature = models.CharField(max_length=255, verbose_name="导师签名", help_text="导师签名", blank=True, null=True)
    image = models.ImageField(upload_to="teacher", null=True, verbose_name="导师封面")
    brief = models.TextField(max_length=1024, verbose_name="导师描述")

    class Meta:
        db_table = "luffy_teacher"
        verbose_name = "导师"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "%s" % self.name


class CourseChapter(BaseModel):
    """章节"""
    # 跟课程一对多，一个课程多个章节，关联字段写在多的一方
    # related_name='coursechapters'    反向操作时，使用的字段名，用于代替原反向查询时的’表名_set’
    # 拿课程下所有章节 course.coursechapter_set.all()   course.coursechapters.all()
    # related_query_name='字符串'    反向查询操作时，使用的连接前缀，用于替换表名
    # __ 连表查询       __表名小写__     __字符串__
    course = models.ForeignKey("Course", related_name='coursechapters', on_delete=models.CASCADE, verbose_name="课程名称")
    chapter = models.SmallIntegerField(verbose_name="第几章", default=1)
    name = models.CharField(max_length=128, verbose_name="章节标题")
    summary = models.TextField(verbose_name="章节介绍", blank=True, null=True)
    pub_date = models.DateField(verbose_name="发布日期", auto_now_add=True)

    class Meta:
        db_table = "luffy_course_chapter"
        verbose_name = "章节"
        verbose_name_plural = verbose_name

    def __str__(self):
        # 可能会出异常
        try:
            return "%s:(第%s章)%s" % (self.course, self.chapter, self.name)
        except Exception as e:
            return "未知课程:(第%s章)%s" % (self.chapter, self.name)


class CourseSection(BaseModel):
    """课时"""
    section_type_choices = (
        (0, '文档'),
        (1, '练习'),
        (2, '视频')
    )
    # 课时跟章节一对多，关联字段写在多的一方
    chapter = models.ForeignKey("CourseChapter", related_name='coursesections', on_delete=models.CASCADE,
                                verbose_name="课程章节")
    name = models.CharField(max_length=128, verbose_name="课时标题")
    orders = models.PositiveSmallIntegerField(verbose_name="课时排序")
    section_type = models.SmallIntegerField(default=2, choices=section_type_choices, verbose_name="课时种类")
    section_link = models.CharField(max_length=255, blank=True, null=True, verbose_name="课时链接",
                                    help_text="若是video，填vid,若是文档，填link")
    duration = models.CharField(verbose_name="视频时长", blank=True, null=True, max_length=32)
    pub_date = models.DateTimeField(verbose_name="发布时间", auto_now_add=True)
    free_trail = models.BooleanField(verbose_name="是否可试看", default=False)

    class Meta:
        db_table = "luffy_course_section"
        verbose_name = "课时"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "%s-%s" % (self.chapter, self.name)

# 表中字段不需要特别重视：只需要重视关联字段，字段多一个少一个都很正常，重视常用的几个字段即可
