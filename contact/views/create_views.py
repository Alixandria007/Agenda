from typing import Any
from django.shortcuts import render,redirect,get_object_or_404
from contact.form import ContactForm, RegisterForm, RegisterUpdateForm
from django.db.models import Q
from django.contrib import auth
from django.contrib.auth.forms import AuthenticationForm
from django.core.paginator import Paginator
from django.urls import reverse
from contact.models import Contact
from django.contrib import messages
from django.contrib.auth.decorators import login_required

@login_required(login_url='contact:login')
def create(request):
    form_action = reverse('contact:create')
    if request.method == 'POST':

        form = ContactForm(request.POST, request.FILES)
        context = {
        'form': form,
        'form_action' : form_action
    }
        
        if form.is_valid():
            contact = form.save(commit=False)
            contact.owner = request.user
            contact = form.save()
            return redirect('contact:update' , id = contact.pk)


        return render(
            request,
            'contact/create.html',
            context,
        )

    context = {
        'form': ContactForm(),
        'form_action' : form_action,
        'save': 'Enviar'
    }


    return render(
        request,
        'contact/create.html',
        context,
    )

@login_required(login_url='contact:login')
def update(request,id):
    contact  = get_object_or_404(
        Contact,pk = id, show = True
    )

    if contact.owner != request.user:
        messages.error(request,'Você não pode fazer update desse contato')
        return redirect('contact:index')
    
    form_action = reverse('contact:update',args=(id,))

    
    if request.method == 'POST':

        form = ContactForm(request.POST , request.FILES, instance=contact)

        context = {
        'form': form,
        'form_action' : form_action
    }
        
        if form.is_valid():
            contact = form.save(commit=False)
            if contact.owner == request.user:
                contact = form.save()
            else:
                messages.error(request,'ERROR')
            return redirect('contact:update', id=contact.pk)


        return render(
            request,
            'contact/create.html',
            context,
        )

    context = {
        'form': ContactForm(instance = contact),
        'form_action' : form_action,
        'save' : 'Salvar'
    }


    return render(
        request,
        'contact/create.html',
        context,
    )

@login_required(login_url='contact:login')
def delete(request,id):
    contact  = get_object_or_404(
        Contact,pk = id, show = True
    )
    confirmation = request.POST.get('confirmation','no')

    if confirmation == 'yes':
        return render(
        request,
        'contact/contact.html',
        {
            'contact': contact,
            'confirmation': confirmation,
        }
    )
    if confirmation == 'yes':
        if contact.owner == request.user:
                contact = contact.delete()
                return redirect('contact:index')
        else:
                messages.error(request,'Você não pode apagar esse contato')
                return redirect('contact:index')
    
    return render(
        request,
        'contact/contact.html',
        {
            'contact': contact,
            'confirmation': confirmation,
        }
    )





def register(request):

    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Usuário registrado')
            return redirect('contact:login')
        else:
            messages.error(request, 'Falha ao registrar')
        
        context = {
            'form': RegisterForm(request.POST),
            'save': 'Enviar'
        }
    
        return render(
            request,
            'contact/register.html',
            context,
        )
    

    context = {
            'form': RegisterForm(),
            'save': 'Enviar'
        }
    
    return render(
        request,
        'contact/register.html',
        context,
    )


def login_view(request):
    form = AuthenticationForm(request)

    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)

        context = {
            'form': form,
            'save': 'Enviar'
        }

        if form.is_valid():
            user = form.get_user()
            auth.login(request, user)
            messages.success(request,'Usuario encontrado')
            return redirect('contact:index')
        else:
            messages.error(request,'Usuario não encontrado')

        return render(
        request,
        'contact/login.html',
        context,
    )

    context = {
            'form': form,
            'save': 'Enviar'
        }

    return render(
        request,
        'contact/login.html',
        context,
    )

@login_required(login_url='contact:login')
def logout_view(request):
    auth.logout(request)
    return redirect('contact:login')

@login_required(login_url='contact:login')
def user_update(request):
    form = RegisterUpdateForm(instance=request.user)

    if request.method == 'POST':
        form = RegisterUpdateForm(instance=request.user, data=request.POST)

        context = {
            'form': form,
            'save' : 'Salvar'
        }

        if form.is_valid:
            form.save()
            messages.success(request, 'Usuario editado com sucesso!!')

        return render(
        request,
        'contact/user_update.html',
        context
        )

    context = {
            'form': form,
            'save' : 'Salvar'
        }
        
    return render(
        request,
        'contact/user_update.html',
        context
    )