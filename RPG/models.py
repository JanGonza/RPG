from django.db import models


class RPG(models.Model):
    page_number = models.IntegerField(unique=True)
    story = models.TextField()

    answer_choice_1 = models.TextField(blank=True, null=True)
    answer_link_1 = models.IntegerField(blank=True, null=True)
    answer_choice_2 = models.TextField(blank=True, null=True)
    answer_link_2 = models.IntegerField(blank=True, null=True)
    answer_choice_3 = models.TextField(blank=True, null=True)
    answer_link_3 = models.IntegerField(blank=True, null=True)
    answer_choice_4 = models.TextField(blank=True, null=True)
    answer_link_4 = models.IntegerField(blank=True, null=True)
    answer_choice_5 = models.TextField(blank=True, null=True)
    answer_link_5 = models.IntegerField(blank=True, null=True)

