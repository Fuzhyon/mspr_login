from flask import render_template, request, redirect, url_for, flash
from main import app

from forms.LoginForm import *
from flask_cors import CORS, cross_origin
from flask.sessions import SecureCookieSessionInterface
from itsdangerous import URLSafeTimedSerializer

from views.global_ldap_authentication import global_ldap_authentication_func


@app.route('/login', methods=['GET', 'POST'])
def index():
    # initiate the form..
    form = LoginValidation()

    if request.method in ('POST'):
        login_id = form.user_name_pid.data
        login_password = form.user_pid_Password.data

        # create a directory to hold the Logs
        login_msg = global_ldap_authentication_func(login_id, login_password)

        # validate the connection
        if login_msg == "Success":
            success_message = f"*** Authentication Success "
            return render_template('success.html', success_message=success_message)

        else:
            error_message = f"*** Authentication Failed - {login_msg}"
            return render_template("error.html", error_message=str(error_message))

    return render_template('login.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
