"""
© Copyright 2020 HP Development Company, L.P.
SPDX-License-Identifier: GPL-2.0-only
"""

import boto3
from botocore.exceptions import ProfileNotFound
from ml_git import log
from ml_git.config import mlgit_config
from ml_git.constants import STORE_FACTORY_CLASS_NAME, StoreType
from ml_git.storages.azure_store import AzureMultihashStore
from ml_git.storages.google_drive_store import GoogleDriveMultihashStore, GoogleDriveStore
from ml_git.storages.s3store import S3Store, S3MultihashStore


def store_factory(config, store_string):
    stores = {StoreType.S3.value: S3Store, StoreType.S3H.value: S3MultihashStore,
              StoreType.AZUREBLOBH.value: AzureMultihashStore, StoreType.GDRIVEH.value: GoogleDriveMultihashStore,
              StoreType.GDRIVE.value: GoogleDriveStore}
    sp = store_string.split('/')
    config_bucket_name, bucket_name = None, None

    try:
        store_type = sp[0][:-1]
        bucket_name = sp[2]
        config_bucket_name = []
        log.debug('Store [%s] ; bucket [%s]' % (store_type, bucket_name), class_name=STORE_FACTORY_CLASS_NAME)
        for k in config['store'][store_type]:
            config_bucket_name.append(k)
        if bucket_name not in config_bucket_name:
            log.warn('Exception creating store -- Configuration not found for bucket [%s]. '
                     'The available buckets in config file for store type [%s] are: %s' % (
                      bucket_name, store_type, config_bucket_name), class_name=STORE_FACTORY_CLASS_NAME)
            return None
        bucket = config['store'][store_type][bucket_name]
        return stores[store_type](bucket_name, bucket)
    except ProfileNotFound as pfn:
        log.error(pfn, class_name=STORE_FACTORY_CLASS_NAME)
        return None


def get_bucket_region(bucket, credentials_profile=None):
    if credentials_profile is not None:
        profile = credentials_profile
    else:
        profile = mlgit_config['store'][StoreType.S3.value][bucket]['aws-credentials']['profile']
    session = boto3.Session(profile_name=profile)
    client = session.client(StoreType.S3.value)
    location = client.get_bucket_location(Bucket=bucket)
    if location['LocationConstraint'] is not None:
        region = location
    else:
        region = 'us-east-1'
    return region
