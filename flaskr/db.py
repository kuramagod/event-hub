import click
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / 'instance' / 'flaskr.sqlite'

engine = create_engine(f'sqlite:///{DB_PATH}', connect_args={"check_same_thread": False})

db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

def _import_models():
    from flaskr import models
    return models

@click.command('init-db')
def init_db_command():
    init_db()
    click.echo('✓ Database initialized.')

@click.command('seed-db')
def seed_db_command():
    try:
        from flaskr.seed import seed_database
        seed_database()
        click.echo('✓ Database seeded with sample data.')
    except Exception as e:
        click.echo(f'✗ Error seeding database: {e}', err=True)
        raise

def shutdown_session(exception=None):
    db_session.remove()

def init_db():
    _import_models()
    Base.metadata.create_all(bind=engine)

def init_app(app):
    _import_models()
    
    app.teardown_appcontext(shutdown_session)
    app.cli.add_command(init_db_command)
    app.cli.add_command(seed_db_command)
