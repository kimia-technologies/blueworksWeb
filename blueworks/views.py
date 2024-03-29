from django.shortcuts import render, redirect, reverse
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.http import JsonResponse, QueryDict
from datetime import datetime
import hashlib
import json
from django.db.models import Count
from blueworks.models import *

# Create your views here.


def handler404(request, exception):
    return render(request,
                  '404.html', locals())


def home(request):
    return redirect('index.html')


def index(request):
    return render(request, 'index.html')


def session(request):
    if request.method == 'POST':
        params = request.POST
        user = json.loads(params['user'])
        request.session[params['token']] = {
            'user': user, 'rf': params['refreshToken']}
        return JsonResponse({'msg': 'created'})
    else:
        if request.session.get(request.GET['token']):
            return JsonResponse({'msg': request.session.get(request.GET['token'])})
        return JsonResponse({'msg': 'not found'})


def logout(request):
    toks = Token.objects.filter(email=request.GET['e'])
    for tok in toks:
        tok.delete()
    return redirect('start')


def reservation(request):
    if request.method == 'GET':
        rsvs = Reservation.objects.all().order_by('-etat')
        out = []
        nom = ''
        button = '<button data-toggle="modal" title="Edit" class="pd-setting-ed" data-target="#myModalUpdate" onclick="const tab = '"$(this).parent().parent()"'; $('"'#update_id'"').val(tab.find('"'td:eq(0)'"').text()); $('"'#typeU'"').val(tab.find('"'td:eq(4)'"').text()); $('"'#formuleU'"').val(tab.find('"'td:eq(3)'"').text()); $('"'#jourU'"').val(tab.find('"'td:eq(7)'"').text()); $('"'#trancheU'"').val(tab.find('"'td:eq(8)'"').text()); $('"'#coworkerU'"').val(tab.find('"'td:eq(6)'"').text());"><i class="fa fa-pencil-square-o" aria-hidden="true"></i></button><button data-toggle="modal" data-target="#myModalDelete" title="Trash" class="pd-setting-ed" onclick="const tab = '"$(this).parent().parent()"'; $('"'#delete_id'"').val(tab.find('"'td:eq(0)'"').text());"><i class="fa fa-trash-o" aria-hidden="true"></i></button>'
        for rsv in rsvs:
            if(rsv.idformule.periode != 0):
                nom = '{0}'.format(rsv.idformule.periode) + \
                    ' ' + rsv.idformule.unite
            else:
                nom = 'consommation direct'
            out.append({'ID': str(rsv.idreservation), 'NOM': str(rsv.email.nom), 'EMAIL': rsv.email.email, 'FORMULE': nom, 'TYPE': rsv.numespace.nomtype.nomtype, 'SALLE': rsv.numespace.nom,
                        'NBCOWORKER': rsv.nbinvite, 'JOUR': rsv.jour, 'EXPIRE': str(rsv.expire), 'DATE': str(rsv.createdat),
                        'TRANCHE': rsv.tranche, 'ETAT': rsv.etat, 'OPTION': button})
        return JsonResponse(out, safe=False)


def utilisateur(request, status):
    out = []
    somme = 0
    annots = []
    rsvs = []
    animateurs = []
    if request.method == 'GET':
        if status == 'customer':
            users = Utilisateur.objects.exclude(email__in=Possede.objects.filter(Q(nomrole='Animateur') |
                                                                                 Q(nomrole='Area Manager') |
                                                                                 Q(nomrole='General Manager'))
                                                .values_list('email', flat=True)).order_by('nom')
            for user in users:
                out.append({'NOM': user.nom, 'PRENOM': user.prenom, 'EMAIL': user.email, 'PHONE': user.phone, 'PSEUDO': user.pseudo,
                            'ANNIV': user.anniv, 'ENT': user.entreprise})
        else:
            rsvs = Reservation.objects.filter(Q(etat=1) | Q(
                etat=-1)).filter(annee=datetime.now().year)
            annots = rsvs.values('mois', 'annee').annotate(
                m=Count('mois'), a=Count('annee'))
            animateurs = Possede.objects.filter(
                nomrole='Animateur')
            for anim in animateurs:
                tmp = []
                for ano in annots:
                    mois = ano['mois']
                    for rsv in rsvs:
                        inv = Invite.objects.filter(
                            animateur=anim.email, person=rsv.email)
                        if rsv.mois == mois and len(inv) != 0:
                            somme = somme + \
                                Offre.objects.get(idformule=rsv.idformule,
                                                  nomtype=rsv.numespace.nomtype).prix
                    tmp.append({'mois': mois, 'revenu': somme})
                    somme = 0
                out.append({'pseudo': anim.email.pseudo, 'nom': anim.email.nom,
                            'photo': anim.email.photo, 'phone': anim.email.phone, 'stats': tmp})
                tmp = []
        return JsonResponse(out, safe=False)
    elif request.method == 'DELETE':
        id = QueryDict(request.body)
        user = Utilisateur.objects.get(email=id['e'])
        user.etat = -1
        user.save()


