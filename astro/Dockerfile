FROM astrocrpublic.azurecr.io/runtime:3.0-1
RUN source env/bin/activate && pip install --no-cache-dir dbt-postgres && deactivate
USER root
RUN apt-get update && apt-get install -y git
USER astro