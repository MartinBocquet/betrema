from django.shortcuts import render

from datetime import datetime

# Create your views here.
def date_actuelle(request):
    return render(request, 'app/date.html', {'date': datetime.now()})