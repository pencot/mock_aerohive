from mock_aerohive import MockAerohive

def test_custom_hostname():
    aerohive = MockAerohive()
    aerohive.hostname = "my-device"
    assert aerohive.prompt() == "my-device#"
