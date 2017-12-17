# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
import os

class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class CartCart(models.Model):
    creation_date = models.DateTimeField()
    checked_out = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'cart_cart'


class CartItem(models.Model):
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=18, decimal_places=2)
    object_id = models.IntegerField()
    cart = models.ForeignKey(CartCart, models.DO_NOTHING)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'cart_item'


class Category(models.Model):
    #category_id = models.IntegerField(primary_key=True)
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=45)
    description = models.CharField(max_length=45, blank=True, null=True)

    def __str__(self):  # __unicode__ on Python 2
        #return self.category_name
        return '%s' % (self.category_name)

    class Meta:
        managed = False
        db_table = 'category'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class EventsCategory(models.Model):
    category_name = models.CharField(max_length=50)
    description = models.CharField(max_length=50)
    category_url = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'events_category'


class EventsUser(models.Model):
    user_id = models.CharField(max_length=50)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=60)
    street1 = models.CharField(max_length=30)
    street2 = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    pin_number = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'events_user'


class Rating(models.Model):
    rating_id = models.AutoField(primary_key=True)
    profile = models.ForeignKey('UserProfile', models.DO_NOTHING)
    rating = models.IntegerField()
    description = models.CharField(max_length=45, blank=True, null=True)
    user = models.ForeignKey('User', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'rating'


class Test(models.Model):
    testid = models.IntegerField(db_column='TestId', primary_key=True)  # Field name made lowercase.
    testname = models.CharField(db_column='TestName', max_length=45, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'test'


class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    username = models.CharField(max_length=50,unique=True)
    password = models.CharField(max_length=60)
    street1 = models.CharField(max_length=30)
    street2 = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    pin_number = models.IntegerField()
    phone = PhoneNumberField(blank=True, null=True)
    verifyFlag = models.BooleanField(default=False)

    class Meta:
        managed = False
        db_table = 'user'

def get_upload_path(instance, filename):
    upload_dir =  os.path.join("EventHubApp/static/events/assets/img/media/","Test")
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
    return os.path.join("Test", filename)

class UserProfile(models.Model):
    #profile_id = models.IntegerField(primary_key=True)
    profile_id = models.AutoField(primary_key=True)
    category = models.ForeignKey(Category, models.DO_NOTHING)
    user = models.ForeignKey(User, models.DO_NOTHING)
    profile_name = models.CharField(max_length=45, blank=True, null=True)
    description = models.CharField(max_length=45, blank=True, null=True)
    pic1 = models.ImageField(upload_to='test')
    pic2 = models.ImageField(blank=True, null=True)
    pic3 = models.ImageField(blank=True, null=True)
    pic4 = models.ImageField(blank=True, null=True)
    pic5 = models.ImageField(blank=True, null=True)
    price = models.FloatField()
    active = models.BooleanField(default=True)

    class Meta:
        managed = False
        db_table = 'user_profile'


class UserType(models.Model):
    user_type_id = models.IntegerField(primary_key=True)
    user_type = models.CharField(max_length=45)
    user = models.ForeignKey(User, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'user_type'


# class Userprofiledetails(models.Model):
#     servicename = models.CharField(db_column='serviceName', max_length=50)  # Field name made lowercase.
#     type = models.CharField(max_length=50)
#     offers = models.CharField(max_length=50)
#     package = models.CharField(max_length=50)
#     servicedetails = models.CharField(db_column='serviceDetails', max_length=50)  # Field name made lowercase.
#     productdescription = models.CharField(db_column='productDescription', max_length=50)  # Field name made lowercase.
#     aboutproduct = models.CharField(db_column='aboutProduct', max_length=50)  # Field name made lowercase.
#     aboutus = models.CharField(db_column='aboutUs', max_length=50)  # Field name made lowercase.
#     profile = models.ForeignKey(UserProfile, models.DO_NOTHING)
# 
#     class Meta:
#         managed = False
#         db_table = 'userprofiledetails'
