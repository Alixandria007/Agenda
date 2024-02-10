from django.shortcuts import render,redirect
from contact.models import Contact
from django.http import Http404
from django.db.models import Q
from django.core.paginator import Paginator

def index(request):

    contacts = Contact.objects.filter(show = True).order_by('-id')
    paginator = Paginator(contacts, 10) 

    page_number = request.GET.get("page", None)
    page_obj = paginator.get_page(page_number)

    context = {
        'contacts': str(list(contacts)),
        'contacts_': contacts,
        'site_title': f'Contatos - ',
        'page_obj' : page_obj,
        
    }


    return render(
        request,
        'contact/index.html',
        context,
    )

def contact(request , id):

    single_contact = Contact.objects.get(id = id)

    if single_contact == None:
        raise Http404('Esse Contato não existe')
        
    context = {
        'contact' : single_contact,
        'site_title': f'{single_contact.first_name} {single_contact.last_name} - ',
    }

    return render(
        request,
        'contact/contact.html',
        context,
    )

def search(request):
    search = request.GET.get('q', '').strip()

    

    contacts = Contact.objects.filter(show = True).filter(Q(first_name__icontains = search) | Q(last_name__icontains = search) ).order_by('-id')

    paginator = Paginator(contacts, 10)
    page_number = request.GET.get("page",'')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'site_title': f'Contatos - ',
        'contacts': str(list(contacts)),
        'page_obj' : page_obj,
        'search': search
    }

    
    return render(
        request,
        'contact/search.html',
        context,
    )