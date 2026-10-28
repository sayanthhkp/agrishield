import random
import smtplib

import joblib
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import Group
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from datetime import datetime
from django.views.decorators.cache import never_cache
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

from myapp.classify import classify_image
from myapp.models import *


# Create your views here.
from myapp.static.chatbot.chatbotmain import get_response

try:
    from myapp.weather_check import get_weather_by_coordinates
except Exception as e:
    print("Error",e)

def login1(request):
    return render(request,'loginmain.html')

def login_post(request):
    name=request.POST['textfield']
    pwd=request.POST['textfield2']
    data=authenticate(request,username=name,password=pwd)
    if data is not None:
        login(request,data)
        if data.is_superuser:
            return HttpResponse("<script>alert('login succesfull');window.location='/adm_home'</script>")
        elif data.groups.filter(name='expert').exists():
            request.session['eid']=expert.objects.get(LOGIN=request.user.id).id
            return HttpResponse("<script>alert('login succesfull');window.location='/exp_home'</script>")

        else:
            return HttpResponse("<script>alert('Login failed password or id not match');window.location='/'</script>")
    else:
        return HttpResponse(
            "<script>alert('Login failed password or id not match');window.location='/'</script>")


def logouts(request):
    logout(request)
    return  redirect('/login1')

@login_required
@never_cache
def adm_add_expert(request):
    return render(request,'Admin/Addexpert.html')
def adm_add_exp_post(request):
    name=request.POST['textfield']
    email= request.POST['textfield2']
    phone = request.POST['textfield3']
    pin = request.POST['textfield4']
    post = request.POST['textfield5']
    lat = request.POST['textfield7']
    longni = request.POST['textfield8']


    if User.objects.filter(username=email).exists():
        return HttpResponse("<script>alert(' Exist ');window.location='/adm_add_expert#home'</script>")
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart

    # ✅ Gmail credentials (use App Password, not real password)
    sender_email = "agrisheild.co@gmail.com"
    receiver_email = email  # change to actual recipient
    app_password = "gdam klfr gwzm dykz"  # App Password from Google
    pwd = str(random.randint(1100, 9999))  # Example password to send
    request.session['otp'] = pwd
    request.session['email'] = email

    # Setup SMTP
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender_email, app_password)

    # Create the email
    msg = MIMEMultipart("alternative")
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = "Your OTP"

    # Plain text (backup)
    # text = f"""
    # Hello,

    # Your password for Smart Donation Website is: {pwd}

    # Please keep it safe and do not share it with anyone.
    # """

    # HTML (attractive)
    html = f"""
            <html>
              <body style="font-family: Arial, sans-serif; color: #333;">
                <h2 style="color:#2c7be5;">Wastemanagement</h2>
                <p>Hello,</p>
                <p>Your OTP is:</p>
                <p style="padding:10px; background:#f4f4f4; 
                          border:1px solid #ddd; 
                          display:inline-block;
                          font-size:18px;
                          font-weight:bold;
                          color:#2c7be5;">
                  {pwd}
                </p>
                <p>Please keep it safe and do not share it with anyone.</p>
                <hr>
                <small style="color:gray;">This is an automated email from Wastemanagement System.</small>
              </body>
            </html>
            """

    # Attach both versions
    # msg.attach(MIMEText(text, "plain"))
    msg.attach(MIMEText(html, "html"))

    # Send email
    server.send_message(msg)
    print("✅ Email sent successfully!")

    # Close connection
    server.quit()

    auth_usr=User()
    auth_usr.username=email
    auth_usr.password=make_password(pwd)
    auth_usr.save()

    group, created = Group.objects.get_or_create(name='expert')
    print(pwd)



    obj=expert()
    obj.name=name
    obj.phone=phone
    obj.email=email
    obj.post=post
    obj.pin=pin
    obj.latitude=lat
    obj.longitude=longni
    obj.LOGIN=auth_usr
    obj.save()

    return HttpResponse("<script>alert('expert added ');window.location='/adm_add_expert#home'</script>")






@login_required
@never_cache
def adm_edit_expert(request,id):
    data=expert.objects.get(id=id)
    return render(request,'Admin/editexpert.html',{'id':id,'data':data})
def adm_edit_expert_post(request,id):
    name=request.POST['textfield']
    phone = request.POST['textfield3']
    pin = request.POST['textfield4']
    post = request.POST['textfield5']
    lat = request.POST['textfield7']
    longni = request.POST['textfield8']
    if expert.objects.filter(name=name,phone=phone,pin=pin,post=post,latitude=lat,longitude=longni).exists():
        return HttpResponse(
            "<script>alert('Exist ');window.location='/adm_view_expert'</script>")

    expert.objects.filter(id=id).update(name=name,phone=phone,pin=pin,post=post,latitude=lat,longitude=longni)
    return HttpResponse("<script>alert('expert info edit successfull ');window.location='/adm_view_expert'</script>")

def adm_dlt_expert(request,id):
    expert.objects.filter(id=id).delete()

    return HttpResponse("<script>alert('expert delete successfull ');window.location='/adm_view_expert'</script>")

@login_required
@never_cache
def adm_view_expert(request):
    data=expert.objects.all()
    return render(request,'Admin/viewexpert.html', {"data":data})


@login_required
@never_cache
def adm_view_farmer(request):
    data = farmer.objects.all()
    return render(request,'Admin/viewfarmer.html',{"data":data})


@login_required
@never_cache
def adm_view_complaint(request):
    data = complaint.objects.all()
    return render(request,'Admin/Viewcomplaint.html', {"data":data})



@login_required
@never_cache
def adm_send_reply(request,id):
    return render(request,'Admin/sendreply.html',{'id':id})
def adm_send_reply_post(request,id):
    reply=request.POST['textarea']
    complaint.objects.filter(id=id).update(reply=reply,reply_date=datetime.now().date())
    return HttpResponse("<script>alert('request added ');window.location='/adm_view_complaint'</script>")



@login_required
@never_cache
def adm_home(request):
    return render(request, 'Admin/Adminhome.html')



@login_required
@never_cache
def adm_changepsswd(request):
    return render(request,'Admin/changepassword.html')