def espace(request):
    if request.method == 'GET':
        espaces = Espace.objects.all()
        button = '<button data-toggle="modal" title="Edit" class="pd-setting-ed" data-target="#myModalUpdateSalle" onclick="const tab = '"$(this).parent().parent()"'; $('"'#update_id'"').val(tab.find('"'td:eq(0)'"').text()); $('"'#s'"').val(tab.find('"'td:eq(1)'"').text()); $('"'#t'"').val(tab.find('"'td:eq(2)'"').text());"><i class="fa fa-pencil-square-o" aria-hidden="true"></i></button><button data-toggle="modal" title="Trash" class="pd-setting-ed" data-target="#myModalDelete" onclick="const tab = '"$(this).parent().parent()"'; $('"'#to_delete'"').val('"'espace'"'); $('"'#delete_id'"').val(tab.find('"'td:eq(0)'"').text());"><i class="fa fa-trash-o" aria-hidden="true"></i></button>'
        out = []
        for space in espaces:
            out.append({'ID': space.numespace, 'NOM': space.nom, 'TYPE': space.nomtype.nomtype,
                        'OCCP': space.occp, 'OPTION': button})
        return JsonResponse(out, safe=False)
    elif request.method == 'POST':
        params = request.POST
        nomtype = Type.objects.get(nomtype=params['t'])
        nomsite = Site.objects.get(nomsite=params['s'])
        space = Espace(nomtype=nomtype, nom=params['n'], nomsite=nomsite, createdat=datetime.now(
        ), updatedat=datetime.now())
        space.save()
        return redirect('sites.html')
    elif request.method == 'PATCH':
        params = QueryDict(request.body)
        space = Espace.objects.get(numespace=params['s'])
        space.nom = params['n']
        space.nomtype = Type.objects.get(nomtype=params['t'])
        space.updatedat = datetime.now()
        space.save()
        return JsonResponse({'msg': 'success'})
    else:
        id = QueryDict(request.body)
        Espace.objects.get(numespace=id['n']).delete()
        return JsonResponse({'msg': 'success'})


def type(request):
    if request.method == 'GET':
        button = '<button data-toggle="tooltip" title="formule" class="pd-setting-ed">Add formule</button><button data-toggle="modal" title="Edit" class="pd-setting-ed" data-target="#myModalUpdateType" onclick="const tab = '"$(this).parent().parent()"'; $('"'#n'"').val(tab.find('"'td:eq(0)'"').text()); $('"'#c'"').val(tab.find('"'td:eq(1)'"').text()); $('"'#d'"').val(tab.find('"'td:eq(3)'"').text())"><i class="fa fa-pencil-square-o" aria-hidden="true"></i></button><button data-toggle="modal" title="Trash" class="pd-setting-ed" data-target="#myModalDelete" onclick="const tab = '"$(this).parent().parent()"'; $('"'#to_delete'"').val('"'type'"'); $('"'#delete_id'"').val(tab.find('"'td:eq(0)'"').text());"> <i class="fa fa-trash-o" aria-hidden="true"></i></button>'
        types = Type.objects.all()
        out = []
        for typ in types:
            offs = []
            offres = Offre.objects.filter(nomtype=typ)
            for off in offres:
                if(off.idformule.periode != 0):
                    offs.append('{0}'.format(off.idformule.periode) +
                                ' ' + off.idformule.unite)
                else:
                    offs.append('consommation direct')
            out.append({'NOM': typ.nomtype, 'CON': typ.contenance, 'INV': typ.invite, 'DESC': typ.description,
                        'FORMULE': str(offs), 'OPTION': button})
        return JsonResponse(out, safe=False)
    elif request.method == 'POST':
        params = request.POST
        typeObj = None
        if params['n'] != 'Open Space':
            typeObj = Type(params['n'], params['c'], params['c'],
                           params['d'], datetime.now(), datetime.now())
        else:
            typeObj = Type(nomtype=params['n'], contenance=params['c'],
                           description=params['d'], createdat=datetime.now(), updatedat=datetime.now())
        typeObj.save()
        return redirect('sites.html')
    elif request.method == 'PATCH':
        params = QueryDict(request.body)
        typ = Type.objects.get(nomtype=params['n'])
        typ.contenance = params['c']
        typ.description = params['d']
        typ.updatedat = datetime.now()
        typ.save()
        return JsonResponse({'msg': 'success'})
    else:
        id = QueryDict(request.body)
        Type.objects.get(nomtype=id['n']).delete()
        return JsonResponse({'msg': 'success'})


