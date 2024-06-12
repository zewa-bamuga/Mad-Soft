from a8t_tools.storage.local_storage import LocalStorageBackend
from a8t_tools.storage.s3_storage import S3StorageBackend
from dependency_injector import containers, providers

from a8t_tools.db.transactions import AsyncDbTransaction
from a8t_tools.storage.facade import FileStorage

from app.domain.storage.attachments.commands import AttachmentCreateCommand
from app.domain.storage.attachments.queries import (
    AttachmentListQuery,
    AttachmentRetrieveQuery,
)
from app.domain.storage.attachments.repositories import AttachmentRepository


class AttachmentContainer(containers.DeclarativeContainer):
    config: providers.Configuration = providers.Configuration()

    transaction = providers.Dependency(instance_of=AsyncDbTransaction)
    bucket = providers.Dependency(instance_of=str)
    repository = providers.Factory(AttachmentRepository, transaction=transaction)
    file_storage = providers.Factory(
        FileStorage,
        backend=providers.Callable(
            lambda use_s3, local_backend, s3_backend, s3_uri, access_key_id, secret_access_key, public_storage_uri: s3_backend if (use_s3 is True) else local_backend,
            config.storage.use_s3,
            providers.Factory(LocalStorageBackend, base_path=config.storage.local_storage.base_path,
                              base_uri=config.storage.local_storage.base_uri),
            providers.Factory(S3StorageBackend, s3_uri=config.storage.s3_storage.endpoint_uri,
                              access_key_id=config.storage.s3_storage.access_key_id,
                              secret_access_key=config.storage.s3_storage.secret_access_key,
                              public_storage_uri=config.storage.s3_storage.public_storage_uri),
            s3_uri=config.storage.s3_storage.endpoint_uri,
            access_key_id=config.storage.s3_storage.access_key_id,
            secret_access_key=config.storage.s3_storage.secret_access_key,
            public_storage_uri=config.storage.s3_storage.public_storage_uri,
        ),
    )

    # Вывод переданных значений в print
    print(f"11111: {config.storage.s3_storage.endpoint_uri.get()}")
    print(f"Access Key ID: {config.storage.s3_storage.access_key_id.get()}")
    print(f"Secret Access Key: {config.storage.s3_storage.secret_access_key.get()}")
    print(f"Public Storage URI: {config.storage.s3_storage.public_storage_uri.get()}")

    bucket = providers.Dependency(instance_of=str)

    repository = providers.Factory(AttachmentRepository, transaction=transaction)

    list_query = providers.Factory(AttachmentListQuery, repository=repository)

    retrieve_query = providers.Factory(AttachmentRetrieveQuery, repository=repository)


    create_command = providers.Factory(
        AttachmentCreateCommand,
        repository=repository,
        file_storage=file_storage,
        bucket=bucket,
    )
