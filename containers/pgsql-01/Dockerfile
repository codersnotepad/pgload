# docker build -t pgsql-01 .
# docker run -p 15432:5432 --name pgsql-01 pgsql-01

FROM postgres:11

RUN /etc/init.d/postgresql start &&\
    psql --command "CREATE ROLE 'ETL_Group' WITH NOLOGIN NOSUPERUSER INHERIT NOCREATEDB NOCREATEROLE NOREPLICATION;" &&\
    createdb -O DB01 ETL_Group
