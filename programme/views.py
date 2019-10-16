import traceback
from django.shortcuts import render, redirect

from .models import Seminar, Attendees
from .forms import SeminarRegistrationForm


def index(request):
    latest_seminar_list = Seminar.objects.order_by('-date')

    latest_talk_list = [talk for seminar in latest_seminar_list
                        for talk in seminar.talk_set.all()]

    content_name = request.path.replace('/', '')
    if content_name == '':
        content_name = 'about'
    context = {
        'talks': latest_talk_list,
        'seminars': latest_seminar_list,
        'content': "programme/{}.html".format(content_name),
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
            return redirect('index')

    a = Attendees(seminar=Seminar.objects.get(id=seminar_id))
    form = SeminarRegistrationForm(instance=a)

    context = {
        'form': form,
        'seminar_id': seminar_id,
        'content': "programme/register.html",
    }
    return render(request, 'programme/index.html', context)
