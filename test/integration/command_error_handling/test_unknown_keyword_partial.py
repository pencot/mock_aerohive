import pexpect
import MockSSH

from test.util.MockAerohiveFixture import MockAerohive

# Create a fake command for testing.
# Syntax: #foobar [foo|foobar|baz]
def add_foobar(server):
    subcommands = ["foo", "foobar", "baz"]
    class command_foobar(MockSSH.SSHCommand):
        name = "foobar"
        def start(self):
            if len(self.args) < 1:
                self.writeln(INCOMPLETE_COMMAND)
            elif self.args[0] not in subcommands:
                self.writeln(server.unknownKeyword("foobar", self.args, 0, subcommands))
            elif(len(self.args) > 1):
                self.writeln(server.unknownKeyword("foobar", self.args, 1, []))
            else:
                self.writeln("correct")
            self.exit()
    return command_foobar

def connect_set_prompt(aerohive, username, password, hostname):
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
    connection.sendline("hostname " + hostname)
    connection.expect_exact("example-1#")
    return connection

def test_wrong_ending(MockAerohive):
    username = "admin"
    password = "aerohive"
    aerohive = MockAerohive()
    aerohive.addUser(username, password)
    aerohive.commands.append(add_foobar(aerohive))

    connection = connect_set_prompt(aerohive, username, password, "example-1")

    connection.expect_exact("example-1#")
    connection.sendline("foobar bazz")
    #        example-1#foobar bazz
    error = "                    ^-- unknown keyword or invalid input"
    connection.expect_exact(error)

    connection.expect_exact(aerohive.prompt())
    connection.sendline("exit")
    connection.expect_exact("closed.")
    connection.expect_exact(pexpect.EOF)

def test_two_possible(MockAerohive):
    username = "admin"
    password = "aerohive"
    aerohive = MockAerohive()
    aerohive.addUser(username, password)
    aerohive.commands.append(add_foobar(aerohive))

    connection = connect_set_prompt(aerohive, username, password, "example-1")

    connection.expect_exact("example-1#")
    connection.sendline("foobar fo1")
    #        example-1#foobar fo1
    error = "                   ^-- unknown keyword or invalid input"
    connection.expect_exact(error)

    connection.expect_exact(aerohive.prompt())
    connection.sendline("exit")
    connection.expect_exact("closed.")
    connection.expect_exact(pexpect.EOF)

def test_one_fork(MockAerohive):
    username = "admin"
    password = "aerohive"
    aerohive = MockAerohive()
    aerohive.addUser(username, password)
    aerohive.commands.append(add_foobar(aerohive))

    connection = connect_set_prompt(aerohive, username, password, "example-1")

    connection.expect_exact("example-1#")
    connection.sendline("foobar foob1")
    #        example-1#foobar foob1
    error = "                     ^-- unknown keyword or invalid input"
    connection.expect_exact(error)

    connection.expect_exact(aerohive.prompt())
    connection.sendline("exit")
    connection.expect_exact("closed.")
    connection.expect_exact(pexpect.EOF)

def test_completely_wrong(MockAerohive):
    username = "admin"
    password = "aerohive"
    aerohive = MockAerohive()
    aerohive.addUser(username, password)
    aerohive.commands.append(add_foobar(aerohive))

    connection = connect_set_prompt(aerohive, username, password, "example-1")

    connection.expect_exact("example-1#")
    connection.sendline("foobar foob1")
    #        example-1#foobar z
    error = "                 ^-- unknown keyword or invalid input"
    connection.expect_exact(error)

    connection.expect_exact(aerohive.prompt())
    connection.sendline("exit")
    connection.expect_exact("closed.")
    connection.expect_exact(pexpect.EOF)
