"""
© Copyright 2020 HP Development Company, L.P.
SPDX-License-Identifier: GPL-2.0-only
"""

from ml_git.config import config_load
from ml_git.log import set_level
from ml_git.repository import Repository

DATASET = 'dataset'
LABELS = 'labels'
MODEL = 'model'
PROJECT = 'project'


def init_repository(entity_type='dataset'):
    return Repository(config_load(), entity_type)


repositories = {
    DATASET: init_repository(DATASET),
    LABELS: init_repository(LABELS),
    MODEL: init_repository(MODEL),
    PROJECT: init_repository(PROJECT)
}


def set_verbose_mode(ctx, param, value):
    if not value:
        return
    set_level("debug")
