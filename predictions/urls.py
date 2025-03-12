
from django.urls import path
from . import views



app_name = "predictions"
urlpatterns = [
    path("", views.feature_1),
    path("prediction_results/",views.feature_2),
    path('qr/', views.generate_qr, name='qr_code')

]