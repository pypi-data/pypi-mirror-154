
from __future__ import annotations
import logging
import msal
from msal import PublicClientApplication
from requests_toolbelt.sessions import BaseUrlSession

from qantio.sdk.public.helpers.user_context import add_to_context, get_context
from qantio.sdk.public.common.log import set_filters
from qantio.sdk.public.common.settings import qantio_settings

logger = logging.getLogger(__name__)

GLOBAL_SETTINGS = qantio_settings()

class QantioClient(object):
    """
        The base object to interact with qantio services.
    
    """
    
    apikey          : str                       = None
    username        : str                       = None
    password        : str                       = None
    client_id       : str                       = None
    authenticated   : bool                      = False
    settings        : str                       = None
    auth_token      : str                       = None
    http_client     : BaseUrlSession            = None
    application     : PublicClientApplication   = None
    claims          : list                      = []
    authenticated_user                          = None
    
    
    def __init__(self,apikey:str):
        
        if apikey is None or not apikey:
            logger.critical(f"apikey is null or empty")

        self.apikey     = apikey
        self.settings   = GLOBAL_SETTINGS
        
        self._create_application()
        self._create_http_client()
        
        add_to_context('apikey', self.apikey)

    def _create_application(self):
        
        """
            https://msal-python.readthedocs.io/

            C#
            this.Application= PublicClientApplicationBuilder.Create(this.ApplicationClientId)
                .WithB2CAuthority(this.ApplicationB2CAuthority)
                .WithRedirectUri(this.ApplicationRedirectUri)
                .Build();
        """
        app = msal.PublicClientApplication(
            client_id           = self.settings['auth']['application_clientid'],
            client_credential   = None,
            authority           = self.settings['auth']['application_b2c_authority'], 
            validate_authority  = False
            )

        self.application = app
        logger.log(11, f"configure client app")

    def _create_http_client(self, proxy:str=None):
        
        # Create session object
        http_session = BaseUrlSession(base_url=self.settings['api']['base_address'])
        
        if proxy is not None and proxy:
            http_session.proxies.update({'https':proxy})
        
        # Configure session object
        with http_session as s:
            s.headers.update({'User-Agent'      : self.settings['sdk']['name']})
            s.headers.update({'Content-type'    : 'application/json'})
            s.headers.update({'apiKey'          : self.apikey})
            s.headers.update({'Sdk.Platform'    : self.settings['sdk']['platform']})
            s.headers.update({'Sdk.Version'     : self.settings['sdk']['version']})
            s.headers.update({'ClientId'        : None})
            
        self.http_client = http_session
        logger.log(11, f"configure http service")

    def http_client_headers(self):
        logger.info(f"headers > {self.http_client.headers}")

    def authenticate(self, username:str, password:str)->QantioClient:
        self.username       = username
        self.password       = password
        self.authenticated  = False
        self._authenticate()
        
        if not self.authenticated :
            logger.critical(f"Authentication > {self.username} > failed")
            raise PermissionError("Authentication failed")
        
        return self

    def _authenticate(self)-> None:
        auth_result=None
        try:
            auth_result = self.application.acquire_token_by_username_password(
                username    = self.username, 
                password    = self.password, 
                scopes      = self.settings['auth']['application_scopes'])
        except Exception as error:
            logger.exception(f"authentication > error > {error}")
            return

        access_token = auth_result.get('access_token', False) 
        
        if not access_token:
            logger.exception(f"authentication > error > {auth_result}", exc_info=auth_result)
            return

        self.auth_token         = auth_result['access_token']
        self.client_id          = auth_result['id_token_claims']['oid']
        self.authenticated      = True
        self.http_client.headers.update({'Authorization'    : f"Bearer {self.auth_token}"})
        self.http_client.headers.update({'ClientId'         : self.client_id})
        self.password = ""

        add_to_context('client_id',       auth_result['id_token_claims']['oid'])
        add_to_context('client_name',     auth_result['id_token_claims']['name'])
        add_to_context('client_email',    self.username)
        
        set_filters(logging.getLogger('qantio'))
        
        logger.info(f"authentication > {self.username} > ok")

    def current_settings(self):
        return self.settings

    def current_user(self):
        return get_context()

    def whoami(self)->str:
        return f'apikey : {self.apikey}, username : {self.username}, authenticated : {self.authenticated}'