def adm_changepsswd_post(request):
    cpsswd=request.POST['textfield']
    npsswd = request.POST['textfield2']
    cnpsswd = request.POST['textfield3']

    check=check_password(cpsswd,request.user.password)
    if check:
        if npsswd == cnpsswd:
            usr=request.user
            usr.set_password(npsswd)
            usr.save()
            logout(request)
            return HttpResponse("<script>alert('password updated');window.location='/adm_changepsswd'</script>")
        else:
            return HttpResponse("<script>alert('password doesnot match');window.location='/adm_changepsswd'</script>")
    else:
        return HttpResponse("<script>alert('Incoorect old password');window.location='/adm_changepsswd'</script>")

# ===========Expert=================
#
#


@login_required
@never_cache
def exp_home(request):
    return render(request,'Expert/Expertindex.html')
    # return render(request,'Expert/experthome.html')


@login_required
@never_cache
def exp_add_tip(request):
    return render(request,'Expert/Addtip.html')
def exp_add_tip_post(request):
    tip= request.POST['textarea']
    date = datetime.now().date()

    if tips.objects.filter(tips=tip,date=date,EXPERT_id=request.session['eid']).exists():
        return HttpResponse("<script>alert('Exist');window.location='/exp_add_tip'</script>")

    obj=tips()
    obj.tips=tip
    obj.date=date
    obj.EXPERT_id=request.session['eid']
    obj.save()


    return HttpResponse("<script>alert('tips added');window.location='/exp_add_tip'</script>")




@login_required
@never_cache
def exp_edit_tip(request,id):
    data=tips.objects.get(id=id)
    return render(request,'Expert/edittip.html',{'id':id,'data':data})
def exp_edit_tip_post(request,id):
    tip=request.POST['textarea']
    tips.objects.filter(id=id).update(tips=tip,date=datetime.now().date())
    return HttpResponse("<script>alert('tips updated');window.location='/exp_view_tip'</script>")

@login_required
@never_cache
def exp_delete_tip(request,id):
    tips.objects.filter(id=id).delete()
    return HttpResponse("<script>alert('tip deleted');window.location='/exp_view_tip'</script>")


@login_required
@never_cache
def exp_view_tip(request):
    data = tips.objects.all()
    return render(request,'Expert/viewtip.html', {"data":data})



@login_required
@never_cache
def exp_add_news(request):
    return render(request,'Expert/Addnews.html')
def exp_add_news_post(request):
    news = request.POST['textarea']
    date = datetime.now().date()

    # ✅ CORRECT - .exists() is called on the queryset
    if farming_news.objects.filter(news=news, news_date=date, EXPERT_id=request.session['eid']).exists():
        return HttpResponse("<script>alert('news exist');window.location='/exp_add_news'</script>")

    obj = farming_news()
    obj.news = news
    obj.news_date = date
    obj.EXPERT_id = request.session['eid']
    obj.save()

    return HttpResponse("<script>alert('news added');window.location='/exp_add_news'</script>")

# @never_cachedef exp_add_news_post(request):
#     news=request.POST['textarea']
#     date = datetime.now().date()
#
#     if farming_news.objects.filter(news = news,_date = date,_id = request.session['eid'].exists()):
#         return HttpResponse("<script>alert('news exist');window.location='/exp_add_news'</script>")
#
#
#     obj =farming_news()
#     obj.news = news
#     obj.news_date = date
#     obj.EXPERT_id = request.session['eid']
#     obj.save()
#
#     return HttpResponse("<script>alert('news added');window.location='/exp_add_news'</script>")



@login_required
def exp_delete_news(request,id):
    farming_news.objects.filter(id=id).delete()
    return HttpResponse("<script>alert('news deleted');window.location='/exp_view_news'</script>")



@login_required
@never_cache
def exp_edit_news(request,id):
    data=farming_news.objects.get(id=id)

    return render(request,'Expert/Editnews.html',{'id':id,'data':data})
def exp_edit_news_post(request,id):
    new = request.POST['textarea']
    farming_news.objects.filter(id=id).update(news=new, news_date=datetime.now().date())
    return HttpResponse("<script>alert('news updated');window.location='/exp_view_news'</script>")




@login_required
@never_cache
def exp_view_news(request):
    data = farming_news.objects.all()
    return render(request,'Expert/Viewnews.html', {"data":data})



@login_required
@never_cache
def exp_add_price(request):
    return render(request,'Expert/Addprices.html')
def exp_add_price_post(request):
    corps = request.POST['textfield']
    prices = request.POST['textfield2']
    date = datetime.now().date()

    # ✅ CORRECT - .exists() is called on the queryset, and field name matches the model
    if marketing_prices.objects.filter(crops=corps, prices=prices, date=date, EXPERT_id=request.session['eid']).exists():
        return HttpResponse("<script>alert('price of crop exist');window.location='/exp_add_price'</script>")

    obj = marketing_prices()
    obj.crops = corps
    obj.prices = prices
    obj.date = date
    obj.EXPERT_id = request.session['eid']
    obj.save()
    return HttpResponse("<script>alert('price added');window.location='/exp_add_price'</script>")
# def exp_add_price_post(request):
#     corps = request.POST['textfield']
#     prices = request.POST['textfield2']
#     date = datetime.now().date()
#
#
#     if marketing_prices.objects.filter(crops=corps,prices = prices,date=date,_id=request.session['eid'].exists()):
#         return HttpResponse("<script>alert('price of crop exist');window.location='/exp_add_price'</script>")
#
#     obj=marketing_prices()
#     obj.crops=corps
#     obj.prices = prices
#     obj.date=date
#     obj.EXPERT_id=request.session['eid']
#     obj.save()
#     return HttpResponse("<script>alert('price added');window.location='/exp_add_price'</script>")




@login_required
@never_cache
def exp_edit_price(request,id):
    data = marketing_prices.objects.get(id=id)
    return render(request,'Expert/Editprices.html',{'id':id,'data':data})
