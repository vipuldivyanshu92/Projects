# -*- coding: cp1252 -*-

from django.db import models
import datetime

class Poll(models.Model):
    question = models.CharField(max_length=200)
    pub_date = models.DateTimeField('Date de publication')
    def __str__(self):
        return self.question

    def was_published_today(self):
        return self.pub_date.date() == datetime.date.today()
    was_published_today.short_description = u'Publié aujourd\'hui ?'
    
    class Admin:
        list_display = ('question', 'pub_date', 'was_published_today')
        list_filter = ['pub_date']
        search_fields = ['question']
        date_hierarchy = 'pub_date'
        fields = (
            (None, {'fields': ('question',)}),
            ('Informations calendaires', {'fields': ('pub_date',), 'classes': 'collapse'}),
        )

class Choice(models.Model):
    poll = models.ForeignKey(Poll, edit_inline=models.TABULAR, num_in_admin=3)
    choice = models.CharField(max_length=200, core=True)
    votes = models.IntegerField(core=True)
    
    def __str__(self):
        return self.choice
