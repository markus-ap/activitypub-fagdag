from flask import Flask, send_from_directory, jsonify, request
import json

app = Flask(__name__, static_url_path='/static')

@app.route('/')
def serve_index():
    return send_from_directory('static', 'index.html')


@app.route('/.well-known/webfinger')
def webfinger():
    resource = validate_resource(request)
    if resource is None:
        return "Invalid resource", 400
    
    username, host = clean_username(resource)
    if username is None:
        return "Invalid resource", 400
    
    if not is_internal_host(host):
        return "External host not supported", 400
    
    user = find_user(username)
    if user is None:
        return "User not found", 404
    
    response = {
        "subject": f"acct:{username}@{host}",
        "links": [
            {
                "rel": "self",
                "href": user['@id']
            }
        ]
    }
    return jsonify(response)

def validate_resource(request):
    resource = request.args.get('resource', default = "*", type = str)
    if resource == None or resource == "":
        return None
    return resource

def clean_username(resource: str):
    if resource.startswith('acct:'):
        username, host = resource[5:].split('@', 1)
        return username, host

def is_internal_host(host: str):
    return host == 'localhost' or host == "127.0.0.1:5000"

def find_user(username: str):
    with open('./static/data/users.jsonld') as f:
        users = json.load(f)

    user = next((user for user in users if user['id'] == username), None)
    return user


if __name__ == '__main__':
    app.run(debug=True)