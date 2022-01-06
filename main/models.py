from django.utils import timezone
from django.db import models
import uuid
from django.template.defaultfilters import slugify

# Create your models here.
class Main(models.Model):
	logo = models.ImageField(upload_to="images/logo/", default=None)
	name_tag1 = models.CharField(max_length=200, null=True)
	name_tag2 = models.CharField(max_length=200, null=True)
	description = models.TextField()
	adresse = models.CharField(max_length=400, null=True)
	email = models.EmailField(default='test@travel.agency.com')
	phone_number =models.CharField(max_length=15, null=True)
	agency_number =models.CharField(max_length=15, null=True)
	facebook = models.URLField(blank=True)
	instagram = models.URLField(blank=True)
	twitter = models.URLField(blank=True)
	slogan = models.TextField(blank=True)
	Image_principal = models.ImageField(upload_to='heros/', null=True)
	video_principal = models.FileField(upload_to='videos/',blank=True)

	def __str__(self):
		return str(self.name_tag1) + ' ' + str(self.name_tag2)	

class Rubrique(models.Model):
	rubrique_name = models.CharField(max_length=200)
	slug = models.SlugField(unique=True)
	photo_representatif = models.ImageField(upload_to="images/rubriques/main/", default=None, null=True, blank = True)
	
	prepopulated_fields = {"slug": ("rubrique_name",)}
	def __str__(self):
		return ''+self.rubrique_name

	def save(self, *args, **kwargs):
		self.slug = slugify(self.rubrique_name)
		super(Rubrique,self).save(*args, **kwargs)

class Reservation(models.Model):
	nom = models.CharField(max_length=200)
	prenom = models.CharField(max_length=200, null=True)
	telephone = models.CharField(max_length=15)
	email = models.EmailField()
	reservation_date = models.DateField(null=True)
	created_at = models.DateTimeField(auto_now_add=False, auto_now=False)

	def save(self, *args, **kwargs):
		if self.created_at == None:
			self.created_at = timezone.now()
		super(Reservation, self).save(*args, **kwargs)
	def get_full_name(self):
		return '{} {}'.format(self.nom, self.prenom)

	def __str__(self):
		return '{} __ {}'.format(self.id, self.email)

class Annonce(models.Model):
	annonce_name = models.CharField(max_length=200)
	categorie = models.ForeignKey('Rubrique', on_delete=models.CASCADE, null=True, related_name='annonces')
	annonce_description = models.TextField(default='')
	post = models.TextField(default='')
	image_principale = models.ImageField(upload_to='images/annonces/pricipal/', height_field=None, width_field=None, max_length=None)
	
	date_debut = models.DateField(auto_now=False, auto_now_add=False)
	date_fin = models.DateField(auto_now=False, auto_now_add=False)


	def __str__(self):
		return ''+self.annonce_name
class Annonce_Photo(models.Model):
	image = models.ImageField(upload_to="images/annoces/", default=None, null=True, blank = True)
	annonce = models.ForeignKey(Annonce, on_delete=models.CASCADE, null=True, related_name='photos')

	class Meta:
		unique_together = (('annonce', 'id'),)
		
	def __str__(self):
		return 'Image {} of {}'.format(self.id ,self.annonce)

class Endroit(models.Model):
	nom_endroit = models.CharField(max_length=200)
	image = models.ImageField(upload_to='images/androits/')

	def __str__(self):
		return self.nom_endroit
	