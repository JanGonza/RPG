from django.shortcuts import render, get_object_or_404
from . import forms
from . import models
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


def start_page(request):
    return render(request, 'index.html')


def fight_status(user, monster_id):
    """Создание словаря с текущими характеристиками

    monster_stats - характеристики монстра
    profile_stats - характеристики персонажа
    """
    profile = get_object_or_404(models.Profile,
                                user=user,
                                )
    monster_status = get_object_or_404(models.MonsterStatus,
                                       user=user,
                                       name=monster_id,
                                       )
    monster_stats = {'stamina': monster_status.stamina,
                     'mastery': monster_status.mastery,
                     'damage': monster_status.damage,
                     }
    profile_stats = {'stamina': profile.current_stamina,
                     'mastery': profile.current_mastery,
                     'damage': 5,
                     }
    return monster_stats, profile_stats


def add_crystal(user, name):
    """Добавление кристало в профиль пользователя"""
    profile = get_object_or_404(models.Profile,
                                user=user,
                                )
    if name == "stamina_crystal":
        models.Profile.objects.filter(user=user).update(stamina_crystal=profile.stamina_crystal + 1)
    elif name == "earth_crystal":
        models.Profile.objects.filter(user=user).update(earth_crystal=profile.earth_crystal + 1)
    elif name == "water_crystal":
        models.Profile.objects.filter(user=user).update(water_crystal=profile.water_crystal + 1)
    elif name == "fire_crystal":
        models.Profile.objects.filter(user=user).update(fire_crystal=profile.fire_crystal + 1)
    elif name == "wind_crystal":
        models.Profile.objects.filter(user=user).update(wind_crystal=profile.wind_crystal + 1)


def story_page(user, page_number, param=None):
    """Создание словаря сюжета

        start_fight - подготовка к бою
        fight - бой с противником
        """
    storyline = get_object_or_404(models.RPG,
                                  page_number=page_number,
                                  )

    if param == "start_fight":
        questions = {storyline.answer_choice_1: page_number}

    elif param == "fight":
        questions = {"Продолжить схватку": page_number}

    else:
        questions = {storyline.answer_choice_1: storyline.answer_link_1}

    questions[storyline.answer_choice_2] = storyline.answer_link_2
    questions[storyline.answer_choice_3] = storyline.answer_link_3
    questions[storyline.answer_choice_4] = storyline.answer_link_4
    questions[storyline.answer_choice_5] = storyline.answer_link_5
    return questions


@login_required()
def crystal(request):
    if request.user.is_authenticated:
        user = request.user.id
    profile = get_object_or_404(models.Profile,
                                user=user,
                                )
    inventory = {'земли': profile.earth_crystal,
                 'огня': profile.fire_crystal,
                 'воды': profile.water_crystal,
                 'ветра': profile.wind_crystal,
                 'выносливости': profile.stamina_crystal}

    return render(request,
                  'content/crystal.html',
                  {'inventory': inventory,
                   })


@login_required()
def use_crystal(request, crystal):
    if request.user.is_authenticated:
        user = request.user.id
        profile = get_object_or_404(models.Profile,
                                    user=user,
                                    )
        storyline = get_object_or_404(models.RPG,
                                      page_number=profile.last_page,
                                      )
        monster_status = get_object_or_404(models.MonsterStatus,
                                           user=profile.user,
                                           name=storyline.monster,
                                           )
        if crystal == "земли":
            models.Profile.objects.filter(user=user).update(earth_crystal=profile.earth_crystal - 1)
            models.MonsterStatus.objects.filter(user=user,
                                                name=storyline.monster,
                                                ).update(stamina=monster_status.stamina - 5)
            use_crystal_result = "Град камней летит в вашего противника нанося ему 5 единиц урона"
        elif crystal == "воды":
            models.Profile.objects.filter(user=user).update(water_crystal=profile.water_crystal - 1)
            models.MonsterStatus.objects.filter(user=user,
                                                name=storyline.monster,
                                                ).update(damage=monster_status.damage - 2)
            use_crystal_result = ("под вашим противником вырывается мощный гейзер истоящая его силу. " +
                                  "Теперь противник будет наносить меньше урона"
                                  )
        elif crystal == "огня":
            models.Profile.objects.filter(user=user).update(fire_crystal=profile.fire_crystal + 1)
            models.MonsterStatus.objects.filter(user=user,
                                                name=storyline.monster,
                                                ).update(stamina=monster_status.damage - 5,
                                                         damage=monster_status.damage - 2,
                                                         )
            use_crystal_result = ("Противник вспыхивает как спичка. " +
                                  "Враг быстро тушит охватившеее его пламя," +
                                  " но получиные ожоги приченяют огромную боль." +
                                  " Урон -2, Здоровье -5"
                                  )
        elif crystal == "ветра":
            models.Profile.objects.filter(user=user).update(wind_crystal=profile.wind_crystal - 1)
            models.MonsterStatus.objects.filter(user=user,
                                                name=storyline.monster,
                                                ).update(mastery=monster_status.mastery - 2)
            use_crystal_result = ("Ветер подымает пыль с земли и направляет точно в глаза" +
                                  "вашего противника, снажая его мастерство на 2"
                                  )
        else:
            models.Profile.objects.filter(user=user).update(stamina_crystal=profile.stamina_crystal - 1)
            models.Profile.objects.filter(user=user).update(current_stamina=profile.default_stamina)
            use_crystal_result = "Вы чувствуете прилив энергии, ваши раны затягиваются. Выносливость восстановлена."

        page_number = profile.last_page
        return render(request,
                      'content/use_crystal.html',
                      {'use_crystal_result': use_crystal_result,
                       'page_number': page_number,
                       })


