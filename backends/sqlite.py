import sqlite3
from functools import wraps
from itertools import groupby
from operator import itemgetter
from os import environ

from backends.exceptions import ErrorException

_ENV_DATABASE_PATH = 'TP_BACKEND_SQLITE_DATABASE_PATH'

_db = None  # type: sqlite3.Connection


def _getenv_required(key):
    try:
        return environ[key]
    except KeyError:
        raise ErrorException(
            'Required environment variable %s not set' % key)


def _wrap_sqlite_exception(func):
    @wraps(func)
    def _adapt_exception_types(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except sqlite3.Error as ex:
            raise ErrorException(
                'Error while communicating with the SQLite database'
            ) from ex

    return _adapt_exception_types


@_wrap_sqlite_exception
def initialize_backend():
    global _db

    _db = sqlite3.connect(_getenv_required(_ENV_DATABASE_PATH))

    with _db:
        _db.execute('''
            CREATE TABLE IF NOT EXISTS pastes (
              id TEXT,
              content TEXT,
              PRIMARY KEY (id))
        ''')
        _db.execute('''
            CREATE TABLE IF NOT EXISTS pastes_metadata (
              id TEXT,
              key TEXT,
              value TEXT,
              PRIMARY KEY (id, key))
        ''')


@_wrap_sqlite_exception
def new_paste(paste_id, paste_content):
    with _db:
        _db.execute('''
            INSERT INTO pastes (id, content) VALUES (?, ?)
        ''', [paste_id, paste_content])


@_wrap_sqlite_exception
def update_paste_metadata(paste_id, metadata):
    with _db:
        _db.execute('''
            DELETE FROM pastes_metadata WHERE id = ?
        ''', [paste_id])
        _db.executemany('''
            INSERT INTO pastes_metadata VALUES (?, ?, ?)
        ''', [(paste_id, key, value) for (key, value) in metadata.items()])


@_wrap_sqlite_exception
def does_paste_exist(paste_id):
    return _db.execute('''
        SELECT 1 FROM pastes WHERE id = ?
    ''', [paste_id]).fetchone() is not None


@_wrap_sqlite_exception
def get_paste_contents(paste_id):
    row = _db.execute('''
        SELECT content FROM pastes WHERE id = ?
    ''', [paste_id]).fetchone()
    return row[0] if row else None


@_wrap_sqlite_exception
def get_paste_metadata(paste_id):
    rows = _db.execute('''
        SELECT key, value FROM pastes_metadata WHERE id = ?
    ''', [paste_id]).fetchall()
    return {key: value for (key, value) in rows}


@_wrap_sqlite_exception
def get_paste_metadata_value(paste_id, key):
    row = _db.execute('''
        SELECT value FROM pastes_metadata WHERE id = ? AND key = ?
    ''', [paste_id, key]).fetchone()
    return row[0] if row else None


def _filters_match(metadata, filters, fdefaults):
    for metadata_key, filter_value in filters.items():
        try:
            metadata_value = metadata[metadata_key]
        except KeyError:
            metadata_value = fdefaults.get(metadata_key)

        if metadata_value != filter_value:
            return False

    return True


def _get_all_paste_ids(filters, fdefaults):
    rows = _db.execute('''
        SELECT id, key, value FROM pastes_metadata
        UNION
        SELECT id, "", "" FROM pastes
    ''').fetchall()

    for paste_id, rows in groupby(rows, itemgetter(0)):
        metadata = {key: value for (_, key, value) in rows}
        if _filters_match(metadata, filters, fdefaults):
            yield paste_id


@_wrap_sqlite_exception
def get_all_paste_ids(filters={}, fdefaults={}):
    return list(_get_all_paste_ids(filters, fdefaults))
