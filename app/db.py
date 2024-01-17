# connect to mysql
import pymysql
from flask import Flask, current_app, g
from flask.cli import with_appcontext
import click

# Path: app/db.py

def get_db():
  if 'db' not in g:
    g.db = pymysql.connect(host='localhost',
      port=3306,
      user='root',
      database='goauth',
      password='hiepnv@970012',
      cursorclass=pymysql.cursors.DictCursor)
  
  return g.db

# Rest of the code...
def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        # close the mysql database connection
        db.close()

def init_db():
    db = get_db()

    # open the schema.sql file
    with current_app.open_resource('schema.sql') as f:
      # execute the commands in the schema.sql file
      sql_commands = f.read().decode('utf8')

    # split the commands and execute each one
    for sql_command in sql_commands.split(';'):
      if sql_command.strip() != '':
        db.cursor().execute(sql_command)

    # commit the changes
    db.commit()

    
@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

def init_app(app: Flask):
  app.teardown_appcontext(close_db)
  app.cli.add_command(init_db_command)