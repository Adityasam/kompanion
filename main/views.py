from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from .models import Database, Center
from django.contrib.auth import login as auth_login, authenticate, logout
from django.contrib import messages
from datetime import date
from datetime import datetime
# Create your views here.

def home(request):
    if request.user.is_superuser:
        return redirect('main:admin_page')
    else:
        return redirect('main:centers')

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

    return render(request, 'point.html', {'tablets':tablets, 'tablets_tobe_received':tablets_tobe_received,
    'free_tablets':free_tablets})

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
    return render(request, 'center.html', {'center_name':center_name, 'allotted_tab':allotted_tab,
     'tobe_received_tab':tobe_received_tab, 'center_id':center_id})

def allot_center(request):
    if request.method == "POST":
        cen=Database.objects.all()
        counting=request.POST.get('count')
        newcount=0
        if(counting == "1"):
            newcount=1
        else:
            newcount = int(counting)+1
        
        for i in range(int(counting)):
            imname='im'+str(i+1)
            imeivalue=request.POST.get(imname)

            brname='brand'+str(i+1)
            brvalue=request.POST.get(brname)

            idname='tid'+str(i+1)
            tid=request.POST.get(idname)
            dat=request.POST.get('date')
            center_id=request.POST.get('center_id')
            pc=center_id+"/"+dat+"/"+""

            if imeivalue != '' and brvalue != '' and tid != '' and dat != '':
                d=Database()
                d.imei=imeivalue
                d.brand=brvalue
                d.tab_id=tid
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

        pac=tab.previous_centers
        newpac=pac+date+"/"

        pc=Database.objects.get(id=tablet_id).previous_centers

        new_pc=newpac+","+transfer_center+"/"+date+"/"+""

        tab.allotted_date=date
        tab.received_date=None
        tab.received=False
        tab.current_center=transfer_center
        tab.previous_centers=new_pc
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

def mark_received(request, tid):
    tab=Database.objects.get(id=tid)
    
    pc=tab.previous_centers
    string_date=date.today().strftime('%Y-%m-%d')
    new_pc=pc+string_date+"/"

    tab.received=True
    tab.received_date=date.today()
    tab.previous_centers=new_pc
    tab.save()

    return redirect('main:tobe')

def allot_from_center(request):
    if request.method == "POST":
        allot=request.POST.get("allot0")
        project=request.POST.get("project0")
        tablet_id=request.POST.get("tablet_id")
        start=request.POST.get("s_date0")
        end=request.POST.get("e_date0")

        if allot != "" and project != "" and tablet_id != "" and start != "" and end != "":
            tab=Database.objects.get(id=tablet_id)
            pal=tab.previous_allotment
            newpal=""
            if pal != None and pal != '':
                newpal=pal+","+str(request.user.id)+"/"+allot+"/"+project+"/"+start+"/"+end+"/"+"ND"+"/"+"NC"+"/"
            else:
                
                newpal=str(request.user.id)+"/"+allot+"/"+project+"/"+start+"/"+end+"/"+"ND"+"/"+"NC"+"/"

            tab.allotted_to=allot
            tab.project=project
            tab.start_date=start
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
                mypals.append("D"+"/"+date.today().strftime('%Y-%m-%d')+"/"+remark)
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

        mypals=spal[-1]+"D"+"/"+date.today().strftime('%Y-%m-%d')+"/"+remark

        if len(newpal) > 2: 
            lastpal=newpal+","+mypals
        else:
            lastpal=mypals
    
        tab.damaged=True
        tab.previous_centers=lastpal
        tab.save()

    return redirect('main:centers')

def mark_complete(request, tid):
    tab=Database.objects.get(id=tid)

    pal=tab.previous_allotment
    spal=pal.split(",")
    sspal=spal[-1].split("/")

    mypal=spal[:-1]
    newpal=",".join(mypal)

    lastpal=""
    mypals=[]
    for m in sspal:
        if(m == "NC"):
            mypals.append("C"+"/"+date.today().strftime('%Y-%m-%d'))
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
        tablet=request.POST.get("tablet_id")
        cid=request.POST.get("cid")

        tab.imei=imei
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