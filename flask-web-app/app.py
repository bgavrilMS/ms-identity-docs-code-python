import os
import requests
from flask import Flask, render_template
from identity.flask import Auth
import app_config

__version__ = "0.9.0"  # The version of this sample, for troubleshooting purpose

app = Flask(__name__)
app.config.from_object(app_config)
auth = Auth(
    app,
    authority=os.getenv("AUTHORITY"),
    client_id=os.getenv("CLIENT_ID"),
    client_credential=os.getenv("CLIENT_SECRET"),
    redirect_uri=os.getenv("REDIRECT_URI"),
    oidc_authority=os.getenv("OIDC_AUTHORITY"),
)

@app.route("/")
@auth.login_required
def index(*, context):
    return render_template(
        'index.html',
        user=context['user'],
        api_endpoint=os.getenv("ENDPOINT"),
        title=f"Flask Web App Sample v{__version__}",
    )

@app.route("/call_api")
@auth.login_required(scopes=os.getenv("SCOPE", "").split())
def call_downstream_api(*, context):
    api_result = requests.get(  # Use access token to call a web api
        os.getenv("ENDPOINT"),
        headers={'Authorization': 'Bearer ' + context['access_token']},
        timeout=30,
    ).json() if context.get('access_token') else "Did you forget to set the SCOPE environment variable?"
    return render_template('display.html', title="API Response", result=api_result)
