from accounts.handlers import FetchCoinData,Forex_Currencies,StockData
from django.shortcuts import render


def HomePage(request):
    # return render(request,'pages/homepage.html')
    return render(request,'pages/homepage.html',{"crypto":FetchCoinData(),})