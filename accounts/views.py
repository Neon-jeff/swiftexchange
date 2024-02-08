from django.shortcuts import render,redirect
from .handlers import FetchCoinData
from django.http import JsonResponse
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages

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
                return redirect('dashboard')
        else:
            messages.error(request,'No existing account')
            return render(request,'pages/login.html')
    return render(request,'pages/login.html',status=200)


def SignUpView(request):
    if request.method=="POST":
        data=request.POST
        print(data)
        email=data['email']
        if User.objects.filter(email=email).first() is not  None:
            messages.error(request,"Email already used")
            return render(request,'pages/register.html',status=200)
        else:
            user=User.objects.create(
                first_name=data['first_name'],
                last_name=data['last_name'],
                email=data['email'],
                username=data['email'],
            )
            user.set_password(data['password'])
            user.save()
            Profile.objects.create(
                user=user
            )
            login(request,user)
            messages.success(request,"Registration Successful")
            return redirect('dashboard')
    return render(request,'pages/register.html',status=200)


@login_required(login_url='login')
def Logout(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def Dashboard(request):
    assets=FetchCoinData()
    return render(request,'dashboard/dashboard.html',{"assets":assets})

def Assets(request):
    assets=FetchCoinData()
    return render(request,'dashboard/assets.html',{"assets":assets})

def Trades(request):
    assets=FetchCoinData()
    if request.method=='POST':
        data=request.POST
        print(request.POST)
        return JsonResponse({"status":"success"},safe=False)
    return render(request,'dashboard/trades.html',{"assets":assets})

def UserCoinBalance(request):
    pass

def Market(request):
    assets=FetchCoinData()
    return render(request,'dashboard/markets.html',{"assets":assets})

def CoinDetails(request):
    pass

def Deposit(request):
    wallet_address=[
        {
            "name":"BTC",
            "address":"bc1qzrfrgl3724mperf2yfj6x6lz46vq4ueuekrh8h",
            "image":"https://s2.coinmarketcap.com/static/img/coins/64x64/1.png"
        },
                {
            "name":"ETH",
            "address":"0x1d6A91643e8eC808a631eA407549E47d1A8A95b2",
            "image":"https://s2.coinmarketcap.com/static/img/coins/64x64/1027.png"
        },
                {
            "name":"USDC",
            "address":"0x1d6A91643e8eC808a631eA407549E47d1A8A95b2",
            "image":"https://s2.coinmarketcap.com/static/img/coins/64x64/3408.png"
        },
                {
            "name":"SOL",
            "address":"7UCrfvnQueCAv8CvEgLAR9D2hLUK73N8piRoTUZupRJf",
            "image":"https://s2.coinmarketcap.com/static/img/coins/64x64/5426.png"
        },
                {
            "name":"XRP",
            "address":"r4sB7FUqpPpQcMKDzKwWVabANJetfCoefZ",
            "image":"https://s2.coinmarketcap.com/static/img/coins/64x64/52.png"
        },
                {
            "name":"ADA",
            "address":"addr1q9v0ewrg6pw6rflngn7y6alu98tkreqg52tuypdcjqp405zcljux35za5xnlx38uf4mlc2whv8jq3g5hcgzm3yqr2lgqcw9nay",
            "image":"https://s2.coinmarketcap.com/static/img/coins/64x64/2010.png"
        },
                {
            "name":"XLM",
            "address":"GAGPB22G7V7QZMDPTOK4JG256QU5QJTEOPBUGOZNPBKFTHGR3WGD6PR4",
            "image":"https://s2.coinmarketcap.com/static/img/coins/64x64/512.png"
        },
                {
            "name":"BNB",
            "address":"bnb1vp0xpxj00u0msy4r35dj3xv0ggmk8g7m6ujk6k",
            "image":"https://s2.coinmarketcap.com/static/img/coins/64x64/1839.png"
        },
                {
            "name":"DOGE",
            "address":"DLXjjitFEXdW7e2w9wFFNMdPMccPrQyY7y",
            "image":"https://s2.coinmarketcap.com/static/img/coins/64x64/74.png"
        }
    ]
    return render(request,'dashboard/deposit.html',{"wallets":wallet_address})

def Withdraw(request):
    wallet_address=[
        {
            "name":"BTC",
            "address":"bc1qzrfrgl3724mperf2yfj6x6lz46vq4ueuekrh8h",
            "image":"https://s2.coinmarketcap.com/static/img/coins/64x64/1.png"
        },
                {
            "name":"ETH",
            "address":"0x1d6A91643e8eC808a631eA407549E47d1A8A95b2",
            "image":"https://s2.coinmarketcap.com/static/img/coins/64x64/1027.png"
        },
                {
            "name":"USDC",
            "address":"0x1d6A91643e8eC808a631eA407549E47d1A8A95b2",
            "image":"https://s2.coinmarketcap.com/static/img/coins/64x64/3408.png"
        },
                {
            "name":"SOL",
            "address":"7UCrfvnQueCAv8CvEgLAR9D2hLUK73N8piRoTUZupRJf",
            "image":"https://s2.coinmarketcap.com/static/img/coins/64x64/5426.png"
        },
                {
            "name":"XRP",
            "address":"r4sB7FUqpPpQcMKDzKwWVabANJetfCoefZ",
            "image":"https://s2.coinmarketcap.com/static/img/coins/64x64/52.png"
        },
                {
            "name":"ADA",
            "address":"addr1q9v0ewrg6pw6rflngn7y6alu98tkreqg52tuypdcjqp405zcljux35za5xnlx38uf4mlc2whv8jq3g5hcgzm3yqr2lgqcw9nay",
            "image":"https://s2.coinmarketcap.com/static/img/coins/64x64/2010.png"
        },
                {
            "name":"XLM",
            "address":"GAGPB22G7V7QZMDPTOK4JG256QU5QJTEOPBUGOZNPBKFTHGR3WGD6PR4",
            "image":"https://s2.coinmarketcap.com/static/img/coins/64x64/512.png"
        },
                {
            "name":"BNB",
            "address":"bnb1vp0xpxj00u0msy4r35dj3xv0ggmk8g7m6ujk6k",
            "image":"https://s2.coinmarketcap.com/static/img/coins/64x64/1839.png"
        },
                {
            "name":"DOGE",
            "address":"DLXjjitFEXdW7e2w9wFFNMdPMccPrQyY7y",
            "image":"https://s2.coinmarketcap.com/static/img/coins/64x64/74.png"
        }
    ]
    return render(request,'dashboard/withdraw.html',{"wallets":wallet_address})
