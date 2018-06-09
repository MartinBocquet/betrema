from django.shortcuts import render

from datetime import datetime
from django.shortcuts import render, redirect
from django.http import HttpResponse
from datetime import datetime
from django.forms import formset_factory
from .models import Phase, Equipe, Match, Pari, User
from .form import ContactForm, ScoreForm, MetaScoreForm, ConnexionForm
from django.contrib.auth import authenticate, login, logout
#from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Count, Min, Sum

# Create your views here.
def date_actuelle(request):
    return render(request, 'app/date.html', {'date': datetime.now()})

def lister_phases(request):    
    liste_match = Match.objects.filter(id_phase = 1)
    form = ScoreForm(request.POST or None)
    liste_pari  = list(Pari.objects.all().filter(id_match__id_phase = 1, id_parieur= request.user.id).order_by('id_match__id_eq1__id_groupe', 'id_match__id_eq1'))
    liste_match = list(Match.objects.filter(id_phase = 1).order_by('id_eq1__id_groupe', 'id_eq1'))
    liste_match2 = Match.objects.filter(id_phase = 1).filter(pari__id_parieur= request.user.id).order_by('id_eq1__id_groupe', 'id_eq1').annotate(pari1= Min('pari__pari_eq1')).annotate(pari2= Min('pari__pari_eq2'))
    machin = request.user.username
    machin = 'aaa'
    result = zip(liste_match, liste_pari)
    if request.method == 'POST':    
        tralala = request.POST
        for match in liste_match:
            pari = Pari()
            pari.id_match = Match.objects.get(id_match = match.id_match)
            pari.id_parieur = User.objects.get(username = request.user.username)
            test = 'f'+str(match.id_match)+'_'+'eq1'
            pari.pari_eq1 = tralala['f'+str(match.id_match)+'_'+'eq1']
            pari.pari_eq2 = tralala['f'+str(match.id_match)+'_'+'eq2']
            pari.save()
        envoi = True
    return render(request, 'app/lister_phases.html', locals())

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
    return render(request, 'blog/test_pari.html', locals())