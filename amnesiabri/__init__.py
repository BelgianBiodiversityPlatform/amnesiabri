# -*- coding: utf-8 -*-

from .model import BRI
from .model import Service
from .model import Taxa
from .model import Ecosystem
from .model import Geofocus

from .resources import BRIEntity
from .resources import BRIResource

from .validation import BRISchema
from .validation import SearchSchema


def includeme(config):
    config.include('.mapper')
    config.include('.views')
