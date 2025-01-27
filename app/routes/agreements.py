from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models import Agreement
from flask import render_template, request, redirect, url_for
from docusign_esign import ApiClient, EnvelopesApi, Signer, SignHere, Tabs, Recipients, EnvelopeDefinition
import os
from docusign_esign.models import RecipientViewRequest
bp = Blueprint('agreements', __name__)
PRIVATE_KEY_FILE_PATH  ="/home/adminstrator/RASS/PRIVATE_KEY_FILE_PATH"
with open(PRIVATE_KEY_FILE_PATH, "r") as key_file:
    private_key = key_file.read()

@bp.route('/agreements')
@login_required
def list_agreements():
    agreements = Agreement.query.filter_by(user_id=current_user.id).all()
    return render_template('agreements.html', agreements=agreements)

@bp.route('/agreements/create', methods=['GET', 'POST'])
@login_required
def create_agreement():
    if request.method == 'POST':
        try:
            # Step 1: Setup the API Client
            api_client = ApiClient()
            api_client.set_base_path('https://demo.docusign.net/restapi')

            # Step 2: Request the JWT token
            response = api_client.request_jwt_user_token(
                client_id="04f9004a-2954-471f-b004-5d823237cafe",
                user_id="d980edaf-9904-48be-9638-a0f08645d4c7",
                scopes=["signature", "impersonation"],
                oauth_host_name="account-d.docusign.com",  # Use "account.docusign.com" for production
                private_key_bytes=private_key.encode("utf-8"),
                expires_in=36000,
            )

            # Step 3: Extract the access token from the response
            access_token = response.access_token  # This is the correct way to access the token

            # Step 4: Set the access token for API requests
            api_client.set_default_header("Authorization", f"Bearer {access_token}")
            account_id = ('bf644e16-ba2e-4b3f-ba3e-b93ba33879ca')

            # Step 2: Create the envelope definition
            signer = Signer(
                email=request.form['email'],
                name=request.form['name'],
                recipient_id="1",
                routing_order="1"
            )
            sign_here = SignHere(
                document_id="1",
                page_number="1",
                recipient_id="1",
                tab_label="SignHere",
                x_position="200",
                y_position="300"
            )
            tabs = Tabs(sign_here_tabs=[sign_here])
            signer.tabs = tabs
            recipients = Recipients(signers=[signer])
            envelope_definition = EnvelopeDefinition(
                email_subject="Please sign this agreement",
                documents=[{
                    "documentBase64": request.form['document_base64'],
                    "documentId": "1",
                    "fileExtension": "pdf",
                    "name": "Agreement Document"
                }],
                recipients=recipients,
                status="sent"
            )

            # Step 3: Send the envelope
            envelopes_api = EnvelopesApi(api_client)
            results = envelopes_api.create_envelope(account_id, envelope_definition=envelope_definition)
            print(results)
            # Step 4: Generate the signing URL
            recipient_view_request = RecipientViewRequest(
                authentication_method="email",
                client_user_id="1",
                recipient_id="1",
                return_url=url_for('thank_you', _external=True),
                user_name=request.form['name'],
                email=request.form['email']
            )
            signing_url = envelopes_api.create_recipient_view(account_id, results.envelope_id, recipient_view_request)

            return redirect(signing_url.url)
        except Exception as e:
            print(f"Error: {e}")
            flash("An error occurred while creating the agreement.")
            return redirect(url_for('agreements.create_agreement'))

    return render_template('create.html')