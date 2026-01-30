from django import forms

# Yapay Zeka sayfasındaki algoritma seçenekleri
ALGORITHM_CHOICES=[
    ('knn', 'K-Nearest Neighbors (KNN)'),
    ('svm', 'Support Vector Machine (SVM)'),
    ('dt', 'Decision Tree')
]

class PredictionForm(forms.Form):
    # predict.html içindeki input isimleri: sl, sw, pl, pw
    # Arkadaşın 'model_type' dediği için burayı da ona göre ayarladık.
    sl = forms.FloatField(label='Sepal Length', min_value=0, required=True)
    sw = forms.FloatField(label='Sepal Width', min_value=0, required=True)
    pl = forms.FloatField(label='Petal Length', min_value=0, required=True)
    pw = forms.FloatField(label='Petal Width', min_value=0, required=True)
    
    # Algoritma seçimi
    model_type = forms.ChoiceField(choices=ALGORITHM_CHOICES, label='Algorithm')