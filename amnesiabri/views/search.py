# -*- coding: utf-8 -*-

import logging


from pyramid.view import view_config
from pyramid.view import view_defaults
from pyramid.httpexceptions import HTTPBadRequest

from marshmallow import ValidationError

from amnesia.views import BaseView

from amnesiabri import Service
from amnesiabri import BRIResource
from amnesiabri import SearchSchema

log = logging.getLogger(__name__)


def includeme(config):
    ''' Pyramid includeme func '''
    config.scan(__name__)


@view_defaults(context=BRIResource, request_method='GET')
class Search(BaseView):

    @view_config(name='form', accept='text/html',
                 renderer='amnesiabri:templates/bri/_search_form.pt')
    def form(self):
        return {
            'services': self.context.get_services(),
            'taxas': self.context.get_taxas(),
            'ecosystems': self.context.get_ecosystems(),
            'geofocuses': self.context.get_geofocuses()
        }

    @view_config(name='search',
                 renderer='amnesiabri:templates/bri/search_results.pt')
    def search(self):
        params = self.request.GET.mixed()

        try:
            data = SearchSchema().load(params)
        except ValidationError as error:
            return HTTPBadRequest(error)

        bris = self.context.search(**data)

        return {
            'bris': bris
        }
