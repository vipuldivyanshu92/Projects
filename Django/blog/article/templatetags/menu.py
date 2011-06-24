from django.template import Library, Node
from blog.article.models import Page

register = Library()

def menu():
    pages = Page.objects.all()
    menu = '<ul>'
    
    for p in pages:
        menu += '<li>' + p.title + '</li>'
        
    menu += '</ul>'
    return menu

register.simple_tag(menu)