from urllib.parse import urlencode
from urllib.request import Request, urlopen
from urllib.error import HTTPError
from datetime import datetime
import json

class TrackingService:
    """TrackingService class"""
    def __init__(self, key):
        if key is None:
            raise Exception('Track-Anything: Key has to be set!')
        self.trackingURL = 'https://tracking.ds2g.io:443/' + key

    def send_track(self, params):
        post_fields = {
            'type': str(params['type']),
            'application': str(params['applicationKey']),
            'value': str(params['value']),
            'trackDate': str(datetime.now().isoformat())
        }

        req = Request(self.trackingURL)
        req.add_header('Content-Type', 'application/json; charset=utf-8')
        jsondata = json.dumps(post_fields)
        jsondataasbytes = jsondata.encode('utf-8')   # needs to be bytes
        req.add_header('Content-Length', len(jsondataasbytes))
        try:
            urlopen(req, jsondataasbytes)
        except HTTPError as e:
            if e.code == 503:
                localTrackingURL = self.trackingURL
                localTrackingURL = localTrackingURL + '?'
                for key, value in post_fields.items():
                    localTrackingURL = localTrackingURL + key + '=' + value + '&'
                localTrackingURL = localTrackingURL[:-1]
                req = Request(localTrackingURL)
                try:
                    urlopen(req)
                except HTTPError as e:
                    print(e)
            else:
                print(e)