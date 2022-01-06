from django import forms
from django.db.models import fields

from main.models import Main, Reservation, Rubrique, Annonce, Annonce_Photo, Endroit
from crispy_forms.helper import FormHelper
from crispy_forms.helper import Layout
from crispy_forms.layout import Layout, HTML
from django.forms import inlineformset_factory
from django.template.defaultfilters import slugify

class ReservationForm(forms.ModelForm):
    def __init__(self,  *args, **kwargs):
        super(ReservationForm, self).__init__(*args, **kwargs)
        helper = self.helper = FormHelper()
        layout = helper.layout = Layout()
        helper.form_show_labels = False
    nom = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'nom'}))
    prenom = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'prenom'}))
    telephone = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'telephone'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'email'}))
    reservation_date = forms.DateField(
        input_formats=['%d/%m/%Y'],
        widget=forms.DateInput(attrs={
            'class': 'form-control datetimepicker-input',
            'data-target': '#datetimepicker1',
            'placeholder' : 'date de reservation'
        })
    )    
    class Meta:
        model = Reservation
        fields = ("nom", "prenom", "telephone", "email", "reservation_date")

class MainForm(forms.ModelForm):
    def __init__(self,  *args, **kwargs):
        super(MainForm, self).__init__(*args, **kwargs)
        helper = self.helper = FormHelper()
        layout = helper.layout = Layout()
        helper.form_show_labels = False
        self.fields['facebook'].required = False
        self.fields['twitter'].required = False
        self.fields['instagram'].required = False
        self.fields['Image_principal'].required = False
        self.fields['description'].required = False
        self.fields['video_principal'].required = False




    name_tag1 = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Premiere partie du Nom'}))
    name_tag2 = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Deuxieme partie du Nom'}))
    description = forms.TextInput(attrs={'placeholder': 'Description'})
    adresse = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Entrer Votre Adresse '}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'test@travel.agency.com'}))
    phone_number =forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Numero de telephone personnel'}))
    agency_number =forms.CharField(widget=forms.TextInput(attrs={'placeholder': "Numero de l'agence"}))
    slogan = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Entrer Votre Slogan Ici'}))
    facebook = forms.URLField(widget=forms.TextInput(attrs={
        'placeholder': 'Entrer Votre Lien Facebook Ici',
        'required' : False
        }))
    twitter = forms.URLField(widget=forms.TextInput(attrs={'placeholder': 'Entrer Votre Lien Twitter Ici'}))
    instagram = forms.URLField(widget=forms.TextInput(attrs={'placeholder': 'Entrer Votre Lien Instagram Ici'}))
    video_principal = forms.FileField()
    class Meta:
        model = Main
        fields = '__all__'
class RubriqueForm(forms.ModelForm):
    def __init__(self,  *args, **kwargs):
        super(RubriqueForm, self).__init__(*args, **kwargs)
        helper = self.helper = FormHelper()
        layout = helper.layout = Layout()
        helper.form_show_labels = False
        self.fields['slug'].required = False


    rubrique_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Nom de rubrique'}))
    slug = forms.SlugField(widget=forms.TextInput(attrs={'placeholder': 'Slug ',
    'type': 'hidden'}))
    prepopulated_fields = {"slug": ("rubrique_name",)}
    class Meta:
        model = Rubrique
        fields = ('rubrique_name', 'photo_representatif')


class AnnonceForm(forms.ModelForm):
    def __init__(self,  *args, **kwargs):
        super(AnnonceForm, self).__init__(*args, **kwargs)
        helper = self.helper = FormHelper()
        layout = helper.layout = Layout()
        helper.form_show_labels = False
    
    annonce_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': "Nom de l'annonce"}))
    annonce_description = forms.CharField(widget=forms.TextInput(attrs={'placeholder': "Description"}))
    post = forms.TextInput(attrs={'placeholder': "Post detail"})
    date_debut = forms.DateField(
        input_formats=['%Y-%m-%d'],
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'placeholder': "date de départ "
            
        })
    )

    date_fin = forms.DateField(
        input_formats=['%Y-%m-%d'],
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'placeholder': "date de retour"
        })
    )
    class Meta:
        model = Annonce
        fields = '__all__'


class AnnoncePhotoForm(forms.ModelForm):
    id = forms.IntegerField(widget=forms.TextInput(attrs={'type': 'hidden','required' : False}))
    
    def __init__(self,  *args, **kwargs):
        super(AnnoncePhotoForm, self).__init__(*args, **kwargs)
        helper = self.helper = FormHelper()
        layout = helper.layout = Layout()
        helper.form_show_labels = False
        self.fields['id'].required = False

    class Meta:
        model = Annonce_Photo
        fields = ('image',)
        exclude = ('id',)

AnnnocePhotoInlineFormset = inlineformset_factory(
    Annonce,
    Annonce_Photo,
    form=AnnoncePhotoForm,
    extra=10,
)
class EndroitForm(forms.ModelForm):
    def __init__(self,  *args, **kwargs):
        super(EndroitForm, self).__init__(*args, **kwargs)
        helper = self.helper = FormHelper()
        layout = helper.layout = Layout()
        helper.form_show_labels = False

    nom_endroit = forms.CharField(widget=forms.TextInput(attrs={'placeholder': "Nom D'endroit "}))
    class Meta:
        model = Endroit
        fields = '__all__'
    