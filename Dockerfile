# =====================================================================
# Dockerfile para Django + MySQL  (molde e-metalurgicaservicos)
# App: pocomanut  —  Django 5.2, MySQL via mysqlclient
# Settings: pocomanut.settings  |  WSGI: pocomanut.wsgi:application
#
# DIFERENÇA EXTRA vs metalurgico: WeasyPrint (PDF) precisa de libs de
# sistema no estagio final (pango/harfbuzz) + fontes (pdf sem fonte = 
# texto branco/tosco).
#
# ATENÇÃO: local_settings.py NÃO entra na imagem (.dockerignore) - 
# ele sobrescreve o settings com DEBUG=True e banco local de root!
# =====================================================================

# ---------------------- Estágio de BUILD (compila o mysqlclient) -----
FROM python:3.12-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /build

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --prefix=/install -r requirements.txt

# ---------------------- Estágio FINAL (leve) ------------------------
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# libmariadb3 = runtime do mysqlclient (compilado no builder).
# pango/harfbuzz/subset0 + fontconfig + fontes = WeasyPrint funcionando.
RUN apt-get update && apt-get install -y --no-install-recommends \
    libmariadb3 \
    libpango-1.0-0 \
    libpangoft2-1.0-0 \
    libharfbuzz0b \
    libharfbuzz-subset0 \
    fontconfig \
    fonts-dejavu-core \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /install /usr/local

COPY . .

RUN mkdir -p media staticfiles

EXPOSE 8000

CMD ["sh", "-c", "\
    python manage.py migrate --noinput && \
    python manage.py collectstatic --noinput && \
    gunicorn pocomanut.wsgi:application \
      --bind 0.0.0.0:8000 \
      --workers ${GUNICORN_WORKERS:-2} \
      --timeout ${GUNICORN_TIMEOUT:-120} \
      --access-logfile - \
      --error-logfile -"]