def exp_edit_price_post(request,id):
    crop = request.POST['textfield']
    pri = request.POST['textfield2']
    marketing_prices.objects.filter(id=id).update(crops=crop,prices=pri,date=datetime.now().date())
    return HttpResponse("<script>alert('prices updated');window.location='/exp_view_price'</script>")


@login_required
@never_cache
def exp_delete_price(request,id):
    marketing_prices.objects.filter(id=id).delete()
    return HttpResponse("<script>alert('price deleted');window.location='/exp_view_price'</script>")


@login_required
@never_cache
def exp_view_price(request):
    data = marketing_prices.objects.all()
    return render(request,'Expert/Viewprices.html', {"data":data})


@login_required
@never_cache
def exp_add_subsidy(request):
    return render(request,'Expert/addsubsidydetails.html')
def exp_add_subsidy_post(request):
    subsidy_details = request.POST['textarea']
    subsidyn = request.POST['textfield']
    subsidy_fromdate = request.POST['textfield2']
    subsidy_todate = request.POST['textfield3']

    # ✅ CORRECT - Use proper field names that match your model
    if subsidy.objects.filter(
        subsidy=subsidyn,
        subsidy_details=subsidy_details,
        subsidy_fromdate=subsidy_fromdate,
        subsidy_todate=subsidy_todate,
        EXPERT_id=request.session['eid']
    ).exists():
        return HttpResponse("<script>alert('subsidy already exists');window.location='/exp_view_subsidy'</script>")

    obj = subsidy()
    obj.subsidy = subsidyn
    obj.subsidy_details = subsidy_details
    obj.subsidy_fromdate = subsidy_fromdate
    obj.subsidy_todate = subsidy_todate
    obj.EXPERT_id = request.session['eid']  # Also fixed: Expert_id → EXPERT_id
    obj.save()
    return HttpResponse("<script>alert('subsidy added');window.location='/exp_view_subsidy'</script>")
# def exp_add_subsidy_post(request):
#     subsidy_details = request.POST['textarea']
#     subsidyn = request.POST['textfield']
#     subsidy_fromdate = request.POST['textfield2']
#     subsidy_todate = request.POST['textfield3']
#
#     if subsidy.objects.filter(subsidy = subsidyn,_details = subsidy_details,_fromdate = subsidy_fromdate,_todate = subsidy_todate,_id = request.session['eid']).exists():
#         return HttpResponse("<script>alert('subsidy already exists');window.location='/exp_view_subsidy'</script>")
#
#
#     obj = subsidy()
#     obj.subsidy = subsidyn
#     obj.subsidy_details = subsidy_details
#     obj.subsidy_fromdate = subsidy_fromdate
#     obj.subsidy_todate = subsidy_todate
#     obj.Expert_id = request.session['eid']
#     obj.save()
#     return HttpResponse("<script>alert('subsidy added');window.location='/exp_view_subsidy'</script>")


@login_required
@never_cache
def exp_delete_subsidy(request,id):
    subsidy.objects.filter(id=id).delete()
    return HttpResponse("<script>alert('subsidy deleted');window.location='/exp_view_subsidy'</script>")



@login_required
@never_cache
def exp_edit_subsidy(request,id):
    data = subsidy.objects.get(id=id)
    return render(request,'Expert/editsubsidy.html',{'id':id,'data':data})
def exp_edit_subsidy_post(request,id):
    subsidy_details = request.POST['textarea']
    subsidyn = request.POST['textfield']
    subsidy_fromdate = request.POST['textfield2']
    subsidy_todate = request.POST['textfield3']
    subsidy.objects.filter(id=id).update(subsidy_details=subsidy_details,subsidy=subsidyn,subsidy_fromdate=subsidy_fromdate,subsidy_todate=subsidy_todate)
    return HttpResponse("<script>alert('subsidy updated');window.location='/exp_view_subsidy'</script>")



@login_required
@never_cache
def exp_view_subsidy(request):
    data = subsidy.objects.all()
    return render(request,'Expert/viewsubsidy.html', {"data":data})


@login_required
@never_cache
def exp_add_scheme(request):
    return render(request,'Expert/Addschemes.html')
def exp_add_scheme_post(request):
    schme_info = request.POST['textarea']
    file = request.FILES['fileField']
    fs = FileSystemStorage()
    file = fs.save(file.name, file)
    date = datetime.now().date()

    # ✅ FIXED - .exists() is now called on the queryset
    if schmes.objects.filter(
        schme_info=schme_info,
        file=fs.url(file),
        date=date,
        EXPERT_id=request.session['eid']
    ).exists():
        return HttpResponse("<script>alert('scheme already exist');window.location='/exp_add_scheme'</script>")

    obj = schmes()
    obj.schme_info = schme_info
    obj.file = fs.url(file)
    obj.date = date
    obj.EXPERT_id = request.session['eid']
    obj.save()
    return HttpResponse("<script>alert('scheme added');window.location='/exp_add_scheme'</script>")
# def exp_add_scheme_post(request):
#     schme_info = request.POST['textarea']
#     file=request.FILES['fileField']
#     fs=FileSystemStorage()
#     file=fs.save(file.name,file)
#     date = datetime.now().date()
#
#
#     if schmes.objects.filter(schme_info = schme_info,file = fs.url(file),date = date,_id = request.session['eid'].exists()):
#         return HttpResponse("<script>alert(' scheme already exist');window.location='/exp_add_scheme'</script>")
#
#
#     obj = schmes()
#     obj.schme_info = schme_info
#     obj.file = fs.url(file)
#     obj.date = date
#     obj.EXPERT_id = request.session['eid']
#     obj.save()
#     return HttpResponse("<script>alert('scheme added');window.location='/exp_add_scheme'</script>")



@login_required
@never_cache
def exp_edit_scheme(request,id):
    data = schmes.objects.get(id=id)
    return render(request,'Expert/Editschemes.html',{'id':id,'data':data})

def exp_edit_scheme_post(request,id):
    schme_info = request.POST['textarea']
    if 'fileField' in request.FILES:

        file = request.FILES['fileField']
        fs = FileSystemStorage()
        file = fs.save(file.name, file)
        schmes.objects.filter(id=id).update(file=fs.url(file))
    schmes.objects.filter(id=id).update(schme_info=schme_info,date=datetime.now().date())
    return HttpResponse("<script>alert('Scheme edited');window.location='/exp_view_scheme'</script>")


