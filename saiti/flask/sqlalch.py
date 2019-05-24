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
from saiti import ConfigProcessor

""" This is Work-In-Progress
"""

class SqlAlchemyConfigBinds( ConfigProcessor ):
    def __init__( self, **kwargs ):
        ConfigProcessor.__init__( self, 'SQLALCHEMY_BINDS', **kwargs )
        # wildcard object
        return


class SqlAlchemyConfigCompiledCache( ConfigProcessor ):
    def __init__( self, **kwargs ):
        ConfigProcessor.__init__( self, 'cache', **kwargs )
        self.__a = 0


class SqlAlchemyConfigSchemaTranslate( ConfigProcessor ):
    def __init__( self, **kwargs ):
        ConfigProcessor.__init__( self, 'schema', **kwargs )
        self.__a = 0


class SqlAlchemyConfigExecutionOptions( ConfigProcessor ):
    def __init__( self, **kwargs ):
        ConfigProcessor.__init__( self, 'execution', **kwargs )
        self.__autocommit              = False  # /True
        self.__compiled_cache          = SqlAlchemyConfigCompiledCache( **kwargs )
        self.__isolation_level         = ''
        self.__no_parameters           = False  # /True
        self.__stream_results          = False  # /True
        self.__schema_translate_map    = SqlAlchemyConfigSchemaTranslate( **kwargs )
        return

    @property
    def autocommit( self ) -> bool:
        return self.__autocommit

    @autocommit.setter
    def autocommit( self, value: bool ):
        self.__autocommit = value
        return

    @property
    def no_parameters( self ) -> bool:
        return self.__no_parameters

    @no_parameters.setter
    def no_parameters( self, value: bool ):
        self.__no_parameters = value
        return

    @property
    def stream_results( self ) -> bool:
        return self.__stream_results

    @stream_results.setter
    def stream_results( self, value: bool ):
        self.__stream_results = value
        return

    @property
    def isolation_level( self ) -> str:
        return self.__isolation_level

    @isolation_level.setter
    def isolation_level( self, value: str ):
        self.__isolation_level = value
        return

    @property
    def compiled_cache( self ) -> str:
        return self.__compiled_cache

    @property
    def schema_translate_map( self ) -> str:
        return self.__schema_translate_map


class SqlAlchemyConfigConnectArgs( ConfigProcessor ):
    def __init__( self, **kwargs ):
        ConfigProcessor.__init__( self, **kwargs )
        self.__host = ''
        self.__port = 0
        self.__user = ''
        self.__password = ''
        self.__database = ''
        return


