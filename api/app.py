import falcon

# Import your endpoint classes:
from endpoints import middleware, default
from endpoints import gripper
from endpoints import init, position

# falcon.API instances are callable WSGI apps, initialise the app
HardwareAPI = api = falcon.API(middleware=middleware.ValidateRequest())

# define your routes
api.add_route('/', default.DefaultResource())
api.add_route('/ping', default.PingResource())
api.add_route('/init', init.InitResource())
api.add_route('/position', position.PositionResource())
api.add_route('/gripper', gripper.GripperResource())