@login_required
@never_cache
def exp_delete_scheme(request,id):
    schmes.objects.filter(id=id).delete()
    return HttpResponse("<script>alert('schme deleted');window.location='/exp_view_scheme'</script>")


@login_required
@never_cache
def exp_view_scheme(request):
    data = schmes.objects.all()
    return render(request,'Expert/viewschemes.html', {"data":data})


@login_required
@never_cache
def exp_changepsswd(request):
    return render(request,'Expert/changepassword.html')
def exp_changepsswd_post(request):
    cpsswd=request.POST['textfield']
    npsswd = request.POST['textfield2']
    cnpsswd = request.POST['textfield3']

    check=check_password(cpsswd,request.user.password)
    if check:
        if npsswd == cnpsswd:
            usr=request.user
            usr.set_password(npsswd)
            usr.save()
            logout(request)
            return HttpResponse("<script>alert('password updated');window.location='/adm_changepsswd'</script>")
        else:
            return HttpResponse("<script>alert('password doesnot match');window.location='/adm_changepsswd'</script>")
    else:
        return HttpResponse("<script>alert('Incoorect old password');window.location='/adm_changepsswd'</script>")


@login_required
@never_cache
def index(request):
    return render(request,'index.html')




@login_required
@never_cache
def viewchat_farmer(request):
    data = chat.objects.filter(Expert=request.session['eid'])
    return render(request,'Expert/viewchat_farmer.html', {"data":data})



@login_required
@never_cache
def chatt(request, u):
    request.session['head'] = "CHAT"
    request.session['uid'] = u
    return render(request, 'Expert/chat.html', {'u': u})


def chatsnd(request, u):
    import datetime
    m = request.POST.get('m', '').strip()
    # Create and save chat message
    obj = chat(
        date=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),  # Added time
        type='Expert',
        Expert_id=request.session['eid'],
        FARMER_id=request.session['uid'],
        message=m
    )
    obj.save()

    return JsonResponse({"status": "ok", "message_id": obj.id})


def chatrply(request):
    last_id = request.POST.get('last_id', 0)
    try:
        last_id = int(last_id)
    except ValueError:
        last_id = 0

    # Get messages with proper ordering and filtering
    messages = chat.objects.filter(
        Expert=request.session['eid'],
        FARMER=request.session['uid'],
        id__gt=last_id  # Only get messages newer than last_id
    ).order_by('id')  # Ensure chronological order

    v = []
    for i in messages:
        v.append({
            'id': i.id,  # Include message ID for tracking
            'type': i.type,
            'chat': i.message,
            'selimage': '',  # You can add actual image paths here
            'uimage': '',  # You can add actual image paths here
            'date': i.date,
        })

    return JsonResponse({
        "status": "ok",
        "data": v,
        "count": len(v),
        "last_id": messages.last().id if messages else last_id
    })


#################################### USER MODULE ####################################################################

def viewtips(request):
    data = tips.objects.all()
    print(data)
    ar = []
    for i in data:
        ar.append({
            'id':i.id,
            'tips':i.tips,
            'date':i.date,
            'EXPERT':i.EXPERT.name,
            'eid':i.EXPERT.id,
        })
    print(ar)
    return JsonResponse({'status':'ok','message':ar})




def viewsubsidydetails(request):
    data=subsidy.objects.all()
    print(data)
    ar=[]
    for i in data:
        ar.append({
            'id':i.id,
            'subsidy_details':i.subsidy_details,
            'subsidy':i.subsidy,
            'subsidy_fromdate':i.subsidy_fromdate,
            'subsidy_todate':i.subsidy_todate,
        })
    print(ar)
    return JsonResponse({'status':'ok','message':ar})



def viewreplay(request):
    data=complaint.objects.all()
    print(data)
    ar=[]
    for i in data:
        ar.append({
            'id':i.id,
            'complaint':i.complaint,
            'complaint_date':i.complaint_date,
            'reply':i.reply,
            'reply_date':i.reply_date,

        })
    print(ar)
    return JsonResponse({'status':'ok','message':ar})


def viewprofile(request):
    fid=request.POST['fid']
    data=farmer.objects.filter(id=fid)
    print(data)
    ar=[]
    for i in data:
        ar.append({
            'id':i.id,
            'name':i.name,
            'email':i.email,
            'phone':i.phone,
            'pin':i.pin,
            'post':i.post,
            'place':i.place,
            'latitude':i.latitude,
            'longitude':i.longitude,
        })
    print(ar)
    return JsonResponse({'status':'ok','message':ar})



def viewnews(request):
    data=farming_news.objects.all()
    print(data)
    ar=[]
    for i in data:
        ar.append({
            'id':i.id,
            'news':i.news,
            'news_date':i.news_date,
            'EXPERT':i.EXPERT.name,
        })
    print(ar)
    return JsonResponse({'status':'ok','message':ar})
def viewmarketprocess(request):
    data=marketing_prices.objects.all()
    print(data)
    ar=[]
    for i in data:
        ar.append({
            'id':i.id,
            'crops':i.crops,
            'prices':i.prices,
            'date':i.date,

        })
    print(ar)
    return JsonResponse({'status':'ok','message':ar})



def viewgovtscheme(request):
    data=schmes.objects.all()
    print(data)
    ar=[]
    for i in data:
        ar.append({
            'id':i.id,
            'schme_info':i.schme_info,
            'date':i.date,
            'file':i.file,
        })
    print(ar)
    return JsonResponse({'status':'ok','message':ar})


