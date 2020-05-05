from django.db import models
from django.conf import settings
from random import randint


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE,
                                )
    weapon = models.CharField(default='меч', max_length=100)
    armor = models.CharField(default='кольчужная рубаха',
                             max_length=100,
                             )
    ring = models.CharField(default='медное кольцо', max_length=100)
    money = models.IntegerField(default=3)
    result = int(randint(1, 7) + 6)
    default_skill = models.IntegerField(default=result)
    current_skill = models.IntegerField(default=result)
    result = int(randint(2, 13) + 12)
    default_stamina = models.IntegerField(default=result)
    current_stamina = models.IntegerField(default=result)
    result = int(randint(1, 7) + 6)
    default_luck = models.IntegerField(default=result)
    current_luck = models.IntegerField(default=result)

    def __str__(self):
        return self.user


class Monster(models.Model):
    name = models.CharField(max_length=100)
    default_skill = models.IntegerField(blank=False, null=False)
    current_skill = models.IntegerField(blank=False, null=False)
    default_stamina = models.IntegerField(blank=False, null=False)
    current_stamina = models.IntegerField(blank=False, null=False)

    def __str__(self):
        return self.name


class RPG(models.Model):
    monster = models.OneToOneField(Monster,
                                   null=True,
                                   on_delete=models.PROTECT,
                                   )
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