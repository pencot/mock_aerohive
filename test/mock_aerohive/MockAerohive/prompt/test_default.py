from mock_aerohive import MockAerohive

# The default device prompt is the last few characters of a MAC address,
# prefixed with "AH-".
def test_default_prompt_format():
    aerohive = MockAerohive()
    prompt = aerohive.prompt()
    assert prompt[:3] == "AH-"

# Prompt should end with "#".
def test_default_prompt_ending():
    aerohive = MockAerohive()
    prompt = aerohive.prompt()
    assert prompt[-1:] == "#"