def fregister(request):
    name=request.POST['name']
    email= request.POST['email']
    phone = request.POST['phone']
    pin = request.POST['pin']
    post = request.POST['post']
    place = request.POST['place']

    latitude = request.POST['latitude']
    longitude = request.POST['longitude']
    password = request.POST['password']
    confirmpassword = request.POST['confirmpassword']
    print(name,email,password,confirmpassword)



    if password == confirmpassword:
        auth_usr=User()
        auth_usr.username=email
        auth_usr.password=make_password(password)
        auth_usr.save()

        auth_usr.groups.add(Group.objects.get(name='farmer'))
        print(password)



        obj=farmer()
        obj.name=name
        obj.phone=phone
        obj.email=email
        obj.post=post
        obj.place=place
        obj.pin=pin
        obj.latitude=latitude
        obj.longitude=longitude
        obj.password=password
        obj.confirmpassword=confirmpassword
        obj.LOGIN=auth_usr
        obj.save()
        return JsonResponse({'status': 'ok'})

    return JsonResponse({'status':'invalid'})



def sendcomplaint(request):
    uid = request.POST['uid']
    complaints=request.POST['complaint']
    print(uid,complaints)
    obj=complaint()
    obj.complaint=complaints
    obj.complaint_date = datetime.now().date()
    obj.reply = "pending"
    obj.reply_date = "pending"
    obj.FARMER_id = uid
    obj.save()

    return JsonResponse({'status':'ok'})


def userlogin(request):
    name=request.POST['username']
    pwd=request.POST['password']
    data=authenticate(request,username=name,password=pwd)
    if data is not None:
        login(request,data)
        if data.groups.filter(name='farmer').exists():
            fid=farmer.objects.get(LOGIN=request.user.id).id
            fname=farmer.objects.get(LOGIN=request.user.id).name
            f_email=farmer.objects.get(LOGIN=request.user.id).email
            print("farmer", fid)
            return JsonResponse({'status':'ok', "fid":str(fid), "fname":fname, "f_email":f_email})

        else:
            return JsonResponse({'status':'no'})
    else:
        return JsonResponse({'status':'no'})


from geopy.geocoders import Nominatim
import socket
import requests
import json


def get_location_geopy():
    """
    Get current location using geopy with IP detection
    Install: pip install geopy
    """
    try:
        # Step 1: Get public IP
        def get_public_ip():
            try:
                response = requests.get('https://api.ipify.org?format=json', timeout=5)
                return response.json()['ip']
            except:
                # Fallback methods
                try:
                    response = requests.get('https://ipinfo.io/json', timeout=5)
                    return response.json()['ip']
                except:
                    return None

        # Step 2: Get location from IP
        def get_location_from_ip(ip_address):
            try:
                response = requests.get(f'http://ip-api.com/json/{ip_address}', timeout=5)
                data = response.json()

                if data['status'] == 'success':
                    return {
                        'ip': ip_address,
                        'latitude': data['lat'],
                        'longitude': data['lon'],
                        'city': data['city'],
                        'region': data['regionName'],
                        'country': data['country'],
                        'isp': data['isp'],
                        'timezone': data['timezone']
                    }
                return None
            except:
                return None

        # Step 3: Get detailed address using coordinates
        def get_address_from_coords(lat, lon):
            try:
                geolocator = Nominatim(user_agent="geo_locator_app")
                location = geolocator.reverse(f"{lat}, {lon}")

                if location:
                    address = location.raw.get('address', {})
                    return {
                        'display_name': location.address,
                        'road': address.get('road', ''),
                        'neighbourhood': address.get('neighbourhood', ''),
                        'suburb': address.get('suburb', ''),
                        'city': address.get('city', address.get('town', address.get('village', ''))),
                        'county': address.get('county', ''),
                        'state': address.get('state', ''),
                        'country': address.get('country', ''),
                        'postcode': address.get('postcode', '')
                    }
                return None
            except:
                return None

        # Get IP and location
        public_ip = get_public_ip()
        if not public_ip:
            print("❌ Could not get public IP")
            return None

        print(f"🌐 Public IP: {public_ip}")

        ip_location = get_location_from_ip(public_ip)
        if not ip_location:
            print("❌ Could not get location from IP")
            return None

        # Get detailed address
        detailed_address = get_address_from_coords(
            ip_location['latitude'],
            ip_location['longitude']
        )

        # Combine all information
        location_info = {
            'ip': ip_location['ip'],
            'latitude': ip_location['latitude'],
            'longitude': ip_location['longitude'],
            'city': ip_location['city'] or (detailed_address['city'] if detailed_address else 'Unknown'),
            'region': ip_location['region'],
            'country': ip_location['country'],
            'timezone': ip_location['timezone'],
            'isp': ip_location['isp'],
            'detailed_address': detailed_address,
            'full_address': detailed_address[
                'display_name'] if detailed_address else f"{ip_location['city']}, {ip_location['country']}"
        }

        # Print results
        print("\n📍 LOCATION INFORMATION:")
        print("=" * 50)
        print(f"Coordinates: {location_info['latitude']:.6f}, {location_info['longitude']:.6f}")
        print(f"City: {location_info['city']}")
        print(f"Region: {location_info['region']}")
        print(f"Country: {location_info['country']}")
        print(f"Timezone: {location_info['timezone']}")
        print(f"ISP: {location_info['isp']}")
        if detailed_address:
            print(f"Full Address: {detailed_address['display_name'][:100]}...")

        return location_info

    except Exception as e:
        print(f"Error getting location: {e}")
        return None



def user_getweather(request):
    # lati=request.POST['lati']
    # logi=request.POST['logi']
    loc=get_location_geopy()
    lati=loc['latitude']
    logi=loc['longitude']
    from myapp.weather_check import get_weather_by_coordinates
    weather_info=get_weather_by_coordinates(lati, logi)
    print(weather_info)
    ar=[]
    ar.append(weather_info)
    return JsonResponse({'status':'ok', "data":ar})



def user_sendchat(request):
    FROM_id=request.POST['from_id']
    TOID_id=request.POST['to_id']



    print(FROM_id, TOID_id,"Lk")



    msg=request.POST['message']
    print(msg)

    from  datetime import datetime
    c=chat()
    c.FARMER_id=FROM_id
    c.Expert_id=TOID_id
    c.message=msg
    c.date=datetime.now()
    c.type="farmer"
    c.save()
    return JsonResponse({'status':"ok"})

