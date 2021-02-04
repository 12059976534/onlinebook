# Generated by Django 3.1.5 on 2021-01-11 04:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Kategoribuku',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kategori', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Leveluser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama', models.CharField(max_length=200)),
                ('email', models.EmailField(max_length=200)),
                ('username', models.CharField(max_length=300)),
                ('password', models.CharField(max_length=100)),
                ('leveluser', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.leveluser')),
            ],
        ),
        migrations.CreateModel(
            name='Buku',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('files', models.TextField(max_length=False)),
                ('judul', models.CharField(max_length=250)),
                ('penulis', models.CharField(max_length=250)),
                ('penerbit', models.CharField(max_length=500)),
                ('status', models.BooleanField(default=True)),
                ('ate', models.DateTimeField(auto_now_add=True, null=True)),
                ('kategori', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.kategoribuku')),
            ],
        ),
    ]