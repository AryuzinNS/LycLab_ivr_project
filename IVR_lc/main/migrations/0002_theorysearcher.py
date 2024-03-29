# Generated by Django 4.2.2 on 2023-11-05 21:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TheorySearcher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('description', models.CharField(max_length=512)),
                ('by', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=100)),
                ('theory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.theory')),
            ],
        ),
    ]
