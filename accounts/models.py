from django.db import models

# Create your models here.

# from __future__ import unicode_literals

from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _

from .managers import UserManager

from phonenumber_field.modelfields import PhoneNumberField

from dex.models import Organization as Org
from opencivicdata.core.models import Jurisdiction, Organization


class User(AbstractBaseUser, PermissionsMixin):
	USER_TYPE_CHOICES = (
			(0, 'superuser'),
			(1, 'lead'),
			(2, 'maintainer'),
			(3, 'organizer'),
			(4, 'activist')
		)


	username = models.CharField(_('username'), max_length=32,  unique=True, default='activist')
	email = models.EmailField(_('email address'), null=True, blank=True, unique=True)
	phone_number = PhoneNumberField(null=True, blank=True)

	first_name = models.CharField(_('first name'), max_length=30, blank=True)
	last_name = models.CharField(_('last name'), max_length=30, blank=True)
	date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)

	is_active = models.BooleanField(_('active'), default=True)
	is_staff = models.BooleanField(_('staff'), default=False)
	is_superuser = models.BooleanField(_('superuser'), default=False)
	user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES, default=4)

	avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

	objects = UserManager()

	USERNAME_FIELD = 'username'
	REQUIRED_FIELDS = []

	class Meta:
	    verbose_name = _('Activist')
	    verbose_name_plural = _('Activists')

	def get_full_name(self):
	    '''
	    Returns the first_name plus the last_name, with a space in between.
	    '''
	    full_name = '%s %s' % (self.first_name, self.last_name)
	    return full_name.strip()

	def get_short_name(self):
	    '''
	    Returns the short name for the user.
	    '''
	    return self.first_name

	def email_user(self, subject, message, from_email=None, **kwargs):
	    '''
	    Sends an email to this User.
	    '''
	    send_mail(subject, message, from_email, [self.email], **kwargs)



class UserJurisdictions(models.Model):
	USER_TYPE_CHOICES = (
			(0, 'complete'),
			(1, 'basic'),
			(2, 'minimal')
			)

	activist = models.ForeignKey(User, on_delete=models.PROTECT)
	jurisdiction = models.ForeignKey(Jurisdiction, on_delete=models.PROTECT)
	info_level = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES, default=0)

	def __unicode__(self):
		return u'%s-%s' % (self.activist.id, self.jurisdiction.name)

	def __str__(self):
		return u'%s-%s' % (self.activist.id, self.jurisdiction.name) 

	class Meta:
	    verbose_name = _('Jurisdiction')
	    verbose_name_plural = _('Jurisdiction')
	    unique_together = (("jurisdiction", "activist"),)



class Organizer(models.Model):
	USER_TYPE_CHOICES = (
			(0, 'director'),
			(1, 'lead'),
			(2, 'maintainer')
			)

	organizer = models.ForeignKey(User, on_delete=models.PROTECT)
	organization = models.ForeignKey(Org, on_delete=models.PROTECT)
	admin_level = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES, default=2)

	def __unicode__(self):
		return u'%s-%s' % (self.organizer.id, self.organization.org.name)

	def __str__(self):
		return u'%s-%s' % (self.organizer.id, self.organization.org.name) 

	class Meta:
	    verbose_name = _('Organizer')
	    verbose_name_plural = _('Organizers')
	    unique_together = (("organizer", "organization"),)



class ActivistOrgs(models.Model):
	activist = models.ForeignKey(User, on_delete=models.PROTECT)
	organization = models.ForeignKey(Organization, on_delete=models.PROTECT)
	newsfeed = models.BooleanField(default=True)
	email = models.BooleanField(default=False)
	phone = models.BooleanField(default=False)

	def __unicode__(self):
		return u'%s-%s' % (self.activist.id, self.organization.name)

	def __str__(self):
		return u'%s-%s' % (self.activist.id, self.organization.name) 


	class Meta:
	    verbose_name = _('Followed Organization')
	    verbose_name_plural = _('Followed Organizations')
	    unique_together = (("activist", "organization"),)
	    