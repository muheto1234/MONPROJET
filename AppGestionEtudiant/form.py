from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Point,Student,Cour


class RegisterForm(UserCreationForm):
    class Meta:
        model=User
        fields={'username','first_name','last_name','email'}

class NoteForm(forms.ModelForm):
    class Meta:
        model = Point
        fields = '__all__'

class CourForm(forms.ModelForm):
    class Meta:
        model = Cour
        fields = '__all__'

class EtudiantForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = '__all__'

class ModifierEtudiantForm(forms.Form):
    etudiant_form = EtudiantForm()
    cour_form = CourForm()
    note_form = NoteForm()