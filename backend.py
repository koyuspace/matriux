#!/usr/bin/python3
# -*- coding: utf-8 -*-

from bottle import get, post, request, response, route, run, redirect, BaseRequest
from mastodon import Mastodon
import subprocess
import os.path
import datetime
import sys

@get("/")
def index():
    f = open("register.html")
    s = f.read().replace("{{year}}", str(datetime.datetime.now().year))
    f.close()
    return s

@get("/success")
def success():
    f = open("success.html")
    s = f.read().replace("{{year}}", str(datetime.datetime.now().year))
    f.close()
    return s

@get("/error")
def error():
    f = open("error.html")
    s = f.read().replace("{{year}}", str(datetime.datetime.now().year))
    f.close()
    return s

@post("/post")
def registration():
    try:
        email = request.forms.get("email") # pylint: disable=no-member
        password = request.forms.get("password") # pylint: disable=no-member
        instance = "koyu.space"
        appname = "Matriux - Matrix registration"
        if not os.path.exists('clientcred.'+instance+'.secret'):
            Mastodon.create_app(
                appname,
                api_base_url = 'https://'+instance,
                to_file = 'clientcred.'+instance+'.secret'
            )
        mastodon = Mastodon(
            client_id = 'clientcred.'+instance+'.secret',
            api_base_url = 'https://'+instance
        )
        mastodon.log_in(
            email,
            password,
            to_file = email+'.'+instance+'.secret',
        )
        userdict = mastodon.account_verify_credentials()
        username = userdict.username
        config = "/etc/matrix-synapse/homeserver.yaml" # default config on debian systems
        subprocess.Popen(["register_new_matrix_user", "-u", username, "-p", password, "--no-admin", "-c", config], shell=False) # Avoid using a shell for security and perhaps password logging by shell history
    except:
        print("Unexpected error:", sys.exc_info()[0]) # Log errors to console
        return redirect("https://matriux.koyu.space/error", code=302)
    return redirect("https://matriux.koyu.space/success", code=302)

run(server="tornado",port=9030,host="0.0.0.0")