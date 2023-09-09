# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
from django.shortcuts import get_object_or_404, render, redirect

from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.template.defaultfilters import slugify
from django.urls import reverse
from main.forms import MainForm, RubriqueForm, AnnonceForm, AnnoncePhotoForm, AnnnocePhotoInlineFormset, EndroitForm 

from main.models import Main, Reservation, Rubrique, Annonce, Annonce_Photo, Endroit

from django.core.paginator import Paginator #import Paginator

from datetime import datetime, timedelta

@login_required(login_url="/login/")
def index(request):
    main = Main.objects.last()
    total_reservation = Reservation.objects.all().count()

    today = datetime.now()
    yesterday = today + timedelta(days=-1)

    week_start = today - timedelta(days=today.weekday()) # 6 days + 1 to finish a week cicle
    week_end = week_start + timedelta(days=6)

    last_week_start = week_start + timedelta( weeks=-1)
    last_week_end = last_week_start + timedelta(days=6)

    monthy = today.month
    last_month = (monthy-1) % 12

    monthly_reservations_count = Reservation.objects.filter(created_at__month = monthy).count()
    last_month_reservations_count = Reservation.objects.filter(created_at__month = last_month).count()

    weekly_reservations_count = Reservation.objects.filter(created_at__date__range=(week_start.date(), week_end.date())).count()
    last_week_reservations_count = Reservation.objects.filter(created_at__date__range=(last_week_start.date(), last_week_end.date())).count()

    daily_reservations_count = Reservation.objects.filter(created_at__date = today.date()).count()
    yesterday_reservations_count = Reservation.objects.filter(created_at__date = yesterday.date()).count()

    if total_reservation != 0:
        monthly_growth = (monthly_reservations_count - last_month_reservations_count) / total_reservation * 100
        weekly_growth = (weekly_reservations_count - last_week_reservations_count) / total_reservation * 100
        daily_growth = (daily_reservations_count - yesterday_reservations_count) / total_reservation * 100
    else:
        monthly_growth = 0
        weekly_growth = 0
        daily_growth = 0

    data_aze = []
    for current_month in range(1,13):
        datas = Reservation.objects.filter(created_at__month = current_month).values_list('created_at__month').count()
        data_aze.append(datas)

    context = {
        'reservations': Reservation.objects.all(),
        'monthly_reservations_count' : monthly_reservations_count,
        'weekly_reservations_count' : weekly_reservations_count,
        'daily_reservations_count' : daily_reservations_count,
        'segment': 'index',
        'monthly_growth' : monthly_growth,
        'weekly_growth' : weekly_growth,
        'daily_growth' : daily_growth,
        'main': main,
        'data_aze': data_aze,
        }

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def info(request):
    main = Main.objects.last()
    submitted = False
    if request.method == "POST":
        form = MainForm(request.POST, request.FILES, instance=main)
        if not form.is_valid():
            return HttpResponse(form.errors.values())
        form.save()
        return HttpResponseRedirect('?submitted=True')
    else:
        form = MainForm(instance=main)
        if 'submitted' in request.GET:
            submitted = True

    context = {
        'segment': 'info',
        'submitted': submitted,
        'main': main,
        'form' : form,
        }

    html_template = loader.get_template('home/infos.html')
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def pages(request):
    main = Main.objects.last()
    context = {'main': main}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:
        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template(f'home/{load_template}')
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except Exception:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))

# CRUD RUBRIQUE
from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect

