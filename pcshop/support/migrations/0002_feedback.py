# Generated migration for Feedback model

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('support', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, help_text='Your name (optional if logged in)', max_length=100)),
                ('email', models.EmailField(blank=True, help_text='Your email (optional if logged in)', max_length=254)),
                ('rating', models.PositiveIntegerField(choices=[(1, '⭐ Poor'), (2, '⭐⭐ Fair'), (3, '⭐⭐⭐ Good'), (4, '⭐⭐⭐⭐ Excellent'), (5, '⭐⭐⭐⭐⭐ Outstanding')], default=5)),
                ('title', models.CharField(help_text='Brief title of your feedback', max_length=200)),
                ('message', models.TextField(help_text='Your detailed feedback or suggestion')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_public', models.BooleanField(default=False, help_text='Display this feedback on the website')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='feedbacks', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
