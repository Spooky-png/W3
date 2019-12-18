from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Fighter
import bcrypt
import random
from django.core.files.storage import FileSystemStorage
from .forms import UserForm

def home(request):
    return render(request,"login.html")

def logout(request):
    request.session.clear()
    return redirect ("/")

def login(request):
    errors = User.objects.loginValidator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/")
    else:
        user = User.objects.get(email=request.POST['email'])
        request.session['user_id'] = user.id
        return redirect('/dashboard')

def register(request):
    errors = User.objects.registerValidator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
            return redirect("/")
    else:
        password = request.POST['password']
        salt = bcrypt.gensalt()
        hashed_pw = bcrypt.hashpw(password.encode(), salt).decode()
        user = User.objects.create(name=request.POST["name"],alias=request.POST["alias"],email=request.POST["email"],password=hashed_pw)
        request.session['user_id'] = user.id
    return redirect("/dashboard")

def dashboard(request):
    if "user_id" not in request.session:
        return redirect ("/")
    else:
        context = {
        "leader" : Fighter.objects.all().order_by("-votes"),
        "last" : Fighter.objects.last(),
        "count" : len(User.objects.all()),
        "user" : User.objects.get(id = request.session['user_id']),
        "newest" : User.objects.last(),
        "totalfighters" : len(Fighter.objects.all()),
        "newestfighter" : Fighter.objects.last()
    }
    return render(request, "dashboard.html", context)

def addfighter(request):
    if request.method == "GET":
        if "user_id" not in request.session:
            return redirect ("/")
        return render(request, "upload.html")
    if request.method == "POST":
        errors = Fighter.objects.fighterValidator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
                return redirect("/addfighter")
        else:
            context = {}
            uploaded_file = request.FILES["picture"]
            fs = FileSystemStorage()
            name = fs.save(uploaded_file.name,uploaded_file)
            context['url'] = fs.url(name)
            user = User.objects.get(id = request.session['user_id'])
            fighter = Fighter.objects.create(fightername=request.POST["fightername"],fighterdesc=request.POST["fighterdesc"],picture=request.FILES["picture"],votes=0,uploaded_by=user)
        return redirect("/dashboard")

def fight(request):
    if "user_id" not in request.session:
        return redirect ("/")
    else:
        context = {
        "user" : User.objects.get(id = request.session['user_id']),
        "all_fighters" : Fighter.objects.all(),
        "fighter1" : random.choice(Fighter.objects.all()),
        "fighter2" : random.choice(Fighter.objects.exclude())
    }
    return render(request, "vote.html", context)

def editprofile(request):
    if request.method == "GET":
        if "user_id" not in request.session:
            return redirect ("/")
        else:
            context = {
            "leader" : Fighter.objects.all().filter(uploaded_by=request.session['user_id']).order_by("-votes"),
            "all_fighters" : Fighter.objects.filter(uploaded_by=request.session['user_id']),
            "user" : User.objects.get(id = request.session['user_id'])
        }
        return render(request, "profile.html", context)
    if request.method =="POST":
        errors = User.objects.editValidator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
                return redirect("/editprofile")
        else:
            context = {}
            uploaded_file = request.FILES['picture']
            fs = FileSystemStorage()
            name = fs.save(uploaded_file.name,uploaded_file)
            context['url'] = fs.url(name)
            user = User.objects.get(id = request.session['user_id'])
            user.picture = request.FILES['picture']
            user.alias = request.POST['alias']
            user.desc = request.POST['desc']
            user.save()
        return redirect("/dashboard")

def vote(request, fighter_id):
    fighter_id = fighter_id
    fighter = Fighter.objects.get(id=fighter_id)
    fighter.votes = fighter.votes + 1
    fighter.save()
    return redirect("/fight")

def upload(request):
    return render(request,"upload.html")