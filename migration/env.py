import importlib
import pkgutil
from logging.config import fileConfig

from alembic import context
from mypy.moduleinspect import ModuleType
from sqlalchemy import engine_from_config, pool, TypeDecorator, String

import app
from internal.config.setting import setting
from internal.domain.entity import Entity

from sqlalchemy.dialects import postgresql

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Entity.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.
config.set_main_option("sqlalchemy.url", setting.pg_dsn)

# Hide migration error
class Vector(TypeDecorator):
    impl = String
    cache_ok = True
postgresql.base.ischema_names['vector'] = Vector


def include_object(object, name, type_, reflected, compare_to):
    if type_ == "table" and name.startswith("langchain_pg_"):
        return False
    return True

def import_entities(package: ModuleType) -> None:
    for importer, modname, ispkg in pkgutil.walk_packages(
            package.__path__, package.__name__ + "."
    ):
        try:
            importlib.import_module(modname)
        except Exception as e:
            print(f"Can't import {modname}: {e}")


import_entities(app)

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        include_object=include_object,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata, include_object=include_object
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
