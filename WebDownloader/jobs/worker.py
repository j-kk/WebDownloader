from .celery import CeleryServer
from ..core.factory import Module

module = Module()

celery = module.set_celery()