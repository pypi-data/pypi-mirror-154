"""
© Copyright 2020 HP Development Company, L.P.
SPDX-License-Identifier: GPL-2.0-only
"""

import os

import toml
from azure.storage.blob import BlobServiceClient, ContainerClient
from ml_git import log
from ml_git.constants import AZURE_STORE_NAME, StoreType
from ml_git.storages.multihash_store import MultihashStore
from ml_git.storages.store import Store


class AzureMultihashStore(Store, MultihashStore):
    def __init__(self, bucket_name, bucket):
        self._bucket = bucket_name
        self._store_type = StoreType.AZUREBLOBH.value
        self._account = self.get_account()
        super().__init__()

    def connect(self):
        log.debug('Connect - Storage [%s] ;' % self._store_type,
                  class_name=AZURE_STORE_NAME)
        try:
            self._store = BlobServiceClient.from_connection_string(self._account, connection_timeout=300)
        except Exception:
            raise RuntimeError('Unable to connect to the Azure storage.')

    def bucket_exists(self):
        container = ContainerClient.from_connection_string(self._account, self._bucket, connection_timeout=300)
        try:
            container.get_container_properties()
            log.debug('Container %s already exists' % self._bucket, class_name=AZURE_STORE_NAME)
            return True
        except Exception:
            return False

    def put(self, key_path, file_path):
        if self.key_exists(key_path) is True:
            log.debug('Object [%s] already in Azure store' % key_path, class_name=AZURE_STORE_NAME)
            return True
        if not os.path.exists(file_path):
            log.debug('File [%s] not present in local repository' % file_path, class_name=AZURE_STORE_NAME)
            return False

        try:
            blob_client = self._store.get_blob_client(container=self._bucket, blob=key_path)
            with open(file_path, 'rb') as data:
                blob_client.upload_blob(data)
        except Exception as e:
            if 'The specified blob already exists.' in str(e):
                log.debug('The specified blob [%s] already exists.' % key_path)
                return key_path
            raise e
        return key_path

    def get(self, file_path, reference):
        try:
            blob_client = self._store.get_blob_client(container=self._bucket, blob=reference)
            with open(file_path, 'wb') as download_file:
                data = blob_client.download_blob().readall()
                download_file.write(data)
            if not self.check_integrity(reference, self.digest(data)):
                return False
        except Exception as e:
            log.error(e, class_name=AZURE_STORE_NAME)
            return False
        return True

    def list_files_from_path(self, path):
        bucket_response = self._store.create_container(path)
        log.info('\nListing blobs in container:' + path)
        blob_list = bucket_response.list_blobs()
        return blob_list

    def get_account(self):
        connection_string = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
        if connection_string is not None:
            return connection_string
        try:
            azure_folder = os.path.expanduser(os.path.join('~', '.azure'))
            config = toml.load(os.path.join(azure_folder, 'config'))
            connection = config['storage']['connection_string']
            if connection != '':
                return connection
        except Exception:
            log.debug('Azure cli configurations not find.', class_name=AZURE_STORE_NAME)
        log.error('Azure credentials could not be found. See the ml-git documentation for how to configure.',
                  class_name=AZURE_STORE_NAME)

    def key_exists(self, key_path):
        try:
            blob_client = self._store.get_blob_client(container=self._bucket, blob=key_path)
            blob_client.get_blob_properties()
            return True
        except Exception:
            return False
