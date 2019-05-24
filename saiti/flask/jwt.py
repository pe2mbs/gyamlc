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
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA  02110-1301, USA.
#
import datetime
import dateutil.relativedelta

MUST_START_WITH_SLASH = "{} must start with '/'"


class FlaskJwtGeneralOptions( object ):
    __ALGORITHMS    = [ 'HS256', 'HS384', 'HS512', 'ES256', 'ES384', 'ES512',
                        'RS256', 'RS384', 'RS512', 'PS256', 'PS384', 'PS512' ]
    __TOKENS        = [ 'headers', 'cookies', 'query_string', 'json' ]

    def __init__( self ):
        self.__jwt_token_location           = 'headers'
        self.__jwt_access_token_expires     = 0
        self.__jwt_refresh_token_expires    = 0
        self.__jwt_algorithm                = 'HS256'
        self.__jwt_secret_key               = ''
        self.__jwt_public_key               = ''
        self.__jwt_private_key              = ''
        self.__jwt_identity_claim           = 'identity'
        self.__jwt_user_claims              = 'user_claims'
        self.__jwt_claims_in_refresh_token  = False
        self.__jwt_error_message_key        = 'msg'
        self.__jwt_decode_audience          = None
        self.__jwt_decode_leeway            = 0
        return

    #: N802
    @property
    def JWT_TOKEN_LOCATION( self ) -> list:
        """Where to look for a JWT when processing a request. The options are
        'headers', 'cookies', 'query_string', or 'json'. You can pass in a
        sequence or a set to check more then one location, such as: ('headers',
        'cookies'). Defaults to ['headers']
        """
        return self.__jwt_token_location

    @JWT_TOKEN_LOCATION.setter
    def JWT_TOKEN_LOCATION( self, value: list ):
        if all( x in self.__TOKENS for x in value ):
                self.__jwt_token_location = value
                return

        raise ValueError( "JWT_TOKEN_LOCATION may contain {}".format( ", ".join( self.__TOKENS ) ) )

    @property
    def JWT_ACCESS_TOKEN_EXPIRES( self ):
        """How long an access token should live before it expires. This takes
        any value that can be safely added to a datetime.datetime object,
        including datetime.timedelta, dateutil.relativedelta, or an int
        (seconds), and defaults to 15 minutes. Can be set to False to
        disable expiration."""
        return self.__jwt_access_token_expires

    @JWT_ACCESS_TOKEN_EXPIRES.setter
    def JWT_ACCESS_TOKEN_EXPIRES( self, value ):
        if type( value ) in int:
            self.__jwt_access_token_expires = datetime.timedelta( minutes = value )

        elif isinstance( value, datetime.timedelta ):
            self.__jwt_refresh_token_expires = value
            return

        elif isinstance( value, dateutil.relativedelta ):
            self.__jwt_refresh_token_expires = value
            return

        raise ValueError( 'JWT_ACCESS_TOKEN_EXPIRES must be int, timedelta or relativedelta' )

    @property
    def JWT_REFRESH_TOKEN_EXPIRES( self ) -> datetime.timedelta:
        """How long a refresh token should live before it expires. This takes
        any value that can be safely added to a datetime.datetime object,
        including datetime.timedelta, dateutil.relativedelta, or an int
        (seconds), and defaults to 30 days. Can be set to False to disable
        expiration.
        """
        return self.__jwt_refresh_token_expires

    @JWT_REFRESH_TOKEN_EXPIRES.setter
    def JWT_REFRESH_TOKEN_EXPIRES( self, value ):
        if type( value ) in int:
            self.__jwt_refresh_token_expires = datetime.timedelta( days = value )
            return

        elif isinstance( value, datetime.timedelta ):
            self.__jwt_refresh_token_expires = value
            return

        elif isinstance( value, dateutil.relativedelta ):
            self.__jwt_refresh_token_expires = value
            return

        raise ValueError( 'JWT_REFRESH_TOKEN_EXPIRES must be int, timedelta or relativedelta' )

    @property
    def JWT_ALGORITHM( self ) -> str:
        """Which algorithm to sign the JWT with. See here for the options.
        Defaults to 'HS256'.
        """
        return self.__jwt_algorithm

    @JWT_ALGORITHM.setter
    def JWT_ALGORITHM( self, value: str ):
        if value in self.__ALGORITHMS:
            self.__jwt_algorithm    = value
            return

        raise ValueError( 'JWT_ALGORITHM must be one of {}'.format( ', '.join( self.__ALGORITHMS ) ) )

    @property
    def JWT_SECRET_KEY( self ) -> str:
        """The secret key needed for symmetric based signing algorithms,
        such as HS*. If this is not set, we use the flask SECRET_KEY value
        instead.
        """
        return self.__jwt_secret_key

    @JWT_SECRET_KEY.setter
    def JWT_SECRET_KEY( self, value: str ):
        self.__jwt_secret_key   = value

    @property
    def JWT_PUBLIC_KEY( self ) -> str:
        """The public key needed for asymmetric based signing algorithms,
        such as RS* or ES*. PEM format expected.
        """
        return self.__jwt_public_key

    @JWT_PUBLIC_KEY.setter
    def JWT_PUBLIC_KEY( self, value: str ):
        self.__jwt_public_key = value
        return

    @property
    def JWT_PRIVATE_KEY( self ) -> str:
        """The private key needed for asymmetric based signing algorithms,
        such as RS* or ES*. PEM format expected.
        """
        return self.__jwt_private_key

    @JWT_PRIVATE_KEY.setter
    def JWT_PRIVATE_KEY( self, value: str ):
        self.__jwt_private_key = value
        return

    @property
    def JWT_IDENTITY_CLAIM( self ) -> str:
        """Claim in the tokens that is used as source of identity. For
        interoperability, the JWT RFC recommends using 'sub'. Defaults
        to 'identity' for legacy reasons.
        """
        return self.__jwt_identity_claim

    @JWT_IDENTITY_CLAIM.setter
    def JWT_IDENTITY_CLAIM( self, value: str ):
        self.__jwt_identity_claim = value
        return

    @property
    def JWT_USER_CLAIMS( self ) -> str:
        """Claim in the tokens that is used to store user claims.
        Defaults to 'user_claims'.
        """
        return self.__jwt_user_claims

    @JWT_USER_CLAIMS.setter
    def JWT_USER_CLAIMS( self, value: str ):
        self.__jwt_user_claims = value
        return

    @property
    def JWT_CLAIMS_IN_REFRESH_TOKEN( self ) -> bool:
        """If user claims should be included in refresh tokens.
        Defaults to False.
        """
        return self.__jwt_claims_in_refresh_token

    @JWT_CLAIMS_IN_REFRESH_TOKEN.setter
    def JWT_CLAIMS_IN_REFRESH_TOKEN( self, value: bool ):
        self.__jwt_claims_in_refresh_token = value
        return

    @property
    def JWT_ERROR_MESSAGE_KEY( self ) -> str:
        """The key of the error message in a JSON error response when
        using the default error handlers. Defaults to 'msg'.
        """
        return self.__jwt_error_message_key

    @JWT_ERROR_MESSAGE_KEY.setter
    def JWT_ERROR_MESSAGE_KEY( self, value: str ):
        self.__jwt_error_message_key    = value
        return

    @property
    def JWT_DECODE_AUDIENCE( self ):
        """The audience or list of audiences you expect in a JWT
        when decoding it. The 'invalid_token_callback' is invoked
        when a JWTs audience is invalid. Defaults to 'None'.
        """
        return self.__jwt_decode_audience

    @JWT_DECODE_AUDIENCE.setter
    def JWT_DECODE_AUDIENCE( self, value ):
        self.__jwt_decode_audience = value
        return

    @property
    def JWT_DECODE_LEEWAY( self ) -> int:
        """Define the leeway part of the expiration time definition,
        which means you can validate an expiration time which is in
        the past but not very far. This leeway is used for nbf
        (“not before”) and exp (“expiration time”). Defaults to 0
        """
        return self.__jwt_decode_leeway

    @JWT_DECODE_LEEWAY.setter
    def JWT_DECODE_LEEWAY( self, value: int ):
        self.__jwt_decode_leeway = value
        return


