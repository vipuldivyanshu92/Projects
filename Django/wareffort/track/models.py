from django.db import models

# Create your models here.
class CharacterInventory(models.Model):
    guid = models.IntegerField()
    bag = models.IntegerField()
    slot = models.IntegerField()
    item = models.IntegerField(primary_key=True)
    item_template = models.IntegerField()
    class Meta:
        db_table = u'character_inventory'

    def __unicode__(self):
        return u'%d' % (self.item)

class Setting(models.Model):
    name = models.CharField('name', max_length=50, unique=True)
    value = models.CharField('value', max_length=50)

    def __unicode__(self):
        return u'%s' % (self.name)

class Category(models.Model):
    name = models.CharField('name', max_length=50)
    phase = models.IntegerField()

    def __unicode__(self):
        return u'%s' % (self.name)

class Aim(models.Model):
    category = models.ForeignKey('Category')
    name = models.CharField('name', max_length=50)
    item = models.IntegerField()
    nbrequired = models.IntegerField()

    def __unicode__(self):
        return u'%s' % (self.name)
