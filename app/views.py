from django.shortcuts import render
from datetime import datetime
from .models import Phase, Equipe, Match, Pari, User, Joueur
from .form import ConnexionForm, UtilisateurForm, JoueurForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.db.models import Min
from django.contrib import messages

# Create your views here.
def date_actuelle(request):
    return render(request, 'app/date.html', {'date': datetime.now()})

@login_required
def pari(request, phase):    
    liste_phase = list(Phase.objects.all())

    try:
        id_p = Phase.objects.filter(nom_phase = phase)[0]
    except IndexError:
        id_p = Phase.objects.all().order_by('id_phase')[0]

    phase_actuelle = id_p.nom_phase
    liste_match = Match.objects.filter(id_phase = id_p).filter(pari__id_parieur= request.user.id).order_by('id_eq1__id_groupe', 'id_eq1').annotate(pari1= Min('pari__pari_eq1')).annotate(pari2= Min('pari__pari_eq2'))
    if not liste_match:
        liste_match=  Match.objects.filter(id_phase = id_p).order_by('id_eq1__id_groupe', 'id_eq1')

    liste_eq_grp= Equipe.objects.all().order_by('id_groupe')
    if request.method == 'POST':    
        tralala = request.POST
        for match in liste_match:
            try:
                pari = Pari.objects.get(id_match = match, id_parieur= request.user.id)
            except Pari.DoesNotExist:
                pari = Pari(id_match = match)
                pari.id_parieur = User.objects.get(username= request.user.username)
            if tralala['f'+str(match.id_match)+'_'+'eq1'] == '':
                pari.pari_eq1 = None
            else:
                pari.pari_eq1 = tralala['f'+str(match.id_match)+'_'+'eq1']
                
            if tralala['f'+str(match.id_match)+'_'+'eq2'] == '':
                pari.pari_eq2 = None
            else:
                pari.pari_eq2 = tralala['f'+str(match.id_match)+'_'+'eq2']
            
            pari.save()
        liste_match = Match.objects.filter(id_phase = id_p).filter(pari__id_parieur= request.user.id).order_by('id_eq1__id_groupe', 'id_eq1').annotate(pari1= Min('pari__pari_eq1')).annotate(pari2= Min('pari__pari_eq2'))
        envoi = True        
    return render(request, 'app/pari.html', locals())

def inscription(request):
    if request.method == 'POST':
        form = JoueurForm(request.POST)
        form2 = UtilisateurForm(request.POST)
        if form.is_valid() and form2.is_valid():
            login = form2.cleaned_data['login']
            password = form2.cleaned_data['password1']
            mail = form.cleaned_data['mail']
            user = User.objects.create_user(login, mail, password)
            joueur = form.save(commit=False)
            joueur.user =   user
            joueur.save()
            messages.success(request, 'Le compte a été créé : vous pouvez maintenant vous connecter')
            return render(request, 'app/pari.html', locals())
    else:
        form = JoueurForm()
        form2 = UtilisateurForm()
    return render(request, 'app/inscription.html', locals())

def connexion(request):
    error = False
    if request.method == "POST":
        form = ConnexionForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)  # Nous vérifions si les données sont correctes
            if user:  # Si l'objet renvoyé n'est pas None
                login(request, user)  # nous connectons l'utilisateur
            else: # sinon une erreur sera affichée
                error = True
    else:
        form = ConnexionForm()
    return render(request, 'blog/connexion.html', locals())
