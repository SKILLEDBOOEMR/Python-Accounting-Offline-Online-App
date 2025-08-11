from flask import Flask, request,jsonify,g
from flask_limiter import *
from flask_limiter.util import get_remote_address
from supabase import *
from dotenv import load_dotenv
import os
from gotrue.errors import *
import jwt

load_dotenv()

app = Flask(__name__)
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_SERVICE_ROLE_KEY')

supabase = create_client(SUPABASE_URL,SUPABASE_KEY,options=ClientOptions(auto_refresh_token=False,persist_session=False))

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits = ['100 per minute']
)


def get_jwk_keys():
    try:
        response = supabase.auth.api.get_jwk_set()
        if response.status_code == 200:
            return response.json()['keys']
        else:
            raise Exception(response.status_code)
        
    except Exception as e:
        raise Exception(f'{e}')
def decode_token(token):
    try:
        jwks = get_jwk_keys()
        unverified_token = jwt.get_unverified_header(token)
        for jwk in jwks:
            if jwk['kid'] == unverified_token['kid']:
                public_key = jwt.algorithms.RSAAlgorithm.from_jwk(jwk)
                return jwt.decode(token, public_key, algorithms=['RS256'], audience='authenticated')
        raise Exception('Invalid token')
    except Exception as e:
        raise Exception(f'{e}')

@app.before_request
@limiter.exempt
def verify_token():
    if request.endpoint in ['ping','signup_email','login_email','check_user_exists']:
        return
    try:
        auth_header = request.headers.get('Authorization', '')
        if not auth_header.lower().startswith('bearer '):
            return jsonify({'error': 'Missing or invalid token'}), 401
        
        token = auth_header.split(' ')[1]
    except Exception as e:
        return jsonify({'error' : str(e)}), 401

    try:
        payload = decode_token(token)
        g.user = payload
    except Exception as e:
        return jsonify({'error': 'Invalid token', 'details': str(e)}), 401

@app.route('/ping',methods=['GET'])
def ping():
    try:
        return jsonify({'status':True})
    except Exception as e:
        return jsonify({'error' : str(e)})

@app.route('/profile',methods=['GET'])
def profile():
    try:
        response = g.user
        return jsonify({
            'user_id': response.get('sub'),
            'email': response.get('email')
        })
    except Exception as e :
        return jsonify({'error' : str(e)}), 501

@app.route('/login_email',methods=['POST'])
def login_email():
    try:
        data = request.get_json()
        res =supabase.auth.sign_in_with_password({
            'email' : data.get('email'),
            'password' : data.get('password')
            })

        if res.session and res.session.access_token:
            return jsonify({'token':res.session.access_token})
        
        return jsonify({'error': 'Unknown authentication error'}), 401
        
    except Exception as e:
        return jsonify({'error': str(e)}),501

@app.route('/signup_email',methods=['POST'])
def signup_email():
    try:
        data = request.get_json()
        response = supabase.auth.sign_up({
            'email': data.get('email'),
            'password' : data.get('password')
        })

        return jsonify({'message': 'Please check your email to confirm your account'}), 200
    
    except AuthApiError as e:
        return jsonify({'error': str(e)}), 400
        
    except Exception as e:
        return jsonify({"error": str(e)}), 501
    
@app.route('/check_user_exists', methods=['POST'])
def check_user_exists():
    try:
        data = request.get_json()
        email = data.get('email')

        if not email:
            return jsonify({'error': 'Email required'}), 400
        
        page = 1
        while True:
            res = supabase.auth.admin.list_users(page=page, per_page=100)
            for user in res:
                if getattr(user, 'email', None) == email:
                    return jsonify({'exists': True}), 200
            
            if len(res) < 100:
                break
            page += 1


        return jsonify({'exists': False}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)