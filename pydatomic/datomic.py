# -*- coding: utf-8 -*-
import requests

from . import edn
from .compat import urljoin


class Database(object):

    def __init__(self, name, conn):
        self.name = name
        self.conn = conn

    def __getattr__(self, name):
        def f(*args, **kwargs):
            get_db = getattr(self.conn, name)
            return get_db(self.name, *args, **kwargs)
        return f


class Datomic(object):

    def __init__(self, location, storage):
        self.location = location
        self.storage = storage
        self._session = requests.Session()

    def _post(self, *args, **kw):
        return self._session.post(*args, **kw)

    def db_url(self, dbname):
        return (urljoin(self.location, 'data/') +
                self.storage + '/' +
                dbname)

    def create_database(self, dbname):
        r = self._session.post(self.db_url(''), data={'db-name':dbname})
        assert r.status_code in (200, 201), r.text
        return Database(dbname, self)

    def transact(self, dbname, data):
        data = '[%s\n]' % '\n'.join(data)
        r = self._session.post(self.db_url(dbname)+'/',
                               data={'tx-data':data},
                               headers={'Accept':'application/edn'})
        assert r.status_code in (200, 201), (r.status_code, r.text)
        return edn.loads(r.content)

    def query(self, dbname, query, extra_args=None, history=False):
        if extra_args is None:
            extra_args = []
        args = '[{:db/alias ' + self.storage + '/' + dbname
        if history:
            args += ' :history true'
        args += '} ' + ' '.join(str(a) for a in extra_args) + ']'
        r = self._session.get(urljoin(self.location, 'api/query'),
                              params={'args': args, 'q': query},
                              headers={'Accept': 'application/edn'})
        assert r.status_code == 200, r.text
        return edn.loads(r.content)

    def entity(self, dbname, eid):
        r = self._session.get(self.db_url(dbname) + '/-/entity',
                              params={'e':eid},
                              headers={'Accept':'application/edn'})
        assert r.status_code == 200
        return edn.loads(r.content)


if __name__ == '__main__':
    q = """[{
  :db/id #db/id[:db.part/db]
  :db/ident :person/name
  :db/valueType :db.type/string
  :db/cardinality :db.cardinality/one
  :db/doc "A person's name"
  :db.install/_attribute :db.part/db}]"""

    conn = Datomic('http://localhost:3000/', 'tdb')
    db = conn.create_database('cms')
    db.transact(q)
    db.transact('[{:db/id #db/id[:db.part/user] :person/name "Peter"}]')
    r = db.query('[:find ?e ?n :where [?e :person/name ?n]]')
    print(r)
    eid = r[0][0]
    print(db.query('[:find ?n :in $ ?e :where [?e :person/name ?n]]',
                   [eid], history=True))
    print(db.entity(eid))
