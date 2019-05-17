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
import importlib
from gyamlc import ConfigProcessor
import flask_apscheduler.auth

class FlaskSchedulerJob( ConfigProcessor ):
    """
        id:         <str>
        func        <str>   FORMAT <MODULE>:<FUNCTION>
        args:       <list>
        trigger:    <str>   default 'interval'
        seconds:    <int>
    """
    def __init__( self, **kwargs ):
        ConfigProcessor.__init__( self, 'job', **kwargs )
        return


class FlaskSchedulerJobStores( ConfigProcessor ):
    """
        default:    'string'    = SQLAlchemyJobStore(url='sqlite://')
    """
    def __init__( self, **kwargs ):
        ConfigProcessor.__init__( self, '*', **kwargs )
        return



class FlaskSchedulerExecutor( ConfigProcessor ):
    """
        type:           <str>       default "threadpool"
        max_workers:    <int>       default 20
    """
    def __init__( self, **kwargs ):
        ConfigProcessor.__init__( self, '*', **kwargs )
        return


class FlaskSchedulerExecutors( ConfigProcessor ):
    """
        default:        <FlaskSchedulerExecutor>
    """
    def __init__( self, **kwargs ):
        ConfigProcessor.__init__( self, 'SCHEDULER_EXECUTORS', **kwargs )
        return


class FlaskSchedulerJobDefaults( ConfigProcessor ):
    """
        coalesce:       <bool>  default False
        max_instances   <int>   default 3
    """
    def __init__( self ):
        ConfigProcessor.__init__( self, 'SCHEDULER_JOB_DEFAULTS' )
        return


class FlaskSchedulerConfigMixin( object ):
    """
        SCHEDULER_API_ENABLED: true
        SCHEDULER_API_PREFIX: /scheduler
        SCHEDULER_AUTH: flask_apscheduler.auth.HTTPBasicAuth()
        SCHEDULER_JOBSTORES
        SCHEDULER_EXECUTORS
        SCHEDULER_JOB_DEFAULTS
    """
    def __init__( self, **kwargs ):
        self.__SCHEDULER_API_ENABLED    =  False
        self.__SCHEDULER_API_PREFIX     = '/scheduler'
        self.__SCHEDULER_AUTH           = flask_apscheduler.auth.HTTPBasicAuth()
        self.__SCHEDULER_JOBSTORES      = FlaskSchedulerJobStores()
        self.__SCHEDULER_EXECUTORS      = FlaskSchedulerExecutors()
        self.__SCHEDULER_JOB_DEFAULTS   = FlaskSchedulerJobDefaults()
        self.__JOBS = []
        return

    @property
    def SCHEDULER_API_ENABLED( self ):
        return self.__SCHEDULER_API_ENABLED

    @SCHEDULER_API_ENABLED.setter
    def SCHEDULER_API_ENABLED( self, value ):
        self.__SCHEDULER_API_ENABLED = value
        return

    @property
    def SCHEDULER_API_PREFIX( self ):
        return self.__SCHEDULER_API_PREFIX

    @SCHEDULER_API_PREFIX.setter
    def SCHEDULER_API_PREFIX( self, value ):
        self.__SCHEDULER_API_PREFIX = value
        return

    @property
    def SCHEDULER_AUTH( self ):
        return self.__SCHEDULER_AUTH

    @SCHEDULER_AUTH.setter
    def SCHEDULER_AUTH( self, value ):
        if type( value ) is str:
            mod_name, cls_name = value.rsplit( '.', 1 )
            mod = importlib.import_module( mod_name )
            if cls_name.endswith( '()' ):
                cls_name = cls_name[:-2]

            cls = getattr( mod, cls_name )
            self.__SCHEDULER_AUTH = cls()
            pass

        elif isinstance( value, flask_apscheduler.auth.HTTPBasicAuth ):
            self.__SCHEDULER_AUTH = value

        else:
            raise ValueError( '' )

        return

