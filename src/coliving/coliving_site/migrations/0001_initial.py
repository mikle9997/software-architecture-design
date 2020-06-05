# Generated by Django 3.0.5 on 2020-06-05 15:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ColivingUser',
            fields=[
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('name', models.CharField(max_length=100)),
                ('login', models.CharField(max_length=100, primary_key=True, serialize=False, unique=True)),
                ('password', models.CharField(max_length=100)),
                ('contact', models.CharField(max_length=100)),
                ('role', models.DecimalField(decimal_places=0, max_digits=1)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=100, null=True)),
                ('description', models.CharField(max_length=400)),
                ('adress', models.CharField(max_length=120)),
                ('freeSpaces', models.DecimalField(blank=True, decimal_places=0, max_digits=2, null=True)),
                ('state', models.DecimalField(decimal_places=0, max_digits=1)),
                ('image', models.FileField(upload_to='images/')),
                ('consultant', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='consultant', to='coliving_site.ColivingUser')),
                ('organizer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='organizer', to='coliving_site.ColivingUser')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user', to='coliving_site.ColivingUser')),
            ],
        ),
    ]
