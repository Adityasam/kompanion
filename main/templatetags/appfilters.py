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
        return sspal[7]
    else:
        return sspal[5]

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


   