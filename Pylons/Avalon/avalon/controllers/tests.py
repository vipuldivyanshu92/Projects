import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from avalon.lib.base import BaseController

import avalon.model as model
from pylons.templating import render_mako as render

log = logging.getLogger(__name__)

class TestsController(BaseController):

    def index(self):
        ipb_q = model.metas['realm'].Session.query(model.IpBanned)
        c.ipb = ipb_q[0]
        return render('tests_index.html')
