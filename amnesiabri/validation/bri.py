# -*- coding: utf-8 -*-

from marshmallow import Schema
from marshmallow import EXCLUDE
from marshmallow import pre_load
from marshmallow import post_load
from marshmallow import post_dump
from marshmallow.fields import Integer
from marshmallow.fields import String
from marshmallow.fields import Url
from marshmallow.fields import Nested
from marshmallow.fields import List

from amnesia.utils.validation import as_list
from amnesia.modules.content.validation import ContentSchema

from amnesiabri import Service
from amnesiabri import Taxa
from amnesiabri import Ecosystem
from amnesiabri import Geofocus


class _NameId(Schema):

    id = Integer(dump_only=True)
    name = String(required=True)


class BRISchema(ContentSchema):
    ''' Schema for the bri model '''

    content_id = Integer(dump_only=True)
    logo_id = Integer(dump_only=True)
    body = String(required=True)
    financial = String()
    url_link = Url(missing=None)
    contact = String()

    services = Nested(_NameId, many=True, dump_only=True)
    taxas = Nested(_NameId, many=True, dump_only=True)
    ecosystems = Nested(_NameId, many=True, dump_only=True)
    geofocuses = Nested(_NameId, many=True, dump_only=True)

    services_id = List(Integer(load_only=True))
    taxas_id = List(Integer(load_only=True))
    ecosystems_id = List(Integer(load_only=True))
    geofocuses_id = List(Integer(load_only=True))

    class Meta:
        unknown = EXCLUDE

    def _as_list(self, data):
        for field in ('services_id', 'taxas_id', 'ecosystems_id',
                      'geofocuses_id'):
            try:
                data[field] = as_list(data[field])
            except KeyError:
                data[field] = []

        return data

    # pylint: disable=no-member
    def _make_objects(self, data):
        if 'services_id' in data:
            data['services'] = self.dbsession.query(Service).filter(
                Service.id.in_(data.pop('services_id'))).all()

        if 'taxas_id' in data:
            data['taxas'] = self.dbsession.query(Taxa).filter(
                Taxa.id.in_(data.pop('taxas_id'))).all()

        if 'ecosystems_id' in data:
            data['ecosystems'] = self.dbsession.query(Ecosystem).filter(
                Ecosystem.id.in_(data.pop('ecosystems_id'))).all()

        if 'geofocuses_id' in data:
            data['geofocuses'] = self.dbsession.query(Geofocus).filter(
                Geofocus.id.in_(data.pop('geofocuses_id'))).all()

        return data

    def _relation_ids(self, data):
        for key in ('services', 'taxas', 'ecosystems', 'geofocuses'):
            data['{}_id'.format(key)] = [_['id'] for _ in data[key]]
        return data

    @pre_load
    def _pre_load(self, data):
        return self._as_list(data)

    @post_load
    def _post_load(self, data):
        return self._make_objects(data)

    @post_dump
    def _post_dump(self, data):
        return self._relation_ids(data)
