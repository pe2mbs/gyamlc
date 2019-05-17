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
import distutils.core

with open( "README.md", "r" ) as fh:
    long_description = fh.read()

exec( open( './gyamlc/version.py' ).read())


distutils.core.setup(
    name                = 'gyamlc',
    version             = __version__,
    author              = __author__,
    author_email        = __email__,
    description         = description,
    long_description    = long_description,
    long_description_content_type="text/markdown",
    url                 = url,
    packages            = [ 'gyamlc', 'gyamlc.flask', 'gyamlc.mixins' ],
    classifiers         = [
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "License :: {}".format( __license__ ),
        "Operating System :: OS Independent",
        'Development Status :: {}'.format( __status__ )
    ],
)