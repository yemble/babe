
import os,logging

import psycopg2
import psycopg2.extras

# probably don't have to modify this file; these methods will be useful if you are writing custom actions or api endpoints

class PgSession(object):
	def __init__(self):
		self.con = None
		pass

	def connected(self):
		if not self.con:
			return False
		return True

	def get_connection(self):
		if not self.connected():
			dsn = "host={host} dbname={name} user={user} password={pwd}".format(
				host=os.environ['DB_HOST'],
				name=os.environ['DB_NAME'],
				user=os.environ['DB_USER'],
				pwd=os.environ['DB_PASS'],
			)
			self.con = psycopg2.connect(dsn, cursor_factory=psycopg2.extras.DictCursor)
		return self.con

	def execute_query(self, sql, params=tuple()):
		logging.debug("execute_query: %s %s", sql, params)
		cur = self.get_connection().cursor()
		cur.execute(sql, params)
		for row in cur:
			yield dict(row)
		cur.close()

	def execute_update(self, sql, params=tuple()):
		logging.debug("execute_update: %s %s", sql, params)
		cur = self.get_connection().cursor()
		cur.execute(sql, params)
		affected = cur.rowcount
		cur.close()
		return affected

	def select(self, table, conditions):
		sql = "SELECT * FROM " + table
		if conditions:
			where_sql, params = _where(conditions)
			sql += " WHERE " + where_sql
		else:
			params = []
		logging.debug("select: %s (%s)", sql, params)
		cur = self.get_connection().cursor()
		cur.execute(sql, tuple(params))
		for row in cur:
			yield dict(row)
		cur.close()

	def delete(self, table, conditions):
		sql = "DELETE FROM " + table
		if conditions:
			where_sql, params = _where(conditions)
			sql += " WHERE " + where_sql
		else:
			params = []
		logging.debug("delete: %s (%s)", sql, params)
		cur = self.get_connection().cursor()
		cur.execute(sql, tuple(params))
		affected = cur.rowcount
		cur.close()
		return affected

	def update(self, table, setters, conditions):
		cols = setters.keys()
		sets = [ '{} = %s'.format(c) for c in cols ]
		params = [ setters.get(c) for c in cols ]
		sql = "UPDATE {t} SET {s}".format(
			t = table,
			s = ','.join(sets),
		)
		if conditions:
			where_sql, where_params = _where(conditions)
			sql += " WHERE " + where_sql
			params.extend(where_params)
		logging.debug("update: %s (%s)", sql, params)
		cur = self.get_connection().cursor()
		cur.execute(sql, tuple(params))
		affected = cur.rowcount
		cur.close()
		return affected

	def insert(self, table, setters):
		cols = setters.keys()
		ph = [ '%s' for c in cols ]
		params = [ setters.get(c) for c in cols ]
		sql = "INSERT INTO {t} ({c}) VALUES ({p}) RETURNING id".format(
			t = table,
			c = ','.join(cols),
			p = ','.join(ph),
		)
		logging.debug("insert: %s (%s)", sql, params)
		cur = self.get_connection().cursor()
		cur.execute(sql, tuple(params))
		new_id = cur.fetchone()[0]
		cur.close()
		return new_id

def _where(where):
	sql = ' AND '.join( [ "{} {} %s".format(left, c) for left, c, right in where ] )
	params = [ r for l,c,r in where ]
	return sql, params
