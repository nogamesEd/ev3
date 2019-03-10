import falcon
import json
from state import robotstate

class ValidateRequest(object):
    def process_request(self, req, resp):

        print("[{}] {}".format(req.method, req.path))

        if req.path in ["/init", "/ping", "/"]:
            return
        
        # Requests require initalisation
        if not robotstate['initialised']:
            print("[ERROR] 428: Robot not initalised. Cannot move yet.")
            raise falcon.HTTPPreconditionRequired(
                title = "428: Robot not initialised",
                description = json.dumps({
                'success': False,
                'error': 'Robot has not been initialised, POST to /init first.'
            }))
        
        # Body must be included in POST requests
        if not req.content_length:
            print("[ERROR] 400: Request missing body.")
            raise falcon.HTTPBadRequest(
                description = json.dumps({
                'success': False,
                'error': 'Request missing body.'
                })
            )
