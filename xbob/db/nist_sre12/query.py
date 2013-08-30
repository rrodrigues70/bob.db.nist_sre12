#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# @author: Elie Khoury <Elie.Khoury@idiap.ch>
# @date: Thu Aug 22 17:49:19 CEST 2013
#
# Copyright (C) 2012-2013 Idiap Research Institute, Martigny, Switzerland
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import xbob.db.verification.filelist
import os

class Database(xbob.db.verification.filelist.Database):
  """Wrapper class for the NIST SRE 2012 database for speaker recognition (http://www.nist_sre12.org/).
  """

  def __init__(self, protocol='male'):
    # call base class constructor
    # By default, the male protocol is used 
    from pkg_resources import resource_filename
    
    lists = resource_filename(__name__, os.path.join('lists', protocol))
    
    xbob.db.verification.filelist.Database.__init__(self, lists)
    
