from django.http import HttpResponseRedirect
from django.shortcuts import render

from customer.forms import MarketCampForm
from customer.models import MarketCamp
from mainApp.code import is_member


def index(request):
    return HttpResponseRedirect('/')


def campanies(request):
    if not (is_member(request.user, "admins")):
        HttpResponseRedirect('/')
    cms = MarketCamp.objects.exclude(adminApproved=1).order_by('startTime')

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
    print(mc.adminApproved)

    if not (is_member(request.user, "admins")):
        return HttpResponseRedirect('/')

    template = 'adminPanel/detail_campany.html'
    context = {
        "mc": mc,
        "id": tid,
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
