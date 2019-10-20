import traceback
from datetime import datetime

from django.contrib import messages
from django.shortcuts import render, redirect

from .models import Seminar, Talk, Attendees
from .forms import SeminarRegistrationForm


def index(request):
    now = datetime.now().date()
    next_seminars = Seminar.objects.filter(date__gte=now).order_by('date')
    past_talks = Talk.objects.filter(seminar__date__lte=now
                                     ).order_by('-seminar__date')
    past_talks = [talk.render(date=talk.seminar.date, place=talk.seminar.place)
                  for talk in past_talks]

    content_name = request.path.replace('/', '')
    if content_name == '':
        content_name = 'about'
    context = {
        'talks': past_talks,
        'seminars': next_seminars,
        'content': "programme/{}.html".format(content_name),
        'messages': messages.get_messages(request)
    }
    try:
        res = render(request, 'programme/index.html', context)
    except Exception:
        traceback.print_exc()
        context["content"] = "programme/about.html"
        res = render(request, 'programme/index.html', context)

    return res


def register(request, seminar_id):
    if request.method == 'POST':
        form = SeminarRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            # import IPython; IPython.embed(colors='neutral')
            messages.success(request, "You have successfully registered")
            return redirect('index', permanent=True)

    a = Attendees(seminar=Seminar.objects.get(id=seminar_id))
    form = SeminarRegistrationForm(instance=a)

    context = {
        'form': form,
        'seminar_id': seminar_id,
        'content': "programme/register.html",
    }
    return render(request, 'programme/index.html', context)
