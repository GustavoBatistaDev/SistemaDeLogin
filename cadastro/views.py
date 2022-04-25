from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.core.validators import validate_email
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

def cadastro(request):
    if request.method != 'POST':
        return render(request, 'cadastro/cadastro.html')
    nome = request.POST.get('nome')
    sobrenome = request.POST.get('sobrenome')
    usuario = request.POST.get('usuario')
    email = request.POST.get('email')
    senha = request.POST.get('senha')
    senha2 = request.POST.get('senha2')

    if not nome or not sobrenome or not usuario or not email or not senha or not senha2:
        messages.add_message(request, messages.ERROR, 'Nenhum campo pode ser nulo.')
        return render(request, 'cadastro/cadastro.html')

    if len(senha) < 8:
        messages.add_message(request, messages.ERROR, 'Senha precisa ter mais que 7 caracteres.')
        return render(request, 'cadastro/cadastro.html')

    try:
        validate_email(email)
    except:
        messages.add_message(request, messages.ERROR, 'Email inválido.')
        return render(request, 'cadastro/cadastro.html')

    if len(usuario) < 6:
        messages.add_message(request, messages.ERROR, 'Nome de suário precisa ter 6 caracteres ou mais. ')
        return render(request, 'cadastro/cadastro.html')

    if senha != senha2:
        messages.add_message(request, messages.ERROR, 'Senhas não conferem.')
        return render(request, 'cadastro/cadastro.html')

    if User.objects.filter(username=usuario).exists():
        messages.error(request, 'Usuário já existe.')
        return render(request, 'cadastro/cadastro.html')

    if User.objects.filter(email=email).exists():
        messages.error(request, 'Email já existe.')
        return render(request, 'cadastro/cadastro.html')

    messages.success(request, 'Cadastrado com sucesso. Faça login.')

    user = User.objects.create_user(username=usuario, first_name=nome, last_name=sobrenome,
                                    email=email, password=senha
                                    )
    user.save()
    return redirect('login')


def login(request):
    if request.method != 'POST':
        return render(request, 'cadastro/login.html')

    usuario = request.POST.get('usuario')
    senha = request.POST.get('senha')

    user = auth.authenticate(request, username=usuario, password=senha)
    if not user:
        messages.error(request, 'Usuário ou senha inválidos.')
        return render(request, 'cadastro/login.html')

    else:
        auth.login(request, user)
        messages.success(request, 'Você fez login com sucesso.')
        return redirect('page_initial')


@login_required(redirect_field_name='login')
def page_initial(request):
    return render(request, 'cadastro/pageinitial.html')


def logout(request):
    auth.logout(request)
    return redirect('cadastro')