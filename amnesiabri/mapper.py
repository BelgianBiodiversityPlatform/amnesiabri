# -*- coding: utf-8 -*-

from sqlalchemy import orm

from amnesia.modules.content import Content
from amnesia.modules.file import File
from amnesia.modules.content_type.utils import get_type_id

from .model import BRI
from .model import Service
from .model import Taxa
from .model import Ecosystem
from .model import Geofocus


def includeme(config):
    tables = config.registry['metadata'].tables

    config.include('amnesia.modules.content.mapper')
    config.include('amnesia.modules.content_type.mapper')

    orm.mapper(Service, tables['amnesiabri.service'])

    orm.mapper(Taxa, tables['amnesiabri.taxa'])

    orm.mapper(Ecosystem, tables['amnesiabri.ecosystem'])

    orm.mapper(Geofocus, tables['amnesiabri.geofocus'])

    orm.mapper(
        BRI, tables['amnesiabri.bri'], inherits=Content,
        polymorphic_identity=get_type_id(config, 'bri'),
        properties={
            'services': orm.relationship(
                Service, secondary=tables['amnesiabri.bri_service']
            ),

            'taxas': orm.relationship(
                Taxa, secondary=tables['amnesiabri.bri_taxa']
            ),

            'ecosystems': orm.relationship(
                Ecosystem, secondary=tables['amnesiabri.bri_ecosystem']
            ),

            'geofocuses': orm.relationship(
                Geofocus, secondary=tables['amnesiabri.bri_geofocus']
            ),

            'logo': orm.relationship(
                File, foreign_keys=[tables['amnesiabri.bri'].c.logo_id]
            )

        }
    )


