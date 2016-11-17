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
from __future__ import unicode_literals

from django.core.exceptions import PermissionDenied
from django.db import models
from django.utils import timezone
# from django.utils.crypto import get_random_string, salted_hmac
# from django.utils.encoding import python_2_unicode_compatible
# from django.utils.translation import ugettext_lazy as _

"""
For many of the classes in this file, I would like to acknowledge the work done on
the XOS (CloudLab) project.  More information on XOS can be found at:

            http://xosproject.org
"""


class StrippedCharField(models.CharField):
    """ CharField that strips trailing and leading spaces."""
    def clean(self, value, *args, **kwds):
        if value is not None:
            value = value.strip()
        return super(StrippedCharField, self).clean(value, *args, **kwds)


class ModelBase(models.Model):
    """ Base models class in the collector module

    This class provides a simple base class from which other Django models
    are derived.  In particular, this class will provide fields for a create
    and update timestamp and a flag to specify that the data should be
    considered as read-only.

    To allow for initial saving of a read-only model, as can occur after
    deserializing a saved model, pass the 'force=True' argument to the
    'save' method.  Likewise, to purge a read-only model, pass the
    'force=True' argument to the 'delete' method.

    Fields / Attributes:
        created (timezone):   The UTC timestamp when this model was first created
        updated (timezone):   The UTC timestamp when this model last saved a change
        write_protect (bool): If true, the entire model should be treated as read-only
    """
    # TODO: Investigate how to make the created field read-only but to still allow deserialization...

    created = models.DateTimeField(editable=False)
    updated = models.DateTimeField()
    write_protect = models.BooleanField(default=False)

    def delete(self, *args, **kwargs):
        allow_delete = kwargs.get('force', False)
        if allow_delete:
            del kwargs['force']

        if self.write_protect and not allow_delete:
            raise PermissionDenied("Delete denied: %s has its write_protect flag set" % self.__class__.__name__)

        super(ModelBase, self).delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        # If write-protected, only allow changes if the 'force' flag is true
        force_save = kwargs.get('force', False)
        if force_save:
            del kwargs['force']

        if self.write_protect and not force_save:
            raise PermissionDenied("Save denied: %s has its write_protect flag set" % self.__class__.__name__)

        # Save created if this is a new field

        now = timezone.now()

        if not self.id:
            self.created = now

        # Update 'updated' field
        self.updated = now

        # TODO do we want to modify the 'updated' here?
        # TODO Will any items ever be read-only (after first commit)?
        super(ModelBase, self).save(*args, **kwargs)


# class BaseUserManager(models.Manager):
#     """
#     This module allows importing AbstractBaseUser even when django.contrib.auth is
#     not in INSTALLED_APPS.
#     """
#
#     @classmethod
#     def normalize_email(cls, email):
#         """
#         Normalize the email address by lowercasing the domain part of the it.
#
#         :param email: (str) email address (any case)
#
#         :return: (str) normalized email
#         """
#         email = email or ''
#
#         try:
#             email_name, domain_part = email.strip().rsplit('@', 1)
#         except ValueError:
#             pass
#         else:
#             email = '@'.join([email_name, domain_part.lower()])
#         return email
#
#     @staticmethod
#     def make_random_password(length=10,
#                              allowed_chars='abcdefghjkmnpqrstuvwxyz'
#                                            'ABCDEFGHJKLMNPQRSTUVWXYZ'
#                                            '23456789'):
#         """
#         Generate a random password with the given length and given
#         allowed_chars. The default value of allowed_chars does not have "I" or
#         "O" or letters and digits that look similar -- just to avoid confusion.
#
#         :param length:  (int) Length for new password
#         :param allowed_chars: (str) Allowed character set
#
#         :return: (str) Random password string
#         """
#         return get_random_string(length, allowed_chars)
#
#     def get_by_natural_key(self, username):
#         return self.get(**{self.model.USERNAME_FIELD: username})
#
#
# @python_2_unicode_compatible
# class AbstractBaseUser(models.Model):
#     password = models.CharField(_('password'), max_length=128)
#     last_login = models.DateTimeField(_('last login'), blank=True, null=True)
#
#     is_active = True
#
#     REQUIRED_FIELDS = []
#
#     class Meta:
#         abstract = True
#
#     def get_username(self):
#         """
#         Return the identifying username for this User
#
#         :return: (str) The user name
#         """
#         return getattr(self, self.USERNAME_FIELD)
#
#     def __init__(self, *args, **kwargs):
#         super(AbstractBaseUser, self).__init__(*args, **kwargs)
#         # Stores the raw password if set_password() is called so that it can
#         # be passed to password_changed() after the model is saved.
#         self._password = None
#
#     def __str__(self):
#         return self.get_username()
#
#     def save(self, *args, **kwargs):
#         super(AbstractBaseUser, self).save(*args, **kwargs)
#         if self._password is not None:
#             password_validation.password_changed(self._password, self)
#             self._password = None
#
#     def natural_key(self):
#         return self.get_username(),
#
#     def is_anonymous(self):
#         """
#         Always return False. This is a way of comparing User objects to
#         anonymous users.
#         """
#         return False
#
#     def is_authenticated(self):
#         """
#         Always return True. This is a way to tell if the user has been
#         authenticated in templates.
#         """
#         return True
#
#     def set_password(self, raw_password):
#         self.password = make_password(raw_password)
#         self._password = raw_password
#
#     def check_password(self, raw_password):
#         """
#         Return a boolean of whether the raw_password was correct. Handles
#         hashing formats behind the scenes.
#         """
#
#         def setter(raw_password):
#             self.set_password(raw_password)
#             # Password hash upgrades shouldn't be considered password changes.
#             self._password = None
#             self.save(update_fields=["password"])
#
#         return check_password(raw_password, self.password, setter)
#
#     def set_unusable_password(self):
#         # Set a value that will never be a valid hash
#         self.password = make_password(None)
#
#     def has_usable_password(self):
#         return is_password_usable(self.password)
#
#     def get_full_name(self):
#         raise NotImplementedError('subclasses of AbstractBaseUser must provide a get_full_name() method')
#
#     def get_short_name(self):
#         raise NotImplementedError('subclasses of AbstractBaseUser must provide a get_short_name() method.')
#
#     def get_session_auth_hash(self):
#         """
#         Return an HMAC of the password field.
#         """
#         key_salt = "django.contrib.auth.models.AbstractBaseUser.get_session_auth_hash"
#         return salted_hmac(key_salt, self.password).hexdigest()
