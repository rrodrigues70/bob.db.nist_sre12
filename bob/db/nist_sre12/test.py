#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Laurent El Shafey <laurent.el-shafey@idiap.ch>
# Fri Aug 23 16:27:27 CEST 2013
#
# Copyright (C) 2012-2014 Idiap Research Institute, Martigny, Switzerland
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
import bob.db.nist_sre12

def db_available(test):
  """Decorator for detecting if the database file is available"""
  from bob.io.base.test_utils import datafile
  from nose.plugins.skip import SkipTest
  import functools

  @functools.wraps(test)
  def wrapper(*args, **kwargs):
    dbfile = datafile("db.sql3", __name__, None)
    if os.path.exists(dbfile):
      return test(*args, **kwargs)
    else:
      raise SkipTest("The database file '%s' is not available; did you forget to run 'bob_dbmanage.py %s create' ?" % (dbfile, 'nist_sre12'))

  return wrapper


@db_available
def test_query():
  from pkg_resources import resource_filename

  db = bob.db.nist_sre12.Database()

  assert len(db.groups()) == 5
  assert len(db.groups(protocol='male')) == 5
  assert len(db.groups(protocol='female')) == 5

  # For Male protocol
  assert len(db.clients(protocol='male')) == 16680
  assert len(db.clients(protocol='male', world_gender='male')) == 7482
  assert len(db.clients(protocol='male', world_gender='female')) == 9961
  assert len(db.clients(protocol='male', groups='world', world_gender='male')) == 6767 # 6766
  assert len(db.clients(protocol='male', groups='world', world_gender='female')) == 9198
  assert len(db.clients(protocol='male', groups='world')) == 15965
  assert len(db.clients(protocol='male', groups='optional_world_1', world_gender='male')) == 673 # 672
  assert len(db.clients(protocol='male', groups='optional_world_1', world_gender='female')) == 941
  assert len(db.clients(protocol='male', groups='optional_world_1')) == 1614
  assert len(db.clients(protocol='male', groups='optional_world_2',  world_gender='male')) == 673 # 672
  assert len(db.clients(protocol='male', groups='optional_world_2',  world_gender='female')) == 941
  assert len(db.clients(protocol='male', groups='optional_world_2')) == 1614
  assert len(db.clients(protocol='male', groups='dev')) == 680
  assert len(db.clients(protocol='male', groups='eval')) == 763

  assert len(db.clients(protocol='male', groups='world', subworld='optional_world_1', world_gender='male')) == 673 # 672
  assert len(db.clients(protocol='male', groups='world', subworld='optional_world_1', world_gender='female')) == 941
  assert len(db.clients(protocol='male', groups='world', subworld='optional_world_1')) == 1614
  assert len(db.clients(protocol='male', groups='world', subworld='optional_world_2',  world_gender='male')) == 673 # 672
  assert len(db.clients(protocol='male', groups='world', subworld='optional_world_2',  world_gender='female')) == 941
  assert len(db.clients(protocol='male', groups='world', subworld='optional_world_2')) == 1614

  assert len(db.model_ids(protocol='male')) == 16680
  assert len(db.model_ids(protocol='male', world_gender='male')) == 7482
  assert len(db.model_ids(protocol='male', world_gender='female')) == 9961
  assert len(db.model_ids(protocol='male', groups='world', world_gender='male')) == 6767 # 6766
  assert len(db.model_ids(protocol='male', groups='world', world_gender='female')) == 9198
  assert len(db.model_ids(protocol='male', groups='world')) == 15965
  assert len(db.model_ids(protocol='male', groups='optional_world_1', world_gender='male')) == 673 # 672
  assert len(db.model_ids(protocol='male', groups='optional_world_1', world_gender='female')) == 941
  assert len(db.model_ids(protocol='male', groups='optional_world_1')) == 1614
  assert len(db.model_ids(protocol='male', groups='optional_world_2',  world_gender='male')) == 673 # 672
  assert len(db.model_ids(protocol='male', groups='optional_world_2',  world_gender='female')) == 941
  assert len(db.model_ids(protocol='male', groups='optional_world_2')) == 1614
  assert len(db.model_ids(protocol='male', groups='dev')) == 680
  assert len(db.model_ids(protocol='male', groups='eval')) == 763

  assert len(db.model_ids(protocol='male', groups='world', subworld='optional_world_1', world_gender='male')) == 673 # 672
  assert len(db.model_ids(protocol='male', groups='world', subworld='optional_world_1', world_gender='female')) == 941
  assert len(db.model_ids(protocol='male', groups='world', subworld='optional_world_1')) == 1614
  assert len(db.model_ids(protocol='male', groups='world', subworld='optional_world_2',  world_gender='male')) == 673 # 672
  assert len(db.model_ids(protocol='male', groups='world', subworld='optional_world_2',  world_gender='female')) == 941
  assert len(db.model_ids(protocol='male', groups='world', subworld='optional_world_2')) == 1614

  assert len(db.objects(protocol='male', groups='world', world_gender='male')) == 33322 # 33311
  assert len(db.objects(protocol='male', groups='world', world_gender='female')) == 42521 # 42532
  assert len(db.objects(protocol='male', groups='world')) == 75843

  assert len(db.objects(protocol='male', groups='optional_world_1', world_gender='male')) == 13714
  assert len(db.objects(protocol='male', groups='optional_world_1', world_gender='female')) == 17810
  assert len(db.objects(protocol='male', groups='optional_world_1')) == 31524
  assert len(db.objects(protocol='male', groups='optional_world_2', world_gender='male')) == 13714
  assert len(db.objects(protocol='male', groups='optional_world_2', world_gender='female')) == 17810
  assert len(db.objects(protocol='male', groups='optional_world_2')) == 31524

  assert len(db.objects(protocol='male', groups='world', subworld='optional_world_1', world_gender='male')) == 13714
  assert len(db.objects(protocol='male', groups='world', subworld='optional_world_1', world_gender='female')) == 17810
  assert len(db.objects(protocol='male', groups='world', subworld='optional_world_1')) == 31524
  assert len(db.objects(protocol='male', groups='world', subworld='optional_world_2', world_gender='male')) == 13714
  assert len(db.objects(protocol='male', groups='world', subworld='optional_world_2', world_gender='female')) == 17810
  assert len(db.objects(protocol='male', groups='world', subworld='optional_world_2')) == 31524

  assert len(db.objects(protocol='male', groups='dev', purposes='enrol')) == 16941
  assert len(db.objects(protocol='male', groups='dev', purposes='enrol', model_ids='MIX104296_M')) == 12
  assert len(db.objects(protocol='male', groups='dev', purposes='probe')) == 19866

  assert len(db.objects(protocol='male', groups='eval', purposes='enrol')) == 47480 # 47486 (see LOGS)
  assert len(db.objects(protocol='male', groups='eval', purposes='enrol', model_ids='MIX104296_M')) == 21
  assert len(db.objects(protocol='male', groups='eval', purposes='probe')) == 29728

  # For Female protocol
  assert len(db.clients(protocol='female')) == 17038
  assert len(db.clients(protocol='female', world_gender='female')) == 10271
  assert len(db.clients(protocol='female', world_gender='male')) == 7922
  assert len(db.clients(protocol='female', groups='world', world_gender='female')) == 9198
  assert len(db.clients(protocol='female', groups='world', world_gender='male')) == 6767 # 6766
  assert len(db.clients(protocol='female', groups='world')) == 15965
  assert len(db.clients(protocol='female', groups='optional_world_1', world_gender='female')) == 941
  assert len(db.clients(protocol='female', groups='optional_world_1', world_gender='male')) == 673 # 672
  assert len(db.clients(protocol='female', groups='optional_world_1')) == 1614
  assert len(db.clients(protocol='female', groups='optional_world_2', world_gender='female')) == 941
  assert len(db.clients(protocol='female', groups='optional_world_2', world_gender='male')) == 673 # 672
  assert len(db.clients(protocol='female', groups='optional_world_2')) == 1614
  assert len(db.clients(protocol='female', groups='dev')) == 1039
  assert len(db.clients(protocol='female', groups='eval')) == 1155

  assert len(db.clients(protocol='female', groups='world', subworld='optional_world_1', world_gender='female')) == 941
  assert len(db.clients(protocol='female', groups='world', subworld='optional_world_1', world_gender='male')) == 673 # 672
  assert len(db.clients(protocol='female', groups='world', subworld='optional_world_1')) == 1614
  assert len(db.clients(protocol='female', groups='world', subworld='optional_world_2',  world_gender='female')) == 941
  assert len(db.clients(protocol='female', groups='world', subworld='optional_world_2',  world_gender='male')) == 673 # 672
  assert len(db.clients(protocol='female', groups='world', subworld='optional_world_2')) == 1614

  assert len(db.model_ids(protocol='female')) == 17038
  assert len(db.model_ids(protocol='female', world_gender='female')) == 10271
  assert len(db.model_ids(protocol='female', world_gender='male')) == 7922
  assert len(db.model_ids(protocol='female', groups='world', world_gender='female')) == 9198
  assert len(db.model_ids(protocol='female', groups='world', world_gender='male')) == 6767 # 6766
  assert len(db.model_ids(protocol='female', groups='world')) == 15965
  assert len(db.model_ids(protocol='female', groups='optional_world_1', world_gender='female')) == 941
  assert len(db.model_ids(protocol='female', groups='optional_world_1', world_gender='male')) == 673 # 672
  assert len(db.model_ids(protocol='female', groups='optional_world_1')) == 1614
  assert len(db.model_ids(protocol='female', groups='optional_world_2', world_gender='female')) == 941
  assert len(db.model_ids(protocol='female', groups='optional_world_2', world_gender='male')) == 673 # 672
  assert len(db.model_ids(protocol='female', groups='optional_world_2')) == 1614
  assert len(db.model_ids(protocol='female', groups='dev')) == 1039
  assert len(db.model_ids(protocol='female', groups='eval')) == 1155

  assert len(db.model_ids(protocol='female', groups='world', subworld='optional_world_1', world_gender='female')) == 941
  assert len(db.model_ids(protocol='female', groups='world', subworld='optional_world_1', world_gender='male')) == 673 # 672
  assert len(db.model_ids(protocol='female', groups='world', subworld='optional_world_1')) == 1614
  assert len(db.model_ids(protocol='female', groups='world', subworld='optional_world_2',  world_gender='female')) == 941
  assert len(db.model_ids(protocol='female', groups='world', subworld='optional_world_2',  world_gender='male')) == 673 # 672
  assert len(db.model_ids(protocol='female', groups='world', subworld='optional_world_2')) == 1614

  assert len(db.objects(protocol='female', groups='world', world_gender='male')) == 33322 # 33311
  assert len(db.objects(protocol='female', groups='world', world_gender='female')) == 42521 # 42532
  assert len(db.objects(protocol='female', groups='world')) == 75843

  assert len(db.objects(protocol='female', groups='optional_world_1', world_gender='female')) == 17810
  assert len(db.objects(protocol='female', groups='optional_world_1', world_gender='male')) == 13714
  assert len(db.objects(protocol='female', groups='optional_world_1')) == 31524
  assert len(db.objects(protocol='female', groups='optional_world_2', world_gender='female')) == 17810
  assert len(db.objects(protocol='female', groups='optional_world_2', world_gender='male')) == 13714
  assert len(db.objects(protocol='female', groups='optional_world_2')) == 31524

  assert len(db.objects(protocol='female', groups='world', subworld='optional_world_1', world_gender='female')) == 17810
  assert len(db.objects(protocol='female', groups='world', subworld='optional_world_1', world_gender='male')) == 13714
  assert len(db.objects(protocol='female', groups='world', subworld='optional_world_1')) == 31524
  assert len(db.objects(protocol='female', groups='world', subworld='optional_world_2', world_gender='female')) == 17810
  assert len(db.objects(protocol='female', groups='world', subworld='optional_world_2', world_gender='male')) == 13714
  assert len(db.objects(protocol='female', groups='world', subworld='optional_world_2')) == 31524

  assert len(db.objects(protocol='female', groups='dev', purposes='enrol')) == 24693
  assert len(db.objects(protocol='female', groups='dev', purposes='enrol', model_ids='MIX108878_F')) == 30
  assert len(db.objects(protocol='female', groups='dev', purposes='probe')) == 25980

  assert len(db.objects(protocol='female', groups='eval', purposes='enrol')) == 66192 # 66220 (see LOGS)
  assert len(db.objects(protocol='female', groups='eval', purposes='enrol', model_ids='MIX108878_F')) == 33
  assert len(db.objects(protocol='female', groups='eval', purposes='probe')) == 43378


