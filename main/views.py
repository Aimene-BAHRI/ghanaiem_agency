from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from main.forms import ReservationForm
from main.models import Main, Reservation, Rubrique, Annonce, Annonce_Photo, Endroit
from django.template import loader

from django.core.paginator import Paginator #import Paginator
from datetime import datetime, timedelta, time
from django.urls import reverse


today = datetime.now().date()
# Create your views here.
def index(request):
	main = Main.objects.last()
	categories = Rubrique.objects.all()
	submitted = False
	endroits = Endroit.objects.all()
	annonces = Annonce.objects.filter(date_debut__gte=today).order_by('date_debut')
	paginator = Paginator(annonces, 9)
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)
	from ghanaiem_agency.settings import MEDIA_ROOT, MEDIA_URL
	if request.method == "POST":
		form = ReservationForm(request.POST)
		if not form.is_valid():
			return HttpResponse(form.errors.values())
		form.save()
		return HttpResponseRedirect(reverse('home'))
	else:
		form = ReservationForm()
		if 'submitted' in request.GET:
			submitted = True

	ctx = {
		'segment': 'home',
		'main': main,
		'form' : form,
		'MEDIA_URL' : MEDIA_URL,
		'submitted': submitted,
		'categories' : categories,
		'endroits' : endroits,
		'annonces': page_obj,
		'range' : range(1, page_obj.paginator.num_pages+1),
	}
	return render(request, 'index.html', ctx)

def annonce_detail(request, pk):
	annonce = get_object_or_404(Annonce, pk = pk)
	main = Main.objects.last()
	categories = Rubrique.objects.all()
	submitted = False

	if request.method == "POST":
		form = ReservationForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse('home:annonce_detail', kwargs={'pk' : pk}))
		else:
			return HttpResponse(form.errors.values())
	else:
		form = ReservationForm()
		if 'submitted' in request.GET:
			submitted = True
	context = {
		'segment': 'annonce',
		'annonce': annonce,
		'main': main,
		'form' : form,
		'submitted': submitted,
		'categories' : categories,
		}

	html_template = loader.get_template('home/annonce_detail.html')
	return HttpResponse(html_template.render(context, request))

def privacy(request):
	main = Main.objects.last()
	categories = Rubrique.objects.all()
	ctx = {
		'main': main,
		'categories' : categories
	}
	return render(request, 'privacy.html', ctx)

def terms(request):
	categories = Rubrique.objects.all()
	main = Main.objects.last()
	ctx = {
		'main': main,
		'categories' : categories
	}
	return render(request, 'terms.html', ctx)

import datetime
def annonces_by_category(request, rubrique_slug = None):
	main = Main.objects.last()
	annonces = Annonce.objects.filter(
		date_debut__gte=datetime.datetime.now()
	).order_by("date_debut")
	categories = Rubrique.objects.all()
	if rubrique_slug:
		category_s = get_object_or_404(Rubrique,slug = rubrique_slug)
		annonces = annonces.filter(categorie = category_s)

	context = {
		'annonces':annonces,
	'categories':categories,
		'main': main
	}
	template = 'annonces_by_category_list.html'
	return render(request,template,context)