FROM migration-alembic:latest
MAINTAINER jawello, jawello@gmail.com

COPY ./alembic/versions /migration-alembic/alembic/versions
COPY alembic.ini /migration-alembic/alembic.ini

ENTRYPOINT ["alembic", "upgrade", "head"]