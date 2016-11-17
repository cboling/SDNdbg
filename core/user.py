"""
Copyright (c) 2015 - 2016.  Boling Consulting Solutions , BCSW.net

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import hashlib

from core.models.base import StrippedCharField
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.mail import EmailMultiAlternatives
from django.db import models
from timezone_field import TimeZoneField


# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, email, firstname, lastname, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.

        :param email:
        :param firstname:
        :param lastname:
        :param password:

        :return:
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(email=UserManager.normalize_email(email),
                          firstname=firstname,
                          lastname=lastname,
                          password=password)
        # user.set_password(password)
        user.is_admin = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, firstname, lastname, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(email,
                                password=password,
                                firstname=firstname,
                                lastname=lastname)
        user.is_admin = True
        user.save(using=self._db)
        return user

    def get_queryset(self):
        parent = super(UserManager, self)
        if hasattr(parent, "get_queryset"):
            return parent.get_queryset().filter(deleted=False)
        else:
            return parent.get_query_set().filter(deleted=False)

    # deprecated in django 1.7 in favor of get_queryset().
    def get_query_set(self):
        return self.get_queryset()


class DeletedUserManager(UserManager):
    def get_queryset(self):
        return super(UserManager, self).get_query_set().filter(deleted=True)

    # deprecated in django 1.7 in favor of get_queryset()
    def get_query_set(self):
        return self.get_queryset()


class User(AbstractBaseUser):
    @property
    def remote_password(self):
        return hashlib.md5(self.password).hexdigest()[:12]

    class Meta:
        app_label = "core"

    email = models.EmailField(verbose_name='email address', max_length=255,
                              unique=True, db_index=True)

    username = StrippedCharField(max_length=255, default="New User")

    firstname = StrippedCharField(help_text="person's given name", max_length=200)
    lastname = StrippedCharField(help_text="person's surname", max_length=200)

    phone = StrippedCharField(null=True, blank=True, help_text="phone number contact", max_length=100)
    user_url = models.URLField(null=True, blank=True)
    # site = models.ForeignKey(Site, related_name='users', help_text="Site this user will be homed too")
    public_key = models.TextField(null=True, blank=True, max_length=1024, help_text="Public key string")

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_readonly = models.BooleanField(default=False)
    is_registering = models.BooleanField(default=False)
    is_appuser = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    enacted = models.DateTimeField(null=True, default=None)
    policed = models.DateTimeField(null=True, default=None)
    backend_status = StrippedCharField(max_length=1024,
                                       default="Provisioning in progress")
    deleted = models.BooleanField(default=False)
    write_protect = models.BooleanField(default=False)

    timezone = TimeZoneField()

    dashboards = models.ManyToManyField('DashboardView', through='UserDashboardView', blank=True)

    objects = UserManager()
    deleted_objects = DeletedUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['firstname', 'lastname']

    PI_FORBIDDEN_FIELDS = ["is_admin"]  # , "site", "is_staff"]
    USER_FORBIDDEN_FIELDS = ["is_admin", "is_active", "is_readonly"]  # "site", "is_staff",

    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)
        # self._initial = self._dict  # for PlModelMixIn

    def is_read_only_user(self):
        return self.is_readonly

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    @property
    def keyname(self):
        return self.email[:self.email.find('@')]

    def __unicode__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # TODO: Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # TODO: Simplest possible answer: Yes, always
        return True

    def is_superuser(self):
        # TODO implement
        return False

    def save(self, *args, **kwds):
        if not self.id:
            self.set_password(self.password)
        if self.is_active and self.is_registering:
            self.send_temporary_password()
            self.is_registering = False

        self.username = self.email
        super(User, self).save(*args, **kwds)

    def send_temporary_password(self):
        password = User.objects.make_random_password()
        self.set_password(password)
        subject, from_email, to = 'SDNdbg Account Credentials', 'support@bcsw.net', str(self.email)
        text_content = 'This is an important message.'
        # TODO: userUrl="http://%s/" % get_request().get_host()
        # html_content = """<p>Your account has been created for SDNdbg. Please log in <a href="""+userUrl+""">here</a> to activate your account<br><br>Username: """+self.email+"""<br>Temporary Password: """+password+"""<br>Please change your password once you successfully login into the site.</p>"""

        html_content = """<p>Your account has been created for SDNdbg. """ + \
                       """Please log in to activate your account<br><br>Username: """ + \
                       self.email + """<br>Temporary Password: """ + \
                       password + """<br>Please change your password once you successfully login into the site.</p>"""

        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

    # TODO: Support granular privs - eventually
    def can_update(self, user):
        return not user.is_readonly

    #     from core.models import SitePrivilege
    #     _cant_update_fieldName = None
    #     if user.can_update_root():
    #         return True
    #
    #     # site pis can update
    #     site_privs = SitePrivilege.objects.filter(user=user, site=self.site)
    #     for site_priv in site_privs:
    #         if site_priv.role.role == 'admin':
    #             return True
    #         if site_priv.role.role == 'pi':
    #             for fieldName in self.diff.keys():
    #                 if fieldName in self.PI_FORBIDDEN_FIELDS:
    #                     _cant_update_fieldName = fieldName
    #                     return False
    #             return True
    #     if (user.id == self.id):
    #         for fieldName in self.diff.keys():
    #             if fieldName in self.USER_FORBIDDEN_FIELDS:
    #                 _cant_update_fieldName = fieldName
    #                 return False
    #         return True
    #
    #     return False

    def can_update_root(self):
        """
        Return True if user has root (global) write access.
        """
        if self.is_readonly:
            return False
        if self.is_admin:
            return True

        return False

    # TODO: Support granular privs - eventually
    def can_update_deployment(self, deployment):
        return self.is_admin

    #     from core.models.site import DeploymentPrivilege
    #     if self.can_update_root():
    #         return True
    #
    #     if DeploymentPrivilege.objects.filter(
    #             deployment=deployment,
    #             user=self,
    #             role__role__in=['admin', 'Admin']):
    #         return True
    #     return False

    # TODO: Support granular privs - eventually
    def can_update_site(self, site, allow=[]):
        return self.is_admin
        # from core.models.site import SitePrivilege
        # if self.can_update_root():
        #     return True
        # if SitePrivilege.objects.filter(
        #         site=site, user=self, role__role__in=['admin', 'Admin']+allow):
        #     return True
        # return False

    def get_permissions(self, filter_by=None):
        """ Return a list of objects for which the user has read or read/write
        access. The object will be an instance of a django model object.
        Permissions will be either 'r' or 'rw'.

        e.g.
        [{'object': django_object_instance, 'permissions': 'rw'}, ...]

        Returns:
          list of dicts

        """
        return None  # TODO: Go back and look at the XOS project and adapt that to our needs
