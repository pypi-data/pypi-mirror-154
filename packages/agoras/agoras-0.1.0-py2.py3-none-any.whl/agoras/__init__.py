# -*- coding: utf-8 -*-
#
# Please refer to AUTHORS.rst for a complete list of Copyright holders.
# Copyright (C) 2016-2022, Agora Developers.

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
``agoras`` is just black magic.

agoras is a package that studies the codebase of your project in search
for internal and external imports. It then discards the imports that are
satisfied with internal code or with the standard library and finally
searches the `PyPIContents`_ index to list which packages satisfy your imports.

.. _PyPIContents: https://github.com/LuisAlejandro/pypicontents

"""


__author__ = 'Luis Alejandro Martínez Faneyth'
__email__ = 'luis@collagelabs.org'
__version__ = '0.1.0'
__url__ = 'https://github.com/LuisAlejandro/agoras'
__description__ = ('A command line python utility to manage your social'
                   ' networks (Twitter, Facebook, LinkedIn and Instagram)')
