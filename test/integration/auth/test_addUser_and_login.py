from hypothesis import given, example, settings

import pexpect

from test.util.MockAerohiveFixture import MockAerohive
from test.util.Strategies import username_strategy, password_strategy

@given(username=username_strategy, password=password_strategy)
@settings(max_examples=5, deadline=None)
@example(username="admin", password="aerohive")
@example(username="Bob", password="PASSWORD123456789!$#")
def test_login_with_user(username, password, MockAerohive):
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
    index = connection.expect_exact(["#", "denied"])
    if index == 1:
        raise Exception("Password rejected.")
    connection.sendline("exit")
    connection.expect_exact("closed.")
    connection.expect_exact(pexpect.EOF)
