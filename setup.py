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
from setuptools import setup
import os


base_dir = os.path.dirname(__file__)

package = {}
exec( open( os.path.join(base_dir, 'saiti', 'version.py' ) ).read(), package )
long_description = open( os.path.join(base_dir, "README.md" ), "r" ).read()

setup(
    name                = 'saiti',
    version             = package[ '__version__' ],
    author              = package[ '__author__' ],
    author_email        = package[ '__email__' ],
    description         = package[ 'description' ],
    long_description    = long_description,
    long_description_content_type='text/markdown',
    url                 = package[ 'url' ],
    project_urls={
        'Documentation':    'https://github.com/pe2mbs/saiti/wiki',
        'Say Thanks!':      'https://saythanks.io/to/pe2mbs',
        'Source':           'https://github.com/pe2mbs/saiti/',
        'Tracker':          'https://github.com/pe2mbs/saiti/issues',
    },
    license             = package[ '__license__' ],
    packages            = [ 'saiti', 'saiti.flask', 'saiti.mixins' ],
    python_requires     = '>=3',
    keywords            = 'config json yaml logging flask generic custom',
    install_requires    = [ 'pyyaml>=4.2b1' ],
    package_data        = {},
    data_files          = [ ( 'example', [ 'example/example.conf'] ) ],
    classifiers         = [
        "Programming Language :: Python :: 3 :: Only",
        "License :: OSI Approved :: {}".format( package[ '__license__' ] ),
        'Topic :: Software Development :: Build Tools',
        'Topic :: Utilities',
        "Operating System :: OS Independent",
        'Development Status :: {}'.format( package[ '__status__' ] ),
        'Environment :: Web Environment',
        'Environment :: Win32 (MS Windows)',
        'Environment :: X11 Applications',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Natural Language :: English'





    ],
)