def user_viewchat(request):
    from_id=request.POST['from_id']
    to_id=request.POST['to_id']
    print(from_id,to_id)

    l=[]
    data=chat.objects.filter(FARMER_id=from_id,Expert_id=to_id).order_by('id')
    print(data)

    for res in data:
        l.append({'id':res.id,'from':res.FARMER.id,'to':res.Expert.id,'msg':res.message,'date':res.date,"type":res.type})

    return JsonResponse({'status':"ok",'data':l})

###   passsss

def forgotpassword(request):
    return render(request,"forgotpassword.html")

def forgotpasswordbuttonclick(request):
    email = request.POST['textfield']
    if User.objects.filter(username=email).exists():
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart

        # ✅ Gmail credentials (use App Password, not real password)
        sender_email = "agrisheild.co@gmail.com"
        receiver_email = email  # change to actual recipient
        app_password = "gdam klfr gwzm dykz"  # App Password from Google
        pwd = str(random.randint(1100,9999))  # Example password to send
        request.session['otp'] = pwd
        request.session['email'] = email

        # Setup SMTP
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, app_password)

        # Create the email
        msg = MIMEMultipart("alternative")
        msg["From"] = sender_email
        msg["To"] = receiver_email
        msg["Subject"] = "Your OTP"

        # Plain text (backup)
        # text = f"""
        # Hello,

        # Your password for Smart Donation Website is: {pwd}

        # Please keep it safe and do not share it with anyone.
        # """

        # HTML (attractive)
        html = f"""
        <html>
          <body style="font-family: Arial, sans-serif; color: #333;">
            <h2 style="color:#2c7be5;">Wastemanagement</h2>
            <p>Hello,</p>
            <p>Your OTP is:</p>
            <p style="padding:10px; background:#f4f4f4; 
                      border:1px solid #ddd; 
                      display:inline-block;
                      font-size:18px;
                      font-weight:bold;
                      color:#2c7be5;">
              {pwd}
            </p>
            <p>Please keep it safe and do not share it with anyone.</p>
            <hr>
            <small style="color:gray;">This is an automated email from Wastemanagement System.</small>
          </body>
        </html>
        """

        # Attach both versions
        # msg.attach(MIMEText(text, "plain"))
        msg.attach(MIMEText(html, "html"))

        # Send email
        server.send_message(msg)
        print("✅ Email sent successfully!")

        # Close connection
        server.quit()
        return HttpResponse("<script>window.location='/otp'</script>")
    else:
        return HttpResponse("<script>alert('Email not found');window.location='/forgotpassword'</script>")

def otp(request):
    return render(request,"otp.html")
def otpbuttonclick(request):
    otp  = request.POST["textfield"]
    if otp == str(request.session['otp']):
        return HttpResponse("<script>window.location='/forgotpswdpswed'</script>")
    else:
        return HttpResponse("<script>alert('incorrect otp');window.location='/otp'</script>")

def forgotpswdpswed(request):
    return render(request,"forgotpswdpswed.html")
def forgotpswdpswedbuttonclick(request):
    np = request.POST["password"]
    User.objects.filter(username=request.session['email']).update(password=make_password(np))
    return HttpResponse("<script>alert('password has been changed');window.location='/' </script>")




###################         MAIN

