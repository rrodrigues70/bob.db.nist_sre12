#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Laurent El Shafey <laurent.el-shafey@idiap.ch>
# Fri Aug 23 16:27:27 CEST 2013
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

"""A few checks on the protocols of a subset of the NIST SRE 2012 database
"""

import os, sys
import unittest
from .query import Database

class NistDatabaseTest(unittest.TestCase):
  """Performs various tests on the protocols of a subset of the NIST SRE 2012 database."""

  def test01_query(self):
    from pkg_resources import resource_filename
    
    db = Database()
    
    self.assertEqual(len(db.groups()), 5)
    self.assertEqual(len(db.groups(protocol='male')), 5)
    self.assertEqual(len(db.groups(protocol='female')), 5)

    # For Male protocol
    self.assertEqual(len(db.clients(protocol='male')), 16680)
    self.assertEqual(len(db.clients(protocol='male', world_gender='male')), 7482)
    self.assertEqual(len(db.clients(protocol='male', world_gender='female')), 9961)
    self.assertEqual(len(db.clients(protocol='male', groups='world', world_gender='male')), 6767) # 6766
    self.assertEqual(len(db.clients(protocol='male', groups='world', world_gender='female')), 9198)
    self.assertEqual(len(db.clients(protocol='male', groups='world')), 15965)
    self.assertEqual(len(db.clients(protocol='male', groups='optional_world_1', world_gender='male')), 673) # 672
    self.assertEqual(len(db.clients(protocol='male', groups='optional_world_1', world_gender='female')), 941)
    self.assertEqual(len(db.clients(protocol='male', groups='optional_world_1')), 1614)
    self.assertEqual(len(db.clients(protocol='male', groups='optional_world_2',  world_gender='male')), 673) # 672
    self.assertEqual(len(db.clients(protocol='male', groups='optional_world_2',  world_gender='female')), 941)
    self.assertEqual(len(db.clients(protocol='male', groups='optional_world_2')), 1614)
    self.assertEqual(len(db.clients(protocol='male', groups='dev')), 680)
    self.assertEqual(len(db.clients(protocol='male', groups='eval')), 763)

    self.assertEqual(len(db.clients(protocol='male', groups='world', subworld='optional_world_1', world_gender='male')), 673) # 672
    self.assertEqual(len(db.clients(protocol='male', groups='world', subworld='optional_world_1', world_gender='female')), 941)
    self.assertEqual(len(db.clients(protocol='male', groups='world', subworld='optional_world_1')), 1614)
    self.assertEqual(len(db.clients(protocol='male', groups='world', subworld='optional_world_2',  world_gender='male')), 673) # 672
    self.assertEqual(len(db.clients(protocol='male', groups='world', subworld='optional_world_2',  world_gender='female')), 941)
    self.assertEqual(len(db.clients(protocol='male', groups='world', subworld='optional_world_2')), 1614)

    self.assertEqual(len(db.model_ids(protocol='male')), 16680)
    self.assertEqual(len(db.model_ids(protocol='male', world_gender='male')), 7482)
    self.assertEqual(len(db.model_ids(protocol='male', world_gender='female')), 9961)
    self.assertEqual(len(db.model_ids(protocol='male', groups='world', world_gender='male')), 6767) # 6766
    self.assertEqual(len(db.model_ids(protocol='male', groups='world', world_gender='female')), 9198)
    self.assertEqual(len(db.model_ids(protocol='male', groups='world')), 15965)
    self.assertEqual(len(db.model_ids(protocol='male', groups='optional_world_1', world_gender='male')), 673) # 672
    self.assertEqual(len(db.model_ids(protocol='male', groups='optional_world_1', world_gender='female')), 941)
    self.assertEqual(len(db.model_ids(protocol='male', groups='optional_world_1')), 1614)
    self.assertEqual(len(db.model_ids(protocol='male', groups='optional_world_2',  world_gender='male')), 673) # 672
    self.assertEqual(len(db.model_ids(protocol='male', groups='optional_world_2',  world_gender='female')), 941)
    self.assertEqual(len(db.model_ids(protocol='male', groups='optional_world_2')), 1614)
    self.assertEqual(len(db.model_ids(protocol='male', groups='dev')), 680)
    self.assertEqual(len(db.model_ids(protocol='male', groups='eval')), 763)

    self.assertEqual(len(db.model_ids(protocol='male', groups='world', subworld='optional_world_1', world_gender='male')), 673) # 672
    self.assertEqual(len(db.model_ids(protocol='male', groups='world', subworld='optional_world_1', world_gender='female')), 941)
    self.assertEqual(len(db.model_ids(protocol='male', groups='world', subworld='optional_world_1')), 1614)
    self.assertEqual(len(db.model_ids(protocol='male', groups='world', subworld='optional_world_2',  world_gender='male')), 673) # 672
    self.assertEqual(len(db.model_ids(protocol='male', groups='world', subworld='optional_world_2',  world_gender='female')), 941)
    self.assertEqual(len(db.model_ids(protocol='male', groups='world', subworld='optional_world_2')), 1614)

    self.assertEqual(len(db.objects(protocol='male', groups='world', world_gender='male')), 33322) # 33311
    self.assertEqual(len(db.objects(protocol='male', groups='world', world_gender='female')), 42521) # 42532
    self.assertEqual(len(db.objects(protocol='male', groups='world')), 75843)

    self.assertEqual(len(db.objects(protocol='male', groups='optional_world_1', world_gender='male')), 13714)
    self.assertEqual(len(db.objects(protocol='male', groups='optional_world_1', world_gender='female')), 17810)
    self.assertEqual(len(db.objects(protocol='male', groups='optional_world_1')), 31524)
    self.assertEqual(len(db.objects(protocol='male', groups='optional_world_2', world_gender='male')), 13714)
    self.assertEqual(len(db.objects(protocol='male', groups='optional_world_2', world_gender='female')), 17810)
    self.assertEqual(len(db.objects(protocol='male', groups='optional_world_2')), 31524)

    self.assertEqual(len(db.objects(protocol='male', groups='world', subworld='optional_world_1', world_gender='male')), 13714)
    self.assertEqual(len(db.objects(protocol='male', groups='world', subworld='optional_world_1', world_gender='female')), 17810)
    self.assertEqual(len(db.objects(protocol='male', groups='world', subworld='optional_world_1')), 31524)
    self.assertEqual(len(db.objects(protocol='male', groups='world', subworld='optional_world_2', world_gender='male')), 13714)
    self.assertEqual(len(db.objects(protocol='male', groups='world', subworld='optional_world_2', world_gender='female')), 17810)
    self.assertEqual(len(db.objects(protocol='male', groups='world', subworld='optional_world_2')), 31524)

    self.assertEqual(len(db.objects(protocol='male', groups='dev', purposes='enrol')), 16941)
    self.assertEqual(len(db.objects(protocol='male', groups='dev', purposes='enrol', model_ids='MIX104296_M')), 12)
    self.assertEqual(len(db.objects(protocol='male', groups='dev', purposes='probe')), 19866)

    self.assertEqual(len(db.objects(protocol='male', groups='eval', purposes='enrol')), 47480) # 47486 (see LOGS)
    self.assertEqual(len(db.objects(protocol='male', groups='eval', purposes='enrol', model_ids='MIX104296_M')), 21)
    self.assertEqual(len(db.objects(protocol='male', groups='eval', purposes='probe')), 29728)

    # For Female protocol
    self.assertEqual(len(db.clients(protocol='female')), 17038)
    self.assertEqual(len(db.clients(protocol='female', world_gender='female')), 10271)
    self.assertEqual(len(db.clients(protocol='female', world_gender='male')), 7922)
    self.assertEqual(len(db.clients(protocol='female', groups='world', world_gender='female')), 9198)
    self.assertEqual(len(db.clients(protocol='female', groups='world', world_gender='male')), 6767) # 6766
    self.assertEqual(len(db.clients(protocol='female', groups='world')), 15965)
    self.assertEqual(len(db.clients(protocol='female', groups='optional_world_1', world_gender='female')), 941)
    self.assertEqual(len(db.clients(protocol='female', groups='optional_world_1', world_gender='male')), 673) # 672
    self.assertEqual(len(db.clients(protocol='female', groups='optional_world_1')), 1614)
    self.assertEqual(len(db.clients(protocol='female', groups='optional_world_2', world_gender='female')), 941)
    self.assertEqual(len(db.clients(protocol='female', groups='optional_world_2', world_gender='male')), 673) # 672
    self.assertEqual(len(db.clients(protocol='female', groups='optional_world_2')), 1614)
    self.assertEqual(len(db.clients(protocol='female', groups='dev')), 1039)
    self.assertEqual(len(db.clients(protocol='female', groups='eval')), 1155)

    self.assertEqual(len(db.clients(protocol='female', groups='world', subworld='optional_world_1', world_gender='female')), 941)
    self.assertEqual(len(db.clients(protocol='female', groups='world', subworld='optional_world_1', world_gender='male')), 673) # 672
    self.assertEqual(len(db.clients(protocol='female', groups='world', subworld='optional_world_1')), 1614)
    self.assertEqual(len(db.clients(protocol='female', groups='world', subworld='optional_world_2',  world_gender='female')), 941)
    self.assertEqual(len(db.clients(protocol='female', groups='world', subworld='optional_world_2',  world_gender='male')), 673) # 672
    self.assertEqual(len(db.clients(protocol='female', groups='world', subworld='optional_world_2')), 1614)

    self.assertEqual(len(db.model_ids(protocol='female')), 17038)
    self.assertEqual(len(db.model_ids(protocol='female', world_gender='female')), 10271)
    self.assertEqual(len(db.model_ids(protocol='female', world_gender='male')), 7922)
    self.assertEqual(len(db.model_ids(protocol='female', groups='world', world_gender='female')), 9198)
    self.assertEqual(len(db.model_ids(protocol='female', groups='world', world_gender='male')), 6767) # 6766
    self.assertEqual(len(db.model_ids(protocol='female', groups='world')), 15965)
    self.assertEqual(len(db.model_ids(protocol='female', groups='optional_world_1', world_gender='female')), 941)
    self.assertEqual(len(db.model_ids(protocol='female', groups='optional_world_1', world_gender='male')), 673) # 672
    self.assertEqual(len(db.model_ids(protocol='female', groups='optional_world_1')), 1614)
    self.assertEqual(len(db.model_ids(protocol='female', groups='optional_world_2', world_gender='female')), 941)
    self.assertEqual(len(db.model_ids(protocol='female', groups='optional_world_2', world_gender='male')), 673) # 672
    self.assertEqual(len(db.model_ids(protocol='female', groups='optional_world_2')), 1614)
    self.assertEqual(len(db.model_ids(protocol='female', groups='dev')), 1039)
    self.assertEqual(len(db.model_ids(protocol='female', groups='eval')), 1155)

    self.assertEqual(len(db.model_ids(protocol='female', groups='world', subworld='optional_world_1', world_gender='female')), 941)
    self.assertEqual(len(db.model_ids(protocol='female', groups='world', subworld='optional_world_1', world_gender='male')), 673) # 672
    self.assertEqual(len(db.model_ids(protocol='female', groups='world', subworld='optional_world_1')), 1614)
    self.assertEqual(len(db.model_ids(protocol='female', groups='world', subworld='optional_world_2',  world_gender='female')), 941)
    self.assertEqual(len(db.model_ids(protocol='female', groups='world', subworld='optional_world_2',  world_gender='male')), 673) # 672
    self.assertEqual(len(db.model_ids(protocol='female', groups='world', subworld='optional_world_2')), 1614)

    self.assertEqual(len(db.objects(protocol='female', groups='world', world_gender='male')), 33322) # 33311
    self.assertEqual(len(db.objects(protocol='female', groups='world', world_gender='female')), 42521) # 42532
    self.assertEqual(len(db.objects(protocol='female', groups='world')), 75843)

    self.assertEqual(len(db.objects(protocol='female', groups='optional_world_1', world_gender='female')), 17810)
    self.assertEqual(len(db.objects(protocol='female', groups='optional_world_1', world_gender='male')), 13714)
    self.assertEqual(len(db.objects(protocol='female', groups='optional_world_1')), 31524)
    self.assertEqual(len(db.objects(protocol='female', groups='optional_world_2', world_gender='female')), 17810)
    self.assertEqual(len(db.objects(protocol='female', groups='optional_world_2', world_gender='male')), 13714)
    self.assertEqual(len(db.objects(protocol='female', groups='optional_world_2')), 31524)

    self.assertEqual(len(db.objects(protocol='female', groups='world', subworld='optional_world_1', world_gender='female')), 17810)
    self.assertEqual(len(db.objects(protocol='female', groups='world', subworld='optional_world_1', world_gender='male')), 13714)
    self.assertEqual(len(db.objects(protocol='female', groups='world', subworld='optional_world_1')), 31524)
    self.assertEqual(len(db.objects(protocol='female', groups='world', subworld='optional_world_2', world_gender='female')), 17810)
    self.assertEqual(len(db.objects(protocol='female', groups='world', subworld='optional_world_2', world_gender='male')), 13714)
    self.assertEqual(len(db.objects(protocol='female', groups='world', subworld='optional_world_2')), 31524)

    self.assertEqual(len(db.objects(protocol='female', groups='dev', purposes='enrol')), 24693)
    self.assertEqual(len(db.objects(protocol='female', groups='dev', purposes='enrol', model_ids='MIX108878_F')), 30)
    self.assertEqual(len(db.objects(protocol='female', groups='dev', purposes='probe')), 25980)

    self.assertEqual(len(db.objects(protocol='female', groups='eval', purposes='enrol')), 66192) # 66220 (see LOGS)
    self.assertEqual(len(db.objects(protocol='female', groups='eval', purposes='enrol', model_ids='MIX108878_F')), 33)
    self.assertEqual(len(db.objects(protocol='female', groups='eval', purposes='probe')), 43378)


  def test02_query_ztnorm(self):
    from pkg_resources import resource_filename
    
    db = Database()

    # For Male protocol
    self.assertEqual(len(db.tclients(protocol='male', gender='male')), 121)
    self.assertEqual(len(db.tclients(protocol='male', gender='female')), 0)
    self.assertEqual(len(db.tclients(protocol='male')), 121)
    self.assertEqual(len(db.tclients(protocol='male', groups='dev', gender='male')), 121)
    self.assertEqual(len(db.tclients(protocol='male', groups='dev', gender='female')), 0)
    self.assertEqual(len(db.tclients(protocol='male', groups='dev')), 121)
    self.assertEqual(len(db.tclients(protocol='male', groups='eval', gender='male')), 121)
    self.assertEqual(len(db.tclients(protocol='male', groups='eval', gender='female')), 0)
    self.assertEqual(len(db.tclients(protocol='male', groups='eval')), 121)

    self.assertEqual(len(db.tobjects(protocol='male', gender='male')), 1181)
    self.assertEqual(len(db.tobjects(protocol='male', gender='female')), 0)
    self.assertEqual(len(db.tobjects(protocol='male')), 1181)
    self.assertEqual(len(db.tobjects(protocol='male', groups='dev', gender='male')), 1181)
    self.assertEqual(len(db.tobjects(protocol='male', groups='dev', gender='female')), 0)
    self.assertEqual(len(db.tobjects(protocol='male', groups='dev')), 1181)
    self.assertEqual(len(db.tobjects(protocol='male', groups='eval', gender='male')), 1181)
    self.assertEqual(len(db.tobjects(protocol='male', groups='eval', gender='female')), 0)
    self.assertEqual(len(db.tobjects(protocol='male', groups='eval')), 1181)

    self.assertEqual(len(db.zobjects(protocol='male', gender='male')), 1411)
    self.assertEqual(len(db.zobjects(protocol='male', gender='female')), 0)
    self.assertEqual(len(db.zobjects(protocol='male')), 1411)
    self.assertEqual(len(db.zobjects(protocol='male', groups='dev', gender='male')), 1411)
    self.assertEqual(len(db.zobjects(protocol='male', groups='dev', gender='female')), 0)
    self.assertEqual(len(db.zobjects(protocol='male', groups='dev')), 1411)
    self.assertEqual(len(db.zobjects(protocol='male', groups='eval', gender='male')), 1411)
    self.assertEqual(len(db.zobjects(protocol='male', groups='eval', gender='female')), 0)
    self.assertEqual(len(db.zobjects(protocol='male', groups='eval')), 1411)

    # For Female protocol
    self.assertEqual(len(db.tclients(protocol='female', gender='female')), 183)
    self.assertEqual(len(db.tclients(protocol='female', gender='male')), 0)
    self.assertEqual(len(db.tclients(protocol='female')), 183)
    self.assertEqual(len(db.tclients(protocol='female', groups='dev', gender='female')), 183)
    self.assertEqual(len(db.tclients(protocol='female', groups='dev', gender='male')), 0)
    self.assertEqual(len(db.tclients(protocol='female', groups='dev')), 183)
    self.assertEqual(len(db.tclients(protocol='female', groups='eval', gender='female')), 183)
    self.assertEqual(len(db.tclients(protocol='female', groups='eval', gender='male')), 0)
    self.assertEqual(len(db.tclients(protocol='female', groups='eval')), 183)

    self.assertEqual(len(db.tobjects(protocol='female', gender='female')), 1643)
    self.assertEqual(len(db.tobjects(protocol='female', gender='male')), 0)
    self.assertEqual(len(db.tobjects(protocol='female')), 1643)
    self.assertEqual(len(db.tobjects(protocol='female', groups='dev', gender='female')), 1643)
    self.assertEqual(len(db.tobjects(protocol='female', groups='dev', gender='male')), 0)
    self.assertEqual(len(db.tobjects(protocol='female', groups='dev')), 1643)
    self.assertEqual(len(db.tobjects(protocol='female', groups='eval', gender='female')), 1643)
    self.assertEqual(len(db.tobjects(protocol='female', groups='eval', gender='male')), 0)
    self.assertEqual(len(db.tobjects(protocol='female', groups='eval')), 1643)

    self.assertEqual(len(db.zobjects(protocol='female', gender='female')), 2117)
    self.assertEqual(len(db.zobjects(protocol='female', gender='male')), 0)
    self.assertEqual(len(db.zobjects(protocol='female')), 2117)
    self.assertEqual(len(db.zobjects(protocol='female', groups='dev', gender='female')), 2117)
    self.assertEqual(len(db.zobjects(protocol='female', groups='dev', gender='male')), 0)
    self.assertEqual(len(db.zobjects(protocol='female', groups='dev')), 2117)
    self.assertEqual(len(db.zobjects(protocol='female', groups='eval', gender='female')), 2117)
    self.assertEqual(len(db.zobjects(protocol='female', groups='eval', gender='male')), 0)
    self.assertEqual(len(db.zobjects(protocol='female', groups='eval')), 2117)


  def test03_driver_api(self):

    from bob.db.script.dbmanage import main
    self.assertEqual(main('nist_sre12 dumplist --self-test'.split()), 0)
    self.assertEqual(main('nist_sre12 checkfiles --directory . --extension .sph --self-test'.split()), 0)