@db_available
def test_query_ztnorm():
  from pkg_resources import resource_filename

  db = bob.db.nist_sre12.Database()

  # For Male protocol
  assert len(db.tclients(protocol='male', gender='male')) == 121
  assert len(db.tclients(protocol='male', gender='female')) == 0
  assert len(db.tclients(protocol='male')) == 121
  assert len(db.tclients(protocol='male', groups='dev', gender='male')) == 121
  assert len(db.tclients(protocol='male', groups='dev', gender='female')) == 0
  assert len(db.tclients(protocol='male', groups='dev')) == 121
  assert len(db.tclients(protocol='male', groups='eval', gender='male')) == 121
  assert len(db.tclients(protocol='male', groups='eval', gender='female')) == 0
  assert len(db.tclients(protocol='male', groups='eval')) == 121

  assert len(db.tobjects(protocol='male', gender='male')) == 1181
  assert len(db.tobjects(protocol='male', gender='female')) == 0
  assert len(db.tobjects(protocol='male')) == 1181
  assert len(db.tobjects(protocol='male', groups='dev', gender='male')) == 1181
  assert len(db.tobjects(protocol='male', groups='dev', gender='female')) == 0
  assert len(db.tobjects(protocol='male', groups='dev')) == 1181
  assert len(db.tobjects(protocol='male', groups='eval', gender='male')) == 1181
  assert len(db.tobjects(protocol='male', groups='eval', gender='female')) == 0
  assert len(db.tobjects(protocol='male', groups='eval')) == 1181

  assert len(db.zobjects(protocol='male', gender='male')) == 1411
  assert len(db.zobjects(protocol='male', gender='female')) == 0
  assert len(db.zobjects(protocol='male')) == 1411
  assert len(db.zobjects(protocol='male', groups='dev', gender='male')) == 1411
  assert len(db.zobjects(protocol='male', groups='dev', gender='female')) == 0
  assert len(db.zobjects(protocol='male', groups='dev')) == 1411
  assert len(db.zobjects(protocol='male', groups='eval', gender='male')) == 1411
  assert len(db.zobjects(protocol='male', groups='eval', gender='female')) == 0
  assert len(db.zobjects(protocol='male', groups='eval')) == 1411

  # For Female protocol
  assert len(db.tclients(protocol='female', gender='female')) == 183
  assert len(db.tclients(protocol='female', gender='male')) == 0
  assert len(db.tclients(protocol='female')) == 183
  assert len(db.tclients(protocol='female', groups='dev', gender='female')) == 183
  assert len(db.tclients(protocol='female', groups='dev', gender='male')) == 0
  assert len(db.tclients(protocol='female', groups='dev')) == 183
  assert len(db.tclients(protocol='female', groups='eval', gender='female')) == 183
  assert len(db.tclients(protocol='female', groups='eval', gender='male')) == 0
  assert len(db.tclients(protocol='female', groups='eval')) == 183

  assert len(db.tobjects(protocol='female', gender='female')) == 1643
  assert len(db.tobjects(protocol='female', gender='male')) == 0
  assert len(db.tobjects(protocol='female')) == 1643
  assert len(db.tobjects(protocol='female', groups='dev', gender='female')) == 1643
  assert len(db.tobjects(protocol='female', groups='dev', gender='male')) == 0
  assert len(db.tobjects(protocol='female', groups='dev')) == 1643
  assert len(db.tobjects(protocol='female', groups='eval', gender='female')) == 1643
  assert len(db.tobjects(protocol='female', groups='eval', gender='male')) == 0
  assert len(db.tobjects(protocol='female', groups='eval')) == 1643

  assert len(db.zobjects(protocol='female', gender='female')) == 2117
  assert len(db.zobjects(protocol='female', gender='male')) == 0
  assert len(db.zobjects(protocol='female')) == 2117
  assert len(db.zobjects(protocol='female', groups='dev', gender='female')) == 2117
  assert len(db.zobjects(protocol='female', groups='dev', gender='male')) == 0
  assert len(db.zobjects(protocol='female', groups='dev')) == 2117
  assert len(db.zobjects(protocol='female', groups='eval', gender='female')) == 2117
  assert len(db.zobjects(protocol='female', groups='eval', gender='male')) == 0
  assert len(db.zobjects(protocol='female', groups='eval')) == 2117


@db_available
def test_driver_api():

  from bob.db.base.script.dbmanage import main
  assert main('nist_sre12 dumplist --self-test'.split()) == 0
  assert main('nist_sre12 checkfiles --directory . --extension .sph --self-test'.split()) == 0