def crop_predict(request):
    uploaded_file = request.FILES['file']
    print(uploaded_file, "pppppppppppppppppp")
    dt = datetime.now().strftime("%Y%m%d-%H%M%S") + ".png"
    if uploaded_file:
        try:
            # Save the file in the MEDIA_ROOT directory
            with open(
                    f'/Users/siva/Desktop/To get a job/Agri-ai/agri-web/myapp/static/uploads/{dt}',
                    'wb') as f:
                for chunk in uploaded_file.chunks():
                    f.write(chunk)
        except Exception as e:
            pass

    path = f'/Users/siva/Desktop/To get a job/Agri-ai/agri-web/myapp/static/uploads/{dt}'
    data, score = classify_image(path)
    output_data = {
        "apple black rot": {"plant": "Apple", "disease": "Black Rot"},
        "apple apple scab": {"plant": "Apple", "disease": "Apple Scab"},
        "apple cedar apple rust": {"plant": "Apple", "disease": "Cedar Apple Rust"},
        "tomato septoria leaf spot": {"plant": "Tomato", "disease": "Septoria Leaf Spot"},
        "tomato bacterial spot": {"plant": "Tomato", "disease": "Bacterial Spot"},
        "apple healthy": {"plant": "Apple", "disease": "Healthy"},
        "tomato healthy": {"plant": "tomato", "disease": "healthy"},
        "pepper bell bacterial spot": {"plant": "pepper", "disease": "bell bacterial spot"},
        "tomato early blight": {"plant": "tomato", "disease": "early blight"},
        "tomato target spot": {"plant": "tomato", "disease": "target spot"},
        "tomato tomato mosaic virus": {"plant": "tomato", "disease": "tomato mosaic virus"},
        "pepper bell healthy": {"plant": "pepper", "disease": "bell healthy"},
        "tomato tomato yellowleaf curl virus": {"plant": "tomato", "disease": "tomato yellowleaf curl virus"},
        "corn maize cercospora leaf spot gray leaf spot": {"plant": "corn","disease": "maize cercospora leaf spot gray leaf spot"},
        "tomato leaf mold": {"plant": "tomato", "disease": "leaf mold"},
        "corn maize healthy": {"plant": "corn maize", "disease": "healthy"},
        "corn maize common rust": {"plant": "corn maize", "disease": "common rust"},
        "corn maize northern leaf blight": {"plant": "corn maize", "disease": "northern leaf blight"},
    }
    print("Plant name  ", output_data[data]['plant'])
    print("Disease name  ", output_data[data]['disease'])
    print("Matching Score  ", score, "%")
    fert_list = {
        "apple black rot": "Recommended Fungicide to use \n FRAC Group 7 (SDHIs): Luna Sensation (7 + 11), Merivon (7 + 11), Fontelis (7) \nFRAC Group 11 (QoIs - Strobilurins): Flint (11), Sovran (11), Pristine (11 + 7) \nFRAC Group 3 (DMI - Sterol Inhibitors): Inspire Super (3 + 9), Rally (3), Cevya (3)",
        "apple apple scab": "Recommended Fungicide to use \n FRAC Group M: Multi-Site Inhibitors (Protectants - Low Resistance Risk) \nFRAC Group 3: Demethylation Inhibitors (DMIs) - Sterol Inhibitors \nFRAC Group 7: Succinate Dehydrogenase Inhibitors (SDHIs)",
        "apple cedar apple rust": "Recommended Fungicide to use \n  FRAC Group 3: Demethylation Inhibitors (DMIs) - Sterol Inhibitors \nFRAC Group 11: Quinone Outside Inhibitors (QoIs) - Strobilurins \nFRAC Group 7: Succinate Dehydrogenase Inhibitors (SDHIs)",
        "tomato septoria leaf spot": "Recommended Fungicide to use \n FRAC Group M: Multi-Site Inhibitors (Protectants - Low Resistance Risk) \nFRAC Group 11: Quinone Outside Inhibitors (QoIs) - Strobilurins \nFRAC Group 7: Succinate Dehydrogenase Inhibitors (SDHIs))",
        "tomato bacterial spot": "Recommended Fungicide to use \nCopper-Based Bactericides (The Cornerstone) \nEBDC Fungicides (Mancozeb) - The Essential Tank-Mix Partner \nSystemic Acquired Resistance (SAR) Inducers)",
        "apple healthy": "No Fungicide is required ",
        "tomato healthy": "No Fungicide is required ",
        "pepper bell bacterial spot": "Recommended Fungicide to use \nCopper-Based Bactericides (The Standard Baseline) \nMancozeb (EBDC) - The Essential Synergist \nSystemic Acquired Resistance (SAR) Inducers",
        "tomato early blight": "Recommended Fungicide to use \nFRAC Group M: Multi-Site Protectants (Low Resistance Risk) \n FRAC Group 11: Quinone Outside Inhibitors (QoIs) - Strobilurins \nFRAC Group 7: Succinate Dehydrogenase Inhibitors (SDHIs)",
        "tomato target spot": "Recommended Fungicide to use \nFRAC Group M: Multi-Site Protectants (Low Resistance Risk)\n  FRAC Group 7: Succinate Dehydrogenase Inhibitors (SDHIs) \nFRAC Group 9: Anilinopyrimidines",
        "tomato tomato mosaic virus ": "Recommended Fungicide to use \nExclusion: Start with Clean Seed & Transplants\n  Sanitation: The Non-Negotiable Practice \nGenetic Resistance: The Most Reliable Long-Term Solution",
        "pepper bell healthy ": "No Fungicide is required",
        "tomato tomato yellowleaf curl virus ": "Recommended Fungicide to use \nPillar 1: Vector Control Agents (Insecticides & Biocontrols)\n Exclusion & Sanitation Agents \nGenetic Resistance Agents (The Most Critical Tool)",
        "corn maize cercospora leaf spot gray leaf spot ": "Recommended Fungicide to use \nFRAC Group 11: Quinone Outside Inhibitors (QoIs) - Strobilurins\n  FRAC Group 3: Demethylation Inhibitors (DMIs) - Triazoles \nFRAC Group 7: Succinate Dehydrogenase Inhibitors (SDHIs)",
        "tomato leaf mold": "Recommended Fungicide to use \n FRAC Group M: Multi-Site Protectants (Low Resistance Risk)\n FRAC Group 11: Quinone Outside Inhibitors (QoIs) - Strobilurins\nFRAC Group 7: Succinate Dehydrogenase Inhibitors (SDHIs)",
        "corn maize healthy": "No Fungicide is required",
        "corn maize common rust": "Recommended Fungicide to use \n FRAC Group 11: Quinone Outside Inhibitors (QoIs) - Strobilurins\n . FRAC Group 3: Demethylation Inhibitors (DMIs) - Triazoles\nFRAC Group 7: Succinate Dehydrogenase Inhibitors (SDHIs)",
        "corn maize northern leaf blight": "Recommended Fungicide to use \n FRAC Group 11: Quinone Outside Inhibitors (QoIs) - Strobilurins\n  FRAC Group 3: Demethylation Inhibitors (DMIs) - Triazoles\n FRAC Group 7: Succinate Dehydrogenase Inhibitors (SDHIs)",

    }
    print("Recommendation")
    print(fert_list[data])

    return JsonResponse({"res": "true", "crop_disease": output_data[data]['disease'] + " in " + output_data[data]['plant'],
                         "fert": fert_list[data]})



# forgot password flutter




