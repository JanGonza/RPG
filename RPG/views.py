from django.shortcuts import render, get_object_or_404
from . import models


def content(request, page_number):
    storyline = get_object_or_404(models.RPG,
                                  page_number=page_number)
    questions = {storyline.answer_choice_1: storyline.answer_link_1,
                 storyline.answer_choice_2: storyline.answer_link_2,
                 storyline.answer_choice_3: storyline.answer_link_3,
                 storyline.answer_choice_4: storyline.answer_link_4,
                 storyline.answer_choice_5: storyline.answer_link_5}
    return render(request,
                  'content/content.html',
                  {'content': storyline,
                   'questions': questions})
