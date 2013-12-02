#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Laurent El Shafey <Laurent.El-Shafey@idiap.ch>
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

"""This module provides the Dataset interface allowing the user to query the
NIST SRE 2012 database in the most obvious ways.
"""

import os
from bob.db import utils
from .models import *
from .driver import Interface

import xbob.db.verification.utils

SQLITE_FILE = Interface().files()[0]

class Database(xbob.db.verification.utils.SQLiteDatabase, xbob.db.verification.utils.ZTDatabase):
  """The dataset class opens and maintains a connection opened to the Database.

  It provides many different ways to probe for the characteristics of the data
  and for the data itself inside the database.
  """

  def __init__(self):
    # call base class constructors
    xbob.db.verification.utils.SQLiteDatabase.__init__(self, SQLITE_FILE, File)

  def groups(self, protocol=None):
    """Returns the names of all registered groups"""

    return ProtocolPurpose.group_choices # Same as Client.group_choices for this database

  def clients(self, protocol=None, groups=None, world_gender=None, subworld=None, filter_ids_unknown=True):
    """Returns a set of clients for the specific query by the user.

    Keyword Parameters:

    protocol
      The protocol to consider ('female', 'male')

    groups
      The groups to which the clients belong ('dev', 'eval', 'world', 'optional_world_1', 'optional_world_2')

    world_gender
      The gender to consider for the world data ('female', 'male')

    subworld
      The subworld to consider (only one at a time is possible).
      This is an alias to the group 'optional_world_X' when groups is 'world' 
      and subworld is 'optional_world_X'.

    filter_ids_unknown
      Do not add the ids unknown 'F_ID_X_F' and 'M_ID_X_M'

    Returns: A list containing all the clients which have the given properties.
    """

    protocol = self.check_parameters_for_validity(protocol, "protocol", self.protocol_names())
    groups = self.check_parameters_for_validity(groups, "group", self.groups())
    world_gender = self.check_parameters_for_validity(world_gender, "world_gender", ('male', 'female'))
    subworld = self.check_parameters_for_validity(subworld, "subworld", ('optional_world_1', 'optional_world_2'))

    # List of the clients
    retval = []
    wgroups = []
    if 'world' in groups:
      if len(subworld) == 2:
        wgroups.append('world')
      elif len(subworld) == 1 and 'world' in groups:
        wgroups.append(subworld[0])
    if 'optional_world_1' in groups: wgroups.append('optional_world_1')
    if 'optional_world_2' in groups: wgroups.append('optional_world_2')
    if len(wgroups) > 0:
      q = self.query(Client).join((ProtocolPurpose, Client.protocolPurposes)).join((Protocol, ProtocolPurpose.protocol)).\
            filter(Protocol.name.in_(protocol)).filter(ProtocolPurpose.sgroup.in_(wgroups)).filter(ProtocolPurpose.purpose == 'train')
      if len(world_gender) == 1:
        q = q.filter(Client.gender.in_(world_gender))
      if filter_ids_unknown == True:
        q = q.filter(not_(Client.id.in_(['F_ID_X_F', 'M_ID_X_M'])))
      q = q.order_by(Client.id)
      retval += list(q)

    degroups = []
    if 'dev' in groups: degroups.append('dev')
    if 'eval' in groups: degroups.append('eval')
    if len(degroups) > 0:
      q = self.query(Client).join((ProtocolPurpose, Client.protocolPurposes)).join((Protocol, ProtocolPurpose.protocol)).\
            filter(Protocol.name.in_(protocol)).filter(ProtocolPurpose.sgroup.in_(degroups)).filter(ProtocolPurpose.purpose == 'enrol').\
            order_by(Client.id)
      if filter_ids_unknown == True:
        q = q.filter(not_(Client.id.in_(['F_ID_X_F', 'M_ID_X_M'])))
      retval += list(q)

    return list(set(retval))

  def tclients(self, protocol=None, groups=None, gender=None):
    """Returns a set of clients for the specific query by the user.

    Keyword Parameters:

    protocol
      The protocol to consider ('female', 'male')

    groups
      The groups to which the clients belong ('dev', 'eval', 'world')

    gender
      The gender to consider ('female', 'male')

    Returns: A list containing all the clients which have the given properties.
    """

    protocol = self.check_parameters_for_validity(protocol, "protocol", self.protocol_names())
    groups = self.check_parameters_for_validity(groups, "group", self.groups())
    gender = self.check_parameters_for_validity(gender, "gender", ('male', 'female'))

    # List of the clients
    retval = []
    degroups = []
    if 'dev' in groups: degroups.append('dev')
    if 'eval' in groups: degroups.append('eval')
    if len(degroups) > 0:
      q = self.query(TClient).join((ProtocolPurpose, TClient.protocolPurposes)).join((Protocol, ProtocolPurpose.protocol)).\
            filter(and_(Protocol.name.in_(protocol), ProtocolPurpose.sgroup.in_(degroups), ProtocolPurpose.purpose == 'tnorm')).\
            order_by(TClient.id)
      if len(gender) == 1:
        q = q.filter(TClient.gender.in_(gender))
      retval += list(q)

    return list(set(retval))


  def models(self, protocol=None, groups=None, world_gender=None, subworld=None, filter_ids_unknown=True):
    """Returns a set of models for the specific query by the user.

    Keyword Parameters:

    protocol
      The protocol to consider ('female', 'male')

    groups
      The groups to which the subjects attached to the models belong ('dev', 'eval', 'world')

    world_gender
      The gender to consider for the world data ('female', 'male')

    subworld
      The subworld to consider (only one at a time is possible).
      This is an alias to the group 'optional_world_X' when groups is 'world' 
      and subworld is 'optional_world_X'.

    filter_ids_unknown
      Do not add the ids unknown 'F_ID_X' and 'M_ID_X'

    Returns: A list containing all the models belonging to the given group.
    """

    return self.clients(protocol, groups, world_gender, subworld, filter_ids_unknown)

  def model_ids(self, protocol=None, groups=None, world_gender=None, subworld=None, filter_ids_unknown=True):
    """Returns a list of model ids for the specific query by the user.

    Keyword Parameters:

    protocol
      The protocol to consider ('female', 'male')

    groups
      The groups to which the subjects attached to the models belong ('dev', 'eval', 'world')

    world_gender
      The gender to consider for the world data ('female', 'male')

    subworld
      The subworld to consider (only one at a time is possible).
      This is an alias to the group 'optional_world_X' when groups is 'world' 
      and subworld is 'optional_world_X'.

    filter_ids_unknown
      Do not add the ids unknown 'F_ID_X' and 'M_ID_X'

    Returns: A list containing the ids of all models belonging to the given group.
    """

    return [client.id for client in self.clients(protocol, groups, world_gender, subworld, filter_ids_unknown)]

  def tmodels(self, protocol=None, groups=None, gender=None):
    """Returns a set of T-Norm models for the specific query by the user.

    Keyword Parameters:

    protocol
      The protocol to consider ('female', 'male')

    groups
      The groups to which the subjects attached to the models belong ('dev', 'eval', 'world')

    gender
      The gender to consider ('female', 'male')

    Returns: A list containing all the T-norm models which have the given properties.
    """

    return self.tclients(protocol, groups, gender)

  def tmodel_ids(self, protocol=None, groups=None, gender=None):
    """Returns a set of T-Norm model ids for the specific query by the user.

    Keyword Parameters:

    protocol
      The protocol to consider ('female', 'male')

    groups
      The groups to which the subjects attached to the models belong ('dev', 'eval', 'world')

    gender
      The gender to consider ('female', 'male')

    Returns: A list containing all the T-norm models which have the given properties.
    """
    return [model.id for model in self.tmodels(protocol, groups, gender)]


  def has_client_id(self, id):
    """Returns True if we have a client with a certain integer identifier"""

    return self.query(Client).filter(Client.id==id).count() != 0

  def client(self, id):
    """Returns the client object in the database given a certain id. Raises
    an error if that does not exist."""

    return self.query(Client).filter(Client.id==id).one()

  def get_client_id_from_model_id(self, model_id):
    """Returns the client_id attached to the given model_id

    Keyword Parameters:

    model_id
      The model_id to consider

    Returns: The client_id attached to the given model_id
    """
    return model_id

  def objects(self, protocol=None, purposes=None, model_ids=None, groups=None, world_gender=None,
      subworld=None, classes=None):
    """Returns a set of filenames for the specific query by the user.
    WARNING: Files used as impostor access for several different models are
    only listed one and refer to only a single model

    Keyword Parameters:

    protocol
      The protocol to consider ('female', 'male')

    purposes
      The purposes required to be retrieved ('enrol', 'probe', 'train') or a tuple
      with several of them. If 'None' is given (this is the default), it is
      considered the same as a tuple with all possible values. This field is
      ignored for the data from the "world" group.

    model_ids
      Only retrieves the files for the provided list of model ids (claimed
      client id). The model ids are string.  If 'None' is given (this is
      the default), no filter over the model_ids is performed.

    groups
      One of the groups ('dev', 'eval', 'world', 'optional_world_1', 'optional_world_2') or a tuple with several of them.
      If 'None' is given (this is the default), it is considered the same as a
      tuple with all possible values.

    world_gender
      The gender to consider for the world data ('female', 'male')

    subworld
      The subworld to consider (only one at a time is possible).
      This is an alias to the group 'optional_world_X' when groups is 'world' 
      and subworld is 'optional_world_X'.

    classes
      The classes (types of accesses) to be retrieved ('client', 'impostor')
      or a tuple with several of them. If 'None' is given (this is the
      default), it is considered the same as a tuple with all possible values.

    Returns: A list of files which have the given properties.
    """

    protocol = self.check_parameters_for_validity(protocol, "protocol", self.protocol_names())
    purposes = self.check_parameters_for_validity(purposes, "purpose", self.purposes())
    groups = self.check_parameters_for_validity(groups, "group", self.groups())
    classes = self.check_parameters_for_validity(classes, "class", ('client', 'impostor'))
    world_gender = self.check_parameters_for_validity(world_gender, "world_gender", ('male', 'female'))
    subworld = self.check_parameters_for_validity(subworld, "subworld", ('optional_world_1', 'optional_world_2'))

    import six
    if (model_ids is None):
      model_ids = ()
    elif (isinstance(model_ids, six.string_types)):
      model_ids = (model_ids,)

    # Now query the database
    retval = []
    wgroups = []
    if 'world' in groups:
      if len(subworld) == 2:
        wgroups.append('world')
      elif len(subworld) == 1 and 'world' in groups:
        wgroups.append(subworld[0])
    if 'optional_world_1' in groups: wgroups.append('optional_world_1')
    if 'optional_world_2' in groups: wgroups.append('optional_world_2')
    if len(wgroups) > 0:
      q = self.query(File).join(Client).join((ProtocolPurpose, File.protocolPurposes)).join(Protocol)
      q = q.filter(and_(Protocol.name.in_(protocol), ProtocolPurpose.sgroup.in_(wgroups)))
      if len(world_gender) == 1:
        q = q.filter(Client.gender.in_(world_gender))
      if model_ids:
        q = q.filter(Client.id.in_(model_ids))
      q = q.order_by(File.path, File.client_id)
      retval += list(q)

    if ('dev' in groups or 'eval' in groups):
      if('enrol' in purposes):
        q = self.query(File).join(Client).join((ProtocolPurpose, File.protocolPurposes)).join(Protocol).\
              filter(and_(Protocol.name.in_(protocol), ProtocolPurpose.sgroup.in_(groups), ProtocolPurpose.purpose == 'enrol'))
        if model_ids:
          q = q.filter(File.client_id.in_(model_ids))
        q = q.order_by(File.path, File.client_id)
        retval += list(q)

      if('probe' in purposes):
        if('client' in classes):
          q = self.query(File).join(Client).join((ProtocolPurpose, File.protocolPurposes)).join(Protocol).\
                filter(and_(Protocol.name.in_(protocol), ProtocolPurpose.sgroup.in_(groups), ProtocolPurpose.purpose == 'probe'))
          if model_ids:
            q = q.filter(Client.id.in_(model_ids))
          q = q.order_by(File.path, File.client_id)
          retval += list(q)

        if('impostor' in classes):
          q = self.query(File).join(Client).join((ProtocolPurpose, File.protocolPurposes)).join(Protocol).\
                filter(and_(Protocol.name.in_(protocol), ProtocolPurpose.sgroup.in_(groups), ProtocolPurpose.purpose == 'probe'))
          if len(model_ids) == 1:
            q = q.filter(not_(File.client_id.in_(model_ids)))
          q = q.order_by(File.path, File.client_id)
          retval += list(q)

    return list(set(retval)) # To remove duplicates

  def tobjects(self, protocol=None, model_ids=None, groups=None, gender=None):
    """Returns a set of filenames for the specific query by the user.
    WARNING: Files used as impostor access for several different models are
    only listed one and refer to only a single model

    Keyword Parameters:

    protocol
      The protocol to consider ('female', 'male')

    model_ids
      Only retrieves the files for the provided list of model ids (claimed
      client id). The model ids are string.  If 'None' is given (this is
      the default), no filter over the model_ids is performed.

    groups
      One of the groups ('dev', 'eval', 'world') or a tuple with several of them.
      If 'None' is given (this is the default), it is considered the same as a
      tuple with all possible values.

    gender
      The gender to consider ('female', 'male')

    Returns: A list of files which have the given properties.
    """

    protocol = self.check_parameters_for_validity(protocol, "protocol", self.protocol_names())
    groups = self.check_parameters_for_validity(groups, "group", self.groups())
    gender = self.check_parameters_for_validity(gender, "gender", ('male', 'female'))

    import six
    if (model_ids is None):
      model_ids = ()
    elif (isinstance(model_ids, six.string_types)):
      model_ids = (model_ids,)

    # Now query the database
    q = self.query(File).join((TClient, File.tclients)).join((ProtocolPurpose, File.protocolPurposes)).join(Protocol).\
          filter(and_(Protocol.name.in_(protocol), ProtocolPurpose.sgroup.in_(groups), ProtocolPurpose.purpose == 'tnorm'))
    if model_ids:
      q = q.filter(TClient.id.in_(model_ids))
    if len(gender) == 1:
      q = q.filter(TClient.gender.in_(gender))
    q = q.order_by(File.path, File.client_id)
    return list(set(q))

  def zobjects(self, protocol=None, model_ids=None, groups=None, gender=None):
    """Returns a set of filenames for the specific query by the user.
    WARNING: Files used as impostor access for several different models are
    only listed one and refer to only a single model

    Keyword Parameters:

    protocol
      The protocol to consider ('female', 'male')

    model_ids
      Only retrieves the files for the provided list of model ids (claimed
      client id). The model ids are string.  If 'None' is given (this is
      the default), no filter over the model_ids is performed.

    groups
      One of the groups ('dev', 'eval', 'world') or a tuple with several of them.
      If 'None' is given (this is the default), it is considered the same as a
      tuple with all possible values.

    gender
      The gender to consider ('female', 'male')

    Returns: A list of files which have the given properties.
    """

    protocol = self.check_parameters_for_validity(protocol, "protocol", self.protocol_names())
    groups = self.check_parameters_for_validity(groups, "group", self.groups())
    gender = self.check_parameters_for_validity(gender, "gender", ('male', 'female'))

    import six
    if (model_ids is None):
      model_ids = ()
    elif (isinstance(model_ids, six.string_types)):
      model_ids = (model_ids,)

    # Now query the database
    q = self.query(File).join(Client).join((ProtocolPurpose, File.protocolPurposes)).join(Protocol).\
          filter(and_(Protocol.name.in_(protocol), ProtocolPurpose.sgroup.in_(groups), ProtocolPurpose.purpose == 'znorm'))
    if model_ids:
      q = q.filter(Client.id.in_(model_ids))
    if len(gender) == 1:
      q = q.filter(Client.gender.in_(gender))
    q = q.order_by(File.path, File.client_id)
    return list(q)

  def protocol_names(self):
    """Returns all registered protocol names"""

    return [str(p.name) for p in self.protocols()]

  def protocols(self):
    """Returns all registered protocols"""

    return list(self.query(Protocol))

  def has_protocol(self, name):
    """Tells if a certain protocol is available"""

    return self.query(Protocol).filter(Protocol.name==name).count() != 0

  def protocol(self, name):
    """Returns the protocol object in the database given a certain name. Raises
    an error if that does not exist."""

    return self.query(Protocol).filter(Protocol.name==name).one()

  def protocol_purposes(self):
    """Returns all registered protocol purposes"""

    return list(self.query(ProtocolPurpose))

  def purposes(self):
    """Returns the list of allowed purposes"""

    return ProtocolPurpose.purpose_choices


