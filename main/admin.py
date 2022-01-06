from django.contrib import admin
from django.db.models import fields

# Register your models here.
from main.models import Main, Reservation, Rubrique, Annonce, Annonce_Photo, Endroit

class MainAdmin(admin.ModelAdmin):
	model = Main

class RubriqueAdmin(admin.ModelAdmin):
    model = Rubrique
    prepopulated_fields = {"slug": ("rubrique_name",)}

class Annonce_Image_Tabular(admin.TabularInline):
    model = Annonce_Photo
    extra = 0

class AnnonceAdmin(admin.ModelAdmin):
    model = Annonce
    inlines = [
        Annonce_Image_Tabular,
    ]


class ReservationAdmin(admin.ModelAdmin):
    model = Reservation
    list_display = ('id', 'email', 'created_at', 'reservation_date')
    list_filter = ('id',)
    list_editable = ('created_at', )

    def get_date_formatted(self, obj):
        if obj:
            return obj.created_at.date()
    get_date_formatted.admin_order_field = 'created_at'
    get_date_formatted.short_description = 'created_at'

admin.site.register(Main, MainAdmin)
admin.site.register(Rubrique, RubriqueAdmin)
admin.site.register(Annonce, AnnonceAdmin)
admin.site.register(Annonce_Photo)
admin.site.register(Reservation, ReservationAdmin)
admin.site.register(Endroit)


