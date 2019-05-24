# Convert a YAML config file into classes.
#
# Copyright (C) 2019  Marc Bertens-Nguyen <m.bertens@pe2mbs.nl
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#
from saiti import ConfigProcessor
from datetime import timedelta
from typing import Union


class FlaskConfigMixin( object ):
    """This is the FLASK configuration class

    """
    __envs = ( 'production', 'testing', 'staging', 'development' )

    def __init__( self, **kwargs ):
        """Constructor of the FLASK configuration class

        :param kwargs:  see ConfigProcessor: kwargs
        """
        self.__testing                          = False
        self.__secret_key                       = None
        self.__env                              = 'production'
        self.__debug                            = False
        self.__propagate_exceptions             = None
        self.__preserve_context_on_exception    = None
        self.__trap_http_exceptions             = False
        self.__trap_bad_request_errors          = None
        self.__session_cookie_name              = 'session'
        self.__session_cookie_domain            = None
        self.__session_cookie_path              = None
        self.__session_cookie_httponly          = True
        self.__session_cookie_secure            = False
        self.__session_cookie_samesite          = None
        self.__permanent_session_lifetime       = timedelta( days = 31 )
        self.__session_refresh_each_request     = True
        self.__use_x_sendfile                   = False
        self.__send_file_max_age_default        = timedelta( hours = 12 )
        self.__server_name                      = None
        self.__application_root                 = None
        self.__preferred_url_scheme             = 'http'
        self.__max_content_length               = None
        self.__json_as_ascii                    = True
        self.__json_sort_keys                   = True
        self.__jsonify_prettyprint_regular      = False
        self.__jsonify_mimetype                 = 'application/json'
        self.__templates_auto_reload            = None
        self.__explain_template_loading         = False
        self.__max_cookie_size                  = 4093
        return

    @property
    def TESTING( self ) -> bool:
        """Enable testing mode. Exceptions are propagated rather than
        handled by the the app’s error handlers. Extensions may
        also change their behavior to facilitate easier testing.
        You should enable this in your own tests.
        """
        return self.__testing

    @TESTING.setter
    def TESTING( self, value: bool ):
        self.__testing = value
        return

    @property
    def ENV( self ) -> str:
        """What environment the app is running in. Flask and
        extensions may enable behaviors based on the environment,
        such as enabling debug mode. The env attribute maps to
        this config key. This is set by the FLASK_ENV environment
        variable and may not behave as expected if set in code.
        """
        return self.__env

    @ENV.setter
    def ENV( self, value: str ):
        if value in self.__envs:
            self.__env = value
            return

        raise ValueError( "ENV must be set to one of {}".format( ", ".join( self.__envs ) ) )

    @property
    def DEBUG( self ) -> bool:
        """Whether debug mode is enabled. When using flask run to
        start the development server, an interactive debugger
        will be shown for unhandled exceptions, and the server
        will be reloaded when code changes. The debug attribute
        maps to this config key. This is enabled when ENV is
        'development' and is overridden by the FLASK_DEBUG
        environment variable. It may not behave as expected
        if set in code.
        """
        return self.__debug

    @DEBUG.setter
    def DEBUG( self, value: bool ):
        self.__debug = value
        return

    @property
    def PROPAGATE_EXCEPTIONS( self ) -> bool:
        """Exceptions are re-raised rather than being handled by
        the app’s error handlers. If not set, this is implicitly
        true if TESTING or DEBUG is enabled.
        """
        return self.__propagate_exceptions

    @PROPAGATE_EXCEPTIONS.setter
    def PROPAGATE_EXCEPTIONS( self, value: bool ):
        self.__propagate_exceptions = value
        return

    @property
    def PRESERVE_CONTEXT_ON_EXCEPTION( self ) -> bool:
        """Don’t pop the request context when an exception occurs.
        If not set, this is true if DEBUG is true. This allows
        debuggers to introspect the request data on errors, and
        should normally not need to be set directly.
        """
        return self.__preserve_context_on_exception

    @PRESERVE_CONTEXT_ON_EXCEPTION.setter
    def PRESERVE_CONTEXT_ON_EXCEPTION( self, value: bool ):
        self.__preserve_context_on_exception = value
        return

    @property
    def TRAP_HTTP_EXCEPTIONS( self ) -> bool:
        """If there is no handler for an HTTPException-type exception,
        re-raise it to be handled by the interactive debugger
        instead of returning it as a simple error response.
        """
        return self.__trap_http_exceptions

    @TRAP_HTTP_EXCEPTIONS.setter
    def TRAP_HTTP_EXCEPTIONS( self, value: bool ):
        self.__trap_http_exceptions = value
        return

    # TODO: set typing on the getter/setter of TRAP_BAD_REQUEST_ERRORS
    @property
    def TRAP_BAD_REQUEST_ERRORS( self ):
        """Trying to access a key that doesn’t exist from request
        dicts like args and form will return a 400 Bad Request
        error page. Enable this to treat the error as an unhandled
        exception instead so that you get the interactive debugger.
        This is a more specific version of TRAP_HTTP_EXCEPTIONS.
        If unset, it is enabled in debug mode.
        """
        return self.__trap_bad_request_errors

    @TRAP_BAD_REQUEST_ERRORS.setter
    def TRAP_BAD_REQUEST_ERRORS( self, value ):
        self.__trap_bad_request_errors = value
        return

    @property
    def SECRET_KEY( self ) -> str:
        """A secret key that will be used for securely signing
        the session cookie and can be used for any other
        security related needs by extensions or your application.
        It should be a long random string of bytes, although
        unicode is accepted too.
        """
        return self.__secret_key

    @SECRET_KEY.setter
    def SECRET_KEY( self, value: str ):
        self.__secret_key = value
        return

    @property
    def SESSION_COOKIE_NAME( self ) -> str:
        """The name of the session cookie. Can be changed in
        case you already have a cookie with the same name.
        """
        return self.__session_cookie_name

    @SESSION_COOKIE_NAME.setter
    def SESSION_COOKIE_NAME( self, value: str ):
        self.__session_cookie_name = value
        return

    @property
    def SESSION_COOKIE_DOMAIN( self ) -> str:
        """The domain match rule that the session cookie will
        be valid for. If not set, the cookie will be valid
        for all subdomains of SERVER_NAME. If False, the
        cookie’s domain will not be set.
        """
        return self.__session_cookie_domain

    @SESSION_COOKIE_DOMAIN.setter
    def SESSION_COOKIE_DOMAIN( self, value: str ):
        self.__session_cookie_domain = value
        return

    @property
    def SESSION_COOKIE_PATH( self ) -> str:
        """The path that the session cookie will be valid for.
        If not set, the cookie will be valid underneath
        APPLICATION_ROOT or / if that is not set.
        """
        return self.__session_cookie_path

    @SESSION_COOKIE_PATH.setter
    def SESSION_COOKIE_PATH( self, value: str ):
        self.__session_cookie_path = value
        return

    @property
    def SESSION_COOKIE_HTTPONLY( self ) -> bool:
        """Browsers will not allow JavaScript access to cookies
        marked as “HTTP only” for security.
        """
        return self.__session_cookie_httponly

    @SESSION_COOKIE_HTTPONLY.setter
    def SESSION_COOKIE_HTTPONLY( self, value: bool ):
        self.__session_cookie_httponly = value
        return

    @property
    def SESSION_COOKIE_SECURE( self ) -> bool:
        """Browsers will only send cookies with requests over HTTPS
        if the cookie is marked “secure”. The application must
        be served over HTTPS for this to make sense.
        """
        return self.__session_cookie_secure

    @SESSION_COOKIE_SECURE.setter
    def SESSION_COOKIE_SECURE( self, value: bool ):
        self.__session_cookie_secure = value
        return

    @property
    def SESSION_COOKIE_SAMESITE( self ) -> str:
        """Restrict how cookies are sent with requests from external
        sites. Can be set to 'Lax' (recommended) or 'Strict'.
        See Set-Cookie options.
        """
        return self.__session_cookie_samesite

    @SESSION_COOKIE_SAMESITE.setter
    def SESSION_COOKIE_SAMESITE( self, value: str ):
        self.__session_cookie_samesite = value
        return

    @property
    def PERMANENT_SESSION_LIFETIME( self ) -> timedelta:
        """If session.permanent is true, the cookie’s expiration
        will be set this number of seconds in the future.
        Can either be a datetime.timedelta or an int.
        Flask’s default cookie implementation validates that
        the cryptographic signature is not older than this
        value.
        """
        return self.__permanent_session_lifetime

    @PERMANENT_SESSION_LIFETIME.setter
    def PERMANENT_SESSION_LIFETIME( self, value: Union[int, str, timedelta] ) -> None:
        if type( value ) is str:
            try:
                self.__permanent_session_lifetime = timedelta( days = int( value, 10 ) )

            except:
                raise ValueError( "PERMANENT_SESSION_LIFETIME must be an integer value" )

        elif type( value ) is int:
            self.__permanent_session_lifetime = timedelta( days = value )

        elif isinstance( value, timedelta ):
            self.__permanent_session_lifetime = value

        else:
            raise ValueError( "PERMANENT_SESSION_LIFETIME must be an integer value or timedelta( days = ? )" )

        return

    @property
    def SESSION_REFRESH_EACH_REQUEST( self ) -> bool:
        """Control whether the cookie is sent with every response
        when session.permanent is true. Sending the cookie every
        time (the default) can more reliably keep the session
        from expiring, but uses more bandwidth. Non-permanent
        sessions are not affected.
        """
        return self.__session_refresh_each_request

    @SESSION_REFRESH_EACH_REQUEST.setter
    def SESSION_REFRESH_EACH_REQUEST( self, value: bool ):
        self.__session_refresh_each_request = value
        return

    @property
    def USE_X_SENDFILE( self ) -> bool:
        """When serving files, set the X-Sendfile header instead of
        serving the data with Flask. Some web servers, such as
        Apache, recognize this and serve the data more efficiently.
        This only makes sense when using such a server.
        """
        return self.__use_x_sendfile

    @USE_X_SENDFILE.setter
    def USE_X_SENDFILE( self, value: bool ) -> None:
        self.__use_x_sendfile = value
        return

    @property
    def SEND_FILE_MAX_AGE_DEFAULT( self ) -> timedelta:
        """When serving files, set the cache control max age to this
        number of seconds. Can either be a datetime.timedelta or
        an int. Override this value on a per-file basis using
        get_send_file_max_age() on the application or blueprint.
        """
        return self.__send_file_max_age_default

    @SEND_FILE_MAX_AGE_DEFAULT.setter
    def SEND_FILE_MAX_AGE_DEFAULT( self, value: Union[int, str, timedelta] ) -> None:
        if type( value ) is str:
            try:
                self.__send_file_max_age_default = timedelta( hours = int( value, 10 ) )

            except:
                raise ValueError( "SEND_FILE_MAX_AGE_DEFAULT must be set to an integer" )

        elif type( value ) is int:
            self.__send_file_max_age_default = timedelta( hours = value )

        elif isinstance( value, timedelta ):
            self.__send_file_max_age_default = value

        else:
            raise ValueError( "SEND_FILE_MAX_AGE_DEFAULT must be set to an integer or timedelta( hours = ? )" )

        return

    @property
    def SERVER_NAME( self ) -> str:
        """Inform the application what host and port it is bound to.
        Required for subdomain route matching support.
        If set, will be used for the session cookie domain if
        SESSION_COOKIE_DOMAIN is not set. Modern web browsers
        will not allow setting cookies for domains without a dot.
        To use a domain locally, add any names that should route
        to the app to your hosts file. If set, url_for can generate
        external URLs with only an application context instead of
        a request context.
        """
        return self.__server_name

    @SERVER_NAME.setter
    def SERVER_NAME( self, value: str ):
        self.__server_name = value
        return

    @property
    def APPLICATION_ROOT( self ) -> str:
        """Inform the application what path it is mounted under
        by the application / web server. Will be used for the
        session cookie path if SESSION_COOKIE_PATH is not set.
        """
        return self.__application_root

    @APPLICATION_ROOT.setter
    def APPLICATION_ROOT( self, value: str ):
        if value.startswith( '/' ):
            self.__application_root = value
            return

        raise ValueError( "APPLICATION_ROOT must start with /" )

    @property
    def PREFERRED_URL_SCHEME( self ) -> str:
        """Use this scheme for generating external URLs when
        not in a request context.
        """
        return self.__preferred_url_scheme

    @PREFERRED_URL_SCHEME.setter
    def PREFERRED_URL_SCHEME( self, value: str ):
        if value in [ 'http', 'https' ]:
            self.__preferred_url_scheme = value
            return

        raise ValueError( "PREFERRED_URL_SCHEME must be one of 'http' or 'https'" )

    @property
    def MAX_CONTENT_LENGTH( self ) -> int:
        """Don’t read more than this many bytes from the
        incoming request data. If not set and the request
        does not specify a CONTENT_LENGTH, no data will
        be read for security.
        """
        return self.__max_content_length

    @MAX_CONTENT_LENGTH.setter
    def MAX_CONTENT_LENGTH( self, value: int ):
        self.__max_content_length = value
        return

    @property
    def JSON_AS_ASCII( self ) -> bool:
        """Serialize objects to ASCII-encoded JSON. If this is
        disabled, the JSON will be returned as a Unicode
        string, or encoded as UTF-8 by jsonify. This has
        security implications when rendering the JSON in to
        JavaScript in templates, and should typically remain
        enabled.
        """
        return self.__json_as_ascii

    @JSON_AS_ASCII.setter
    def JSON_AS_ASCII( self, value: bool ):
        self.__json_as_ascii = value
        return

    @property
    def JSON_SORT_KEYS( self ) -> bool:
        """Sort the keys of JSON objects alphabetically.
        This is useful for caching because it ensures the
        data is serialized the same way no matter what
        Python’s hash seed is. While not recommended, you
        can disable this for a possible performance
        improvement at the cost of caching.
        """
        return self.__json_sort_keys

    @JSON_SORT_KEYS.setter
    def JSON_SORT_KEYS( self, value: bool ):
        self.__json_sort_keys = value
        return

    @property
    def JSONIFY_PRETTYPRINT_REGULAR( self ) -> bool:
        """jsonify responses will be output with newlines,
        spaces, and indentation for easier reading by
        humans. Always enabled in debug mode.
        """
        return self.__jsonify_prettyprint_regular

    @JSONIFY_PRETTYPRINT_REGULAR.setter
    def JSONIFY_PRETTYPRINT_REGULAR( self, value: bool ):
        self.__jsonify_prettyprint_regular = value
        return

    @property
    def JSONIFY_MIMETYPE( self ):
        """The mimetype of jsonify responses.
        """
        return self.__jsonify_mimetype

    @JSONIFY_MIMETYPE.setter
    def JSONIFY_MIMETYPE( self, value ):
        self.__jsonify_mimetype = value
        return

    @property
    def TEMPLATES_AUTO_RELOAD( self ) -> bool:
        """Reload templates when they are changed. If not set,
        it will be enabled in debug mode.
        """
        return self.__templates_auto_reload

    @TEMPLATES_AUTO_RELOAD.setter
    def TEMPLATES_AUTO_RELOAD( self, value: bool ):
        self.__templates_auto_reload = value
        return

    @property
    def EXPLAIN_TEMPLATE_LOADING( self ) -> bool:
        """Log debugging information tracing how a template file
        was loaded. This can be useful to figure out why a
        template was not loaded or the wrong file appears to
        be loaded.
        """
        return self.__explain_template_loading

    @EXPLAIN_TEMPLATE_LOADING.setter
    def EXPLAIN_TEMPLATE_LOADING( self, value: bool ):
        self.__explain_template_loading = value
        return

    @property
    def MAX_COOKIE_SIZE( self ) -> int:
        """Warn if cookie headers are larger than this many bytes.
        Defaults to 4093. Larger cookies may be silently
        ignored by browsers. Set to 0 to disable the warning.
        """
        return self.__max_cookie_size

    @MAX_COOKIE_SIZE.setter
    def MAX_COOKIE_SIZE( self, value: int ):
        self.__max_cookie_size = value
        return



class FlaskConfig( ConfigProcessor, FlaskConfigMixin ):
    def __init__( self, **kwargs ):
        ConfigProcessor.__init__( self, 'flask', **kwargs )
        FlaskConfigMixin.__init__( self, **kwargs )