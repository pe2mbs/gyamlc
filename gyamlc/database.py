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
import os
from gyamlc import ConfigProcessor
from gyamlc.mixins.userpass import UserPassConfigMixin
from gyamlc.mixins.hostport import HostPortConfigMixin


class DatabaseConfig( ConfigProcessor,
                      UserPassConfigMixin,
                      HostPortConfigMixin ):
    """
        engine:     <str>
        database:   <str>
        hostname:   <str>   optional
        port:       <int>   optional
        username:   <str>   optional
        password:   <str>   optional
    """
    def __init__( self, **kwargs ):
        ConfigProcessor.__init__( self, 'database', **kwargs )
        UserPassConfigMixin.__init__( self, **kwargs )
        HostPortConfigMixin.__init__( self, **kwargs )
        self.__engines  = ( 'sqlite3',
                            'postgresql',
                            'postgresql+pg8000',
                            'postgresql+psycopg2',
                            'mysql',
                            'mysql+mysqldb',
                            'mysql+pymysql',
                            'oracle',
                            'oracle+cx_oracle',
                            'mssql+pyodbc',
                            'mssql+pymssql' )
        self.__engine   = ''
        self.__database = ''
        return

    @property
    def engine( self ):
        return self.__engine

    @engine.setter
    def engine( self, value ):
        if value in self.__engines:
            self.__engine = value
            return

        raise ValueError( "{} not a valid engine, expected one of {}".format( value, ", ".join( self.__engines ) ) )

    @property
    def database( self ):
        return self.__database

    @database.setter
    def database( self, value ):
        if os.path.isfile( value ) or os.path.isdir( os.path.split( value )[ 0 ] ):
            self.__database = value
            return

        raise ValueError( "database doesn't contain a valid path" )


