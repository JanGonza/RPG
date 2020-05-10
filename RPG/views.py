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


def story_page(user, page_number, param=None):
    """Создание словаря с сюжета

        start_fight - подготовка к бою
        fight - бой с противником
        win - окончание боя, переход на следующую страницу
        lose - окончание боя, переход на страницу поражения
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
                models.MonsterStatus.objects.filter(user=user).update(stamina=result_stamina)
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
                                   'questions': questions})

                result_stamina = profile.current_stamina - 1
                models.Profile.objects.filter(user=user).update(current_stamina=result_stamina)
                if result_stamina < 1:
                    return HttpResponse('Poragenie')
                questions = story_page(user, page_number, "fight")
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
            questions = story_page(user, page_number)
            models.Profile.objects.filter(user=user).update(last_page=page_number)
            return render(request,
                          'content/content.html',
                          {'content': storyline,
                           'questions': questions})
    else:
        HttpResponse("not login user")

