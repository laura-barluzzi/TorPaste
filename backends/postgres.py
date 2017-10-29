from psycopg2 import Error
from psycopg2 import connect

from backends.dbapi2 import DbApi2
from backends.utils import getenv_required
from backends.utils import wrap_exception

_ENV_DATABASE_CONNECTION = 'TP_BACKEND_POSTGRES_DATABASE_CONNECTION'

_wrap_postgres_exception = wrap_exception(
    Error,
    'Error while communicating with the Postgres database')

_db = None  # type: DbApi2


@_wrap_postgres_exception
def initialize_backend():
    global _db

    _db = DbApi2(
        connection=connect(getenv_required(_ENV_DATABASE_CONNECTION)),
        paramstyle='%s')

    return _db.initialize_backend()


@_wrap_postgres_exception
def new_paste(paste_id, paste_content):
    return _db.new_paste(paste_id, paste_content)


@_wrap_postgres_exception
def update_paste_metadata(paste_id, metadata):
    return _db.update_paste_metadata(paste_id, metadata)


@_wrap_postgres_exception
def does_paste_exist(paste_id):
    return _db.does_paste_exist(paste_id)


@_wrap_postgres_exception
def get_paste_contents(paste_id):
    return _db.get_paste_contents(paste_id)


@_wrap_postgres_exception
def get_paste_metadata(paste_id):
    return _db.get_paste_metadata(paste_id)


@_wrap_postgres_exception
def get_paste_metadata_value(paste_id, key):
    return _db.get_paste_metadata_value(paste_id, key)


@_wrap_postgres_exception
def get_all_paste_ids(filters={}, fdefaults={}):
    return _db.get_all_paste_ids(filters, fdefaults)
