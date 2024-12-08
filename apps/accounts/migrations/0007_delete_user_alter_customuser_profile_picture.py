# Generated by Django 5.1.3 on 2024-12-07 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_alter_customuser_role'),
    ]

    operations = [
        migrations.DeleteModel(
            name='User',
        ),
        migrations.AlterField(
            model_name='customuser',
            name='profile_picture',
            field=models.ImageField(blank=True, default='profile_pictures/default-profile.jpg', null=True, upload_to='profile_pictures/'),
        ),
    ]
