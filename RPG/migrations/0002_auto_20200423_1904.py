# Generated by Django 3.0.5 on 2020-04-23 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RPG', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rpg',
            name='answer_choice_1',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='rpg',
            name='answer_choice_2',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='rpg',
            name='answer_choice_3',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='rpg',
            name='answer_choice_4',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='rpg',
            name='answer_choice_5',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='rpg',
            name='answer_link_1',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='rpg',
            name='answer_link_2',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='rpg',
            name='answer_link_3',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='rpg',
            name='answer_link_4',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='rpg',
            name='answer_link_5',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
