from django.db import models

# 1. Model: Konum (Yan Model - Zorunluluk: En az 5 field)
class Location(models.Model):
    region_name = models.CharField(max_length=100, verbose_name="Bölge Adı")
    city = models.CharField(max_length=50, verbose_name="Şehir")
    altitude = models.IntegerField(verbose_name="Rakım (m)")
    climate_type = models.CharField(max_length=50, verbose_name="İklim Tipi")
    recorded_date = models.DateField(auto_now_add=True, verbose_name="Kayıt Tarihi")

    def __str__(self):
        return f"{self.region_name} - {self.city}"

# 2. Model: Iris Çiçeği (Ana Model - Zorunluluk: Iris verileri + İlişki)
class IrisPlant(models.Model):
    # İlişki: Bir çiçeğin bir konumu olur (ForeignKey)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, verbose_name="Toplandığı Konum", null=True, blank=True)
    
    sepal_length = models.FloatField(verbose_name="Çanak Yaprak Uzunluğu")
    sepal_width = models.FloatField(verbose_name="Çanak Yaprak Genişliği")
    petal_length = models.FloatField(verbose_name="Taç Yaprak Uzunluğu")
    petal_width = models.FloatField(verbose_name="Taç Yaprak Genişliği")
    species = models.CharField(max_length=50, verbose_name="Tür") # Setosa, Versicolor vb.
    
    created_at = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return f"{self.species} ({self.sepal_length}, {self.sepal_width})"

