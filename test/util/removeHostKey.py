import pexpect

def removeIP(ip, port=22):
    command = "ssh-keygen -f \"$HOME/.ssh/known_hosts\" -R [" + ip + "]:" + str(port)
    print(command)
    removal = pexpect.spawn(command)
    index = removal.expect_exact(["updated.", "not found in"])
    if index != 1:
        removal.expect_exact("Original contents retained as")
    removal.expect_exact(pexpect.EOF)
