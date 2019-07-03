# Generated by Django 2.1.5 on 2019-07-01 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('uju', '0002_auto_20190701_1648'),
    ]

    operations = [
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city_name', models.CharField(max_length=100)),
                ('city_pinyin', models.CharField(max_length=20)),
                ('city_url', models.CharField(max_length=255)),
                ('region_name', models.CharField(max_length=100)),
                ('region_pinyin', models.CharField(max_length=20)),
                ('region_url', models.CharField(max_length=255)),
                ('region_code', models.CharField(max_length=20)),
                ('is_finish', models.BooleanField(default=False)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='region',
            unique_together={('city_pinyin', 'region_pinyin')},
        ),
    ]