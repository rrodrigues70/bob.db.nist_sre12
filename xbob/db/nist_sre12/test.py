#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Laurent El Shafey <laurent.el-shafey@idiap.ch>
# Fri Aug 23 16:27:27 CEST 2013
#
# Copyright (C) 2011-2013 Idiap Research Institute, Martigny, Switzerland
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

"""A few checks on the protocols of a subset of the NIST SRE 2012 database
"""

import os, sys
import unittest
from .query import Database

class NistDatabaseTest(unittest.TestCase):
  """Performs various tests on the protocols of a subset of the NIST SRE 2012 database."""

  def test01_query(self):
    from pkg_resources import resource_filename
    
    # For Male protocol
    db_m = Database('male')

    self.assertEqual(len(db_m.client_ids()), 7482)
    self.assertEqual(len(db_m.client_ids(groups='world')), 6766)
    self.assertEqual(len(db_m.client_ids(groups='optional_world_1')), 672)
    self.assertEqual(len(db_m.client_ids(groups='optional_world_2')), 672)
    self.assertEqual(len(db_m.client_ids(groups='dev')), 680)
    self.assertEqual(len(db_m.client_ids(groups='eval')), 763)

    self.assertEqual(len(db_m.model_ids()), 7482)
    self.assertEqual(len(db_m.model_ids(groups='world')), 6766)
    self.assertEqual(len(db_m.model_ids(groups='optional_world_1')), 672)
    self.assertEqual(len(db_m.model_ids(groups='optional_world_2')), 672)
    self.assertEqual(len(db_m.model_ids(groups='dev')), 680)
    self.assertEqual(len(db_m.model_ids(groups='eval')), 763)

    self.assertEqual(len(db_m.objects(groups='world')), 33311)

    self.assertEqual(len(db_m.objects(groups='dev', purposes='enrol')), 16941)
    self.assertEqual(len(db_m.objects(groups='dev', purposes='enrol', model_ids='MIX104296')), 12)
    self.assertEqual(len(db_m.objects(groups='dev', purposes='probe')), 19866)

    self.assertEqual(len(db_m.objects(groups='eval', purposes='enrol')), 47486)
    self.assertEqual(len(db_m.objects(groups='eval', purposes='enrol', model_ids='MIX104296')), 21)
    self.assertEqual(len(db_m.objects(groups='eval', purposes='probe')), 29728)

    # For Female protocol
    db_f = Database('female')

    self.assertEqual(len(db_f.client_ids()), 10271)
    self.assertEqual(len(db_f.client_ids(groups='world')), 9198)
    self.assertEqual(len(db_f.client_ids(groups='optional_world_1')), 941)
    self.assertEqual(len(db_f.client_ids(groups='optional_world_2')), 941)
    self.assertEqual(len(db_f.client_ids(groups='dev')), 1039)
    self.assertEqual(len(db_f.client_ids(groups='eval')), 1155)

    self.assertEqual(len(db_f.model_ids()), 10271)
    self.assertEqual(len(db_f.model_ids(groups='world')), 9198)
    self.assertEqual(len(db_f.model_ids(groups='optional_world_1')), 941)
    self.assertEqual(len(db_f.model_ids(groups='optional_world_2')), 941)
    self.assertEqual(len(db_f.model_ids(groups='dev')), 1039)
    self.assertEqual(len(db_f.model_ids(groups='eval')), 1155)

    self.assertEqual(len(db_f.objects(groups='world')), 42532)

    self.assertEqual(len(db_f.objects(groups='dev', purposes='enrol')), 24693)
    self.assertEqual(len(db_f.objects(groups='dev', purposes='enrol', model_ids='MIX108878')), 30)
    self.assertEqual(len(db_f.objects(groups='dev', purposes='probe')), 25980)

    self.assertEqual(len(db_f.objects(groups='eval', purposes='enrol')), 66220)
    self.assertEqual(len(db_f.objects(groups='eval', purposes='enrol', model_ids='MIX108878')), 33)
    self.assertEqual(len(db_f.objects(groups='eval', purposes='probe')), 43378)

  def test02_driver_api(self):

    from bob.db.script.dbmanage import main
    self.assertEqual(main('nist_sre12 dumplist --self-test'.split()), 0)
    self.assertEqual(main('nist_sre12 checkfiles --list-directory . --self-test'.split()), 0)

