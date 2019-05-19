import socket
from saiti import (ConfigFile,
                   ConfigProcessor,
                   PathList,
                   LoggingConfig)

class WebHostConfig( ConfigProcessor ):
    """
        interface:      <str>   default localhost
        port:           <int>   default 7070
    """
    def __init__( self, **kwargs ):
        ConfigProcessor.__init__( self, 'web', **kwargs )
        self.__interface    = 'localhost'
        self.__port         = 7070
        return

    @property
    def interface( self ) -> str:
        return self.__interface

    @interface.setter
    def interface( self, value: str ):
        try:
            if value not in ( '0.0.0.0' ):
                result = socket.getaddrinfo( value,
                                             self.__port,
                                             proto = socket.IPPROTO_TCP )

            self.__interface = value

        except Exception as exc:
            raise ValueError( "interface must be an valid IP address or hostname: {}".format( value ) )

        return

    @property
    def port( self ) -> int:
        return self.__port

    @port.setter
    def port( self, value: int ):
        if type( value ) is int:
            self.__port = value
            return

        raise ValueError( "port must be an integer" )


class PathsConfig( ConfigProcessor ):
    """

        library_paths
        keyword_paths
        resource_paths

    """
    def __init__( self, **kwargs ):
        ConfigProcessor.__init__( self, 'paths', **kwargs )
        self.__library_paths    = PathList()
        self.__keyword_paths    = PathList()
        self.__resource_paths   = PathList()
        return

    @property
    def library_paths( self ) -> PathList:
        return self.__library_paths

    @property
    def keyword_paths( self ) -> PathList:
        return self.__keyword_paths

    @property
    def resource_paths( self ) -> PathList:
        return self.__resource_paths


class CustomConfig( ConfigProcessor ):
   def __init__( self, **kwargs ):
       ConfigProcessor.__init__( self, 'common', **kwargs )
       self.__paths     = PathsConfig( **kwargs )
       self.__debug     = False # default
       self.__web       = WebHostConfig( **kwargs )
       self.__logging   = LoggingConfig( **kwargs )
       return

   @property
   def paths( self ) -> PathsConfig:
       return self.__paths

   @property
   def debug( self ) -> bool:
       return self.__debug

   @debug.setter
   def debug( self, value: bool ):
       self.__debug = value
       return


class CustonConfigFile( ConfigFile ):
    def __init__( self, filename: str, **kwargs ):
        ConfigFile.__init__( self, filename, **kwargs )
        self.__common = CustomConfig( **kwargs )
        self.getWildcardObject( CustomConfig, **kwargs )

    @property
    def common( self ) -> CustomConfig:
        return self.__common
