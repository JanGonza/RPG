from django.shortcuts import render, get_object_or_404
from . import forms
from . import models
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


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
        monster_status = get_object_or_404(models.MonsterStatus,
                                           user=user,
                                           )
        if storyline.monster:
            if profile.last_page != page_number:
                questions = {storyline.answer_choice_1: page_number,
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
                questions = {"Продолжить схватку": page_number,
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
        else:
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
    else:
        HttpResponse("not login user")
