#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Laurent El Shafey <laurent.el-shafey@idiap.ch>
# Fri Aug 23 16:27:27 CEST 2013
#
# Copyright (C) 2011-2012 Idiap Research Institute, Martigny, Switzerland
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

    self.assertEqual(len(db_m.client_ids()), 7482) # 10 client ids for world, dev and eval
    self.assertEqual(len(db_m.client_ids(groups='world')), 6766) # 10 client ids for world
    self.assertEqual(len(db_m.client_ids(groups='optional_world_1')), 672) # 10 client ids for optional world 1
    self.assertEqual(len(db_m.client_ids(groups='optional_world_2')), 672) # 10 client ids for optional world 2
    self.assertEqual(len(db_m.client_ids(groups='dev')), 680) # 10 client ids for dev
    self.assertEqual(len(db_m.client_ids(groups='eval')), 763) # 10 client ids for eval

    self.assertEqual(len(db_m.model_ids()), 7482) # 30 model ids for world, dev and eval
    self.assertEqual(len(db_m.model_ids(groups='world')), 6766) # 10 model ids for world
    self.assertEqual(len(db_m.model_ids(groups='optional_world_1')), 672) # 10 model ids for optional world 1
    self.assertEqual(len(db_m.model_ids(groups='optional_world_2')), 672) # 10 model ids for optional world 2
    self.assertEqual(len(db_m.model_ids(groups='dev')), 680) # 10 model ids for dev
    self.assertEqual(len(db_m.model_ids(groups='eval')), 763) # 10 model ids for eval

    self.assertEqual(len(db_m.objects(groups='world')), 33311) # 3148 samples in the world set

    self.assertEqual(len(db_m.objects(groups='dev', purposes='enrol')), 16941) # 1304 samples for enrollment in the dev set
    self.assertEqual(len(db_m.objects(groups='dev', purposes='enrol', model_ids='MIX104296')), 12) # 240 samples to enroll model 'Dcoetzee' in the dev set
    self.assertEqual(len(db_m.objects(groups='dev', purposes='probe')), 19866) # 300 samples as probes in the dev set

    self.assertEqual(len(db_m.objects(groups='eval', purposes='enrol')), 1509) # 1509 samples for enrollment in the eval set
    self.assertEqual(len(db_m.objects(groups='eval', purposes='enrol', model_ids='MIX104296')), 21)) # 120 samples to enroll model 'rortiz' in the eval set
    self.assertEqual(len(db_m.objects(groups='eval', purposes='probe')), 29728) # 300 samples as probes in the eval set

    # For Female protocol
    db_f = Database('female')

    self.assertEqual(len(db_f.client_ids()), 10271) # 10 client ids for world, dev and eval
    self.assertEqual(len(db_f.client_ids(groups='world')), 9198) # 10 client ids for world
    self.assertEqual(len(db_f.client_ids(groups='optional_world_1')), 941) # 10 client ids for optional world 1
    self.assertEqual(len(db_f.client_ids(groups='optional_world_2')), 941) # 10 client ids for optional world 2
    self.assertEqual(len(db_f.client_ids(groups='dev')), 1039) # 10 client ids for dev
    self.assertEqual(len(db_f.client_ids(groups='eval')), 1155) # 10 client ids for eval

    self.assertEqual(len(db_f.model_ids()), 10271) # 30 model ids for world, dev and eval
    self.assertEqual(len(db_f.model_ids(groups='world')), 9198) # 10 model ids for world
    self.assertEqual(len(db_f.model_ids(groups='optional_world_1')), 941) # 10 model ids for optional world 1
    self.assertEqual(len(db_f.model_ids(groups='optional_world_2')), 941) # 10 model ids for optional world 2
    self.assertEqual(len(db_f.model_ids(groups='dev')), 1039) # 10 model ids for dev
    self.assertEqual(len(db_f.model_ids(groups='eval')), 1155) # 10 model ids for eval

    self.assertEqual(len(db_f.objects(groups='world')), 42532) # 3148 samples in the world set

    self.assertEqual(len(db_f.objects(groups='dev', purposes='enrol')), 24693) # 1304 samples for enrollment in the dev set
    self.assertEqual(len(db_f.objects(groups='dev', purposes='enrol', model_ids='MIX108878')), 30) # 240 samples to enroll model 'Dcoetzee' in the dev set
    self.assertEqual(len(db_f.objects(groups='dev', purposes='probe')), ) # 300 samples as probes in the dev set

    self.assertEqual(len(db_f.objects(groups='eval', purposes='enrol')), 66220) # 1509 samples for enrollment in the eval set
    self.assertEqual(len(db_f.objects(groups='eval', purposes='enrol', model_ids='MIX108878')), 33)) # 120 samples to enroll model 'rortiz' in the eval set
    self.assertEqual(len(db_f.objects(groups='eval', purposes='probe')), 43378) # 300 samples as probes in the eval set

