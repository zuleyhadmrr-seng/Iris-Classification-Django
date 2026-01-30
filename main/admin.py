from django.contrib import admin
from .models import Location, IrisPlant

# Yan modeli panele ekle
admin.site.register(Location)

# Ana modeli özelleştirerek panele ekle (Filtreleme ve Arama kutusu ekliyoruz)
@admin.register(IrisPlant)
class IrisPlantAdmin(admin.ModelAdmin):
    list_display = ('species', 'sepal_length', 'sepal_width', 'location', 'created_at')
    list_filter = ('species', 'location') # Sağ tarafta filtre menüsü çıkar
    search_fields = ('species',) # Üstte arama kutusu çıkar
