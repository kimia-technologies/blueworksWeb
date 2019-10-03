from django.db import models


class Actualite(models.Model):
    # Field name made lowercase.
    idactualite = models.AutoField(db_column='IDACTUALITE', primary_key=True)
    # Field name made lowercase.
    contenu = models.CharField(db_column='CONTENU', max_length=128)
    # Field name made lowercase.
    valide = models.IntegerField(db_column='VALIDE', blank=True, null=True)
    # Field name made lowercase.
    createdat = models.DateTimeField(db_column='createdAt')
    # Field name made lowercase.
    updatedat = models.DateTimeField(db_column='updatedAt')

    class Meta:
        managed = False
        db_table = 'actualite'


class Attacher(models.Model):
    # Field name made lowercase.
    idattach = models.AutoField(db_column='IDATTACH', primary_key=True)
    # Field name made lowercase.
    idactualite = models.ForeignKey(
        Actualite, models.CASCADE, db_column='IDACTUALITE')
    # Field name made lowercase.
    lien = models.CharField(
        db_column='LIEN', max_length=128, blank=True, null=True)
    # Field name made lowercase.
    createdat = models.DateTimeField(db_column='createdAt')
    # Field name made lowercase.
    updatedat = models.DateTimeField(db_column='updatedAt')

    class Meta:
        managed = False
        db_table = 'attacher'


class Consommation(models.Model):
    # Field name made lowercase.
    nomservice = models.ForeignKey(
        'Service', models.CASCADE, db_column='NOMSERVICE', primary_key=True)
    # Field name made lowercase.
    idreservation = models.ForeignKey(
        'Reservation', models.CASCADE, db_column='IDRESERVATION')
    # Field name made lowercase.
    quantite = models.IntegerField(db_column='QUANTITE')
    # Field name made lowercase.
    consome = models.FloatField(db_column='CONSOME')
    jour = models.DateTimeField(db_column='JOUR')  # Field name made lowercase.
    etat = models.IntegerField(db_column='ETAT')  # Field name made lowercase.
    # Field name made lowercase.
    createdat = models.DateTimeField(db_column='createdAt')
    # Field name made lowercase.
    updatedat = models.DateTimeField(db_column='updatedAt')

    class Meta:
        managed = False
        db_table = 'consommation'
        unique_together = (('nomservice', 'idreservation'),)


class Contient(models.Model):
    # Field name made lowercase.
    idformule = models.ForeignKey(
        'Formule', models.CASCADE, db_column='IDFORMULE', primary_key=True)
    # Field name made lowercase.
    nomservice = models.ForeignKey(
        'Service', models.CASCADE, db_column='NOMSERVICE')
    # Field name made lowercase.
    quantite = models.IntegerField(db_column='QUANTITE')

    class Meta:
        managed = False
        db_table = 'contient'
        unique_together = (('idformule', 'nomservice'),)


class Employe(models.Model):
    # Field name made lowercase.
    idemploye = models.CharField(
        db_column='IDEMPLOYE', primary_key=True, max_length=36)
    # Field name made lowercase.
    email = models.ForeignKey('Utilisateur', models.CASCADE, db_column='EMAIL')
    # Field name made lowercase.
    nomsite = models.ForeignKey('Site', models.CASCADE, db_column='NOMSITE')

    class Meta:
        managed = False
        db_table = 'employe'


class Espace(models.Model):
    # Field name made lowercase.
    numespace = models.AutoField(db_column='NUMESPACE', primary_key=True)
    # Field name made lowercase.
    nomtype = models.ForeignKey('Type', models.CASCADE, db_column='NOMTYPE')
    # Field name made lowercase.
    nom = models.CharField(
        db_column='NOM', max_length=128, blank=True, null=True)
    # Field name made lowercase.
    concerne = models.IntegerField(db_column='CONCERNE', default=0)
    # Field name made lowercase.
    occp = models.IntegerField(db_column='OCCP', default=0)
    # Field name made lowercase.
    nomsite = models.ForeignKey('Site', models.CASCADE, db_column='NOMSITE')
    # Field name made lowercase.
    createdat = models.DateTimeField(db_column='createdAt')
    # Field name made lowercase.
    updatedat = models.DateTimeField(db_column='updatedAt')

    class Meta:
        managed = False
        db_table = 'espace'


