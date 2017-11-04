from django.forms import formset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render

from adminPanel.forms import ConsumerViewsForm
from consumer.models import ConsumerMarketCamp
from customer.forms import MarketCampForm
from customer.models import MarketCamp
from mainApp.code import is_member
from mainApp.forms import PostIdForm






# получить страницу ошибки доступа к админской странице
from mainApp.views import getErrorPage


def adminError(request):
    return getErrorPage(request, 'Ошибка доступа', 'Эта страница доступна только администраторам')




def index(request):
    return HttpResponseRedirect('/')


def campanies(request):
    if not (is_member(request.user, "admins")):
        HttpResponseRedirect('/')
    cms = MarketCamp.objects.all().order_by('startTime')

    campanies = []
    for t in cms:
        campanies.append(
            {"viewPrice": t.viewPrice, "targetViewCnt": t.targetViewCnt,
             "platform": MarketCamp.platforms[t.platform],
             "cid": t.id, 'curViewCnt': t.curViewCnt, "isActive": t.isActive,
             "startTime": t.startTime.strftime("%d.%m.%y"),
             "endTime": t.endTime.strftime("%d.%m.%y"),
             })

    template = 'adminPanel/campanies.html'
    context = {
        'campanies': campanies,
        'caption': "Рекламные кампании"
    }
    return render(request, template, context)


def detailCampany(request, tid):
    mc = MarketCamp.objects.get(id=tid)

    if not (is_member(request.user, "admins")):
        return HttpResponseRedirect('/')

    if request.method == 'POST':
        # строим форму на основе запроса
        form = PostIdForm(request.POST)
        if form.is_valid():
            mc.vkPostID = form.cleaned_data["id"]
            mc.save()

    form = PostIdForm(initial={"id": mc.vkPostID})
    template = 'adminPanel/detail_campany.html'
    context = {
        "mc": mc,
        "id": tid,
        "form": form,
    }
    return render(request, template, context)


def approveCampany(request, tid):
    mc = MarketCamp.objects.get(id=tid)
    if not (is_member(request.user, "admins")):
        return HttpResponseRedirect('/')

    mc.adminApproved = 1
    mc.save()

    return HttpResponseRedirect('/adminPanel/campanies/')


def dismissCampany(request, tid):
    mc = MarketCamp.objects.get(id=tid)

    if not (is_member(request.user, "admins")):
        return HttpResponseRedirect('/')

    mc.adminApproved = 2
    mc.save()

    return HttpResponseRedirect('/adminPanel/campanies/')


def generateData():
    arr = []
    for mc in ConsumerMarketCamp.objects.filter(joinType=1):
        arr.append({'link': str(mc.link),
                    'cnt': str(mc.viewCnt),
                    'id': str(mc.pk)})
    return arr


def consumerViews(request):
    if not (is_member(request.user, "admins")):
        return HttpResponseRedirect('/')

    Formset = formset_factory(ConsumerViewsForm)
    if request.method == 'POST':
        formset = Formset(request.POST, request.FILES)
        if formset.is_valid():
            for form in formset.forms:
                if form.is_valid:
                    d = form.cleaned_data
                    # print(form.id)
                    try:
                        cnt = d["cnt"]
                        id = d["id"]
                        cm = ConsumerMarketCamp.objects.get(pk=id)
                        m = cm.marketCamp
                        m.curViewCnt += cnt-cm.viewCnt
                        m.save()
                        cm.viewCnt = cnt
                        cm.save()

                    except:
                        print("ошибка работы формы из формсета")
                else:
                    print("form is not valid")

    c = {'formset': Formset(initial=generateData()),

         }
    return render(request, "adminPanel/consumerViews.html", c)
