from django.db import models

# Create your models here.
from django.contrib.auth.models import User
# Create your models here.
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator

class Equipe(models.Model):
    id_equipe = models.AutoField(primary_key=True)
    nom_equipe = models.CharField(max_length=42)
    lien_logo = models.CharField(max_length=100)
    id_groupe = models.CharField(max_length=1)

    def __str__(self):
        return self.nom_equipe
    
    
class Pari(models.Model):
    id_pari = models.AutoField(primary_key=True)
    id_parieur = models.ForeignKey(User, on_delete=models.CASCADE,)
    #id_match = models.IntegerField()
    id_match = models.ForeignKey('Match', on_delete=models.CASCADE,)
    pari_eq1 = models.PositiveSmallIntegerField(null = True,blank=True)
    pari_eq2 = models.PositiveSmallIntegerField(null = True,blank=True)
    
    def __str__(self):
        return str(self.id_match)+'_'+str(self.pari_eq1)+'_'+str(self.pari_eq2)

class Match(models.Model):
    id_match = models.AutoField(primary_key=True)
    id_eq1 = models.ForeignKey('Equipe', on_delete=models.CASCADE,related_name="id_eq1")
    id_eq2 = models.ForeignKey('Equipe', on_delete=models.CASCADE,related_name="id_eq2")
    date = models.DateTimeField()
    lieu = models.CharField(max_length=42) 
    score_eq1 = models.PositiveSmallIntegerField(null = True,blank=True)
    score_eq2 = models.PositiveSmallIntegerField(null = True,blank=True)
    id_phase = models.ForeignKey('Phase', on_delete=models.CASCADE,)
    ferme = models.BooleanField()
    
    def __str__(self):
        return self.lieu  
      
class Resultat(models.Model):
    user = models.OneToOneField(User)
    nb_match_pari = models.PositiveIntegerField()
    nb_match_gagnant = models.PositiveIntegerField()
    nb_score_gagnant = models.PositiveIntegerField()
    nb_match_point = models.PositiveIntegerField()
    nb_score_point = models.PositiveIntegerField()    
    
class Phase(models.Model):
    id_phase = models.AutoField(primary_key=True)
    nom_phase = models.CharField(max_length=42) 
    groupe = models.BooleanField()
    point_pari =  models.PositiveSmallIntegerField()
    point_score =  models.PositiveSmallIntegerField()

    def __str__(self):
        return self.nom_phase

class Joueur(models.Model):
     user = models.OneToOneField(User, on_delete=models.CASCADE,  primary_key=True)
     prenom = models.CharField(max_length=42) 
     nom = models.CharField(max_length=42) 
     service = models.CharField(max_length=42, null = True,blank=True)
     mail = models.EmailField(max_length=80) 
     
     def __str__(self):
        return self.prenom
