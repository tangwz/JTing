# coding: utf-8

import os
from flask import Blueprint, request, session, current_app, json
from flask import render_template, abort, redirect

bp = Blueprint('front', __name__, template_folder='template')
bp.add_app_template_filter()

@bp.before_request
def manifest_hook():
    manifest_file = current_app.config.get('SITE_MANIFEST')
    if not manifest_file or not os.path.isfile(manifest_file):
        request.manifest = None
        return

    manifest_mtime = os.path.getmtime(manifest_file)
    latest = getattr(current_app, 'manifest_mtime', 0)
    if latest != manifest_mtime:
        current_app.manifest_mtime = manifest_mtime
        with open(manifest_file) as f:
            manifest = json.load(f)
            current_app.manifest = manifest

    request.manifest = getattr(current_app, 'manifest', None)

@bp.route('/')
def home():
    return render_template(
        'front/index.html',

    )