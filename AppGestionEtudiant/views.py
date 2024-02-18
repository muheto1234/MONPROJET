from django.shortcuts import render
from .models import Student, Cour, Point
from .form import ModifierEtudiantForm,NoteForm,CourForm,EtudiantForm
from django.shortcuts import get_object_or_404
import pandas as pd
# import numpy as np
import statistics
from django.views import View
from django.shortcuts import render, redirect
# from django.contrib.auth import login, logout, authenticate
# from django.contrib.auth.decorators import login_required
from django.contrib import messages
# from .form import RegisterForm
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.views.generic import ListView
from django.core.exceptions import ObjectDoesNotExist
from .models import Utilisateur as CustomUser


User = get_user_model()
# Create your views here.


def CalculEcarType(request):
    etudiants = Student.objects.all()
    selected_etudiant = None
    if request.method == 'POST':
        selected_etudiant = Student.objects.get(CodeEtudiant=request.POST['etudiant'])
        notes = selected_etudiant.point_set.all().values_list('note', flat=True)
        if len(notes) > 1:
            selected_etudiant.ecart_type = statistics.stdev(notes)
        else:
            selected_etudiant.ecart_type = 0
    return render(request, 'base.html', {'etudiants': etudiants, 'selected_etudiant': selected_etudiant})





class ExporterExcelView(View):
    def get(self, request, *args, **kwargs):
        # Récupérer les données de la base de données
        queryset = Point.objects.select_related('etudiant', 'cours').all()

        # Convertir le queryset en une liste de dictionnaires
        data = queryset.values('CodeNote', 'etudiant__NomEtudiant', 'etudiant__PrenomEtudiant',
                               'cours__NomCours', 'cours__VolumeCours', 'note', 'dateNote')

        # Convertir la liste de dictionnaires en un DataFrame pandas
        df = pd.DataFrame.from_records(data)

        # Rendre les objets datetime indépendants du fuseau horaire
        df['dateNote'] = df['dateNote'].dt.tz_convert(None)

        # Créer une réponse HTTP avec un type de contenu Excel
        response = HttpResponse(content_type='application/vnd.ms-excel')

        # Créer un nom de fichier
        response['Content-Disposition'] = 'attachment; filename=Note2.xlsx'

        # Écrire le DataFrame dans la réponse HTTP
        df.to_excel(response, index=False)

        return response

class acceuil(ListView):
    model = Point
    context_object_name = 'form'
    template_name = 'acceuil.html'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.GET.get('q')
        if q:
            return queryset.filter(
                Q(note__icontains=q) |
                Q(etudiant__NomEtudiant__icontains=q) |
                Q(etudiant__PrenomEtudiant__icontains=q) |
                Q(cours__NomCours__icontains=q) |
                Q(etudiant__Matricule__icontains=q)
            )
        return queryset


def create_note(request):
    if request.method == 'POST':
        etudiant_name = request.POST['Nom']
        etudiant_prenom = request.POST['PrenomEtudiant']
        etudiant_matricule = request.POST['Matricule']
        cours_name = request.POST['cours']
        note_value = request.POST['note']
        

        etudiant, _ = Student.objects.get_or_create(NomEtudiant=etudiant_name,PrenomEtudiant=etudiant_prenom,Matricule=etudiant_matricule)
        cours, _ = Cour.objects.get_or_create(NomCours=cours_name)

        note = Point(etudiant=etudiant, cours=cours, note=note_value)
        note.save()

        return redirect('acceuil')

    else:
        return render(request, 'note.html')



# def modifier_etudiant(request, etudiant_id):
#     etudiant = Student.objects.get(CodeEtudiant=etudiant_id)
    
#     try:
#         notes = Point.objects.filter(etudiant=etudiant)
#         note_forms = []
#         for note in notes:
#             note_form = NoteForm(instance=note)
#             note_forms.append(note_form)
#     except ObjectDoesNotExist:
#         note_forms = []
    
#     if request.method == 'POST':
#         form = ModifierEtudiantForm(request.POST, initial={
#             'etudiant_form': EtudiantForm(instance=etudiant),
#             'note_forms': note_forms,
#         })
#         if form.is_valid():
#             etudiant_form = form.cleaned_data['etudiant_form']
#             note_forms = form.cleaned_data['note_forms']
            
#             etudiant_form.save()
#             for note_form in note_forms:
#                 note_form.save()
            
#             return redirect('liste_etudiants')
#     else:
#         form = ModifierEtudiantForm(initial={
#             'etudiant_form': EtudiantForm(instance=etudiant),
#             'note_forms': note_forms,
#         })
    
#     context = {
#         'form': form,
#         'notes': notes,
#     }
#     return render(request, 'modifier_etudiant.html', context)

# def update_roles(request, id):
#     user = CustomUser.objects.get(id=id)
#     if request.method == 'POST':
#         is_enseignant = request.POST.get('is_enseignant', False)
#         is_ettudiant = request.POST.get('is_ettudiant', False)
#         user.is_enseignant = bool(is_enseignant)
#         user.is_ettudiant = bool(is_ettudiant)

#         user.save()
#         return redirect('users')
#     return render(request,'update_roles.html',{'user':user})
    
# def users(request):
#     users = CustomUser.objects.all()
#     return render(request, 'users.html', {'users': users})
