import pexpect

from test.util.MockAerohiveFixture import MockAerohive

def test_stop_server(MockAerohive):
    username = "admin"
    password = "aerohive"
    aerohive = MockAerohive()
    aerohive.addUser(username, password)
    port = aerohive.run("127.0.0.1")

    alive = pexpect.spawn(
        "ssh -o ConnectTimeout=1 -o UserKnownHostsFile=/dev/null \"" + username + "@" + "127.0.0.1\" -p " + str(port),
        timeout=5
    )
    index = alive.expect_exact(["Connection refused", "Connection timed out", "continue connecting"])
    if index != 2:
        raise Exception("Server is not alive.")
    alive.terminate(force=True)

    aerohive.stop()

    dead = pexpect.spawn(
        "ssh -o ConnectTimeout=1 -o UserKnownHostsFile=/dev/null \"" + username + "@" + "127.0.0.1\" -p " + str(port),
        timeout=5
    )
    index = dead.expect_exact(["Connection refused", "Connection timed out", "continue connecting"])
    if index == 2:
        raise Exception("Server is still alive.")
    dead.expect_exact(pexpect.EOF)
