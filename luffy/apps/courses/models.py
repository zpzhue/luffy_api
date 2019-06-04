from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
# Create your models here.
from luffy.utils.base_model import BaseModel


class CourseCategory(BaseModel):
    '''课程分类模型类'''
    name = models.CharField(max_length=64, unique=True, verbose_name='分类名称')
    order = models.IntegerField(null=True, verbose_name='分类排序')
    is_show = models.BooleanField(default=False, verbose_name='是否上线')

    class Meta:
        db_table = 'lf_course_category'
        verbose_name = '课程分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Teacher(BaseModel):
    '''讲师、导师模型类'''
    ROLE_CHOICES = (
        (0, '讲师'),
        (1, '导师')
    )

    name = models.CharField(max_length=32, verbose_name='讲师名字')
    role = models.SmallIntegerField(choices=ROLE_CHOICES, default=0, verbose_name='讲师身份（角色）')
    title = models.CharField(max_length=64, verbose_name='讲师职位，职称')
    signature = models.CharField(max_length=255, null=True, blank=True, help_text='讲师签名', verbose_name='讲师签名')
    image = models.ImageField(upload_to='teacher', null=True, blank=True, verbose_name='讲师封面')
    brief = models.TextField(max_length=1024, verbose_name='讲师描述')

    class Meta:
        db_table = 'lf_teacher'
        verbose_name = '讲师、导师'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class Course(BaseModel):
    '''专题课程模型类'''
    course_choices = (
        (0, '免费'),
        (1, '付费'),
        (2, 'VPI专享'),
        (3, '学位课程'),
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

    name = models.CharField(max_length=128, verbose_name='课程名称')
    course_img = models.ImageField(upload_to='course',null=True, blank=True, verbose_name='课程封面图')
    course_type = models.SmallIntegerField(choices=course_choices, verbose_name='付费类型')
    brief = RichTextUploadingField(null=True, blank=True, verbose_name='课程介绍')
    level = models.SmallIntegerField(choices=level_choices, default=1, verbose_name='课程难度等级')
    pub_date = models.DateField(auto_now_add=True, verbose_name='发布日期')
    preiod = models.IntegerField(default=7, verbose_name='建议学习周期(day)')
    order = models.IntegerField(verbose_name='课程排序')
    attachment_path = models.FileField(max_length=128, null=True, blank=True, verbose_name='课件路径')
    status = models.SmallIntegerField(choices=status_choices, default=0, verbose_name='课程状态')
    course_category = models.ForeignKey(to='CourseCategory', on_delete=models.CASCADE, null=True, blank=True, verbose_name='课程分类')
    studys = models.IntegerField(default=0, verbose_name='学习人数')
    lessons = models.IntegerField(default=0, verbose_name='总课程数量')
    pub_lessons = models.IntegerField(default=0, verbose_name='课程更新数量')
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0, verbose_name='课程原价')
    teacher = models.ForeignKey(to='Teacher', null=True, blank=True, on_delete=models.DO_NOTHING, verbose_name='授课老师')
    price_service_type = models.ManyToManyField(to='PriceServiceType', verbose_name='价格服务类型')
    is_show = models.BooleanField(default=True, verbose_name='是否上线')

    class Meta:
        db_table = 'lf_course'
        verbose_name = '专题课程'
        verbose_name_plural = verbose_name


    def __str__(self):
        return self.name


class CourseChapter(BaseModel):
    '''课程章节模型类'''
    course = models.ForeignKey(to='Course', related_name='coursechapters', on_delete=models.CASCADE, verbose_name='课程标题')
    chapter = models.SmallIntegerField(default=0, verbose_name='课程章节')
    name = models.CharField(max_length=128, verbose_name='章节标题')
    summary = models.TextField(null=True, blank=True, verbose_name='章节介绍')
    pubdate = models.DateField(auto_now_add=True, verbose_name='发布日期')
    is_show = models.BooleanField(default=True, verbose_name='是否上线')


    class Meta:
        db_table = 'lf_course_chapter'
        verbose_name = '课程章节'
        verbose_name_plural= verbose_name

    def __str__(self):
        return f"{self.course.name}:(第{self.chapter}章){self.name}"


class CourseLesson(BaseModel):
    '''课程课时模型类'''
    section_type_choice = (
        (0, '文档'),
        (1, '练习'),
        (2, '视频'),
    )

    chapter = models.ForeignKey(to='CourseChapter', related_name='coursesections', on_delete=models.CASCADE)
    name = models.CharField(max_length=128, verbose_name='课时标题')
    order = models.PositiveSmallIntegerField(verbose_name='课时排序')
    section_type = models.SmallIntegerField(choices=section_type_choice, default=2, verbose_name='课时种类')
    section_link = models.CharField(max_length=255, null=True, blank=True, verbose_name='课时链接', help_text='若是video，填vid,若是文档，填link')
    duration = models.CharField(max_length=32, null=True, blank=True, verbose_name='视频时长')
    pub_date = models.DateField(auto_now_add=True, verbose_name='发布日期')
    free_trial = models.BooleanField(default=False, verbose_name='是否可以试看')
    is_show = models.BooleanField(default=True, verbose_name='是否上线')

    class Meta:
        db_table = 'lf_course_lesson'
        verbose_name = '课程课时'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'{self.chapter.name}:{self.name}'


class PriceServiceType(BaseModel):
    '''价格服务类型模型表'''
    name = models.CharField(max_length=32, verbose_name='服务类型名称')

    class Meta:
        db_table = 'lf_price_service_type'
        verbose_name = '价格服务'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class PricePolicyService(BaseModel):
    '''价格服务策略'''
    POLICY_CHOICES = (
        (0, '积分兑换'),
        (1, '限时减免'),
        (2, '折扣优惠'),
        (3, '限时免费'),
    )
    service_type = models.ForeignKey('PriceServiceType', related_name='pricepolicy', on_delete=models.CASCADE, verbose_name='服务类型')
    condition = models.IntegerField(verbose_name='满足优惠条件的价格')
    policy_type = models.SmallIntegerField(choices=POLICY_CHOICES, verbose_name='优惠类型')
    policy_value = models.IntegerField(verbose_name='优惠值（根据优惠类型来填写）',
                                       help_text='如果是积分兑换优惠，则填写的值为可以兑换的最大积分；<br /> 如果是折扣优惠则填写折扣的百分比值，如8折则填写80; <br /> 如果是限时免费，则可以不填')
    start_time = models.DateTimeField(verbose_name="优惠策略的开始时间")
    end_time = models.DateTimeField(verbose_name="优惠策略的结束时间")


    class Meta:
        db_table = "lf_price_policy_service"
        verbose_name = "价格服务策略"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "%s：优惠条件:%s,优惠值:%s" % (self.service_type.name, self.condition, self.policy_value)