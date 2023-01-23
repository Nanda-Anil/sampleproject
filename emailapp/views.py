import uuid

from django.contrib.auth import authenticate
from django.http import HttpResponse

from .models import *

from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import *
from django.core.mail import send_mail
from djemail.settings import EMAIL_HOST_USER
# Create your views here.


def regis(request):
    a=register()
    return render(request,'reg.html',{'form':a})
    #a ye formilek pass cheythu

# email sendingnte formene html page ayt convert cheyyan ulla function

def email_send(request):
    a=contactusform()

    if request.method=='POST':
        # post vazhi kittiya datas ellam sub enna variablelek store
        sub=contactusform(request.POST)
    #     vannirikuna datas valid anon check cheyynam
        if sub.is_valid():
            nm=sub.cleaned_data['Name']
            em=sub.cleaned_data['Email']
            ms=sub.cleaned_data['Message']
            #         ee datas ne mail lek send cheyynam...
            #         oru server ninn mattoru serverlek send cheyyan use cheyuna function ahn send_mail()
            #         send_mail(subject,message,EMAIL_HOST_USER,[EMAIL])
            send_mail(str(nm)+"||",ms,EMAIL_HOST_USER,[em])
        return render(request,'success.html')
    return render(request,'email.html',{'forms':a})


def registration(request):
    if request.method=='POST':
        username=request.POST.get('username')
        # request chyth POST vazhi kittiya username ne username enna variablek store akunu
        email=request.POST.get('email')
        password=request.POST.get('password')
        if User.objects.filter(username=username).first():
            # it will get first object from filter query. nammal kodtha username already stored anon nokunu
            messages.success(request,'username already taken')
            # enth message ano request pageil displaay cheyyendath..athan message.succesil kodukunnath
            return redirect(registration)
        # same pagel refresh cheyth nikkan vendi..
        # aa pagel thanne message display cheyikan

        if User.objects.filter(email=email).first():
            messages.success(request,'email already taken')
            return redirect(registration)

        # ee rand if um work avunilelnkil new user aanen manasilakum..appo ath store akan object creation.
        # inbuild nu vendi object creation
        # user name and email direct saved to user_obj..bt password secure akan vendi seperate ayit set_password vech store cheyunu
        user_obj=User(username=username, email=email)
        user_obj.set_password(password)
        user_obj.save()
         # site authenticated ayond nalla security ayirikum
        # auth token creation....uuid vech generate cheyikuna token string akiyt auth token enna variablek store
        auth_token=str(uuid.uuid4())

#         user defined field nu vendi function creation-->profiile object
        profile_obj=profile.objects.create(user=user_obj,auth_token=auth_token)
        profile_obj.save()
# ethrem ok ane oru function work cheyyanam
#         passing email and auth_token in a function
        send_mail_regis(email,auth_token)
        return render(request,'success.html')
    return render(request,'register.html')

# molilathe send_ail_regis funcion creation

def send_mail_regis(email,auth_token):
    subject="your account has been verified"
    # f is a string formatting function
    message=f'paste the link to verify your account http://127.0.0.1:8000/emailapp/verify/{auth_token}'
    email_from=EMAIL_HOST_USER
    recipient=[email]
    send_mail(subject,message,email_from,recipient)
#     ee fucntionu url creation venda..bc.. return cheyikunnila ath,,


# molilathe http pathile verify function creation

def verify(request,auth_token):
    # auth tokene verify cheyyan request cheyunu
    # aa kodtha tokene already ulla token  ayit compare chyth filter chyunu,ennit athil first varunna ale return chyth profile_obj enna variablek store
    profile_obj=profile.objects.filter(auth_token=auth_token).first()
    if profile_obj:
        # profile object already use cheythenkil...ath verfified anon nokunu..default ayt verify value false aki set chythitund in models.
        if profile_obj.is_verified:
            # if profile object is false
            messages.success(request,'your account is already verified')
            return redirect(login)
        # athalla profile object athil illenkil..new token anen manasilakunnu..athine save cheyunu
        profile_obj.is_verified=True
        profile_obj.save()
        messages.success(request,'your account has been verified')
        return redirect(login)
    else:
        messages.success(request,'user not found')
        return redirect(login)

# # login pagenu vendi function
#
# def login(request):
#     return render(request,'login.html')

# login page full function:

def login(request):
    if request.method=='POST':
        # request cheyth kttiya method post anenkil, oro variableslek aa fieldsle values ne post vazhi get chytht store
        username=request.POST.get('username')
        password=request.POST.get('password')
        # user_objects enna inbuild modelsl kodtha datayil ippo kodtha username undon filter chyth nokunu
        user_obj=User.objects.filter(username=username).first()
        if user_obj is None:
            # angane oru user exist cheyunila enkil
            messages.success(request,'user not found')
            return redirect(login)
        # profile models le datayumayt compare
        profile_obj=profile.objects.filter(user=user_obj).first()
        if not profile_obj.is_verified:
            # if not profile object is false.....> mail chennitum athil click cheyyatha un verified user anenkil
            messages.success(request,'profile not verified check your mail')
            return redirect(login)
        #  user valid anon authenticate function vazhi check cheyunu
        user=authenticate(username=username,password=password)
        # authenticate---> if the given credentials are valid, it returns a user object
        if user is None:
            # user valid allenkil
            messages.success(request,'wrong password or username')
            return redirect(login)
        return HttpResponse('success')
    return render(request,'login.html')