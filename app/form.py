'''
Created on 31 mai 2018

@author: Martin
'''

from django import forms


class ContactForm(forms.Form):
    sujet = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)
    envoyeur = forms.EmailField(label="Votre adresse e-mail")
    renvoi = forms.BooleanField(help_text="Cochez si vous souhaitez obtenir une copie du mail envoyé.", required=False)
    
class ScoreForm(forms.Form):
    score_eq1 = forms.IntegerField(required=False, min_value = 0, max_value = 10)
    score_eq2 = forms.IntegerField(required=False, min_value = 0, max_value = 10)   
     
class MetaScoreForm(forms.Form):
    score_eq1 = forms.IntegerField(required=False, min_value = 0, max_value = 10)
    score_eq2 = forms.IntegerField(required=False, min_value = 0, max_value = 10)
    score_eq3 = forms.IntegerField(required=False, min_value = 0, max_value = 10)
    
class ConnexionForm(forms.Form):
    username = forms.CharField(label="Nom d'utilisateur", max_length=30)
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)