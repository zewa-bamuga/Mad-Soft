#!/bin/bash

set -o errexit
set -o pipefail

# Let the DB start
python -m a8t_tools.db.wait_for_db

alembic upgrade head

# Create meme
if [ -n "${DESCRIPTION}" ]; then
  python manage.py create-meme "${DESCRIPTION}"  || true
fi

exec "$@"