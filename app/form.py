'''
Created on 31 mai 2018

@author: Martin
'''

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Joueur
    
    
class ConnexionForm(forms.Form):
    username = forms.CharField(label="Nom d'utilisateur", max_length=30)
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)
    
class UtilisateurForm(forms.Form):#UserCreationForm):
    login = forms.CharField(label="Login", max_length=30)
    password1 = forms.CharField(label="Mot de passe",
        widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirmer le mot de passe",
        widget=forms.PasswordInput,
        help_text="Les deux mots de passe doivent être identiques")
    
    
    error_messages = {
        'password_mismatch': ("Les deux pass ne correspondent pas"),
    }
    
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
    
class JoueurForm(forms.ModelForm):
    class Meta:
        model = Joueur
        exclude = ['user']