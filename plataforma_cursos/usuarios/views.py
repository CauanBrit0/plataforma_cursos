from django.shortcuts import render, redirect
from django.contrib.messages import constants
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib import auth

def login(request):
    if request.method =="GET":
        if request.user.is_authenticated:
            return redirect('/home/')
        return render(request, 'login.html')
    
    if request.method =="POST":
        nome = request.POST.get('nome')
        senha = request.POST.get('senha')
        print(senha)
        if len(senha.strip()) == 0 or len(nome.strip()) == 0:
            messages.add_message(request,constants.ERROR,'Preencha todos os campos em branco.')
            return redirect('/auth/login/')

        usuario = auth.authenticate(request, username = nome, password = senha)
        if usuario:
            auth.login(request, usuario)
            return redirect('/home/')
        if not usuario:
            messages.add_message(request,constants.ERROR,'Credenciais inválidas.')
            return redirect('/auth/login/')



def cadastro(request):

    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect('/home/')
        return render(request,'cadastro.html')
    
    if request.method == "POST":

        nome = request.POST.get('nome')
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        if len(nome.strip()) == 0 or len(senha.strip()) == 0 or len(email.strip()) == 0:
            messages.add_message(request,constants.ERROR,'Preencha todos os campos em branco.')
            return redirect('/auth/cadastro/')
        
        if User.objects.filter(username = nome).exists():
            messages.add_message(request,constants.ERROR,'Nome de Usuario já existente.')
            return redirect('/auth/cadastro/')
        
        if User.objects.filter(email = email).exists():
            messages.add_message(request,constants.ERROR,'Email já existente.')
            return redirect('/auth/cadastro/')

        if len(senha.strip()) < 6:
            messages.add_message(request,constants.ERROR,'Sua senha deverá ter no mínimo 6 caracteres.')
            return redirect('/auth/cadastro/')
        
        try:
            usuario = User.objects.create_user(username = nome, email = email, password = senha)
            usuario.save()
            messages.add_message(request,constants.SUCCESS,'Usuario cadastrado com sucesso! Realize seu login agora mesmo!')
            return redirect('/auth/login/')

        except:
            messages.add_message(request,constants.ERROR,'Erro interno do sistema.')
            
            return redirect('/auth/cadastro/')
    





def sair(request):
    auth.logout(request)
    return redirect('/auth/login/')