"""Musical Track Database.

Read an iTunes export CSV file and build a normalized SQLite database with
Artist, Genre, Album, and Track tables.
"""

import csv
import sqlite3


def lookup_id(cursor, table, column, value):
	cursor.execute(f'SELECT id FROM {table} WHERE {column} = ?', (value,))
	row = cursor.fetchone()
	if row is not None:
		return row[0]

	cursor.execute(
		f'INSERT INTO {table} ({column}) VALUES (?)',
		(value,),
	)
	return cursor.lastrowid


conn = sqlite3.connect('trackdb.sqlite')
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS Track')
cur.execute('DROP TABLE IF EXISTS Album')
cur.execute('DROP TABLE IF EXISTS Genre')
cur.execute('DROP TABLE IF EXISTS Artist')

cur.execute(
	'''
	CREATE TABLE Artist (
		id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
		name TEXT UNIQUE
	)
	'''
)

cur.execute(
	'''
	CREATE TABLE Genre (
		id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
		name TEXT UNIQUE
	)
	'''
)

cur.execute(
	'''
	CREATE TABLE Album (
		id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
		artist_id INTEGER,
		title TEXT UNIQUE
	)
	'''
)

cur.execute(
	'''
	CREATE TABLE Track (
		id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
		title TEXT UNIQUE,
		album_id INTEGER,
		genre_id INTEGER,
		len INTEGER, rating INTEGER, count INTEGER
	)
	'''
)

fname = input('Enter file name: ')
if len(fname) < 1:
	fname = 'tracks.csv'

with open(fname, newline='', encoding='utf-8') as fh:
	reader = csv.reader(fh)

	for row in reader:
		print(row)
		if len(row) < 7:
			continue

		title = row[0]
		artist = row[1]
		album = row[2]
		count = int(row[3]) if row[3] else None
		rating = int(row[4]) if row[4] else None
		length = int(row[5]) if row[5] else None
		genre = row[6]

		artist_id = lookup_id(cur, 'Artist', 'name', artist)
		genre_id = lookup_id(cur, 'Genre', 'name', genre)

		cur.execute('SELECT id FROM Album WHERE title = ?', (album,))
		row_album = cur.fetchone()
		if row_album is None:
			cur.execute(
				'INSERT INTO Album (title, artist_id) VALUES (?, ?)',
				(album, artist_id),
			)
			album_id = cur.lastrowid
		else:
			album_id = row_album[0]

		cur.execute(
			'''
			INSERT OR REPLACE INTO Track
				(title, album_id, genre_id, len, rating, count)
			VALUES (?, ?, ?, ?, ?, ?)
			''',
			(title, album_id, genre_id, length, rating, count),
		)

	conn.commit()

cur.close()
conn.close()