def forgotemail(request):
    import random
    import smtplib
    email = request.POST['email']
    print(email)
    data = User.objects.filter(username=email)
    print(data)
    if data.exists():
        otp = str(random.randint(000000, 999999))
        print(otp)
        # *✨ Python Email Codeimport smtplib*

        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart

        # ✅ Gmail credentials (use App Password, not real password)
        try:
            sender_email = "agrisheild.co@gmail.com"
            receiver_email = "receiver_email@gmail.com"  # change to actual recipient
            app_password = "pthc hmrx niip xszn"
            # Setup SMTP
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(sender_email, app_password)

            # Create the email
            msg = MIMEMultipart("alternative")
            msg["From"] = sender_email
            msg["To"] = receiver_email
            msg["Subject"] = "🔑 Forgot Password "

            # Plain text (backup)
            # text = f"""
            # Hello,

            # Your password for Smart Donation Website is: {pwd}

            # Please keep it safe and do not share it with anyone.
            # """

            # HTML (attractive)
            html = f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>Password Reset OTP</title>
                </head>
                <body style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                            line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px;">

                    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                                padding: 30px; text-align: center; border-radius: 10px 10px 0 0;">
                        <h1 style="color: white; margin: 0; font-size: 28px;">
                            🔐 Smart Donation
                        </h1>
                    </div>

                    <div style="background-color: #f9f9f9; padding: 40px 30px; border-radius: 0 0 10px 10px; 
                                border: 1px solid #eaeaea;">

                        <h2 style="color: #2d3748; margin-top: 0;">Password Reset Request</h2>

                        <p style="color: #4a5568; font-size: 16px;">
                            Hello,
                        </p>

                        <p style="color: #4a5568; font-size: 16px;">
                            You requested to reset your password. Use the OTP below to proceed:
                        </p>

                        <div style="background: white; border-radius: 8px; padding: 20px; 
                                    text-align: center; margin: 30px 0; border: 2px dashed #cbd5e0;">
                            <div style="font-size: 32px; font-weight: bold; letter-spacing: 10px; 
                                        color: #2c7be5; margin: 10px 0;">
                                {otp}
                            </div>
                            <div style="font-size: 14px; color: #718096; margin-top: 10px;">
                                (Valid for 10 minutes)
                            </div>
                        </div>

                        <p style="color: #4a5568; font-size: 16px;">
                            Enter this code on the password reset page to complete the process.
                        </p>

                        <div style="background-color: #fef3c7; border-left: 4px solid #d97706; 
                                    padding: 15px; margin: 25px 0; border-radius: 4px;">
                            <p style="color: #92400e; margin: 0; font-size: 14px;">
                                ⚠️ <strong>Security tip:</strong> Never share this OTP with anyone. 
                                Our team will never ask for your password or OTP.
                            </p>
                        </div>

                        <p style="color: #718096; font-size: 14px;">
                            If you didn't request this password reset, please ignore this email or 
                            contact our support team if you have concerns.
                        </p>

                        <hr style="border: none; border-top: 1px solid #e2e8f0; margin: 30px 0;">

                        <p style="text-align: center; color: #a0aec0; font-size: 12px;">
                            This is an automated email from Smart Donation System.<br>
                            © {datetime.now().year} Smart Donation. All rights reserved.
                        </p>

                    </div>
                </body>
                </html>
                """

            # Attach both versions
            # msg.attach(MIMEText(text, "plain"))
            msg.attach(MIMEText(html, "html"))

            # Send email
            server.send_message(msg)
            print("✅ Email sent successfully!", otp)

            # Close connection
            server.quit()

        except Exception as e:
            print("❌ Error loading email credentials:", e)
            return JsonResponse({'status': "ok", 'otpp': otp})

        return JsonResponse({'status': 'ok', 'otpp': otp})
    return JsonResponse({'status': "not found"})


def forgotpass(request):
    email = request.POST['email']
    npass = request.POST['password']
    cpass = request.POST['confirmpassword']
    print(email, npass, cpass)
    if npass == cpass:
        User.objects.filter(username=email).update(password=make_password(npass))
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'invalid'})

def soil_crop_recommendation(request):
    """
    API endpoint to analyze soil parameters and recommend best crop using Gemini AI
    """
    try:
        # Parse incoming JSON data
        data = json.loads(request.body)

        # Extract and validate parameters
        required_fields = ['temperature', 'humidity', 'moisture', 'nitrogen', 'phosphorus', 'potassium', 'soil_type']
        print(data)
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return JsonResponse({
                'success': False,
                'error': f'Missing required fields: {", ".join(missing_fields)}'
            })

        # Extract values
        temperature = float(data['temperature'])
        humidity = float(data['humidity'])
        moisture = float(data['moisture'])
        print(temperature, humidity, moisture)
        nitrogen = float(data['nitrogen'])
        phosphorus = float(data['phosphorus'])
        potassium = float(data['potassium'])
        soil_type = data['soil_type'].lower()


        # Validate numerical ranges
        if not (0.0 <= temperature <= 50):
            return JsonResponse({
                'success': False,
                'error': 'Temperature must be between 0-50°C'
            })

        if not (0.0 <= humidity <= 100):
            return JsonResponse({
                'success': False,
                'error': 'Humidity must be between 0-100%'
            })

        if not (0.0 <= moisture <= 2000):
            return JsonResponse({
                'success': False,
                'error': 'Moisture must be between 0-2000mBar'
            })

        soil_mapping = {"black": 0, "clayey": 1, "loamy": 2, "red": 3, "sandy": 4}
        crop_list = ["Barley", "Cotton", "Ground Nuts", "Maize", "Millets", "Oil Seeds", "Paddy", "Pulses", "Sugarcane","Tobacco", "Wheat"]
        data = [temperature, humidity, moisture, soil_type, nitrogen, potassium, phosphorus]
        data[3] = soil_mapping[data[3]]
        print(data)

        model = joblib.load(r"\Users\siva\Desktop\To get a job\Agri-ai\agri-web\myapp\static\rf_model.joblib")
        pred = model.predict([data])
        idx=pred[0]
        print("Pred ", idx)
        # Get crop recommendation from Gemini AI
        recommendation = crop_list[int(idx)]

        # Prepare response data
        response_data = {
            'success': True,
            'crop_recommendation': recommendation,
            'timestamp': datetime.now().strftime("%d-%m-%Y")  # Simplified timestamp
        }

        print(f"Crop recommendation generated for soil type: {soil_type}", "\nCrop : ",recommendation)
        return JsonResponse(response_data)

    except ValueError as e:
        return JsonResponse({
            'success': False,
            'error': f'Invalid parameter value: {str(e)}'
        })

    except Exception as e:
        print(f"Error in soil_crop_recommendation: {str(e)}")
        return JsonResponse({
            'success': False,
            'error': 'Internal server error'
        })


#   chatbot
def flutter_add_chatbot(request):
    fid=request.POST['fid']
    msg=request.POST['message']
    obj=chatbot()
    obj.FARMER_id=fid
    obj.message=msg
    obj.date=datetime.now().date()
    obj.type="farmer"
    obj.save()
    response=get_response(msg)
    obj=chatbot()
    obj.FARMER_id=fid
    obj.message=response
    obj.date=datetime.now().date()
    obj.type="chatbot"
    obj.save()
    return JsonResponse({'status':"ok"})

def flutter_view_chatbot(request):
    fid=request.POST['fid']
    res=chatbot.objects.filter(FARMER_id=fid)
    ar=[]
    for i in res:
        ar.append({
            "msg":i.message, 'date':i.date, 'type':i.type, 'id':i.id
        })
    print(ar)
    return JsonResponse({'status':'ok', 'data':ar})