@login_required(login_url="/login/")
def create_rubrique(request):
    main = Main.objects.last()
    rubrique_form = RubriqueForm()
    if request.method == "POST":
        rubrique_form = RubriqueForm(request.POST, request.FILES)
        if rubrique_form.is_valid():
            created_rubrique = rubrique_form.save(commit=False)
            created_rubrique.slug = slugify(request.POST['rubrique_name'])
            created_rubrique.save()
            return HttpResponseRedirect(reverse('home:rubriques'))
    context = {
        'segment': 'create_rubrique',
        'main': main,
        'form' : rubrique_form,
    }
    html_template = loader.get_template('home/create_rubrique.html')
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def rubriques(request):
    main = Main.objects.last()
    rubriques = Rubrique.objects.all()
    paginator = Paginator(rubriques, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'segment': 'rubriques',
        'rubriques': page_obj,
        'main': main,
        'range' : range(1, page_obj.paginator.num_pages+1),
        }
    html_template = loader.get_template('home/rubriques.html')
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def rubrique(request, pk):
    rubrique = get_object_or_404(Rubrique, pk = pk)
    main = Main.objects.last()
    context = {
        'segment': 'rubrique',
        'rubrique': rubrique,
        'annonces': rubrique.annonces.order_by('-date_debut'),
        'main': main
        }
    html_template = loader.get_template('home/rubrique.html')
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def edit_rubrique(request, pk):
    main = Main.objects.last()
    rubrique = Rubrique.objects.get(pk=pk) if pk else Rubrique()
    rubrique_form = RubriqueForm(instance=rubrique)
    if request.method == "POST":
        rubrique_form = RubriqueForm(request.POST, request.FILES, instance=rubrique)
        if rubrique_form.is_valid():
            created_rubrique = rubrique_form.save(commit=False)
            created_rubrique.save()
            return HttpResponseRedirect(reverse('home:rubriques'))
    context = {
        'segment': 'edit_rubrique',
        'rubrique': rubrique,
        'form' : rubrique_form,
        'main': main,
        }

    html_template = loader.get_template('home/edit_rubrique.html')
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def delete_rubrique(request, pk):
    query = Rubrique.objects.get(pk=pk)
    query.delete()
    return redirect('home:rubriques')

# CRUD ANNONCE
@login_required(login_url="/login/")
def create_annonce(request):
    main = Main.objects.last()
    annonce_form = AnnonceForm()
    formset = AnnnocePhotoInlineFormset()
    if request.method == "POST":
        annonce_form = AnnonceForm(request.POST, request.FILES)
        formset = AnnnocePhotoInlineFormset(request.POST, request.FILES, queryset=Annonce_Photo.objects.none())
        if annonce_form.is_valid():
            instance = annonce_form.save(commit=False)
            if formset.is_valid():
                instance.save()
                for f in formset:
                    cd = f.cleaned_data
                    image = cd.get('image')
                    annonce_photo = Annonce_Photo(annonce = instance, image = image)
                    annonce_photo.save()
            return HttpResponseRedirect(reverse('home:annonces'))

    context = {
        'segment': 'create_annonce',
        'main': main,
        'form' : annonce_form,
        'formset' : formset
    }
    html_template = loader.get_template('home/create_annonce.html')
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def annonces(request):
    main = Main.objects.last()
    if request.method == "POST":
        postForm = AnnonceForm(request.POST, request.FILES)
        if not postForm.is_valid():
            return HttpResponse(postForm.errors.values())
        postForm.save()
        return HttpResponseRedirect('?submitted=True')
    else:
        postForm = AnnonceForm()

    annonces = Annonce.objects.all()
    paginator = Paginator(annonces, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'segment': 'annonces',
        'annonces': page_obj,
        'main': main,
        'range' : range(1, page_obj.paginator.num_pages+1),
        'form' : postForm,
        }

    html_template = loader.get_template('home/annonces.html')
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def annonce(request, pk):
    annonce = get_object_or_404(Annonce, pk = pk)
    main = Main.objects.last()
    context = {
        'segment': 'annonce',
        'annonce': annonce,
        'main': main
        }

    html_template = loader.get_template('home/annonce.html')
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def edit_annonce(request, pk):
    annonce = get_object_or_404(Annonce, pk = pk)
    main = Main.objects.last()
    annonce_form = AnnonceForm(instance = annonce)
    formset = AnnnocePhotoInlineFormset(instance=annonce)
    if request.method == "POST":
        annonce_form = AnnonceForm(request.POST, request.FILES, instance = annonce)
        formset = AnnnocePhotoInlineFormset(request.POST, request.FILES,instance = annonce, queryset=annonce.photos)
        if not annonce_form.is_valid():
            return HttpResponse(annonce_form.errors.values())
        instance = annonce_form.save(commit=False)
        if not formset.is_valid():
            return HttpResponse(formset.errors.values())
        instance.save()
        for f in formset:
            cd = f.cleaned_data
            image = cd.get('image')
            annonce_photo = Annonce_Photo(annonce = instance, image = image)
            annonce_photo.save()
        return HttpResponseRedirect(reverse('home:annonces'))
    context = {
        'segment': 'edit_annonce',
        'main': main,
        'form' : annonce_form,
        'formset' : formset
    }
    html_template = loader.get_template('home/edit_annonce.html')
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def delete_annonce(request, pk):
    query = Annonce.objects.get(pk=pk)
    query.delete()
    return redirect('home:annonces')

