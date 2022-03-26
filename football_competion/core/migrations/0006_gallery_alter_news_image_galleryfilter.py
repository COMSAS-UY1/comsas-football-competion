# Generated by Django 4.0.2 on 2022-03-26 21:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_news'),
    ]

    operations = [
        migrations.CreateModel(
            name='Gallery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='gallerie/')),
                ('alt', models.CharField(blank=True, max_length=20, null=True)),
                ('title', models.CharField(blank=True, max_length=300, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='news',
            name='image',
            field=models.ImageField(default='news_placeholder.jpg', upload_to='actualite/'),
        ),
        migrations.CreateModel(
            name='GalleryFilter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.gallery')),
            ],
        ),
    ]