@login_required
def content(request, page_number):
    if request.user.is_authenticated:
        user = request.user.id
        storyline = get_object_or_404(models.RPG,
                                      page_number=page_number,
                                      )
        profile = get_object_or_404(models.Profile,
                                    user=user,
                                    )
        if storyline.crystal_name:
            crystal_name = str(storyline.crystal_name)
            add_crystal(user, crystal_name)

        if storyline.monster:
            monster_status = get_object_or_404(models.MonsterStatus,
                                               user=user,
                                               name=storyline.monster.id,
                                               )
            if profile.last_page != page_number:
                questions = story_page(user, page_number, "start_fight")
                models.Profile.objects.filter(user=user).update(last_page=page_number)
                monster_stats, profile_stats = fight_status(user, storyline.monster.id)
                return render(request,
                              'content/content.html',
                              {'content': storyline,
                               'questions': questions,
                               'monster_stats': monster_stats,
                               'profile_stats': profile_stats,
                               })
            else:
                result_stamina = monster_status.stamina - 5
                models.MonsterStatus.objects.filter(user=user, name=storyline.monster.id).update(stamina=result_stamina)
                if result_stamina < 1:
                    storyline = get_object_or_404(models.RPG,
                                                  page_number=storyline.answer_link_1,
                                                  )
                    questions = {storyline.answer_choice_1: storyline.answer_link_1,
                                 storyline.answer_choice_2: storyline.answer_link_2,
                                 storyline.answer_choice_3: storyline.answer_link_3,
                                 storyline.answer_choice_4: storyline.answer_link_4,
                                 storyline.answer_choice_5: storyline.answer_link_5}
                    models.Profile.objects.filter(user=user).update(last_page=page_number)
                    return render(request,
                                  'content/content.html',
                                  {'content': storyline,
                                   'questions': questions,
                                   })

                result_stamina = profile.current_stamina - 1
                models.Profile.objects.filter(user=user).update(current_stamina=result_stamina)
                if result_stamina < 1:
                    return HttpResponse('К сожалению удача была не на вашей стороне. Поражение')
                questions = story_page(user, page_number, "fight")
                models.Profile.objects.filter(user=user).update(last_page=page_number)
                monster_stats, profile_stats = fight_status(user, storyline.monster.id)
                user_crystal = {"Кристал восполнения выносливости": profile.stamina_crystal,
                                "Кристал огня": profile.fire_crystal,
                                "Кристал земли": profile.earth_crystal,
                                "Кристал воды": profile.water_crystal,
                                "Кристал ветра": profile.wind_crystal
                                }
                if max(user_crystal.values()):
                    return render(request,
                                  'content/content.html',
                                  {'content': storyline,
                                   'questions': questions,
                                   'monster_stats': monster_stats,
                                   'profile_stats': profile_stats,
                                   'user_crystal': user_crystal,
                                   })
                else:
                    return render(request,
                                  'content/content.html',
                                  {'content': storyline,
                                   'questions': questions,
                                   'monster_stats': monster_stats,
                                   'profile_stats': profile_stats,
                                   })
        else:
            questions = story_page(user, page_number)
            models.Profile.objects.filter(user=user).update(last_page=page_number)
            return render(request,
                          'content/content.html',
                          {'content': storyline,
                           'questions': questions})
    else:
        return render(request, 'index.html')


def register(request):
    if request.method == "POST":
        user_form = forms.UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(
                user_form.cleaned_data['password'],
            )
            new_user.save()
            models.Profile.objects.create(user=new_user)
            all_monsters = models.Monster.objects.all()
            for monster in all_monsters:
                models.MonsterStatus.objects.create(user=new_user,
                                                    name=monster,
                                                    stamina=monster.stamina,
                                                    mastery=monster.mastery,
                                                    damage=monster.damage,
                                                    )

            return render(request, 'reg_complete.html', {'new_user': new_user})
    else:
        user_form = forms.UserRegistrationForm()
    return render(request, 'reg.html', {'form': user_form})

