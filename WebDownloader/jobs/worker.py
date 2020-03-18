from ..core.factory import Module

# Initialise app module only with celery on board
module = Module()

celery = module.set_celery()
