from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser


# Create your models here.

class Utilisateur(AbstractUser):
    is_enseignant=models.BooleanField(default=False)
    is_ettudiant=models.BooleanField(default=False)
    
    

#création du table Etudian
class Student(models.Model):
    CodeEtudiant = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    Matricule=models.CharField(max_length=20)
    NomEtudiant=models.CharField(max_length=50) 
    PrenomEtudiant=models.CharField(max_length=50) 
    DateNaissance=models.DateTimeField(auto_now=True)
    
    #pour mettre le nom en majiscule
    @property
    def nom(self):
        return str(self.NomEtudiant).upper()

    #pour mettre la premiere mot en majiscule
    @property
    def prenom(self):
        return str(self.PrenomEtudiant).capitalize()


        
    def __str__(self):
        return self.NomEtudiant

class Cour(models.Model) :
    CodeCours = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    NomCours=models.CharField(max_length=20)
    VolumeCours=models.CharField(max_length=20)
    
    def __str__(self):
        return self.NomCours
    
#création du table Cour

class Point(models.Model):
    CodeNote = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    etudiant=models.ForeignKey(Student,on_delete=models.CASCADE) 
    cours=models.ForeignKey(Cour,on_delete=models.CASCADE) 
    note= models.DecimalField(max_digits=5, decimal_places=2)
    dateNote=models.DateTimeField(auto_now=True)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['etudiant', 'cours'], name='unique_etudiant_cours')
        ]



    def __str__(self):
        return f"{self.etudiant.PrenomEtudiant} {self.etudiant.NomEtudiant} - {self.cours.NomCours}: {self.note}"