class FlaskJwtHeaderOptions( object ):
    def __init__( self ):
        self.__jwt_header_type              = 'Bearer'
        self.__jwt_header_name              = 'Authorization'
        return

    @property
    def JWT_HEADER_NAME( self ) -> str:
        """What header to look for the JWT in a request. Defaults to 'Authorization'
        """
        return self.__jwt_header_name

    @JWT_HEADER_NAME.setter
    def JWT_HEADER_NAME( self, value: str ):
        self.__jwt_header_name  = value
        return

    @property
    def JWT_HEADER_TYPE( self ):
        """What type of header the JWT is in. Defaults to 'Bearer'. This can be an
        empty string, in which case the header contains only the JWT (insead of
        something like HeaderName: Bearer <JWT>)
        """
        return self.__jwt_header_type

    @JWT_HEADER_TYPE.setter
    def JWT_HEADER_TYPE( self, value ):
        self.__jwt_header_type  = value
        return


class FlaskJwtQueryStringOptions( object ):
    def __init__( self ):
        self.__jwt_query_string_name        = 'jwt'
        return

    @property
    def JWT_QUERY_STRING_NAME( self ) -> str:
        """What query paramater name to look for a JWT in a request. Defaults to 'jwt'
        """
        return self.__jwt_query_string_name

    @JWT_QUERY_STRING_NAME.setter
    def JWT_QUERY_STRING_NAME( self, value: str ):
        self.__jwt_query_string_name = value
        return


