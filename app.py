import pyotp
from flask import *
from flask import render_template, request
from ldap3 import Server, Connection, ALL, Tls, NTLM
import ssl

from forms.LoginForm import *
from main import app
from main import csrf




def global_ldap_authentication_func(user_name, user_pwd):

    ldsp_server = "192.168.1.150:389"
    # ldap user and password
    ldap_password = 'Fhfctk97450'
    # user
    admin = "Administrateur@local.chatelet.tk"

    server_admin = Server(ldsp_server, get_info=ALL)

    connection_admin = Connection(server_admin, user=admin, password=ldap_password, auto_bind=True)
    connection_admin.bind()

    if connection_admin:


        # fetch the username and password
        ldap_user_name = user_name
        ldap_user_pwd = user_pwd

        # user
        user = ldap_user_name+"@local.chatelet.tk"

        tls_configuration = Tls(validate=ssl.CERT_REQUIRED, version=ssl.PROTOCOL_TLSv1_2)
        server = Server('192.168.1.150', use_ssl=False, tls=tls_configuration)
        con_user = Connection(server, user=user, password=ldap_user_pwd, auto_referrals=False)

        if not con_user.bind():
            print(f" *** Cannot bind to ldap server: {con_user.last_error} ")
            l_success_msg = f' ** Failed Authentication: {con_user.last_error}'
        else:
            print(f" *** Successful bind to ldap server")
            l_success_msg = 'Success'

        return l_success_msg
    else:
        print(connection_admin)


@app.route('/login/', methods=['GET', 'POST'])
def index():
    # initiate the form..
    form = LoginValidation(request.form)

    if request.method in 'POST':
        login_id = form.user_name_pid.data
        login_password = form.user_pid_Password.data

        # create a directory to hold the Logs
        login_msg = global_ldap_authentication_func(login_id, login_password)

        # validate the connection
        if login_msg == "Success":
            success_message = f"*** Authentication Success "
            return redirect(url_for("login_2fa"))

        else:
            error_message = f"*** Authentication Failed - {login_msg}"
            return render_template("error.html", error_message=str(error_message))

    return render_template('login.html', form=form)


# 2FA page route
@app.route("/login/2fa/")
@csrf.exempt
def login_2fa():
    # generating random secret key for authentication
    secret = pyotp.random_base32()
    return render_template("includes/login_2fa.html", secret=secret)


# 2FA form route
@app.route("/login/2fa/", methods=['GET', 'POST'])
@csrf.exempt
def login_2fa_form():
    # getting secret key used by user
    secret = request.form.get("secret")
    # getting OTP provided by user
    otp = int(request.form.get("otp"))

    # verifying submitted OTP with PyOTP
    if pyotp.TOTP(secret).verify(str(otp)):
        # inform users if OTP is valid
        flash("The TOTP 2FA token is valid", "success")
        return redirect(url_for("login_2fa"))
    else:
        # inform users if OTP is invalid
        flash("You have supplied an invalid 2FA token!", "danger")
        return redirect(url_for("login_2fa"))


if __name__ == '__main__':
    app.run(debug=True)
