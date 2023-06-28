# Generated by Django 3.2.4 on 2023-06-27 12:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('employee', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Salary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('basic', models.FloatField()),
                ('hra', models.FloatField()),
                ('pf', models.FloatField()),
                ('esi', models.FloatField()),
                ('allowance', models.FloatField()),
                ('net_salary', models.FloatField()),
                ('employee', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='employee.employee')),
            ],
        ),
    ]