class FlaskJwtCookieOptions( object ):
    def __init__( self ):
        self.__jwt_access_cookie_name       = 'access_token_cookie'
        self.__jwt_refresh_cookie_name      = 'refresh_token_cookie'
        self.__jwt_access_cookie_path       = '/'
        self.__jwt_refresh_cookie_path      = '/'
        self.__jwt_cookie_secure            = False
        self.__jwt_cookie_domain            = None
        self.__jwt_session_cookie           = True
        self.__jwt_cookie_samesite          = None
        self.__jwt_cookie_csrf_protect      = True
        return

    @property
    def JWT_ACCESS_COOKIE_NAME( self ) -> str:
        """The name of the cookie that holds the access token. Defaults to
        access_token_cookie
        """
        return self.__jwt_access_cookie_name

    @JWT_ACCESS_COOKIE_NAME.setter
    def JWT_ACCESS_COOKIE_NAME( self, value: str ):
        self.__jwt_access_cookie_name = value
        return

    @property
    def JWT_REFRESH_COOKIE_NAME( self ) -> str:
        """The name of the cookie that holds the refresh token. Defaults to
        refresh_token_cookie
        """
        return self.__jwt_refresh_cookie_name

    @JWT_REFRESH_COOKIE_NAME.setter
    def JWT_REFRESH_COOKIE_NAME( self, value: str ):
        self.__jwt_refresh_cookie_name = value
        return

    @property
    def JWT_ACCESS_COOKIE_PATH( self ):
        """What path should be set for the access cookie. Defaults to '/',
        which will cause this access cookie to be sent in with every request.
        Should be modified for only the paths that need the access cookie
        """
        return self.__jwt_access_cookie_path

    @JWT_ACCESS_COOKIE_PATH.setter
    def JWT_ACCESS_COOKIE_PATH( self, value ):
        if value.startswith( '/' ):
            self.__jwt_access_cookie_path = value
            return

        raise ValueError( MUST_START_WITH_SLASH.format( 'JWT_ACCESS_COOKIE_PATH' ) )

    @property
    def JWT_REFRESH_COOKIE_PATH( self ) -> str:
        """What path should be set for the refresh cookie. Defaults to '/',
        which will cause this refresh cookie to be sent in with every request.
        Should be modified for only the paths that need the refresh cookie
        """
        return self.__jwt_refresh_cookie_path

    @JWT_REFRESH_COOKIE_PATH.setter
    def JWT_REFRESH_COOKIE_PATH( self, value: str ):
        if value.startswith( '/' ):
            self.__jwt_refresh_cookie_path = value
            return

        raise ValueError( MUST_START_WITH_SLASH.format( 'JWT_REFRESH_COOKIE_PATH' ) )

    @property
    def JWT_COOKIE_SECURE( self ) -> bool:
        """If the secure flag should be set on your JWT cookies. This will
        only allow the cookies to be sent over https. Defaults to False,
        but in production this should likely be set to True.
        """
        return self.__jwt_cookie_secure

    @JWT_COOKIE_SECURE.setter
    def JWT_COOKIE_SECURE( self, value: bool ):
        self.__jwt_cookie_secure = value
        return

    @property
    def JWT_COOKIE_DOMAIN( self ):
        """Value to use for cross domain cookies. Defaults to None which sets
        this cookie to only be readable by the domain that set it.
        """
        return self.__jwt_cookie_domain

    @JWT_COOKIE_DOMAIN.setter
    def JWT_COOKIE_DOMAIN( self, value ):
        self.__jwt_cookie_domain = value
        return

    @property
    def JWT_SESSION_COOKIE( self ) -> bool:
        """If the cookies should be session cookies (deleted when the browser
        is closed) or persistent cookies (never expire). Defaults to True
        (session cookies).
        """
        return self.__jwt_session_cookie

    @JWT_SESSION_COOKIE.setter
    def JWT_SESSION_COOKIE( self, value: bool ):
        self.__jwt_session_cookie = value
        return

    @property
    def JWT_COOKIE_SAMESITE( self ):
        """If the cookies should be sent in a cross-site browsing context.
        Defaults to None, which means cookies are always sent.
        """
        return self.__jwt_cookie_samesite

    @JWT_COOKIE_SAMESITE.setter
    def JWT_COOKIE_SAMESITE( self, value ):
        self.__jwt_cookie_samesite = value
        return

    @property
    def JWT_COOKIE_CSRF_PROTECT( self ) -> bool:
        """Enable/disable CSRF protection when using cookies. Defaults to
        True.
        """
        return self.__jwt_cookie_csrf_protect

    @JWT_COOKIE_CSRF_PROTECT.setter
    def JWT_COOKIE_CSRF_PROTECT( self, value: bool ):
        self.__jwt_cookie_csrf_protect = value
        return


