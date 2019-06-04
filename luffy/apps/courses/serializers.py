from rest_framework import serializers

from . import models


class CourseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CourseCategory
        fields = ('id', 'name')


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Teacher
        fields = ('name', 'title')

class CourseSerializer(serializers.ModelSerializer):
    starts_lesson = serializers.SerializerMethodField(read_only=True)
    teacher = TeacherSerializer(read_only=True)
    preferentials = serializers.SerializerMethodField(read_only=True)
    # policy_type = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = models.Course
        fields = (
            'id', 'name', 'course_img', 'studys', 'lessons', 'pub_lessons', 'price', 'preferentials',
             'teacher', 'price_service_type', 'starts_lesson', 'teacher',
        )

    def get_starts_lesson(self, obj):
        query_lessons = obj.coursechapters.first().coursesections.filter(is_show=True).order_by('order')[:4].values('name', 'order', 'free_trial')
        return  query_lessons

    def get_preferentials(self, obj):
        '''获取优惠价格'''
        price = float(obj.price)
        pricepolicy_list = obj.price_service_type.filter(pricepolicy__condition__lte=price).\
            values('pricepolicy__condition', 'pricepolicy__policy_value', 'pricepolicy__policy_type')
        preferential = 0
        policy_type = 3

        for item in pricepolicy_list:
            if item['pricepolicy__condition'] < price:
                preferential = item['pricepolicy__policy_value']
                policy_type = item['pricepolicy__policy_type']
        preferential_price = self.cal_price(price, policy_type, preferential)
        return {
            'preferential_price': preferential_price,
            'policy_type': models.PricePolicyService.POLICY_CHOICES[policy_type][1]
        }

    def cal_price(self, price, policy_type, preferential):
        '''计算优惠价格'''

        preferential_price = 0
        if policy_type == 0:
            # 积分兑换计算
            pass
        elif policy_type == 1:
            # 限时减免
            preferential_price = price - preferential
        elif policy_type == 2:
            # 折扣优惠
            preferential_price = price * preferential * 0.01
        elif policy_type == 3:
            # 限时免费
            preferential_price = 0
        else:
            preferential_price = -1
        return f'{preferential_price:.2f}'




class CourseLessonModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CourseLesson
        fields = ('order', 'name', 'chapter')


class CourseChaptersModelSerializer(serializers.ModelSerializer):
    coursesections = CourseLessonModelSerializer(many=True)
    class Meta:
        model = models.CourseChapter
        fields = ('id', 'name', 'chapter', 'coursesections')



class CourseDetailModelSerializer(serializers.ModelSerializer):
    # 这里调用的序列化器,必须事先在前面已经声明好的,否则报错
    teacher = TeacherSerializer()
    # 课程和课程章节的外键,因为需要获取具体的数据而不是ID,所以我们需要自定义序列化器
    coursechapters=CourseChaptersModelSerializer(many=True)
    preferentials = serializers.SerializerMethodField(read_only=True)
    # price_service_type = serializers.CharField(choices=models.)
    class Meta:
        model= models.Course
        fields = ("id", "name", "course_img", "studys", "lessons", "brief", "level",
                  "pub_lessons","price", "teacher", "preferentials", 'coursechapters',
                                                                     'price_service_type')

    def get_preferentials(self, obj):
        '''获取优惠价格'''
        price = float(obj.price)
        pricepolicy_list = obj.price_service_type.filter(pricepolicy__condition__lte=price).\
            values('pricepolicy__condition', 'pricepolicy__policy_value', 'pricepolicy__policy_type')
        preferential = 0
        policy_type = 3

        for item in pricepolicy_list:
            if item['pricepolicy__condition'] < price:
                preferential = item['pricepolicy__policy_value']
                policy_type = item['pricepolicy__policy_type']
        preferential_price = self.cal_price(price, policy_type, preferential)
        return {
            'preferential_price': preferential_price,
            'policy_type': models.PricePolicyService.POLICY_CHOICES[policy_type][1]
        }

    def cal_price(self, price, policy_type, preferential):
        '''计算优惠价格'''

        preferential_price = 0
        if policy_type == 0:
            # 积分兑换计算
            pass
        elif policy_type == 1:
            # 限时减免
            preferential_price = price - preferential
        elif policy_type == 2:
            # 折扣优惠
            preferential_price = price * preferential * 0.01
        elif policy_type == 3:
            # 限时免费
            preferential_price = 0
        else:
            preferential_price = -1
        return f'{preferential_price:.2f}'