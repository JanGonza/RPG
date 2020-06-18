from django.db import models
from django.conf import settings
from random import randint


class Monster(models.Model):
    monster_name = models.CharField(blank=False, null=False, max_length=100)
    stamina = models.IntegerField(blank=False, null=False)
    mastery = models.IntegerField(blank=False, null=False)
    damage = models.IntegerField(blank=False, null=False)

    def __str__(self):
        return self.monster_name


class Items(models.Model):
    item_name = models.CharField(blank=False, null=False, max_length=100)
    stamina = models.IntegerField(blank=False, null=False)
    mastery = models.IntegerField(blank=False, null=False)
    gold = models.IntegerField(blank=False, null=False)

    def __str__(self):
        return self.item_name


class Crystal(models.Model):
    crystal_name = models.CharField(blank=False, null=False, max_length=100)
    # regeneration = models.IntegerField(blank=False, null=False)
    # stamina = models.IntegerField(blank=False, null=False)
    # mastery = models.IntegerField(blank=False, null=False)
    # damage = models.IntegerField(blank=False, null=False)

    def __str__(self):
        return self.crystal_name


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE,
                                unique=True,
                                )
    result = int(randint(1, 7) + 6)
    default_mastery = models.IntegerField(default=result)
    current_mastery = models.IntegerField(default=result)
    result = int(randint(2, 13) + 12)
    default_stamina = models.IntegerField(default=result)
    current_stamina = models.IntegerField(default=result)
    result = int(randint(1, 7) + 6)
    default_luck = models.IntegerField(default=result)
    current_luck = models.IntegerField(default=result)
    weapon = models.IntegerField(default=1)
    armor = models.IntegerField(default=2)
    helmet = models.IntegerField(default=3)
    gold = models.IntegerField(default=4)
    stamina_crystal = models.IntegerField(default=0)
    earth_crystal = models.IntegerField(default=0)
    water_crystal = models.IntegerField(default=0)
    fire_crystal = models.IntegerField(default=0)
    wind_crystal = models.IntegerField(default=0)
    last_page = models.IntegerField(default=0)


class RPG(models.Model):
    crystal_name = models.ForeignKey(Crystal,
                                     blank=True,
                                     null=True,
                                     on_delete=models.PROTECT,
                                     )
    monster = models.ForeignKey(Monster,
                                blank=True,
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


class MonsterStatus(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             null=True,
                             on_delete=models.CASCADE,
                             )
    name = models.ForeignKey(Monster,
                             null=True,
                             on_delete=models.PROTECT,
                             )
    stamina = models.IntegerField(blank=False, null=False)
    mastery = models.IntegerField(blank=False, null=False)
    damage = models.IntegerField(blank=False, null=False)
