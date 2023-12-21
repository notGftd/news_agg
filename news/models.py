from django.db import models


class Website1(models.Model):
  title = models.CharField(max_length=200)
  image = models.URLField(null=True, blank=True)
  url = models.TextField()
  scraped = models.DateTimeField(null=True, auto_now_add=True)

  def __str__(self):
    return self.title
  
  class Meta: 
        ordering = ['-scraped']
        verbose_name = "ZNBC"
        verbose_name_plural = "ZNBC"

class Website2(models.Model):
  title = models.CharField(max_length=200)
  image = models.URLField(null=True, blank=True)
  url = models.TextField()
  scraped = models.DateTimeField(null=True, auto_now_add=True)

  def __str__(self):
    return self.title
  
  class Meta: 
        ordering = ['-scraped']
        verbose_name = "Zambian Observer"
        verbose_name_plural = "Zambian Observer"

class Website3(models.Model):
  title = models.CharField(max_length=200)
  image = models.URLField(null=True, blank=True)
  url = models.TextField()
  scraped = models.DateTimeField(null=True, auto_now_add=True)

  def __str__(self):
    return self.title
  
  class Meta: 
        ordering = ['-scraped']
        verbose_name = "Lusaka Times"
        verbose_name_plural = "Lusaka Times"