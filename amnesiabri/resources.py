# -*- coding: utf-8 -*-

import logging

from sqlalchemy import orm
from sqlalchemy.exc import DatabaseError

from amnesia.modules.content import Entity
from amnesia.modules.content import EntityManager
from amnesia.modules.state import State
from amnesia.modules.folder import Folder
from amnesia.modules.file import File

from amnesiabri import BRI
from amnesiabri import Service
from amnesiabri import Taxa
from amnesiabri import Ecosystem
from amnesiabri import Geofocus
from amnesiabri import BRISchema

log = logging.getLogger(__name__)  # pylint: disable=invalid-name


class BRIEntity(Entity):
    """ BRI entity """

    def get_validation_schema(self):
        return BRISchema(context={'request': self.request})


class BRIResource(EntityManager):

    __name__ = 'bri'

    def __getitem__(self, path):
        if path.isdigit():
            entity = self.dbsession.query(BRI).get(path)
            if entity:
                return BRIEntity(self.request, entity)
        raise KeyError

    def get_services(self):
        return self.dbsession.query(Service).all()

    def get_taxas(self):
        return self.dbsession.query(Taxa).all()

    def get_ecosystems(self):
        return self.dbsession.query(Ecosystem).all()

    def get_geofocuses(self):
        return self.dbsession.query(Geofocus).all()

    def get_validation_schema(self):
        return BRISchema(context={'request': self.request})

    def query(self):
        return self.dbsession.query(BRI)

    def search(self, services=None, taxas=None, geofocus=None,
               ecosystems=None):
        query = self.query()

        # pylint: disable=no-member
        # XXX: tables should be joined

        if services:
            query = query.filter(BRI.services.any(Service.id.in_(services)))

        if taxas:
            query = query.filter(BRI.taxas.any(Taxa.id.in_(taxas)))

        if geofocus:
            query = query.filter(BRI.geofocuses.any(Geofocus.id.in_(geofocus)))

        if ecosystems:
            query = query.filter(
                BRI.ecosystems.any(Ecosystem.id.in_(ecosystems))
            )

        return query.all()

    def create(self, data):
        state = self.dbsession.query(State).filter_by(name='published').one()
        container = self.dbsession.query(Folder).enable_eagerloads(False).\
            get(data['container_id'])

        logo = self.dbsession.query(File).enable_eagerloads(False).\
            get(data['logo_id']) if 'logo_id' in data else None

        new_entity = BRI(
            owner=self.request.user,
            state=state,
            container=container,
            logo=logo,
            **data
        )

        try:
            self.dbsession.add(new_entity)
            self.dbsession.flush()
            return new_entity
        except DatabaseError:
            return False