def site(request):
    if request.method == 'GET':
        sites = Site.objects.all()
        out = []
        for st in sites:
            out.append({'NOM': site.nomsite, 'QUARTIER': site.quartier})
        return JsonResponse(out, safe=False)
    elif request.method == 'POST':
        params = request.POST
        Site(params['n'], params['q'], params['d']).save()
        return redirect('sites.html')
    elif request.method == 'PATCH':
        params = request.body
        st = Site.objects.get(nomsite=params['n'])
        st.quartier = params['q']
        st.description = params['d']
        st.save()
        return JsonResponse({'msg': 'success'})
    else:
        Site.objects.get(nomsite=request.GET['n']).delete()
        return JsonResponse({'msg': 'success'})


def formule(request):
    if request.method == 'GET':
        formules = Formule.objects.all()
        button = '<button data-toggle="tooltip" title="formule" class="pd-setting-ed">Add service</button><button data-toggle="modal" title="Edit" class="pd-setting-ed" data-target="#myModalUpdateFormule" onclick="const tab = '"$(this).parent().parent()"'; $('"'#update_formule_id'"').val(tab.find('"'td:eq(0)'"').text()); $('"'#f'"').val(tab.find('"'td:eq(1)'"').text()); $('"'#p'"').val(tab.find('"'td:eq(2)'"').text()); $('"'#u'"').val(tab.find('"'td:eq(3)'"').text())"><i class="fa fa-pencil-square-o" aria-hidden="true"></i></button><button data-toggle="modal" title="Trash" class="pd-setting-ed" data-target="#myModalDelete" onclick="const tab = '"$(this).parent().parent()"'; $('"'#to_delete'"').val('"'formule'"'); $('"'#delete_id'"').val(tab.find('"'td:eq(0)'"').text());"> <i class="fa fa-trash-o" aria-hidden="true"></i></button>'
        out = []
        nom = ''
        for formule in formules:
            servs = []
            if formule.nom == None:
                if(formule.periode != 0):
                    nom = '{0}'.format(formule.periode) + ' ' + formule.unite
                else:
                    nom = 'consommation direct'
            else:
                nom = formule.nom
            contients = Contient.objects.filter(idformule=formule)
            for cont in contients:
                servs.append(str(cont.nomservice.nomservice) +
                             ' {0} {1}'.format(cont.quantite, cont.nomservice.unite))
            out.append({'ID': formule.idformule, 'NOM': nom, 'PERIODE': formule.periode, 'UNITE': formule.unite,
                        'SERVICE': str(servs), 'OPTION': button})
        return JsonResponse(out, safe=False)
    elif request.method == 'POST':
        params = request.POST
        formu = Formule(nom=params['f'],
                        periode=params['p'], unite=params['u'])
        formu.save()
        return redirect('sites.html')
    elif request.method == 'PATCH':
        params = QueryDict(request.body)
        formu = Formule.objects.get(idformule=params['id'])
        formu.periode = params['p']
        formu.unite = params['u']
        formu.nom = params['f']
        formu.save()
        return JsonResponse({'msg': 'success'})
    else:
        id = QueryDict(request.body)
        Formule.objects.get(idformule=id['n']).delete()
        return JsonResponse({'msg': 'success'})


def service(request):
    if request.method == 'GET':
        services = Service.objects.all()
        out = []
        button = '<button data-toggle="modal" title="Edit" class="pd-setting-ed" data-target="#myModalUpdateService" onclick="const tab = '"$(this).parent().parent()"'; $('"'#ns'"').val(tab.find('"'td:eq(0)'"').text()); $('"'#us'"').val(tab.find('"'td:eq(1)'"').text()); $('"'#ds'"').val(tab.find('"'td:eq(2)'"').text());"><i class="fa fa-pencil-square-o" aria-hidden="true"></i></button><button data-toggle="modal" title="Trash" class="pd-setting-ed" data-target="#myModalDelete" onclick="const tab = '"$(this).parent().parent()"'; $('"'#to_delete'"').val('"'service'"'); $('"'#delete_id'"').val(tab.find('"'td:eq(0)'"').text());"><i class="fa fa-trash-o" aria-hidden="true"></i></button>'
        for serv in services:
            out.append({'NOM': serv.nomservice, 'UNITE': serv.unite,
                        'DESCRIPTION': serv.description, 'OPTION': button})
        return JsonResponse(out, safe=False)
    elif request.method == 'POST':
        params = request.POST
        Service(params['n'], params['d'], params['u']).save()
        return redirect('sites.html')
    elif request.method == 'PATCH':
        params = QueryDict(request.body)
        serv = Service.objects.get(nomservice=params['n'])
        serv.description = params['d']
        serv.unite = params['u']
        serv.save()
        return JsonResponse({'msg': 'success'})
    else:
        id = QueryDict(request.body)
        Service.objects.get(nomservice=id['n']).delete()
        return JsonResponse({'msg': 'success'})


