# coding: utf-8

import sys
from jting import create_app
from jting.models import db

app = create_app({'DEBUG': True})

def create_database():
    import fixtures
    with app.app_context():
        db.drop_all()
        db.create_all()
        fixtures.run()

if '--initdb' in sys.argv:
    create_database()
    sys.exit()

with app.app_context():
    db.create_all()

app.run(host='0.0.0.0')