class FlaskJwtJsonBodyOptions( object ):
    def __init__( self ):
        self.__jwt_json_key         = 'access_token'
        self.__jwt_refresh_json_key = 'refresh_token'
        return

    @property
    def JWT_JSON_KEY( self ) -> str:
        """Key to look for in the body of an application/json request.
        Defaults to 'access_token'
        """
        return self.__jwt_json_key

    @JWT_JSON_KEY.setter
    def JWT_JSON_KEY( self, value: str ):
        self.__jwt_json_key = value
        return

    @property
    def JWT_REFRESH_JSON_KEY( self ) -> str:
        """Key to look for the refresh token in an application/json
        request. Defaults to 'refresh_token'
        """
        return self.__jwt_refresh_json_key

    @JWT_REFRESH_JSON_KEY.setter
    def JWT_REFRESH_JSON_KEY( self, value: str ):
        self.__jwt_refresh_json_key = value
        return


class FlaskJwtCrossSiteRequestForgeryOptions( object ):
    __CSRF_METHODS = [ 'POST', 'PUT', 'PATCH', 'DELETE', 'GET' ]

    def __init__( self ):
        self.__jwt_csrf_methods             = [ 'POST', 'PUT', 'PATCH', 'DELETE' ]
        self.__jwt_access_csrf_header_name  = 'X-CSRF-TOKEN'
        self.__jwt_refresh_csrf_header_name = 'X-CSRF-TOKEN'
        self.__jwt_csrf_in_cookies          = False
        self.__jwt_access_csrf_cookie_name  = 'csrf_access_token'
        self.__jwt_refresh_csrf_cookie_name = 'csrf_refresh_token'
        self.__jwt_access_csrf_cookie_path  = '/'
        self.__jwt_refresh_csrf_cookie_path = '/'
        return

    @property
    def JWT_CSRF_METHODS( self ):
        """The request types that will use CSRF protection.
        Defaults to ['POST', 'PUT', 'PATCH', 'DELETE']
        """
        return self.__jwt_csrf_methods

    @JWT_CSRF_METHODS.setter
    def JWT_CSRF_METHODS( self, value ):
        if type( value ) in ( list, tuple ):
            if all( x in self.__CSRF_METHODS for x in value ):
                self.__jwt_csrf_methods = value
                return

        raise ValueError( "JWT_CSRF_METHODS may contain {}".format( ", ".join( self.__CSRF_METHODS ) ) )

    @property
    def JWT_ACCESS_CSRF_HEADER_NAME( self ) -> str:
        """Name of the header that should contain the CSRF
        double submit value for access tokens. Defaults
        to X-CSRF-TOKEN.
        """
        return self.__jwt_access_csrf_header_name

    @JWT_ACCESS_CSRF_HEADER_NAME.setter
    def JWT_ACCESS_CSRF_HEADER_NAME( self, value: str ):
        self.__jwt_access_csrf_header_name = value

    @property
    def JWT_REFRESH_CSRF_HEADER_NAME( self ) -> str:
        """Name of the header that should contains the CSRF
        double submit value for refresh tokens. Defaults to
        X-CSRF-TOKEN.
        """
        return self.__jwt_refresh_csrf_header_name

    @JWT_REFRESH_CSRF_HEADER_NAME.setter
    def JWT_REFRESH_CSRF_HEADER_NAME( self, value: str ):
        self.__jwt_refresh_csrf_header_name = value
        return

    @property
    def JWT_CSRF_IN_COOKIES( self ) -> str:
        """If we should store the CSRF double submit value
        in another cookies when using set_access_cookies()
        and set_refresh_cookies(). Defaults to True.
        If this is False, you are responsible for getting
        the CSRF value to the callers
        (see: get_csrf_token(encoded_token)).
        """
        return self.__jwt_csrf_in_cookies

    @JWT_CSRF_IN_COOKIES.setter
    def JWT_CSRF_IN_COOKIES( self, value: str ):
        self.__jwt_csrf_in_cookies = value
        return

    @property
    def JWT_ACCESS_CSRF_COOKIE_NAME( self ) -> str:
        """Name of the CSRF access cookie. Defaults to
        'csrf_access_token'. Only applicable if
        JWT_CSRF_IN_COOKIES is True
        """
        return self.__jwt_access_csrf_cookie_name

    @JWT_ACCESS_CSRF_COOKIE_NAME.setter
    def JWT_ACCESS_CSRF_COOKIE_NAME( self, value: str ):
        self.__jwt_access_csrf_cookie_name = value
        return

    @property
    def JWT_REFRESH_CSRF_COOKIE_NAME( self ) -> str:
        """Name of the CSRF refresh cookie. Defaults to
        'csrf_refresh_token'. Only applicable if
        JWT_CSRF_IN_COOKIES is True
        """
        return self.__jwt_refresh_csrf_cookie_name

    @JWT_REFRESH_CSRF_COOKIE_NAME.setter
    def JWT_REFRESH_CSRF_COOKIE_NAME( self, value: str ):
        self.__jwt_refresh_csrf_cookie_name = value
        return

    @property
    def JWT_ACCESS_CSRF_COOKIE_PATH( self ) -> str:
        """Path for the CSRF access cookie. Defaults to '/'.
        Only applicable if JWT_CSRF_IN_COOKIES is True
        """
        return self.__jwt_access_csrf_cookie_path

    @JWT_ACCESS_CSRF_COOKIE_PATH.setter
    def JWT_ACCESS_CSRF_COOKIE_PATH( self, value: str ):
        if value.startswith( '/' ):
            self.__jwt_access_csrf_cookie_path = value
            return

        raise ValueError( MUST_START_WITH_SLASH.format( 'JWT_ACCESS_CSRF_COOKIE_PATH' ) )

    @property
    def JWT_REFRESH_CSRF_COOKIE_PATH( self ) -> str:
        """Path of the CSRF refresh cookie. Defaults to '/'.
        Only applicable if JWT_CSRF_IN_COOKIES is True
        """
        return self.__jwt_refresh_csrf_cookie_path

    @JWT_REFRESH_CSRF_COOKIE_PATH.setter
    def JWT_REFRESH_CSRF_COOKIE_PATH( self, value: str ):
        if value.startswith( '/' ):
            self.__jwt_refresh_csrf_cookie_path = value
            return

        raise ValueError( MUST_START_WITH_SLASH.format( 'JWT_REFRESH_CSRF_COOKIE_PATH' ) )


