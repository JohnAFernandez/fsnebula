import re
import requests
from flask import render_template, abort, redirect, g

from .. import app


def fetch_kn_version():
    try:
        resp = requests.get('https://github.com/ngld/knossos/releases')
        m = re.search(r'<h1 class="release-title text-normal">\s*<a href="/ngld/knossos/releases/tag/v([0-9\.]+)">Knossos ', resp.text)
        if not m:
            return False

        g.kn_version = m.group(1)
    except Exception:
        app.logger.exception('Failed to retrieve Knossos version!')
        return False
    else:
        return True


@app.route('/')
def index():
    return render_template('index.html.j2')


@app.route('/knossos/')
def show_knossos():
    return render_template('knossos.html.j2')


@app.route('/knossos/stable/version')
def get_kn_version():
    if 'kn_version' not in g:
        fetch_kn_version()

    return g.kn_version


@app.route('/knossos/stable/<base>.<ext>')
def knossos_dl(base, ext):
    if base == 'updater':
        base = 'update'

    if base not in ('Knossos', 'update') or ext not in ('exe', 'dmg'):
        abort(404)

    if 'kn_version' not in g:
        fetch_kn_version()

    url = 'https://github.com/ngld/knossos/releases/download/v%(version)s/%(base)s-%(version)s.%(ext)s' % {
        'base': base,
        'version': g.kn_version,
        'ext': ext
    }
    return redirect(url)


@app.route('/knossos/release_update')
def knossos_update():
    if fetch_kn_version():
        return 'YES'
    else:
        return 'OH NO!'
