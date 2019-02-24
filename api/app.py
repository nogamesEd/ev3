import falcon

# Import your endpoint classes:
from endpoints import default, init, position

# falcon.API instances are callable WSGI apps, initialise the app
HardwareAPI = api = falcon.API()
api.req_options = {
    'initialised': False,
    'Xlength': 100,
    'Ylength': 100,
    'gripper': 'irobot'
}

# define your routes
api.add_route('/', default.DefaultResource())
api.add_route('/ping', default.PingResource())
api.add_route('/init', init.InitResource())
api.add_route('/position', position.PositionResource())
