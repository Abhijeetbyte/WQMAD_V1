from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from .forms import LoginForm
from django.contrib.auth.decorators import login_required
import pyrebase

def home(request):
    return render(request, "home.html")

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authenticated Successfully')
                else:
                    return HttpResponse('Disabled Account')
            else:
                return HttpResponse('Invalid Login')
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form':form})

config = {
    "apiKey": "AIzaSyDy4WPZBRFC_0L_BJocOUWe1FMpmIWztcQ",
    "authDomain": "kilkari-f04c2.firebaseapp.com",
    "databaseURL": "https://kilkari-f04c2-default-rtdb.asia-southeast1.firebasedatabase.app",
    "projectId": "kilkari-f04c2",
    "storageBucket": "kilkari-f04c2.appspot.com",
    "messagingSenderId": "530410018597",
    "appId": "1:530410018597:web:c665f460df3079e95a6ccc"
}

firebase = pyrebase.initialize_app(config)
authe = firebase.auth()
database = firebase.database()

@login_required
def dashboard(request):
    filter_type = database.child('Data').child('Filter Type').get().val()
    manufacturer = database.child('Data').child('Manufacturer').get().val()
    name = database.child('Data').child('Name').get().val()
    product_ID = database.child('Data').child('Prodcut ID').get().val()
    product_phase = database.child('Data').child('Product Phase').get().val()
    return render(request,
                  'account/dashboard.html',
                  {'section':'dashboard',
                   "filter_type": filter_type,
                   "manufacturer": manufacturer,
                   "name": name,
                   "product_ID": product_ID,
                   "product_phase": product_phase,
                   })