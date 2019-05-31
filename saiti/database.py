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
from saiti import ConfigProcessor
from saiti.mixins.userpass import UserPassConfigMixin
from saiti.mixins.hostport import HostPortConfigMixin


class DatabaseConfig( ConfigProcessor,
                      UserPassConfigMixin,
                      HostPortConfigMixin ):
    """Database configuration class that handles: engine, database (name),
    username, password, hostname, hostport.

    """
    def __init__( self, **kwargs ):
        """Constructor to setup the database object with default values

        :param kwargs:  dict:   keywords for the ConfigProcessor class
        :return:
        """
        ConfigProcessor.__init__( self, 'database', **kwargs )
        UserPassConfigMixin.__init__( self, **kwargs )
        HostPortConfigMixin.__init__( self, **kwargs )
        self.__engines  = ( 'sqlite',
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
    def engine( self ) -> str:
        """The engine name to be used with the SQL database.
        """
        return self.__engine

    @engine.setter
    def engine( self, value: str ):
        if value in self.__engines:
            self.__engine = value
            return

        raise ValueError( "{} not a valid engine, expected one of {}".format( value, ", ".join( self.__engines ) ) )

    @property
    def database( self ) -> str:
        """The database name

        """
        return self.__database

    @database.setter
    def database( self, value: str ):
        self.__database = value
        return

    def getConnectString( self, library = 'sqlalchemy' ):
        """Returns a connect string to connect to the database.
        """
        if library == 'sqlalchemy':
            if self.engine == 'sqlite':
                return '{engine}:///{database}'.format( **self.props() )

            elif self.engine == 'oracle+cx_oracle' or self.engine == 'mssql+pyodbc://scott:tiger@mydsn':
                return '{engine}://{username}:{password}@{database}'.format( **self.props() )

            if type( self.username ) is str and self.username != '':
                return '{engine}://{username}:{password}@{host}:{port}/{database}'.format( **self.props() )

            return '{engine}://{host}:{port}/{database}'.format( **self.props() )

        raise AttributeError( '{} not yet supported'.format( library ) )
