from app.models import User, UserLogged


def add_access_headers(response):
    response['Access-Control-Allow-Origin'] = '*'
    response['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS, DELETE, PUT'
    response['Access-Control-Allow-Headers'] = 'X-Requested-With, Content-Type, Origin, Authorization, ' \
                                               + 'Accept, Client-Security-Token, Accept-Encoding, ' \
                                               + 'X-Auth-Token, content-type'
    return response

def checkCredentials(req):
    if 'authorization' not in req.headers:
        return

    token = req.headers['authorization']
    lst_token = token.split(';;')

    tokens = UserLogged.objects.filter(token=lst_token[0])

    for tkn in tokens:
        return tkn.owner_id

    return


