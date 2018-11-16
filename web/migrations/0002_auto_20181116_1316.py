# Generated by Django 2.1.3 on 2018-11-16 13:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Setting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('site_slogan_1', 'شعار ۱'), ('site_slogan_2', 'شعار ۲'), ('default_keywords', 'کلید واژه\u200cهای پیش\u200cفرض'), ('default_description', 'توضیح پیش\u200cفرض'), ('contact_email', 'ایمیل ارتباطی'), ('google_analytics_id', 'شناسه\u200cی Google Analytics')], help_text='از هر نوع فقط یک نمونه می\u200cتوانید ایجاد کنید.', max_length=32, unique=True, verbose_name='نوع')),
                ('content', models.CharField(help_text='محتوایی که در سایت نمایش داده می\u200cشود.', max_length=1024, verbose_name='محتوا')),
            ],
            options={
                'verbose_name': 'تنظیم',
                'verbose_name_plural': 'تنظیمات',
            },
        ),
        migrations.AlterModelOptions(
            name='page',
            options={'ordering': ['-created_on'], 'verbose_name': 'صفحه', 'verbose_name_plural': 'صفحه'},
        ),
        migrations.AlterField(
            model_name='report',
            name='description',
            field=models.TextField(blank=True, help_text='درصورتی که نیاز به یادآوری توضیحاتی در آینده وجود دارد در این قسمت وارد کنید.        هم\u200cچنین در صورت رد گزارش محتوای این فیلد برای کاربر ارسال می\u200cشود.', max_length=1024, verbose_name='توضیحات'),
        ),
        migrations.AlterField(
            model_name='report',
            name='status',
            field=models.CharField(choices=[('pending', 'در انتظار'), ('accepted', 'نایید شده'), ('denied', 'رد شده')], default='pending', help_text='در تعیین وضیعت رسیدگی دقت کنید. این قسمت تنها یک بار قابل تفییر است.', max_length=32, verbose_name='وضعیت رسیدگی'),
        ),
    ]
