from django.contrib import admin
from .models import Student,Cour,Point,Utilisateur

# Register your models here.

class EtudiantAdmin(admin.ModelAdmin):
    
    list_display=['CodeEtudiant','Matricule','NomEtudiant','PrenomEtudiant','DateNaissance']
    
class CourAdmin(admin.ModelAdmin):
    
    list_display=['CodeCours','NomCours','VolumeCours']
    
class NoteAdmin(admin.ModelAdmin):
    
    list_display=['CodeNote','note','dateNote']
    
admin.site.register(Student,EtudiantAdmin)
admin.site.register(Cour,CourAdmin)
admin.site.register(Point,NoteAdmin)
admin.site.register(Utilisateur)