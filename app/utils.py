def add_access_headers(response):
    response['Access-Control-Allow-Origin'] = '*'
    response['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS, DELETE, PUT'
    response['Access-Control-Allow-Headers'] = 'X-Requested-With, Content-Type, Origin, Authorization, ' \
                                               + 'Accept, Client-Security-Token, Accept-Encoding, ' \
                                               + 'X-Auth-Token, content-type'
    return response
