# docker build -t pgsql-01 .
# docker run -p 15432:5432 --name pgsql-01 pgsql-01

FROM postgres:11

RUN /etc/init.d/postgresql start &&\
    psql --command "CREATE ROLE 'ETL_Group' WITH NOLOGIN NOSUPERUSER INHERIT NOCREATEDB NOCREATEROLE NOREPLICATION;" &&\
    createdb -O DB01 ETL_Group

https://mobile.facebook.com/messages/read/?tid=cid.c.511525363%3A679314437&last_message_timestamp=https://mobile.facebook.com/messages/read/?tid=cid.c.511525363%3A679314437&last_message_timestamp=1422748800000&pagination_direction=1&show_delete_message_button&refid=12&pagination_direction=1&show_delete_message_button&refid=12
