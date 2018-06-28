from hypothesis import given, example, settings
from hypothesis.strategies import just
import pexpect

from mock_aerohive.MockAerohive import INCOMPLETE_COMMAND

import mock_aerohive.MockAerohiveFixture as MockAerohive

@given(command=just("hostname"))
@settings(max_examples=5, deadline=None)
@example(command="hostname ")
def test_incomplete_command(command, MockAerohive):
    username = "admin"
    password = "aerohive"
    aerohive = MockAerohive()
    aerohive.addUser(username, password)
    port = aerohive.run("127.0.0.1")

    connection = pexpect.spawn(
        "ssh -o UserKnownHostsFile=/dev/null \"" + username + "@" + "127.0.0.1\" -p " + str(port),
        timeout=5
    )
    connection.expect_exact("continue connecting (yes/no)? ")
    connection.sendline("yes")
    connection.expect_exact("assword: ")
    connection.sendline(password)
    connection.expect_exact(aerohive.prompt())
    connection.sendline(command)
    connection.expect_exact(INCOMPLETE_COMMAND)
    connection.expect_exact(aerohive.prompt())
    connection.sendline("exit")
    connection.expect_exact("closed.")
    connection.expect_exact(pexpect.EOF)
