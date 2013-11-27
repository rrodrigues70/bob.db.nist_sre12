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

"""This script creates the NIST SRE 2012 database in a single pass.
"""

import os

from .models import *

def add_files(session, all_files, verbose):
  """Add files to the NIST SRE 2012 database."""
  
  def add_client(session, id, gender, verbose):
    """Add a client to the database"""
    if verbose>1: print("  Adding client '%s'..." %(id,))
   
    client = Client(id, gender)
    session.add(client)
    session.flush()
    session.refresh(client)
    return client

  def add_file(session, c_id, path, verbose):
    """Parse a single filename and add it to the list.
       Also add a client entry if not already in the database."""
    if verbose>1: print("  Adding file '%s'..." %(path,))
    file_ = File(c_id, path)
    session.add(file_)
    session.flush()
    session.refresh(file_)
    return file_

  client_dict = {}
  file_dict = {}
  f = open(all_files)
  for line in f:
    path, c_id, gender = line.split()
    # Append gender information to client id
    # since there are lots of wrong gender information
    if gender == 'male': c_id = c_id + '_M'
    elif gender == 'female': c_id = c_id + '_F'
    else: raise RuntimeError("Gender unknown while parsing line '%s'." % line.strip())
    if not c_id in client_dict:
      client_dict[c_id] = add_client(session, c_id, gender, verbose)
    if not path in file_dict:
      file_dict[path] = add_file(session, c_id, path, verbose)
  return (file_dict, client_dict)

def add_protocols(session, protocol_dir, file_dict, client_dict, verbose):
  """Adds protocols"""

  tclient_dict = {}
  protocols = os.listdir(protocol_dir)

  # 2. ADDITIONS TO THE SQL DATABASE
  protocolPurpose_list = [('world', 'train', 'norm/train_world.lst'), ('optional_world_1', 'train', 'norm/train_optional_world_1.lst'), ('optional_world_2', 'train', 'norm/train_optional_world_2.lst'), ('dev', 'enrol', 'dev/for_models.lst'), ('dev', 'probe', 'dev/for_probes.lst'), ('dev', 'tnorm', 'dev/for_tnorm.lst'), ('dev', 'znorm', 'dev/for_znorm.lst'), ('eval', 'enrol', 'eval/for_models.lst'), ('eval', 'probe', 'eval/for_probes.lst'), ('eval', 'tnorm', 'dev/for_tnorm.lst'), ('eval', 'znorm', 'dev/for_znorm.lst')]
  for proto in protocols:
    p = Protocol(proto)
    # Add protocol
    if verbose>1: print("Adding protocol %s..." % (proto))
    session.add(p)
    session.flush()
    session.refresh(p)

    # Add protocol purposes
    for key in range(len(protocolPurpose_list)):
      purpose = protocolPurpose_list[key]
      pu = ProtocolPurpose(p.id, purpose[0], purpose[1])
      if verbose>1: print("  Adding protocol purpose ('%s','%s')..." % (purpose[0], purpose[1]))
      session.add(pu)
      session.flush()
      session.refresh(pu)

      pu_client_dict = {}
      pu_tclient_dict = {}
      # Add files attached with this protocol purpose
      f = open(os.path.join(protocol_dir, proto, purpose[2]))
      for line in f:
        path = line.split()[0]
        if (path in file_dict):      
          if verbose>1: print("    Adding protocol file '%s'..." % (path, ))
          pu.files.append(file_dict[path])
          c_id = file_dict[path].client_id
          # If T-Norm client does not exist, add it to the database
          if not c_id in pu_tclient_dict and purpose[1] == 'tnorm':
            if verbose>1: print("    Adding protocol T-client '%s'..." % (c_id, ))
            if not c_id in tclient_dict:
              tclient = TClient(c_id, proto)
              session.add(tclient)
              session.flush()
              session.refresh(tclient)
              tclient_dict[c_id] = tclient
            pu.tclients.append(tclient_dict[c_id])
            pu_tclient_dict[c_id] = tclient_dict[c_id]
          # If T-Norm files is not associated to its client, do it
          if purpose[1] == 'tnorm':
            if not path in [k.path for k in tclient_dict[c_id].files]:
              tclient_dict[c_id].files.append(file_dict[path])
          # If Client does not exist, add it to the database
          if not c_id in pu_client_dict:
            if verbose>1: print("    Adding protocol client '%s'..." % (c_id, ))
            if c_id in client_dict:
              pu.clients.append(client_dict[c_id])
              pu_client_dict[c_id] = client_dict[c_id]
            else:
              raise RuntimeError("Client '%s' is in the protocol list but not in the database" % c_id)
        else:
          raise RuntimeError("File '%s' is in the protocol list but not in the database" % path)
            

def create_tables(args):
  """Creates all necessary tables (only to be used at the first time)"""

  from bob.db.utils import create_engine_try_nolock

  engine = create_engine_try_nolock(args.type, args.files[0], echo=(args.verbose > 2))
  Base.metadata.create_all(engine)

# Driver API
# ==========

def create(args):
  """Creates or re-creates this database"""

  from bob.db.utils import session_try_nolock

  dbfile = args.files[0]

  if args.recreate:
    if args.verbose and os.path.exists(dbfile):
      print('unlinking %s...' % dbfile)
    if os.path.exists(dbfile): os.unlink(dbfile)

  if not os.path.exists(os.path.dirname(dbfile)):
    os.makedirs(os.path.dirname(dbfile))

  # the real work...
  create_tables(args)
  s = session_try_nolock(args.type, args.files[0], echo=(args.verbose > 2))
  file_dict, client_dict = add_files(s, os.path.join(args.datadir, 'all_files.lst'), args.verbose)
  add_protocols(s, os.path.join(args.datadir, 'protocols'), file_dict, client_dict, args.verbose)
  s.commit()
  s.close()

def add_command(subparsers):
  """Add specific subcommands that the action "create" can use"""

  parser = subparsers.add_parser('create', help=create.__doc__)

  parser.add_argument('-R', '--recreate', action='store_true', help="If set, I'll first erase the current database")
  parser.add_argument('-v', '--verbose', action='count', help="Do SQL operations in a verbose way")
  from pkg_resources import resource_filename
  prism_basedir = 'prism'
  prism_path = resource_filename(__name__, prism_basedir)
  parser.add_argument('-D', '--datadir', metavar='DIR', default=prism_path, help="Change the path to the containing information about the NIST SRE 2012 database.")

  parser.set_defaults(func=create) #action
