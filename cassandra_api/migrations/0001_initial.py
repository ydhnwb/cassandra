# Generated by Django 3.0.5 on 2020-04-24 13:01

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=255, unique=True)),
                ('name', models.CharField(max_length=255, validators=[django.core.validators.MinLengthValidator(4)])),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('image', models.ImageField(default='https://miro.medium.com/max/560/1*MccriYX-ciBniUzRKAUsAw.png', null=True, upload_to='')),
                ('password', models.CharField(max_length=255, validators=[django.core.validators.MinLengthValidator(8)])),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Plant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('image', models.ImageField(default=None, null=True, upload_to='plants')),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cassandra_api.Location')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Watering',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('water_time', models.TimeField()),
                ('last_watered', models.DateTimeField(null=True)),
                ('remind_in_day', models.IntegerField(default=1)),
                ('plant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='watering', to='cassandra_api.Plant')),
            ],
        ),
        migrations.CreateModel(
            name='Type',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Prune',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prune_time', models.TimeField()),
                ('last_pruned', models.DateTimeField(null=True)),
                ('remind_in_day', models.IntegerField(default=1)),
                ('plant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prune', to='cassandra_api.Plant')),
            ],
        ),
        migrations.AddField(
            model_name='plant',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cassandra_api.Type'),
        ),
        migrations.CreateModel(
            name='Fertilization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fertilize_time', models.TimeField()),
                ('last_fertilized', models.DateTimeField(null=True)),
                ('remind_in_day', models.IntegerField(default=1)),
                ('plant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fertilization', to='cassandra_api.Plant')),
            ],
        ),
    ]
