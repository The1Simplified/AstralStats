from flask import render_template as flask_render_template, request

def render_template(*args, **kwargs):
    return flask_render_template(*args, **kwargs, domain_url=request.url_root)