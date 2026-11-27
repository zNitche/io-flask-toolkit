from alembic import command, config
from sqlalchemy import Engine
from importlib.resources import files, as_file
import os
import shutil


def get_config(migrations_dir: str, db_engine: Engine):
    cfg = config.Config(os.path.join(migrations_dir, "alembic.ini"))

    cfg.set_main_option("sqlalchemy.url", str(db_engine.url))
    cfg.set_main_option("script_location", migrations_dir)
    cfg.set_main_option("compare_type", "true")

    return cfg


def init_migrations(migrations_dir: str, db_engine: Engine):
    if not os.path.exists(migrations_dir):
        target_path = os.path.join(migrations_dir, "env.py")
        template_path = os.path.join("io_db", "alembic_template", "env.template.py")
        template_source = files(anchor="io_flask_toolkit").joinpath(template_path)

        cfg = get_config(migrations_dir, db_engine)

        command.init(cfg, migrations_dir)
        os.makedirs(exist_ok=True, name=os.path.dirname(target_path))

        with as_file(template_source) as template_source_path:
            shutil.copy2(template_source_path, target_path)

        command.stamp(cfg, "head", purge=True)


def migrate(migrations_dir: str, db_engine: Engine):
    alembic_config = get_config(migrations_dir, db_engine)

    with db_engine.begin() as connection:
        alembic_config.attributes["connection"] = connection

        command.revision(alembic_config, autogenerate=True)
        command.upgrade(alembic_config, "head")
