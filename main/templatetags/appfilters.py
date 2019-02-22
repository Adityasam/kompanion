from django import template
from django.template.defaultfilters import stringfilter
from django.shortcuts import HttpResponse
from django.contrib import messages
register = template.Library()

@register.filter(name='splitdamage')
@stringfilter
def splitdamage(string):
    spal=string.split(",")
    sspal=spal[-1].split("/")
    if len(sspal) > 6:
        return sspal[8]
    else:
        return sspal[7]

@register.filter(name='tablet_history')
@stringfilter
def tablet_history(string):
    spal=string.split(",")
    
    tablets=[]
    for s in spal:
        tablet=[]
        sspal=s.split("/")
        for ss in sspal:
            tablet.append(ss)
        tablets.append(tablet)
    
    return tablets

@register.filter(name='get_name')
@stringfilter
def get_name(string):
    from main.models import Center
    cid=int(string)
    nam=Center.objects.get(center_id=cid)
    name=nam.name
    return name

@register.filter(name='spitdamage')
@stringfilter
def spitdamage(string):
    from main.models import Database
    db=Database.objects.get(id=string)
    pal=db.previous_allotment
    pc=db.previous_centers

    if pal != "":
        spal=pal.split(",")
        sspal=spal[-1].split("/")
        if sspal[6] == "D":
            return sspal[8]

    if pc != "":
        spal=pc.split(",")
        sspal=spal[-1].split("/")
        if sspal[5] == "D":
            return sspal[7]