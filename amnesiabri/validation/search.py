# -*- coding: utf-8 -*-

import logging

from marshmallow import Schema
from marshmallow import EXCLUDE
from marshmallow import pre_load
from marshmallow.fields import List
from marshmallow.fields import Integer

from amnesia.utils.validation import as_list

log = logging.getLogger(__name__)  # pylint: disable=invalid-name


class SearchSchema(Schema):

    services = List(Integer())
    taxas = List(Integer())
    ecosystems = List(Integer())
    geofocus = List(Integer())

    def _as_list(self, data):
        for field in ('services', 'taxas', 'ecosystems',
                      'geofocus'):
            try:
                data[field] = as_list(data[field])
            except KeyError:
                data[field] = []

        return data

    @pre_load
    def _pre_load(self, data):
        return self._as_list(data)


