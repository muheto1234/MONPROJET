"""
URL configuration for monprojet project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
# from monApp.models import CalculEcarType
from AppGestionEtudiant.views import create_note,CalculEcarType,ExporterExcelView,acceuil

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('accounts/', include('allauth.urls')),
    path('Ecartype/',CalculEcarType, name='CalculEcarType'),
    # path('modifier_etudiant/<uuid:etudiant_id>',modifier_etudiant, name='modifier_etudiant'),
    
    path('create_note/',create_note, name='create_note'),
    path('voire_en_excel/',ExporterExcelView.as_view(), name='voire_en_excel'),
    path('', acceuil.as_view(), name='acceuil'),
   
]
