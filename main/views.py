"""from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .models import IrisPlant, Location
import csv
import io

# --- CSV İNDİRME (EXPORT) ---
def export_iris_csv(request):
    # 1. Dosya tipini ayarla
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="iris_verileri.csv"'

    # 2. Yazıcıyı başlat ve başlıkları yaz
    writer = csv.writer(response)
    writer.writerow(['SepalLengthCm', 'SepalWidthCm', 'PetalLengthCm', 'PetalWidthCm', 'Species'])

    # 3. Veritabanındaki verileri satır satır dosyaya yaz
    plants = IrisPlant.objects.all()
    for plant in plants:
        writer.writerow([
            plant.sepal_length,
            plant.sepal_width,
            plant.petal_length,
            plant.petal_width,
            plant.species
        ])

    return response

# --- CSV YÜKLEME (IMPORT) ---
def import_iris_csv(request):
    if request.method == "POST":
        try:
            csv_file = request.FILES['csv_file']
            
            # Sadece .csv dosyası mı kontrol et
            if not csv_file.name.endswith('.csv'):
                messages.error(request, 'Lütfen bir CSV dosyası yükleyin.')
                return render(request, 'import.html')

            # Dosyayı oku
            data_set = csv_file.read().decode('UTF-8')
            io_string = io.StringIO(data_set)
            next(io_string) # Başlık satırını atla

            # Satır satır veritabanına kaydet
            for column in csv.reader(io_string, delimiter=',', quotechar="|"):
                # Örnek CSV yapısı: ID, SepalL, SepalW, PetalL, PetalW, Species
                # Eğer ID sütunu varsa 1. indexten başla, yoksa 0'dan.
                # Biz garanti olsun diye ID varmış gibi (Dataset yapısına göre) alıyoruz:
                
                # Basit bir kontrol: Veri satırı dolu mu?
                if len(column) > 4:
                    IrisPlant.objects.create(
                        sepal_length=float(column[1]), # ID'yi atladık
                        sepal_width=float(column[2]),
                        petal_length=float(column[3]),
                        petal_width=float(column[4]),
                        species=column[5]
                    )
            
            messages.success(request, 'Veriler başarıyla yüklendi!')
            return redirect('/admin/') # Şimdilik admin paneline yönlendirsin
            
        except Exception as e:
            messages.error(request, f"Hata: {e}")

    return render(request, 'import.html')
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from .models import IrisPlant
import csv
import io

# --- BONUS: API & ML Kütüphaneleri ---
from rest_framework import viewsets
from .serializers import IrisPlantSerializer
try:
    from sklearn.datasets import load_iris
    from sklearn.neighbors import KNeighborsClassifier
    from sklearn.svm import SVC
    from sklearn.tree import DecisionTreeClassifier
except ImportError:
    pass 

# --- 1. CSV İŞLEMLERİ (SENİN KISMIN) ---
def export_iris_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="iris_verileri.csv"'
    writer = csv.writer(response)
    writer.writerow(['SepalLengthCm', 'SepalWidthCm', 'PetalLengthCm', 'PetalWidthCm', 'Species'])
    plants = IrisPlant.objects.all()
    for plant in plants:
        writer.writerow([plant.sepal_length, plant.sepal_width, plant.petal_length, plant.petal_width, plant.species])
    return response

def import_iris_csv(request):
    if request.method == "POST":
        try:
            csv_file = request.FILES.get('csv_file')
            if not csv_file or not csv_file.name.endswith('.csv'):
                messages.error(request, 'Lütfen bir CSV dosyası yükleyin.')
                return redirect('list_view')
            
            data_set = csv_file.read().decode('UTF-8')
            io_string = io.StringIO(data_set)
            next(io_string) 
            for column in csv.reader(io_string, delimiter=',', quotechar="|"):
                if len(column) > 4:
                    IrisPlant.objects.create(
                        sepal_length=float(column[1]) if len(column)>5 else float(column[0]),
                        sepal_width=float(column[2]) if len(column)>5 else float(column[1]),
                        petal_length=float(column[3]) if len(column)>5 else float(column[2]),
                        petal_width=float(column[4]) if len(column)>5 else float(column[3]),
                        species=column[5] if len(column)>5 else column[4]
                    )
            messages.success(request, 'Veriler yüklendi!')
            return redirect('list_view')
        except Exception as e:
            messages.error(request, f"Hata: {e}")
            return redirect('list_view')
    return render(request, 'import.html')

# --- 2. SAYFALAR ---

def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('search_view')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def list_view(request):
    plants = IrisPlant.objects.all()
    return render(request, 'list.html', {'plants': plants})

def add_view(request):
    if request.method == "POST":
        # add.html içindeki name değerlerini alıyoruz
        IrisPlant.objects.create(
            sepal_length=request.POST.get('sepal_length'),
            sepal_width=request.POST.get('sepal_width'),
            petal_length=request.POST.get('petal_length'),
            petal_width=request.POST.get('petal_width'),
            species=request.POST.get('species')
        )
        return redirect('list_view')
    return render(request, 'add.html')

def delete_view(request, id):
    plant = get_object_or_404(IrisPlant, id=id)
    plant.delete()
    return redirect('list_view')

def search_view(request):
    results = IrisPlant.objects.all()
    # search.html içindeki input isimleri: min_sepal_len, max_sepal_len, species
    query_species = request.GET.get('species')
    query_min = request.GET.get('min_sepal_len')
    query_max = request.GET.get('max_sepal_len')

    if query_species and query_species != "":
        results = results.filter(species__icontains=query_species)
    if query_min:
        results = results.filter(sepal_length__gte=query_min)
    if query_max:
        results = results.filter(sepal_length__lte=query_max)

    return render(request, 'search.html', {'results': results})

# --- 3. BONUS (YAPAY ZEKA) ---

class IrisPlantViewSet(viewsets.ModelViewSet):
    queryset = IrisPlant.objects.all()
    serializer_class = IrisPlantSerializer

def predict_view(request):
    predictionResult = None
    if request.method == 'POST':
        # predict.html içindeki name değerleri: sl, sw, pl, pw, model_type
        sl = request.POST.get('sl')
        sw = request.POST.get('sw')
        pl = request.POST.get('pl')
        pw = request.POST.get('pw')
        alg = request.POST.get('model_type')

        if sl and sw and pl and pw:
            try:
                iris = load_iris()
                x, y = iris.data, iris.target
                
                if alg == 'knn':
                    model = KNeighborsClassifier(n_neighbors=3)
                elif alg == 'svm':
                    model = SVC()
                else:
                    model = DecisionTreeClassifier()
                
                model.fit(x, y)
                # Tahmin yap
                pred_index = model.predict([[float(sl), float(sw), float(pl), float(pw)]])[0]
                predictionResult = iris.target_names[pred_index]
            except:
                predictionResult = "Hata oluştu"

    return render(request, 'predict.html', {'result': predictionResult})