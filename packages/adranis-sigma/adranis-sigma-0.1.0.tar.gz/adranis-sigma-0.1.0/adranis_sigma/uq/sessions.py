import time
import sys
import uuid
import logging
import json
import ssl
import urllib.request
import numpy as np
import adranis_sigma.uq.helpers as helpers
import adranis_sigma.uq.interface as interface


class uq_session():

    def __init__(self, name=None, log_level=None, log_format=None):
        # Try to retrieve the Sigma API configuration from a file if available
        theConfig = helpers.sigma_load_config()
        self.stored_host = theConfig['host']
        self.stored_token = theConfig['token']
        self.compute_url = 'undefined'
        self.update_url = 'undefined'
        self.update_intermid_url = 'undefined'
        self.timeout = 1
        self.refresh_period = 0.5
        self.token = 'undefined'
        self.ssl_context = ''

        if name is None:
            self.name = uuid.uuid4().hex
        else:
            self.name = name
        # Set the logging output format
        if log_format is None:
            # Set the default log format if not specified
            log_format = ' %(name)s :: %(levelname)-8s :: %(message)s'
        # Initialize a logger
        logging.basicConfig(stream=sys.stdout, format=log_format)
        self.logger = logging.getLogger(__name__)
        # Set the logger log level
        self.set_log_level(log_level=log_level)

    def set_log_level(self, log_level=None):
        if log_level is not None:
            level = logging.getLevelName(log_level.upper())
            self.logger.setLevel(level)

    def rename(self, new_name):
        name_prev = self.name
        self.name = new_name
        return f"Session renamed from {name_prev} to {new_name}."

    def throw_worker_error(self, msg):
        self.logger.error('UQLab worker error: %s', msg)

    def get_resp_value(self, resp):
        # Build a response list if resp contains more than 1 'Value' keys
        if sum([1 for d in resp if 'Value' in d]) > 1:
            resp_final = []
            for respi in resp:
                if respi['Errors']:
                    self.throw_worker_error(respi['Message'])
                    return -1
                else:
                    resp_final.append(respi['Value'])
            return resp_final
        else:
            if resp['Errors']:
                self.throw_worker_error(resp['Message'])
                return -1
            else:
                return resp['Value']

    def rest_call(self, request=None, url=None, httpobj=False):
        if url is None:
            url = self.compute_url
        if request is None:
            raise ValueError('Empty request, aborting rest call.')
        return self.rest_poll(request=request, httpobj=httpobj)

    def rest_poll(self, request, httpobj=False):
        # send request
        resp = self.rest_call_cloud(url=self.compute_url,
                                    request=request,
                                    httpobj=True)
        if resp.getcode() == 201:
            resp_string = resp.read().decode('utf-8')
            resp_json = json.loads(resp_string)
            jobID = int(resp_json['jobID'])
        else:
            jobID = -2

        if jobID < 0:
            self.throw_worker_error(
                'UQ Engine error: the submitted request could not be completed.'
            )

        update_url = f"{self.update_url}{str(jobID)}"
        timeout = time.time() + self.timeout
        # wait until timeout
        while True:
            resp = self.rest_call_cloud(url=update_url,
                                        request='',
                                        httpobj=True)
            if resp.getcode() == 200:
                # return result
                return json.loads(resp.read().decode('utf-8'))
            if resp.getcode() == 201:
                # there is an intermediate step

                intermid_info_json = json.loads(resp.read().decode('utf-8'))
                intermid_fun = intermid_info_json['function']
                intermid_input = intermid_info_json['data']
                self.logger.info(
                    "Received intermediate compute request, function: %s.",
                    intermid_fun)
                self.logger.info('Carrying out local computation...')
                if 'parameters' in intermid_info_json:
                    intermid_parameters = intermid_info_json['parameters']
                    res_intermid = helpers.function_eval(
                        intermid_fun, intermid_input, intermid_parameters)
                else:
                    res_intermid = helpers.function_eval(
                        intermid_fun, intermid_input)
                self.logger.info('Local computation complete.')
                req_intermid = {
                    'data': np.array(res_intermid).tolist(),
                    'jobID': jobID
                }
                self.logger.info(
                    'Starting transmission of intermediate compute results (%s)...',
                    np.array(res_intermid).shape)
                resp = self.rest_call_cloud(url=self.update_intermid_url,
                                            request=req_intermid,
                                            httpobj=True)
                self.logger.info('Intermediate compute results sent.')
                timeout = time.time() + self.timeout
            if time.time() > timeout:
                return {'Errors': True, 'Message': 'Timeout reached'}
            time.sleep(self.refresh_period)

    def rest_call_cloud(self, url, request, httpobj=False):
        req = urllib.request.Request(url)
        req.add_header('Authorization', f"Token {self.token}")
        req.add_header('Content-Type', 'application/json; charset=utf-8')
        try:
            jsondataasbytes = request.encode('utf-8')
        except BaseException:
            jsondataasbytes = json.dumps(request,
                                         sort_keys=True).encode('utf-8')
        req.add_header('Content-Length', len(jsondataasbytes))
        response = urllib.request.urlopen(req,
                                          jsondataasbytes,
                                          context=self.ssl_context)
        if httpobj:
            return response
        else:
            return json.loads(response.read().decode('utf-8'))


