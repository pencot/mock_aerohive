import pexpect

import mock_aerohive.MockAerohiveFixture as MockAerohive

def test_hostname_change(MockAerohive):
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
    connection.sendline("hostname example-1")
    connection.expect_exact("example-1#example-1#")
    connection.sendline("exit")
    connection.expect_exact("closed.")
    connection.expect_exact(pexpect.EOF)
