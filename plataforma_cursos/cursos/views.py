from django.shortcuts import render, redirect
from django.contrib.messages import constants
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Cursos, Aulas
from django.contrib.auth.decorators import login_required


@login_required(login_url="/auth/login/")
def home(request):
    if request.method =="GET":
        cursos = Cursos.objects.all()
        aulas = Aulas.objects.all()
        return render(request,'cursos.html',{'cursos':cursos,'aulas':aulas})



@login_required(login_url="/auth/login/")
def curso(request, id):
    curso = Cursos.objects.get(id = id)
    aulas = Aulas.objects.filter(curso_id = id)
    return render(request,'curso.html',{'curso':curso,'aulas':aulas})



@login_required(login_url="/auth/login/")
def aula(request, id):
    aula = Aulas.objects.get( id = id)
    return render(request, 'aula.html', {'aula': aula})