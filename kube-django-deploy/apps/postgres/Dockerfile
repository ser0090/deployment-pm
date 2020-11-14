FROM postgres:9.4

ENTRYPOINT []
CMD export POSTGRES_DB=postgres; export POSTGRES_USER=postgres; export POSTGRES_PASSWORD=$(cat /etc/secrets/djangouserpw) ;./docker-entrypoint.sh postgres;

