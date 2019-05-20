import socket
from saiti import (YamlConfigFile,
                   ConfigProcessor,
                   PathList,
                   DatabaseConfig,
                   WebHostConfig,
                   LoggingConfig)



class PathsConfig( ConfigProcessor ):
    """

        library_paths
        keyword_paths
        resource_paths

    """
    def __init__( self, **kwargs ):
        ConfigProcessor.__init__( self, 'paths', **kwargs )
        self.__library_paths    = PathList( must_exists = False )
        self.__keyword_paths    = PathList( must_exists = False )
        self.__resource_paths   = PathList( must_exists = False )
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
    def __init__( self, name = 'common', **kwargs ):
        ConfigProcessor.__init__( self, name, **kwargs )
        self.__paths        = PathsConfig( must_exists = False, **kwargs )
        self.__debug        = False # default
        self.__poll         = False # default
        self.__web          = WebHostConfig( **kwargs )
        self.__database     = DatabaseConfig( **kwargs )
        self.__logging      = LoggingConfig( **kwargs )
        return

    @property
    def paths( self ) -> PathsConfig:
        return self.__paths

    @property
    def database( self ) -> DatabaseConfig:
        return self.__database

    @property
    def web( self ) -> WebHostConfig:
        return self.__web

    @property
    def debug( self ) -> bool:
        return self.__debug

    @debug.setter
    def debug( self, value: bool ):
        self.__debug = value
        return

    @property
    def poll( self ) -> bool:
        return self.__poll

    @poll.setter
    def poll( self, value: bool ):
        self.__poll = value
        return


class CustonConfigFile( YamlConfigFile ):
    def __init__( self, filename: str, **kwargs ):
        YamlConfigFile.__init__( self, filename, loadLater = True, **kwargs )
        self.__common = CustomConfig( **kwargs )
        self.setWildcardObject( CustomConfig, **kwargs )
        self.Load()
        return

    @property
    def common( self ) -> CustomConfig:
        return self.__common


if __name__ == '__main__':
    cfg = CustonConfigFile( './example.conf' )
    cfg.dump()