# CRUD ENDROIT
def endroits(request):
    main = Main.objects.last()
    if request.method == "POST":
        form = EndroitForm(request.POST)
        if not form.is_valid():
            return HttpResponse(form.errors.values())
        form.save()
        return HttpResponseRedirect('?submitted=True')
    else:
        form = EndroitForm()

        if 'submitted' in request.GET:
            submitted = True
    endroits = Endroit.objects.all()
    paginator = Paginator(endroits, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'segment': 'endroits',
        'endroits': page_obj,
        'main': main,
        'range' : range(1, page_obj.paginator.num_pages+1),
        'form' : form,
        }

    html_template = loader.get_template('home/endroits.html')
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def endroit(request, pk):
    endroit = get_object_or_404(Endroit, pk = pk)
    main = Main.objects.last()

    context = {
        'segment': 'endroit',
        'endroit': endroit,
        'main': main
        }

    html_template = loader.get_template('home/endroit.html')
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def edit_endroit(request, pk):
    endroit = get_object_or_404(Endroit, pk = pk)
    main = Main.objects.last()
    submitted = False
    if request.method == "POST":
        form = EndroitForm(request.POST, files=request.FILES, instance=endroit)
        if not form.is_valid():
            return HttpResponse(form.errors.values())
        form.save()
        return HttpResponseRedirect(reverse('home:endroits'))
    else:
        form = EndroitForm(instance=endroit)
        if 'submitted' in request.GET:
            submitted = True
    context = {
        'segment': 'edit_endroit',
        'submitted': submitted,
        'endroit': endroit,
        'form' : form,
        'main': main
        }

    html_template = loader.get_template('home/edit_endroit.html')
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def create_endroit(request):
    main = Main.objects.last()
    submitted = False
    if request.method == "POST":
        form = EndroitForm(request.POST, files=request.FILES)
        if not form.is_valid():
            return HttpResponse(form.errors.values())
        form.save()
        return HttpResponseRedirect(reverse('home:endroits'))
    else:
        form = EndroitForm()
        if 'submitted' in request.GET:
            submitted = True
    context = {
        'segment': 'create_endroit',
        'submitted': submitted,
        'endroit': endroit,
        'form' : form,
        'main': main
        }

    html_template = loader.get_template('home/create_endroit.html')
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def delete_endroit(request, pk):
    query = Endroit.objects.get(pk=pk)
    query.delete()
    return redirect('home:endroits')

def reservations(request):
    main = Main.objects.last()
    reservations = Reservation.objects.all()
    context = {
        'segment': 'reservations',
        'reservations': reservations,
        'main': main,
        }

    html_template = loader.get_template('home/reservations.html')
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def delete_reservation(request, pk):
    query = Reservation.objects.get(pk=pk)
    query.delete()
    return redirect('home:reservations')