class FlaskJwtBlacklistOptions( object ):
    __BLACKLIST_OPTIONS = [ 'access', 'refresh' ]

    def __init__( self ):
        self.__jwt_blacklist_enabled        = False
        self.__jwt_blacklist_token_checks   = [ 'access', 'refresh' ]
        return

    @property
    def JWT_BLACKLIST_ENABLED( self ) -> bool:
        """Enable/disable token revoking. Defaults to False
        """
        return self.__jwt_blacklist_enabled

    @JWT_BLACKLIST_ENABLED.setter
    def JWT_BLACKLIST_ENABLED( self, value: bool ):
        self.__jwt_blacklist_enabled = value
        return

    @property
    def JWT_BLACKLIST_TOKEN_CHECKS( self ) -> list:
        """What token types to check against the blacklist.
        The options are 'refresh' or 'access'. You can pass
        in a sequence or a set to check more then one type.
        Defaults to ('access', 'refresh'). Only used if
        blacklisting is enabled.
        """
        return self.__jwt_blacklist_token_checks

    @JWT_BLACKLIST_TOKEN_CHECKS.setter
    def JWT_BLACKLIST_TOKEN_CHECKS( self, value ):
        if type( value ) is str:
            if ',' in value:
                value = value.split()
                value = [ x.strip() for x in value ]

            elif value in self.__BLACKLIST_OPTIONS:
                self.__jwt_blacklist_token_checks = [ value ]
                return

        if type( value ) in ( list, tuple ):
            if all( x in self.__BLACKLIST_OPTIONS for x in value ):
                self.__jwt_blacklist_token_checks = value
                return

        raise ValueError( "JWT_BLACKLIST_TOKEN_CHECKS may contain {}".format( ", ".join( self.__BLACKLIST_OPTIONS ) ) )


class FlaskJwtConfigMixin( FlaskJwtGeneralOptions, FlaskJwtHeaderOptions,
                           FlaskJwtQueryStringOptions, FlaskJwtCookieOptions,
                           FlaskJwtJsonBodyOptions, FlaskJwtBlacklistOptions,
                           FlaskJwtCrossSiteRequestForgeryOptions ):
    def __init__( self ):
        FlaskJwtGeneralOptions.__init__( self )
        FlaskJwtHeaderOptions.__init__( self )
        FlaskJwtQueryStringOptions.__init__( self )
        FlaskJwtCookieOptions.__init__( self )
        FlaskJwtJsonBodyOptions.__init__( self )
        FlaskJwtCrossSiteRequestForgeryOptions.__init__( self )
        FlaskJwtBlacklistOptions.__init__( self )
        return
