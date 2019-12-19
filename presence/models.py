from django.db import models

# Create your models here.


class Individu(models.Model):
    nom = models.CharField(max_length=255)
    prenom = models.CharField(max_length=255)
    cin = models.CharField(max_length=255, blank=True)
    face_id = models.ImageField(upload_to="photos/")

    def __str__(self):
        return "{0} {1}".format(self.nom, self.prenom)


class Responsable(models.Model):
    individu = models.OneToOneField(Individu, on_delete=models.CASCADE)
    code_responsable = models.CharField(max_length=255)

    def __str__(self):
        return "{0} {1}".format(self.individu.nom, self.individu.prenom)


class Etudiant(models.Model):
    individu = models.OneToOneField(Individu, on_delete=models.CASCADE)
    num_matricule = models.IntegerField()
    niveau = models.CharField(max_length=255)
    parcours = models.CharField(max_length=255)

    def __str__(self):
        return "{0} {1}".format(self.individu.nom, self.individu.prenom)


class GroupeParticipant(models.Model):
    membres = models.ManyToManyField(
        Etudiant, through='Appartenir', related_name='+')
    nom_groupe_participant = models.CharField(max_length=255)

    def __str__(self):
        return self.nom_groupe_participant


class Appartenir(models.Model):
    numero = models.IntegerField(blank=True, null=True)
    groupe = models.ForeignKey(GroupeParticipant, on_delete=models.CASCADE)
    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE)

    def __str__(self):
        return "{0} => {1}".format(self.groupe.nom_groupe_participant, self.etudiant)


class Categorie(models.Model):
    nom_categorie = models.CharField(max_length=255)

    def __str__(self):
        return self.nom_categorie


class Matiere(models.Model):
    nom_matiere = models.CharField(max_length=255)

    def __str__(self):
        return self.nom_matiere


class Evenement(models.Model):
    responsables = models.ManyToManyField(
        Responsable, related_name="evenements")
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE)
    matiere = models.ForeignKey(
        Matiere, blank=True, null=True, on_delete=models.CASCADE)
    presences = models.ManyToManyField(
        Etudiant, related_name="evenements")
    date_debut = models.DateTimeField(blank=True, null=True)
    date_fin = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.categorie.nom_categorie