def values(request):
    if request.method == 'GET':
        offres = Offre.objects.filter(nomtype=request.GET['t'])
        out = []
        nom = ''
        for offre in offres:
            if(offre.idformule.periode != 0):
                nom = '{0}'.format(offre.idformule.periode) + \
                    ' ' + offre.idformule.unite
            else:
                nom = 'consommation direct'
            out.append({'FORMULE': offre.idformule.idformule,
                        'PERIODE': offre.idformule.periode, 'NOM': nom, 'PRIX': offre.prix})
        return JsonResponse(out, safe=False)
    elif request.method == 'POST':
        params = request.POST
        Offre(params['t'], params['f'], params['p']).save()
        return JsonResponse({'msg': 'success'})
    elif request.method == 'PATCH':
        pass
    else:
        id = QueryDict(request.body)
        Offre.objects.get(nomtype=Type.objects.get(
            nomtype=id['t']), idformule=Formule.objects.get(idformule=id['f'])).delete()
        return JsonResponse({'msg': 'success'})


def plan(request):
    if request.method == 'GET':
        plans = Contient.objects.filter(idformule=request.GET['f'])
        out = []
        for pl in plans:
            out.append(
                {'SERVICE': pl.nomservice.nomservice, 'QTE': pl.quantite})
        return JsonResponse(out, safe=False)
    elif request.method == 'POST':
        params = request.POST
        Offre(params['f'], params['s'], params['p']).save()
        return JsonResponse({'msg': 'success'})
    elif request.method == 'PATCH':
        pass
    else:
        id = QueryDict(request.body)
        Contient.objects.get(nomservice=Service.objects.get(
            nomservice=id['s']), idformule=Formule.objects.get(idformule=id['f'])).delete()
        return JsonResponse({'msg': 'success'})


def stats(request, annee, cible):
    rsvs = Reservation.objects.filter(Q(etat=1) | Q(
        etat=-1)).filter(annee=annee)
    annots = rsvs.values('mois', 'annee').annotate(
        m=Count('mois'), a=Count('annee'))
    out = []
    somme = 0
    if cible == 'general':
        for ano in annots:
            mois = ano['mois']
            for rsv in rsvs:
                if rsv.mois == mois:
                    somme = somme + \
                        Offre.objects.get(idformule=rsv.idformule,
                                          nomtype=rsv.numespace.nomtype).prix
            out.append({'mois': mois, 'revenu': somme})
            somme = 0
    elif cible == 'animateur':
        animateurs = Possede.objects.filter(
            nomrole='Animateur')
        for anim in animateurs:
            tmp = []
            for ano in annots:
                mois = ano['mois']
                for rsv in rsvs:
                    inv = Invite.objects.filter(
                        animateur=anim.email, person=rsv.email)
                    if rsv.mois == mois and len(inv) != 0:
                        somme = somme + \
                            Offre.objects.get(idformule=rsv.idformule,
                                              nomtype=rsv.numespace.nomtype).prix
                tmp.append({'mois': mois, 'revenu': somme})
                somme = 0
            out.append({'nom': anim.email.nom, 'stats': tmp})
            tmp = []
    else:
        types = Type.objects.all()
        for typ in types:
            rev = 0
            tmp = []
            for ano in annots:
                mois = ano['mois']
                for rsv in rsvs:
                    if rsv.numespace.nomtype == typ and rsv.mois == mois:
                        somme = somme + \
                            Offre.objects.get(idformule=rsv.idformule,
                                              nomtype=rsv.numespace.nomtype).prix
                tmp.append({'mois': mois, 'revenu': somme})
                somme = 0
            for r in tmp:
                rev += r.get('revenu')
            out.append({'nom': typ.nomtype, 'somme': rev, 'stats': tmp})
    return JsonResponse(out, safe=False)


def link(request):
    if request.method == 'GET':
        links = Invite.objetcs.filter(email=request.GET['e'])
        out = []
        for lk in links:
            out.append(lk.person.email, lk.person.nom)
        return JsonResponse({'link': out})


def invent(request):
    site = Site.objects.all().count()
    typ = Type.objects.all().count()
    formule = Formule.objects.all().count()
    service = Service.objects.all().count()
    return JsonResponse({'site': site, 'type': typ, 'formule': formule, 'service': service})


def dashboard(request):
    return render(request, 'dashboard.html')


def accueil(request):
    return render(request, 'Accueil.html')


def coworker(request):
    return render(request, 'coworker.html')


def animateur(request):
    return render(request, 'animateur.html')


def salle(request):
    types = Type.objects.all()
    sites = Site.objects.all()
    tps = []
    sts = []
    for typ in types:
        tps.append(typ.nomtype)
    for st in sites:
        sts.append(st.nomsite)
    return render(request, 'sites.html', {'types': tps, 'sites': sts})
