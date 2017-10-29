from contextlib import contextmanager
from itertools import groupby
from operator import itemgetter

from backends.utils import filters_match


class DbApi2(object):
    def __init__(self, connection, paramstyle):
        self._connection = connection
        self._paramstyle = paramstyle

    @contextmanager
    def _get_cursor(self, commit):
        cursor = self._connection.cursor()

        yield cursor

        if commit:
            self._connection.commit()

    def _read_cursor(self):
        return self._get_cursor(commit=False)

    def _write_cursor(self):
        return self._get_cursor(commit=True)

    def _prepare_sql(self, sql):
        return sql.replace('?', self._paramstyle)

    def initialize_backend(self):
        with self._write_cursor() as cursor:
            cursor.execute(self._prepare_sql('''
                CREATE TABLE IF NOT EXISTS pastes (
                  id TEXT,
                  content TEXT,
                  PRIMARY KEY (id))
            '''))
            cursor.execute(self._prepare_sql('''
                CREATE TABLE IF NOT EXISTS pastes_metadata (
                  id TEXT,
                  key TEXT,
                  value TEXT,
                  PRIMARY KEY (id, key))
            '''))

    def new_paste(self, paste_id, paste_content):
        with self._write_cursor() as cursor:
            cursor.execute(self._prepare_sql('''
                INSERT INTO pastes (id, content) VALUES (?, ?)
            '''), [paste_id, paste_content])

    def update_paste_metadata(self, paste_id, metadata):
        with self._write_cursor() as cursor:
            cursor.execute(self._prepare_sql('''
                DELETE FROM pastes_metadata WHERE id = ?
            '''), [paste_id])
            cursor.executemany(self._prepare_sql('''
                INSERT INTO pastes_metadata VALUES (?, ?, ?)
            '''), [(paste_id, key, value) for (key, value) in
                   metadata.items()])

    def does_paste_exist(self, paste_id):
        with self._read_cursor() as cursor:
            cursor.execute(self._prepare_sql('''
                SELECT 1 FROM pastes WHERE id = ?
            '''), [paste_id])
            row = cursor.fetchone()
        return row is not None

    def get_paste_contents(self, paste_id):
        with self._read_cursor() as cursor:
            cursor.execute(self._prepare_sql('''
                SELECT content FROM pastes WHERE id = ?
            '''), [paste_id])
            row = cursor.fetchone()
        return row[0] if row else None

    def get_paste_metadata(self, paste_id):
        with self._read_cursor() as cursor:
            cursor.execute(self._prepare_sql('''
                SELECT key, value FROM pastes_metadata WHERE id = ?
            '''), [paste_id])
            rows = cursor.fetchall()
        return {key: value for (key, value) in rows}

    def get_paste_metadata_value(self, paste_id, key):
        with self._read_cursor() as cursor:
            cursor.execute(self._prepare_sql('''
                SELECT value FROM pastes_metadata WHERE id = ? AND key = ?
            '''), [paste_id, key])
            row = cursor.fetchone()
        return row[0] if row else None

    def _get_all_paste_ids(self, filters, fdefaults):
        with self._read_cursor() as cursor:
            cursor.execute(self._prepare_sql('''
                SELECT id, key, value FROM pastes_metadata
                UNION
                SELECT id, '', '' FROM pastes
            '''))
            rows = cursor.fetchall()

        for paste_id, rows in groupby(rows, itemgetter(0)):
            metadata = {key: value for (_, key, value) in rows}
            if filters_match(metadata, filters, fdefaults):
                yield paste_id

    def get_all_paste_ids(self, filters={}, fdefaults={}):
        return list(self._get_all_paste_ids(filters, fdefaults)) or ['none']