class Formule(models.Model):
    # Field name made lowercase.
    idformule = models.AutoField(db_column='IDFORMULE', primary_key=True)
    # Field name made lowercase.
    periode = models.IntegerField(db_column='PERIODE', blank=True, null=True)
    # Field name made lowercase.
    unite = models.CharField(
        db_column='UNITE', max_length=3, blank=True, null=True)
    # Field name made lowercase.
    nom = models.CharField(
        db_column='NOM', max_length=128, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'formule'


class Image(models.Model):
    # Field name made lowercase.
    idimage = models.AutoField(db_column='IDIMAGE', primary_key=True)
    # Field name made lowercase.
    contenu = models.CharField(db_column='CONTENU', max_length=255)
    # Field name made lowercase.
    nomtype = models.ForeignKey('Type', models.CASCADE, db_column='NOMTYPE')

    class Meta:
        managed = False
        db_table = 'image'


class Invite(models.Model):
    # Field name made lowercase.
    animateur = models.ForeignKey(
        'Utilisateur', models.CASCADE, db_column='ANIMATEUR', related_name='animateur', primary_key=True)
    # Field name made lowercase.
    person = models.ForeignKey(
        'Utilisateur', models.CASCADE, db_column='PERSON', related_name='person', primary_key=True)
    # Field name made lowercase.
    lien = models.CharField(db_column='LIEN', max_length=32)
    # Field name made lowercase.
    createdat = models.DateTimeField(db_column='createdAt')
    # Field name made lowercase.
    updatedat = models.DateTimeField(db_column='updatedAt')

    class Meta:
        managed = False
        db_table = 'invite'
        unique_together = (('animateur', 'person'),)


class Notification(models.Model):
    # Field name made lowercase.
    email = models.ForeignKey(
        'Utilisateur', models.CASCADE, db_column='EMAIL', primary_key=True)
    # Field name made lowercase.
    idactualite = models.ForeignKey(
        Actualite, models.CASCADE, db_column='IDACTUALITE')
    # Field name made lowercase.
    type = models.CharField(db_column='TYPE', max_length=128)
    # Field name made lowercase.
    date = models.DateTimeField(db_column='DATE', blank=True, null=True)
    # Field name made lowercase.
    createdat = models.DateTimeField(db_column='createdAt')
    # Field name made lowercase.
    updatedat = models.DateTimeField(db_column='updatedAt')

    class Meta:
        managed = False
        db_table = 'notification'
        unique_together = (('email', 'idactualite'),)


class Offre(models.Model):
    # Field name made lowercase.
    idformule = models.ForeignKey(
        Formule, models.CASCADE, db_column='IDFORMULE', primary_key=True)
    # Field name made lowercase.
    nomtype = models.ForeignKey('Type', models.CASCADE, db_column='NOMTYPE')
    prix = models.FloatField(db_column='PRIX')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'offre'
        unique_together = (('idformule', 'nomtype'),)


class Permission(models.Model):
    # Field name made lowercase.
    nomrole = models.ForeignKey(
        'Role', models.CASCADE, db_column='NOMROLE', primary_key=True)
    # Field name made lowercase.
    nomressource = models.ForeignKey(
        'Ressource', models.CASCADE, db_column='NOMRESSOURCE')
    # Field name made lowercase.
    create = models.IntegerField(db_column='CREATE')
    read = models.IntegerField(db_column='READ')  # Field name made lowercase.
    # Field name made lowercase.
    update = models.IntegerField(db_column='UPDATE')
    # Field name made lowercase.
    delete = models.IntegerField(db_column='DELETE')
    # Field name made lowercase.
    read_all = models.IntegerField(db_column='READ_ALL')

    class Meta:
        managed = False
        db_table = 'permission'
        unique_together = (('nomrole', 'nomressource'),)


class Possede(models.Model):
    # Field name made lowercase.
    nomrole = models.ForeignKey(
        'Role', models.CASCADE, db_column='NOMROLE', primary_key=True)
    # Field name made lowercase.
    email = models.ForeignKey(
        'Utilisateur', models.CASCADE, db_column='EMAIL', primary_key=True)
    # Field name made lowercase.
    createdat = models.DateTimeField(db_column='createdAt')
    # Field name made lowercase.
    updatedat = models.DateTimeField(db_column='updatedAt')

    class Meta:
        managed = False
        db_table = 'possede'
        unique_together = (('nomrole', 'email'),)


class Question(models.Model):
    # Field name made lowercase.
    idquestion = models.AutoField(db_column='IDQUESTION', primary_key=True)
    # Field name made lowercase.
    idreponse = models.ForeignKey(
        'Reponse', models.CASCADE, db_column='IDREPONSE', blank=True, null=True)
    # Field name made lowercase.
    email = models.ForeignKey('Utilisateur', models.CASCADE, db_column='EMAIL')
    # Field name made lowercase.
    contenu = models.CharField(db_column='CONTENU', max_length=128)
    # Field name made lowercase.
    createdat = models.DateTimeField(db_column='createdAt')
    # Field name made lowercase.
    updatedat = models.DateTimeField(db_column='updatedAt')

    class Meta:
        managed = False
        db_table = 'question'


class Recharge(models.Model):
    # Field name made lowercase.
    idreservation = models.ForeignKey(
        'Reservation', models.CASCADE, db_column='IDRESERVATION', primary_key=True)
    # Field name made lowercase.
    nomservice = models.ForeignKey(
        'Service', models.CASCADE, db_column='NOMSERVICE')
    jour = models.DateTimeField(db_column='JOUR')  # Field name made lowercase.
    # Field name made lowercase.
    source = models.CharField(
        db_column='SOURCE', max_length=128, blank=True, null=True)
    etat = models.IntegerField(db_column='ETAT')  # Field name made lowercase.
    # Field name made lowercase.
    createdat = models.DateTimeField(db_column='createdAt')
    # Field name made lowercase.
    updatedat = models.DateTimeField(db_column='updatedAt')
    # Field name made lowercase.
    utilisateuremail = models.ForeignKey(
        'Utilisateur', models.CASCADE, db_column='utilisateurEMAIL', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'recharge'
        unique_together = (('idreservation', 'nomservice'),)


class Reponse(models.Model):
    # Field name made lowercase.
    idreponse = models.AutoField(db_column='IDREPONSE', primary_key=True)
    # Field name made lowercase.
    contenu = models.CharField(db_column='CONTENU', max_length=128)
    # Field name made lowercase.
    createdat = models.DateTimeField(db_column='createdAt')
    # Field name made lowercase.
    updatedat = models.DateTimeField(db_column='updatedAt')

    class Meta:
        managed = False
        db_table = 'reponse'


class Reservation(models.Model):
    # Field name made lowercase.
    idreservation = models.CharField(
        db_column='IDRESERVATION', primary_key=True, max_length=36)
    # Field name made lowercase.
    numespace = models.ForeignKey(
        Espace, models.CASCADE, db_column='NUMESPACE')
    # Field name made lowercase.
    email = models.ForeignKey('Utilisateur', models.CASCADE, db_column='EMAIL')
    # Field name made lowercase.
    idformule = models.ForeignKey(
        Formule, models.CASCADE, db_column='IDFORMULE')
    etat = models.IntegerField(db_column='ETAT')  # Field name made lowercase.
    # Field name made lowercase.
    nbinvite = models.IntegerField(db_column='NBINVITE')
    jour = models.DateField(db_column='JOUR')  # Field name made lowercase.
    mois = models.IntegerField(db_column='MOIS')  # Field name made lowercase.
    # Field name made lowercase.
    annee = models.CharField(db_column='ANNEE', max_length=4)
    # Field name made lowercase.
    tranche = models.CharField(
        db_column='TRANCHE', max_length=128, blank=True, null=True)
    # Field name made lowercase.
    expire = models.DateTimeField(db_column='EXPIRE')
    # Field name made lowercase.
    createdat = models.DateTimeField(db_column='createdAt')
    # Field name made lowercase.
    updatedat = models.DateTimeField(db_column='updatedAt')

    class Meta:
        managed = False
        db_table = 'reservation'


class Ressource(models.Model):
    # Field name made lowercase.
    nomressource = models.CharField(
        db_column='NOMRESSOURCE', primary_key=True, max_length=128)
    # Field name made lowercase.
    createdat = models.DateTimeField(db_column='createdAt')
    # Field name made lowercase.
    updatedat = models.DateTimeField(db_column='updatedAt')

    class Meta:
        managed = False
        db_table = 'ressource'


class Role(models.Model):
    # Field name made lowercase.
    nomrole = models.CharField(
        db_column='NOMROLE', primary_key=True, max_length=128)

    class Meta:
        managed = False
        db_table = 'role'


class Service(models.Model):
    # Field name made lowercase.
    nomservice = models.CharField(
        db_column='NOMSERVICE', primary_key=True, max_length=128)
    # Field name made lowercase.
    description = models.CharField(
        db_column='DESCRIPTION', max_length=128, blank=True, null=True)
    # Field name made lowercase.
    unite = models.CharField(
        db_column='UNITE', max_length=15, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'service'


class Site(models.Model):
    # Field name made lowercase.
    nomsite = models.CharField(
        db_column='NOMSITE', primary_key=True, max_length=128)
    # Field name made lowercase.
    quartier = models.CharField(db_column='QUARTIER', max_length=128)
    # Field name made lowercase.
    description = models.CharField(
        db_column='DESCRIPTION', max_length=15, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'site'


class Token(models.Model):
    # Field name made lowercase.
    id = models.CharField(db_column='ID', primary_key=True, max_length=255)
    # Field name made lowercase.
    email = models.ForeignKey('Utilisateur', models.CASCADE, db_column='EMAIL')
    # Field name made lowercase.
    createdat = models.DateTimeField(db_column='createdAt')
    # Field name made lowercase.
    updatedat = models.DateTimeField(db_column='updatedAt')

    class Meta:
        managed = False
        db_table = 'token'


class Type(models.Model):
    # Field name made lowercase.
    nomtype = models.CharField(
        db_column='NOMTYPE', primary_key=True, max_length=128)
    # Field name made lowercase.
    contenance = models.IntegerField(db_column='CONTENANCE')
    # Field name made lowercase.
    invite = models.IntegerField(db_column='INVITE', default=1)
    # Field name made lowercase.
    description = models.TextField(
        db_column='DESCRIPTION', blank=True, null=True)
    # Field name made lowercase.
    createdat = models.DateTimeField(db_column='createdAt')
    # Field name made lowercase.
    updatedat = models.DateTimeField(db_column='updatedAt')

    class Meta:
        managed = False
        db_table = 'type'


class Utilisateur(models.Model):
    # Field name made lowercase.
    email = models.CharField(
        db_column='EMAIL', primary_key=True, max_length=128)
    # Field name made lowercase.
    nom = models.CharField(
        db_column='NOM', max_length=128, blank=True, null=True)
    # Field name made lowercase.
    prenom = models.CharField(
        db_column='PRENOM', max_length=128, blank=True, null=True)
    # Field name made lowercase.
    sexe = models.CharField(
        db_column='SEXE', max_length=128, blank=True, null=True)
    # Field name made lowercase.
    password = models.CharField(db_column='PASSWORD', max_length=128)
    # Field name made lowercase.
    phone = models.CharField(db_column='PHONE', unique=True, max_length=128)
    # Field name made lowercase.
    pseudo = models.CharField(db_column='PSEUDO', unique=True, max_length=128)
    # Field name made lowercase.
    etat = models.IntegerField(db_column='ETAT', default=0)
    # Field name made lowercase.
    createdat = models.DateTimeField(db_column='createdAt')
    # Field name made lowercase.
    updatedat = models.DateTimeField(db_column='updatedAt')
    # Field name made lowercase.
    code = models.CharField(
        db_column='CODE', max_length=4, blank=True, null=True)
    # Field name made lowercase.
    photo = models.CharField(
        db_column='PHOTO', max_length=32, blank=True, null=True)
    # Field name made lowercase.
    entreprise = models.CharField(
        db_column='ENTREPRISE', max_length=32, blank=True, null=True)
    # Field name made lowercase.
    entrerole = models.CharField(
        db_column='ENTREROLE', max_length=32, blank=True, null=True)
    # Field name made lowercase.
    anniv = models.DateField(db_column='ANNIV', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'utilisateur'