class CloudSession(uq_session):

    def __init__(self,
                 host=None,
                 token=None,
                 name=None,
                 strict_ssl=True,
                 log_level="INFO",
                 log_format=None):
        super().__init__(name, log_level, log_format)
        if host is None:
            self.host = self.stored_host
        else:
            self.host = host
        if token is None:
            self.token = self.stored_token
        else:
            self.token = token
        self.refresh_period = 0.3  # in seconds
        self.timeout = 120  # in seconds
        self.compute_url = f"{self.host}/compute/"
        self.update_url = f"{self.host}/update/"
        self.update_intermid_url = f"{self.host}/update-intermid/"
        self.session_type = 'cloud'

        # In case the strict_ssl flag is set to False, requests to the Sigma
        # API will not involve checking the SSL certificate of the API. This can
        # be used to bypass certificate errors that may randomly occur in some
        # OS's
        if strict_ssl:
            self.ssl_context = None
        else:
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            self.ssl_context = ctx
            # Raise a warning to remind the user that this is risky and they should
            # know what they are doing
            warn_msg = (
                "The SSL certificate of the API host will not be verified." +
                " Make sure that you understand the risks involved!")
            self.logger.warning(warn_msg)

        self.new()

    def new(self):

        self.cli = interface.uq(self)
        REQ = {
            'Command': 'disp',
            'Argument': [{
                'Value': 'Session started.'
            }],
            'nargout': 0,
        }
        resp = self.rest_call(REQ)
        if resp['Errors']:
            raise RuntimeError(resp['Message'])
        else:
            self.logger.info('A new session (%s) started.', self.name)

    def quit(self):
        REQ = {
            'Command': 'exit',
            'nargout': 0,
        }
        #resp = self.rest_call(REQ)
        resp = self.rest_call_cloud(url=self.compute_url,
                                    request=REQ,
                                    httpobj=False)
        if resp['Errors']:
            self.logger.error(
                'Something went wrong while terminating session %s.',
                self.name)
            return False
        else:
            self.logger.info('Session %s terminated.', self.name)
            self.name = None
            return True

    def list(self):
        REQ = {
            'Command': 'uq_list_sessions_web',
        }
        resp = self.rest_call(REQ)
        resp_value = self.get_resp_value(resp)
        print(resp_value)

    def reset(self):
        REQ = {'Command': 'uqlab', 'nargout': 0}
        resp = self.rest_call(REQ)
        if resp:
            self.logger.info('Reset successful.')
        else:
            self.logger.error('Reset failed.')

    def remove(self, name):
        REQ = {
            'Command': 'uq_delete_session_web',
            'Argument': [{
                'Value': name
            }],
            'nargout': 2
        }
        resp = self.rest_call(REQ)
        resp_value = self.get_resp_value(resp)
        if resp_value:
            if name == '*':
                self.logger.info('All sessions removed.')
            else:
                self.logger.info("Session %s  removed.", name)
        else:
            self.logger.error("Session %s  removal failed.", name)

    def save(self, name=None):
        if name is None:
            session_name = self.name
        else:
            session_name = name

        REQ = {
            'Command': 'uq_save_session_web',
            'Argument': [{
                'Value': session_name
            }]
        }
        resp = self.rest_call(REQ)
        resp_value = self.get_resp_value(resp)
        if resp_value:
            self.logger.info('Session %s saved.', session_name)
        else:
            self.logger.error('Tried to save Session %s but failed.',
                              session_name)

    def load(self, name):
        REQ = {'Command': 'uq_load_session_web', 'Argument': [{'Value': name}]}
        resp = self.rest_call(REQ)
        resp_value = self.get_resp_value(resp)
        self.name = name
        if resp_value:
            self.logger.info('Session %s loaded.', name)
        else:
            self.logger.error('Session %s loading failed.', name)

    def save_config(self):
        self.logger.info(helpers.sigma_save_config(self.host, self.token))
