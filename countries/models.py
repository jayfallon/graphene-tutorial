from django.db import models

# Create your models here.

class Continent(models.Model):
	name = models.CharField(max_length=100)

	def __str__(self):
		return self.name

class Country(models.Model):
	name = models.CharField(max_length=100)
	capital = models.CharField(max_length=100)
	continent = models.ForeignKey(Continent, related_name='countries')

	def __str__(self):
		return self.name


