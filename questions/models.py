from django.db import models

# Create your models here.
class Propositions (models.Model) :
    proposition = models.TextField()
    theme = models.CharField(max_length=255)
    section = models.CharField(max_length=255)
    candidat = models.CharField(max_length=255)

    def __str__(self):
        return '{}, {}, {}, {}'.format(self.proposition, self.section, self.theme, self.candidat)

class RandomPropositions (models.Model):
    proposition = models.TextField()
    theme = models.CharField(max_length=255)
    section = models.CharField(max_length=255)
    candidat = models.CharField(max_length=255)

    def __str__(self):
        return '{}, {}, {}, {}'.format(self.proposition, self.section, self.theme, self.candidat)