class SqlAlchemyConfigEngineOptions( ConfigProcessor ):
    def __init__( self, **kwargs ):
        ConfigProcessor.__init__( self, 'options', **kwargs )
        self.__case_sensitive      = False  # /True
        self.__connect_args        = {}
        self.__convert_unicode     = True   # /False
        self.__echo                = False  # /True
        self.__echo_pool           = False  # /True
        self.__encoding            = 'utf-8'
        self.__execution_options   = SqlAlchemyConfigExecutionOptions( **kwargs )
        self.__implicit_returning  = True   # /False
        self.__isolation_level     = ''
        self.__label_length        = None
        self.__logging_name        = ''
        self.__max_overflow        = 10
        self.__paramstyle          = None
        self.__pool                = None
        self.__poolclass           = None
        self.__pool_logging_name   = ''
        self.__pool_pre_ping       = False  # /True
        self.__pool_size           = 5
        self.__pool_recycle        = -1
        self.__pool_reset_on_return= 'rollback'
        self.__pool_timeout        = 30
        self.__pool_use_lifo       = False  # /True
        self.__strategy            = 'plain'
        self.__executor            = None
        return

    @property
    def case_sensitive( self ) -> bool:
        return self.__case_sensitive

    @case_sensitive.setter
    def case_sensitive( self, value: bool ):
        self.__case_sensitive = value
        return

    @property
    def convert_unicode( self ) -> bool:
        return self.__convert_unicode

    @convert_unicode.setter
    def convert_unicode( self, value: bool ):
        self.__convert_unicode = value
        return

    @property
    def echo( self ) -> bool:
        return self.__echo

    @echo.setter
    def echo( self, value: bool ):
        self.__echo = value
        return

    @property
    def echo_pool( self ) -> bool:
        return self.__echo_pool

    @echo_pool.setter
    def echo_pool( self, value: bool ):
        self.__echo_pool = value
        return

    @property
    def implicit_returning( self ) -> bool:
        return self.__implicit_returning

    @implicit_returning.setter
    def implicit_returning( self, value: bool ):
        self.__implicit_returning = value
        return

    @property
    def pool_pre_ping( self ) -> bool:
        return self.__pool_pre_ping

    @pool_pre_ping.setter
    def pool_pre_ping( self, value: bool ):
        self.__pool_pre_ping = value
        return

    @property
    def pool_use_lifo( self ) -> bool:
        return self.__pool_use_lifo

    @pool_use_lifo.setter
    def pool_use_lifo( self, value: bool ):
        self.__pool_use_lifo = value
        return

    @property
    def encoding( self ) -> str:
        return self.__encoding

    @encoding.setter
    def encoding( self, value: str ):
        self.__encoding = value
        return

    @property
    def isolation_level( self ) -> str:
        return self.__isolation_level

    @isolation_level.setter
    def isolation_level( self, value: str ):
        self.__isolation_level = value
        return

    @property
    def logging_name( self ) -> str:
        return self.__logging_name

    @logging_name.setter
    def logging_name( self, value: str ):
        self.__logging_name = value
        return

    @property
    def pool_logging_name( self ) -> str:
        return self.__pool_logging_name

    @pool_logging_name.setter
    def pool_logging_name( self, value: str ):
        self.__pool_logging_name = value
        return

    @property
    def strategy( self ) -> str:
        return self.__strategy

    @strategy.setter
    def strategy( self, value: str ):
        self.__strategy = value
        return

    @property
    def label_length( self ) -> str:
        return self.__label_length

    @label_length.setter
    def label_length( self, value: str ):
        self.__label_length = value
        return

    @property
    def max_overflow( self ) -> str:
        return self.__max_overflow

    @max_overflow.setter
    def max_overflow( self, value: str ):
        self.__max_overflow = value
        return

    @property
    def pool_size( self ) -> str:
        return self.__pool_size

    @pool_size.setter
    def pool_size( self, value: str ):
        self.__pool_size = value
        return

    @property
    def pool_recycle( self ) -> str:
        return self.__pool_recycle

    @pool_recycle.setter
    def pool_recycle( self, value: str ):
        self.__pool_recycle = value
        return

    @property
    def pool_timeout( self ) -> str:
        return self.__pool_timeout

    @pool_timeout.setter
    def pool_timeout( self, value: str ):
        self.__pool_timeout = value
        return

    @property
    def paramstyle( self ) -> str:
        return self.__paramstyle

    @paramstyle.setter
    def paramstyle( self, value: str ):
        self.__paramstyle = value
        return

    @property
    def pool( self ) -> str:
        return self.__pool

    @pool.setter
    def pool( self, value: str ):
        self.__pool = value
        return

    @property
    def poolclass( self ) -> str:
        return self.__poolclass

    @poolclass.setter
    def poolclass( self, value: str ):
        self.__poolclass = value
        return

    @property
    def executor( self ) -> str:
        return self.__executor

    @executor.setter
    def executor( self, value: str ):
        self.__executor = value
        return

    @property
    def connect_args( self ) -> str:
        return self.__connect_args



class FlaskSqlAlchemyConfigMixin( object ):
    def __init__( self, **kwargs ):
        self.__sqlalchemy_database_uri          = ''
        self.__sqlalchemy_binds                 = SqlAlchemyConfigBinds( **kwargs )
        self.__sqlalchemy_echo                  = False
        self.__sqlalchemy_record_queries        = False
        self.__sqlalchemy_track_modifications   = None
        self.__sqlalchemy_engine_options        = SqlAlchemyConfigEngineOptions( **kwargs )
        if 'database_settings' in kwargs:
            self.__database_settings    = kwargs[ 'database_settings' ]

        else:
            self.__database_settings    = None

        return

    @property
    def SQLALCHEMY_DATABASE_URI( self ) -> str:
        if self.__database_settings is not None:
            return self.__database_settings.getConnectString( 'sqlalchemy' )

        return self.__sqlalchemy_database_uri

    @SQLALCHEMY_DATABASE_URI.setter
    def SQLALCHEMY_DATABASE_URI( self, value: str ):
        self.__sqlalchemy_database_uri = value
        return

    @property
    def SQLALCHEMY_BINDS( self ):
        return self.__sqlalchemy_binds

    @property
    def SQLALCHEMY_ECHO( self ) -> bool:
        return self.__sqlalchemy_echo

    @SQLALCHEMY_ECHO.setter
    def SQLALCHEMY_ECHO( self, value: bool ):
        self.__sqlalchemy_echo = value

    @property
    def SQLALCHEMY_RECORD_QUERIES( self ) -> bool:
        return self.__sqlalchemy_record_queries

    @SQLALCHEMY_RECORD_QUERIES.setter
    def SQLALCHEMY_RECORD_QUERIES( self, value: bool ):
        self.__sqlalchemy_record_queries = value
        return

    @property
    def SQLALCHEMY_TRACK_MODIFICATIONS( self ):
        return self.__sqlalchemy_track_modifications

    @property
    def SQLALCHEMY_ENGINE_OPTIONS( self ):
        return self.__sqlalchemy_engine_options

