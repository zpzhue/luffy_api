# Generated by Django 2.1.7 on 2019-04-04 18:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='is_show',
            field=models.BooleanField(default=True, verbose_name='是否上线'),
        ),
        migrations.AlterField(
            model_name='coursechapter',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='coursechapters', to='courses.Course', verbose_name='课程标题'),
        ),
        migrations.AlterField(
            model_name='pricepolicyservice',
            name='policy_type',
            field=models.SmallIntegerField(choices=[(0, '积分兑换'), (1, '限时减免'), (2, '折扣优惠'), (3, '限时免费')], verbose_name='优惠类型'),
        ),
    ]
