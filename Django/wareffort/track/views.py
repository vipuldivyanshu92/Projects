from django.shortcuts import render_to_response
from wareffort.track.models import *

def index(request):
    outCategories = {}
    outStats = {'totalrequired' : 0, 'totalgathered' : 0, 'totalpercent' : 0}

    # Get the current phase
    phase = Setting.objects.get(name='PHASE')
    
    categories = Category.objects.filter(phase=phase.value)

    for c in categories:
        # Retrieve every aims for this category
        aims = Aim.objects.filter(category=c.id)
        # Create an entry for this category
        outCategories[c.id] = {'name' : c.name, 'aims' : {}}
        for a in aims:
            # The number of ingame items shouldn't be greater than the required one
            nbingame = len(CharacterInventory.objects.filter(item_template=a.item))
            if nbingame > a.nbrequired:
                nbingame = a.nbrequired

            # pcachieved is the pourcentage achieved    
            pcachieved = (nbingame * 100) / a.nbrequired
            # Create the dictionnary of datas
            outCategories[c.id]['aims'][a.id] = {'name' : a.name, 'item' : a.item, 'nbrequired' : a.nbrequired, 'nbingame' : nbingame, 'pcachieved' : pcachieved}
            # Update overall stats
            outStats['totalrequired'] += a.nbrequired
            outStats['totalgathered'] += nbingame

    outStats['totalpercent'] = (outStats['totalgathered'] * 100) / outStats['totalrequired']

    return render_to_response('effort.html', {'phase' : phase.value, 'categories' : outCategories, 'stats' : outStats})
