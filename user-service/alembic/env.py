from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool
from sqlmodel import SQLModel
from app.model.models import * # type: ignore
from app.setting import DATABASE_URL, TEST_DATABASE_URL # type: ignore
from alembic import context

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
target_metadata = SQLModel.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    # Set SQLAlchemy URL for offline mode
    config.set_main_option("sqlalchemy.url", str(DATABASE_URL))
    run_migrations_offline()
else:
    # Set SQLAlchemy URL for online mode (both development and testing)
    config.set_main_option("sqlalchemy.url", str(DATABASE_URL))
    run_migrations_online()
    # Set SQLAlchemy URL for testing database
    config.set_main_option("sqlalchemy.url", str(TEST_DATABASE_URL))
    run_migrations_online()