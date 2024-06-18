FROM odoo:17.0

# Instala dependencias adicionales si es necesario
USER root
RUN apt-get update && apt-get install -y python3-pip
USER odoo

# Copia los archivos del módulo a la carpeta de addons
COPY ./extra_addons /mnt/extra-addons