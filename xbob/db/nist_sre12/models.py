#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Laurent El Shafey <laurent.el-shafey@idiap.ch>
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

"""Table models and functionality for the NIST SRE 2012 database.
"""

import os, numpy
import bob.db.utils
from sqlalchemy import Table, Column, Integer, String, ForeignKey, or_, and_, not_
from bob.db.sqlalchemy_migration import Enum, relationship
from sqlalchemy.orm import backref
from sqlalchemy.ext.declarative import declarative_base

import xbob.db.verification.utils

Base = declarative_base()

protocolPurpose_file_association = Table('protocolPurpose_file_association', Base.metadata,
  Column('protocolPurpose_id', Integer, ForeignKey('protocolPurpose.id')),
  Column('file_id',  String(20), ForeignKey('file.id')))

protocolPurpose_client_association = Table('protocolPurpose_client_association', Base.metadata,
  Column('protocolPurpose_id', Integer, ForeignKey('protocolPurpose.id')),
  Column('client_id',  String(20), ForeignKey('client.id')))

protocolPurpose_tclient_association = Table('protocolPurpose_tclient_association', Base.metadata,
  Column('protocolPurpose_id', Integer, ForeignKey('protocolPurpose.id')),
  Column('tclient_id',  String(20), ForeignKey('tclient.id')))

tclient_file_association = Table('tclient_file_association', Base.metadata,
  Column('tclient_id',  String(20), ForeignKey('tclient.id')),
  Column('id', Integer, ForeignKey('file.id')))

class Client(Base):
  """Database clients, marked by an integer identifier and the group they belong to"""

  __tablename__ = 'client'

  # Key identifier for the client
  id = Column(String(20), primary_key=True) # speaker_pin
  gender_choices = ('male', 'female')
  gender = Column(Enum(*gender_choices))

  def __init__(self, id, gender):
    self.id = id
    self.gender = gender

  def __repr__(self):
    return "Client(%s, %s)" % (self.id, self.gender)


class File(Base, xbob.db.verification.utils.File):
  """Generic file container"""

  __tablename__ = 'file'

  # Key identifier for the file
  id = Column(Integer, primary_key=True)
  # Key identifier of the client associated with this file
  client_id = Column(String(20), ForeignKey('client.id')) # for SQL
  # Unique path to this file inside the database
  path = Column(String(100), unique=True)

  # for Python
  client = relationship("Client", backref=backref("files", order_by=id))

  def __init__(self, client_id, path):
    # call base class constructor
    xbob.db.verification.utils.File.__init__(self, client_id = client_id, path = path)

class Protocol(Base):
  """NIST SRE 2012 protocols"""

  __tablename__ = 'protocol'

  # Unique identifier for this protocol object
  id = Column(Integer, primary_key=True)
  # Name of the protocol associated with this object
  name = Column(String(20), unique=True)

  def __init__(self, name):
    self.name = name

  def __repr__(self):
    return "Protocol('%s')" % (self.name)

class ProtocolPurpose(Base):
  """NIST SRE 2012 purposes"""

  __tablename__ = 'protocolPurpose'

  # Unique identifier for this protocol purpose object
  id = Column(Integer, primary_key=True)
  # Id of the protocol associated with this protocol purpose object
  protocol_id = Column(Integer, ForeignKey('protocol.id')) # for SQL
  # Group associated with this protocol purpose object
  group_choices = ('world', 'dev', 'eval', 'optional_world_1', 'optional_world_2')
  sgroup = Column(Enum(*group_choices))
  # Purpose associated with this protocol purpose object
  purpose_choices = ('train', 'enrol', 'probe', 'tnorm', 'znorm')
  purpose = Column(Enum(*purpose_choices))

  # For Python: A direct link to the Protocol object that this ProtocolPurpose belongs to
  protocol = relationship("Protocol", backref=backref("purposes", order_by=id))
  # For Python: A direct link to the File objects associated with this ProtcolPurpose
  files = relationship("File", secondary=protocolPurpose_file_association, backref=backref("protocolPurposes", order_by=id))
  # For Python: A direct link to the Client objects associated with this ProtcolPurpose
  clients = relationship("Client", secondary=protocolPurpose_client_association, backref=backref("protocolPurposes", order_by=id))
  # For Python: A direct link to the T-Norm Client objects associated with this ProtcolPurpose
  tclients = relationship("TClient", secondary=protocolPurpose_tclient_association, backref=backref("protocolPurposes", order_by=id))

  def __init__(self, protocol_id, sgroup, purpose):
    self.protocol_id = protocol_id
    self.sgroup = sgroup
    self.purpose = purpose

  def __repr__(self):
    return "ProtocolPurpose('%s', '%s', '%s')" % (self.protocol.name, self.sgroup, self.purpose)

class TClient(Base):
  """Database T-clients, marked by an integer identifier and the group they belong to"""

  __tablename__ = 'tclient'

  # Key identifier for the client
  id = Column(String(20), primary_key=True) # speaker_pin
  gender_choices = ('male', 'female')
  gender = Column(Enum(*gender_choices))

  # For Python: A direct link to the File objects associated with this T-Norm client
  files = relationship("File", secondary=tclient_file_association, backref=backref("tclients", order_by=id))

  def __init__(self, id, gender):
    self.id = id
    self.gender = gender

  def __repr__(self):
    return "TClient(%s, %s)" % (self.id, self.gender)

