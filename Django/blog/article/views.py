from django.shortcuts import render_to_response, get_object_or_404
from blog.article.models import Page

def index(request):
    response = HttpResponse()
    response.write("<HTML><BODY>\n")
    response.write("<H1>Pages</H1><HR />")
    pList = Page.objects.all()
    for p in pList:
        link = "<a href=\"page/%d\">" % (p.id)
        response.write("<li>%s%s</a></li>" % (link, p.title))
    response.write("</BODY></HTML>")
    return response
    
def page(request, pID='0'):
    p = get_object_or_404(Page, pk=pID)
    
    return render_to_response('base_site.html', {'p' : p})