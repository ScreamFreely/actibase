from django.contrib.contenttypes.fields import GenericRelation
from django.utils.text import slugify
from datetime import date, datetime
from django.utils import timezone
from django.db import models

from versatileimagefield.fields import VersatileImageField
from django.core.files.storage import FileSystemStorage

from opencivicdata.core.models import Organization


#from .dx_cities import dx_City, dx_County, dx_State, dx_PostalCode, dx_District
#from pupa.scrape import Person, Organization
#Ps = FileSystemStorage(location='media/maps/districts/')


################
# Dex Entities #
################
class FBEvent(models.Model): 
    link = models.CharField(max_length=128, blank=False, null=False) 
    published = models.BooleanField()   
    
    def __unicode__(self):
        return u'%s' % (self.link)

    def __str__(self):
        return u'%s' % (self.link) 



class Quote(models.Model):
    quote = models.CharField(max_length=8, blank=False, null=False) 
    author = models.CharField(max_length=8, blank=False, null=False)  
    link = models.CharField(max_length=128, blank=False, null=False) 
    published = models.BooleanField()   
    
    def __unicode__(self):
        return u'%s' % (self.quote)

    def __str__(self):
        return u'%s' % (self.quote) 


class Apple(models.Model):
    first = models.CharField(max_length=8, blank=False, null=False) 
    last = models.CharField(max_length=8, blank=False, null=False)  
    email = models.CharField(max_length=128, blank=False, null=False)   
    state = models.CharField(max_length=3, blank=False, null=False)
    
    def __unicode__(self):
        return u'%s' % (self.email)

    def __str__(self):
        return u'%s' % (self.email) 


class Comment(models.Model):
    comment_type = models.CharField(max_length=8, blank=False, null=False)  
    email = models.CharField(max_length=128, blank=False, null=False)  
    description = models.TextField(blank=False, null=False)  
    
    def __unicode__(self):
        return u'%s' % (self.email)

    def __str__(self):
        return u'%s' % (self.email)        


class UserAddedEvent(models.Model):
    event_type = models.CharField(max_length=8, blank=False, null=False)  
    name = models.CharField(max_length=128, blank=False, null=False)  
    location = models.CharField(max_length=128,
                               blank=False,
                                null=False)
    link = models.CharField(max_length=64, blank=False, null=False)
    startdate = models.DateTimeField(auto_now_add=False, blank=False, null=False)
    description = models.TextField(blank=False, null=False)
    city = models.CharField(max_length=64, blank=False, null=False)
    participants = models.CharField(max_length=512, blank=True, null=True)
    password = models.CharField(max_length=128, blank=True, null=True) 
    published = models.BooleanField() 

    
    def __unicode__(self):
        return u'%s' % (self.name)

    def __str__(self):
        return u'%s' % (self.name)        

    class Meta:
        verbose_name_plural = 'User Added Events'
        ordering = ['city', 'name', ]



class Organization(models.Model):
    org = models.OneToOneField(Organization, on_delete=models.PROTECT)
    description = models.TextField()
 #   candidate = models.ForeignKey(PublicOfficial)

    def __unicode__(self):
        return u'%s' % (self.org.name)

    def __str__(self):
        return u'%s' % (self.org.name)  

    class Meta:
        verbose_name_plural = 'Organization'
        verbose_name = 'Organizations'


'''
class SocialOutput(models.Model):
    office = models.ForeignKey(
        'Org',
        blank=True,
        null=True,
        related_name='social_output',
        on_delete=models.PROTECT)
    official = models.ForeignKey(BasePerson, blank=True, null=True, on_delete=models.PROTECT)
    op_type = models.CharField(max_length=128,
                               blank=False,
                               null=False)
    op_id = models.CharField(max_length=64, blank=False, null=False)
    timedate = models.DateTimeField(auto_now_add=False, blank=True, null=True)
    title = models.CharField(max_length=128, blank=True, null=True)
    message = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return u'%s, %s' % (self.op_type, self.title)

    def __str__(self):
        return u'%s, %s' % (self.op_type, self.title)

    class Meta:
        verbose_name_plural = 'Social Outputs'
        ordering = ['op_type', '-timedate', ]


class Endorsement(models.Model):
    org = models.ForeignKey(Org, on_delete=models.PROTECT)
 #   candidate = models.ForeignKey(PublicOfficial)

    class Meta:
        verbose_name_plural = 'Endorsements'
        verbose_name = 'Endorsement'
'''
