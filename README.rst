Mock Aerohive
-------------
.. image:: https://img.shields.io/pypi/v/mock-aerohive.svg
  :target: https://pypi.org/project/mock-aerohive/

.. image:: https://gitlab.com/pencot/mock_aerohive/badges/master/pipeline.svg
  :target: https://github.com/pencot/mock_aerohive/commits/master

.. image:: https://codecov.io/gh/pencot/mock_aerohive/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/pencot/mock_aerohive

.. image:: https://img.shields.io/pypi/pyversions/mock_aerohive.svg
  :target: https://pypi.org/project/mock-aerohive/

A mock SSH server emulating Aerohive devices.

Install::

  pip install mock-aerohive

Basic usage::

  from mock_aerohive import MockAerohive

  aerohive = MockAerohive()
  # You must add at least 1 user before starting the server!  (Library limitation)
  aerohive.addUser("admin", "aerohive")

  port = aerohive.run("127.0.0.1")
  # Or provide a port: aerohive.run("127.0.0.1", 2222)

  # Now you can SSH in:
  # ssh admin@127.0.0.1 -p 2222

  aerohive.stop() # Stop a single server.

  aerohive.stopAll() # Terminate the background thread running all SSH servers (otherwise the process will hang)
                     # Once you stop the background thread, you may not start another server (with 'run') -
                     # another library limitation.

For an example of a py.test fixture that automates starting and stopping servers
(which cleans up servers at the end of the testing session, but allows multiple servers to be run),
see ``test/util/MockAerohiveFixture.py``, and ``test/integration/auth/test_addUser_and_login.py`` for an example.

Some Aerohive commands have been created, for instance, ``hostname``::

  ssh admin@127.0.0.1 -p 2222
  admin@127.0.0.1's password:
  Aerohive Networks Inc.
  Copyright (C) 2006-2012
  AH-2A0B00#hostname example-1
  example-1#example-1#hostname example-2 invalid-extra-argument
                                         ^-- unknown keyword or invalid input
  example-1#exit
  Connection to 127.0.0.1 closed.

Versioning
^^^^^^^^^^

This package uses semantic versioning.
