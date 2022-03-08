
from datetime import datetime
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from django.urls import reverse
from acceso.models import User
from deseos.forms import WishForm
from deseos.models import Wish
from django.db.models import Count

def index(request):
    if request.method == 'GET':
        if 'usuario' not in request.session:
            messages.error(request, 'No estás logeado')
            return redirect(reverse('acceso:index'))
        else:
            print(request.session['usuario'])
            user = request.session['usuario']

            context = {
            #'allwishes' : Wish.objects.all(),
            'usuario' : User.objects.get(id = user['id']),
            'allwishes' : Wish.objects.annotate(numero_likes = Count('users_who_liked'))

            #'equipos_mas_doce' : Team.objects.annotate(player_count = Count('all_players'))
            }
            return render(request, 'deseos/index.html', context)

# Create your views here.
