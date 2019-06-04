import xadmin
from . import models

class CourseCategoryModelAdmin(object):
    """课程分类模型管理类"""
    pass
xadmin.site.register(models.CourseCategory, CourseCategoryModelAdmin)


class CourseModelAdmin(object):
    """课程模型管理类"""
    pass
xadmin.site.register(models.Course, CourseModelAdmin)


class TeacherModelAdmin(object):
    """老师模型管理类"""
    pass
xadmin.site.register(models.Teacher, TeacherModelAdmin)


class CourseChapterModelAdmin(object):
    """课程章节模型管理类"""
    list_filter = ['course']
    ordering = ['chapter']

xadmin.site.register(models.CourseChapter, CourseChapterModelAdmin)


class CourseLessonModelAdmin(object):
    """课程课时模型管理类"""
    list_filter = ['chapter']
    ordering = ['order']
xadmin.site.register(models.CourseLesson, CourseLessonModelAdmin)


class PriceServiceTypeModelAdmin(object):
    """价格服务类型模型管理类"""
    pass
xadmin.site.register(models.PriceServiceType, PriceServiceTypeModelAdmin)


class PricePolicyServiceModelAdmin(object):
    """价格服务类型模型管理类"""
    pass
xadmin.site.register(models.PricePolicyService, PricePolicyServiceModelAdmin)