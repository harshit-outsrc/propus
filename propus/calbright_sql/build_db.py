from propus.aws.ssm import AWS_SSM
from propus.calbright_sql import Base
from propus.calbright_sql.calbright import Calbright
from propus.anthology import Anthology
from propus.strut import Strut

from propus.calbright_sql.seed_data.views import (
    student_info_view,
    student_enrollment_view,
    progress_by_course_view,
    progress_by_enrollment_view,
)


def init_db(cc):
    cc.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')
    Base.metadata.create_all(bind=cc.engine)
    cc.execute(
        """CREATE TABLE IF NOT EXISTS public.alembic_version
        (version_num character varying(32) COLLATE pg_catalog."default" NOT NULL,
        CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num))"""
    )
    cc.execute("ALTER TABLE IF EXISTS public.alembic_version OWNER to calbright;")


def drop_db(cc):
    for view in ["student_enrollment", "student_info", "progress_by_course", "progress_by_enrollment"]:
        cc.execute(f"DROP VIEW IF EXISTS {view}")
    Base.metadata.drop_all(bind=cc.engine)
    cc.execute("DROP TABLE IF EXISTS alembic_version;")


def seed_db(cc, ssm, anthology_creds):
    anthology = Anthology(**anthology_creds)
    strut = Strut(ssm.get_param("strut"))
    for model in cc.all_models:
        if not hasattr(model, "seed_data"):
            continue
        model.seed_data(self=model, session=cc.session, anthology=anthology, strut=strut)


def finalize_db(cc):
    cc.execute("INSERT INTO public.alembic_version(version_num) VALUES ('ffda5c32701e');")
    cc.execute(
        """INSERT INTO public.alembic_version_history(version_number, revision_type, message) VALUES
        ('ffda5c32701e', 'upgrade', 'Initial State of Calbright Database');
        """
    )


def build_views(cc):
    cc.execute(student_info_view)
    cc.execute(student_enrollment_view)
    cc.execute(progress_by_course_view)
    cc.execute(progress_by_enrollment_view)


if __name__ == "__main__":
    import os
    import sys

    ssm = AWS_SSM.build("us-west-2")
    env = os.environ.get("env")
    anthology_ssm = "anthology.test"
    if env == "localhost":
        calbright = Calbright.build(
            {
                "db": os.environ.get("DB"),
                "host": env,
                "user": os.environ.get("USER"),
                "password": os.environ.get("PASSWORD"),
            },
            verbose=os.environ.get("verbose", "false").lower() == "true",
        )
    elif env == "stage":
        creds = ssm.get_param("psql.calbright.stage.write", "json")
        calbright = Calbright.build(creds, verbose=False)
    elif env == "prod":
        anthology_ssm = "anthology.prod"
        creds = ssm.get_param("psql.calbright.prod.write", "json")
        calbright = Calbright.build(creds, verbose=False)
    else:
        print("'env' environment variable must be set to 'localhost' or 'stage' prior to calling build_db.py")
        sys.exit()

    drop_db(calbright)
    init_db(calbright)
    seed_db(calbright, ssm, anthology_creds=ssm.get_param(anthology_ssm, "json"))
    finalize_db(calbright)
    build_views(calbright)
