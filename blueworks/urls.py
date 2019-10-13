from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='start'),
    path('session', views.session),
    path('index.html', views.index),
    path('logout', views.logout),
    path('reservation', views.reservation, name='reservation'),
    path('utilisateur/<str:status>', views.utilisateur),
    path('coworker.html/', views.coworker),
    path('dashboard.html/', views.dashboard),
    path('accueil.html/', views.accueil, name='home'),
    path('animateur.html/', views.animateur),
    path('sites.html/', views.salle),
    path('espace', views.espace, name='space'),
    path('type', views.type, name='type'),
    path('site', views.site, name='site'),
    path('service', views.service, name='service'),
    path('formule', views.formule, name='formule'),
    path('values', views.values),
    path('plan', views.plan),
    path('stats/<str:annee>/<str:cible>/', views.stats),
    path('link', views.link)
]
handler404 = 'blueworks.views.handler404'
