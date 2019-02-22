from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from .models import Database, Center
from django.contrib.auth import login as auth_login, authenticate, logout
from django.contrib import messages
from datetime import date
from datetime import datetime
from pytz import timezone
from django.db.models import Q
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags

# Create your views here.

def home(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('main:admin_page')
        else:
            return redirect('main:centers')
    else:
        return redirect('main:original_home')

def login(request):
    if request.method == "POST":
        username=request.POST.get("username")
        password=request.POST.get("pass")

        user=authenticate(username=username,password=password)
        if user is not None:
            if user.is_active:
                if user.is_superuser:
                    auth_login(request,user)
                    return redirect('main:admin_page')
                else:
                    auth_login(request,user)
                    return redirect('main:centers')
            else:
                return HttpResponse("Your login has been deactivated")

        else:
            messages.error(request,"Wrong username or password")
            return render(request,'login.html')
    else:
        return render(request, 'login.html')

def centers(request): 
    tablets=Database.objects.filter(current_center=request.user.id)
    tablets_tobe_received=Database.objects.filter(current_center=request.user.id, received=False)
    free_tablets=Database.objects.filter(current_center=request.user.id, allotted=False, received=True, damaged=False)
    damaged=Database.objects.filter(current_center=request.user.id,damaged=True)
    return render(request, 'point.html', {'tablets':tablets, 'tablets_tobe_received':tablets_tobe_received,
    'free_tablets':free_tablets, 'damaged':damaged})

def original_home(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('main:admin_page')
        else:
            return redirect('main:centers')
    else:
        return render(request, 'home.html')

def logouts(request):
    logout(request)
    return redirect('main:original_home')

def admin_page(request):
    return render(request, "admin_page_new.html")

def detail(request, center_id):
    center_name=User.objects.get(id=center_id)
    allotted_tab=Database.objects.filter(current_center=center_id)
    tobe_received_tab=Database.objects.filter(current_center=center_id, received=False)
    damaged=Database.objects.filter(current_center=center_id, damaged=True)
    return render(request, 'center.html', {'center_name':center_name, 'allotted_tab':allotted_tab,
     'tobe_received_tab':tobe_received_tab, 'center_id':center_id, 'damaged':damaged})

def allot_center(request):
    if request.method == "POST":
        cen=Database.objects.all()
        counting=request.POST.get('count')
        center_id=request.POST.get('center_id')
        newcount=0
        if(counting == "1"):
            newcount=1
        else:
            newcount = int(counting)+1
        
        data=[]
        adate=""
        atime=""

        for i in range(int(counting)):
            imeilist=[]
            imname='im'+str(i+1)
            imeivalue=request.POST.get(imname)

            brname='brand'+str(i+1)
            brvalue=request.POST.get(brname)

            idname='tid'+str(i+1)
            tid=request.POST.get(idname)
            dat=request.POST.get('date')
            tim=request.POST.get('time')
            pc=center_id+"/"+dat+"/"+tim+"/"

            adate=dat
            atime=tim

            if imeivalue != '' and brvalue != '' and tid != '' and dat != '':
                imeilist.append(imeivalue)
                imeilist.append(brvalue)
                imeilist.append(tid)
                data.append(imeilist)

                d=Database()
                d.imei=imeivalue
                d.brand=brvalue
                d.tab_id=tid
                d.allotted_date=dat
                d.allotted_time=tim
                d.current_center=center_id
                d.previous_centers=pc
                d.save()

                cen=Center.objects.get(center_id=center_id)
                a=cen.allotted
                newal=a+1
                cen.allotted=newal
                cen.save()

            else:
                center_id=request.POST.get('center_id')
                messages.error(request,"All fields are required!")
                return redirect('main:detail', center_id=center_id)

        context = {
            'imei':data,
            'adate':adate,
            'atime':atime
        }
        to_mail=User.objects.get(id=center_id).email
        subject="New Tablets Allotted"
        from_email="tabletkadence@gmail.com"
        html_content = render_to_string('tablet_allotment_mail.html', context)
        text_content = strip_tags(html_content)
        msg = EmailMultiAlternatives(subject, text_content, from_email,[to_mail])
        msg.attach_alternative(html_content, "text/html")
        msg.send() 
        
        return render(request, "success.html", {'center_id':center_id})

def center_detail(request, center_id):
    center_name=User.objects.get(id=center_id)
    database=Database.objects.filter(current_center=center_id)
    return render(request, 'center_detail.html', {'center_name':center_name, 'database':database})

def tablet_transfer(request,tid,center_id):
    tab_detail=Database.objects.get(id=tid)
    return render(request, 'transfer.html', {'tab_detail':tab_detail, 'center_id':center_id})

def transfer(request):
    if request.method == "POST":
        tablet_id=request.POST.get("ids")

        tab=Database.objects.get(id=tablet_id)
        home_center=request.POST.get("cid")
        date=request.POST.get("date")
        transfer_center=request.POST.get("center")

        currentDT =datetime.now()
        h=currentDT.hour
        m=currentDT.minute

        hh=0
        mm='%02d' % m
        ampm=""
        if h > 12:
            hh='%02d' % (h-12)
            ampm="PM"
        else:
            hh='%02d' % h
            ampm="AM"

        t=str(hh)+":"+str(mm)+ampm

        pac=tab.previous_centers
        newpac=pac+"/"+date+"/"+t+"/"

        pc=Database.objects.get(id=tablet_id).previous_centers

        new_pc=newpac+","+transfer_center+"/"+date+"/"+t+"/"

        tab.allotted_date=date
        tab.received_date=None
        tab.received=False
        tab.current_center=transfer_center
        tab.previous_centers=new_pc
        tab.save()

        if tab.damaged == True:
            tab.under_maintenance=True
            tab.save()

        cen=Center.objects.get(center_id=transfer_center)
        a=cen.allotted
        newal=a+1
        cen.allotted=newal
        cen.save()

        c=Center.objects.get(center_id=home_center)
        s=c.allotted
        news=s-1
        c.allotted=news
        c.save()

        return redirect('main:center_detail', center_id=home_center)

def tobe(request):
    tablets=Database.objects.filter(current_center=request.user.id, received=False)
    return render(request, 'received.html', {'tablets':tablets})

def mark_received(request):
    if request.method == "POST":
        counting=request.POST.get("counting")
        data=[]
        adate=""
        atime=""
        for i in range(int(counting)):
            imeilist=[]
            c=i+1
            tname="check"+str(c)
            t=request.POST.get(tname)
            if t != None:
                print(tname+"/"+t)
                tab=Database.objects.get(id=t)
                
                imeilist.append(tab.imei)
                imeilist.append(tab.brand)
                imeilist.append(tab.tab_id)
                data.append(imeilist)

                currentDT =datetime.now()
                h=currentDT.hour
                m=currentDT.minute

                hh=0
                mm='%02d' % m
                ampm=""
                if h > 12:
                    hh='%02d' % (h-12)
                    ampm="PM"
                else:
                    hh='%02d' % h
                    ampm="AM"

                t=str(hh)+":"+str(mm)+ampm

                pc=tab.previous_centers
                string_date=date.today().strftime('%Y-%m-%d')
                new_pc=pc+string_date+"/"+t+"/"

                adate=string_date
                atime=t

                tab.received=True
                tab.received_date=date.today()
                tab.received_time=t
                tab.previous_centers=new_pc
                tab.save()
        
        context = {
            'imei':data,
            'adate':adate,
            'atime':atime,
            'center_name':request.user.username
        }
        to_mail="adityanathtiwari62@gmail.com"
        subject="Tablets Received"
        from_email=request.user.email
        html_content = render_to_string('receive_mail.html', context)
        text_content = strip_tags(html_content)
        msg = EmailMultiAlternatives(subject, text_content, from_email,[to_mail])
        msg.attach_alternative(html_content, "text/html")
        msg.send() 

        return redirect('main:tobe')

def allot_from_center(request):
    if request.method == "POST":
        allot=request.POST.get("allot0")
        project=request.POST.get("project0")
        tablet_id=request.POST.get("tablet_id")
        start=request.POST.get("s_date0")
        starttime=request.POST.get("time")
        end=request.POST.get("e_date0")

        if allot != "" and project != "" and tablet_id != "" and start != "" and end != "" and starttime != "":
            tab=Database.objects.get(id=tablet_id)
            pal=tab.previous_allotment
            newpal=""
            if pal != None and pal != '':
                newpal=pal+","+str(request.user.id)+"/"+allot+"/"+project+"/"+start+"/"+starttime+"/"+end+"/"+"ND"+"/"+"NC"+"/"
            else:
                
                newpal=str(request.user.id)+"/"+allot+"/"+project+"/"+start+"/"+starttime+"/"+end+"/"+"ND"+"/"+"NC"+"/"

            tab.allotted_to=allot
            tab.project=project
            tab.start_date=start
            tab.start_time=starttime
            tab.end_date=end
            tab.allotted=True
            tab.previous_allotment=newpal
            tab.save()

            return redirect('main:centers')
        else:
            messages.error(request,"All fields are required!")
            return redirect('main:centers')

def mark_damaged(request, tid):
    tab=Database.objects.get(id=tid)
    remark=request.POST.get("remark")

    if( tab.allotted == True):
        pal=tab.previous_allotment
        spal=pal.split(",")
        sspal=spal[-1].split("/")

        mypal=spal[:-1]
        newpal=",".join(mypal)

        lastpal=""
        mypals=[]
        for m in sspal:
            if(m == "ND"):
                mypals.append("D"+"/"+date.today().strftime('%Y-%m-%d')+"/"+remark+"/")
            else:
                mypals.append(m)

        newpals="/".join(mypals)
        if len(newpal) > 2:
            lastpal=newpal+","+newpals
        else:
            lastpal=newpals

        tab.damaged=True
        tab.previous_allotment=lastpal
        tab.save()
    else:
        pal=tab.previous_centers
        spal=pal.split(",")
        mypal=spal[:-1]
        newpal=",".join(mypal)
        lastpal=""
        mypals=[]

        mypals=spal[-1]+"D"+"/"+date.today().strftime('%Y-%m-%d')+"/"+remark+"/"

        if len(newpal) > 2: 
            lastpal=newpal+","+mypals
        else:
            lastpal=mypals
    
        tab.damaged=True
        tab.previous_centers=lastpal
        tab.save()

    if tab.allotted == True:
        return redirect('main:mark_complete', tid=tid)
    else:
        return redirect('main:centers')

def mark_complete(request, tid):
    tab=Database.objects.get(id=tid)

    pal=tab.previous_allotment
    spal=pal.split(",")
    sspal=spal[-1].split("/")

    currentDT =datetime.now()
    h=currentDT.hour
    m=currentDT.minute

    hh=0
    mm='%02d' % m
    ampm=""
    if h > 12:
        hh='%02d' % (h-12)
        ampm="PM"
    else:
        hh='%02d' % h
        ampm="AM"

    t=str(hh)+":"+str(mm)+ampm

    mypal=spal[:-1]
    newpal=",".join(mypal)

    lastpal=""
    mypals=[]
    for m in sspal:
        if(m == "NC"):
            mypals.append("C"+"/"+date.today().strftime('%Y-%m-%d')+"/"+t)
        else:
            mypals.append(m)

    newpals="/".join(mypals)
    if len(newpal) > 2:
        lastpal=newpal+","+newpals
    else:
        lastpal=newpals

    tab.allotted=False
    tab.allotted_to=None
    tab.start_date=None
    tab.end_date=None
    tab.project=None
    tab.previous_allotment=lastpal
    tab.save()

    return redirect('main:centers')

def update_tablet(request, tid):
    if request.method == "POST":
        tab=Database.objects.get(id=tid)
        imei=request.POST.get("imei")
        brand=request.POST.get("brand")
        tablet=request.POST.get("tablet_id")
        cid=request.POST.get("cid")

        tab.imei=imei
        tab.brand=brand
        tab.tab_id=tablet
        tab.save()
        return redirect('main:center_detail', center_id=cid)
        
def delete_tab(request, tid, cid):
    tab=Database.objects.get(id=tid)
    cenid=tab.current_center
    center=Center.objects.get(center_id=cenid)
    tabcount=center.allotted
    tabcount=tabcount-1
    center.allotted=tabcount
    center.save()
    tab.delete()
    return redirect('main:center_detail', center_id=cid)

def tablet_history(request, tid):
    tab=Database.objects.get(id=tid)
    return render(request, 'tablet_history.html', {'tablet':tab})

def all_tablets(request):
    tab=Database.objects.all()
    return render(request, 'all_tablets.html', {'tablets':tab})

def query(request):
    if request.method == "POST":
        q=request.POST.get("query")
        tablets=Database.objects.filter(
            Q(imei__icontains=q) |
            Q(brand__icontains=q) |
            Q(tab_id__icontains=q)
        ).distinct()

    return render(request, 'all_tablets_query.html', {'tablets':tablets})

def repair(request, tid, cid):
    tab=Database.objects.get(id=tid)

    currentDT =datetime.now()
    h=currentDT.hour
    m=currentDT.minute

    hh=0
    mm='%02d' % m
    ampm=""
    if h > 12:
        hh='%02d' % (h-12)
        ampm="PM"
    else:
        hh='%02d' % h
        ampm="AM"

    t=str(hh)+":"+str(mm)+ampm

    dr=tab.damage_record
    ndr=dr+date.today().strftime('%Y-%m-%d')+"/"+t+"/"

    tab.under_maintenance=True
    tab.damage_record=ndr
    tab.save()
    return redirect('main:center_detail', center_id=cid)

def repaired(request, tid):
    tab=Database.objects.get(id=tid)
    tab.damaged=False
    tab.under_maintenance=False
    tab.save()

    return redirect('main:centers')