from django.shortcuts import render, redirect, HttpResponse
from django.contrib.messages import constants
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Cursos, Aulas, Comentarios,NotasAulas
from django.contrib.auth.decorators import login_required
import json


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
    comentarios = Comentarios.objects.filter(aula = id).order_by('-data')
    usuario_avaliou = NotasAulas.objects.filter(aula_id = id).filter(usuario_id = request.user.id)
    avaliacoes = NotasAulas.objects.filter(aula_id = id)
    return render(request, 'aula.html', {'aula': aula,'usuario_id':request.user.id,'comentarios':comentarios,'usuario_avaliou':usuario_avaliou,'avaliacoes':avaliacoes})


@login_required(login_url="/auth/login/")
def comentarios(request):
    usuario_id = int(request.POST.get('usuario_id'))
    comentario = request.POST.get('comentario')
    aula_id = int(request.POST.get('aula_id'))

    comentario_instancia = Comentarios(usuario_id = usuario_id,
                                       comentario = comentario,
                                       aula_id = aula_id)
    comentario_instancia.save()

    comentarios = Comentarios.objects.filter(aula = aula_id).order_by('-data')
    somente_nomes = [i.usuario.username for i in comentarios]
    somente_comentarios = [i.comentario for i in comentarios]
    comentarios = list(zip(somente_nomes, somente_comentarios))

    return HttpResponse(json.dumps({'status': '1', 'comentarios': comentarios }))



@login_required(login_url="/auth/login/")
def processa_avaliacao(request):

        avaliacao = request.POST.get('avaliacao')
        aula_id = request.POST.get('aula_id')
        usuario_id = request.user.id

        usuario_avaliou = NotasAulas.objects.filter(aula_id = aula_id).filter(usuario_id = usuario_id)

        if not usuario_avaliou:
            nota_aulas = NotasAulas(aula_id = aula_id,
                                    nota = avaliacao,
                                    usuario_id = usuario_id,
                                    )
            nota_aulas.save()
            return redirect(f'/home/aula/{aula_id}')
        else:
            return redirect(f'/home/aula/{aula_id}')
