# Generated by Django 5.2.1 on 2025-07-22 22:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('badges', '0004_userprogress'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprogress',
            old_name='start_date',
            new_name='joined_at',
        ),
        migrations.RemoveField(
            model_name='userprogress',
            name='completed',
        ),
        migrations.AddField(
            model_name='userprogress',
            name='completed_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='userprogress',
            name='status',
            field=models.CharField(choices=[('in_progress', 'In Progress'), ('pending_review', 'Pending Review'), ('completed', 'Completed')], default='in_progress', max_length=20),
        ),
    ]
