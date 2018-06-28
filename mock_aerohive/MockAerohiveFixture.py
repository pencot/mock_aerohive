try:
    import pytest
except ImportError:
    class pytest:
        @staticmethod
        def fixture(fix):
            def wrappedFixture():
                raise ImportError("pytest is required to use the MockAerohiveFixture.")
            return wrappedFixture

import mock_aerohive.MockAerohive

@pytest.fixture(scope="session")
def MockAerohive():
    """A PyTest fixture to create new MockAerohive instances.
    Terminates the thread running the SSH servers when all tests have completed.

    Servers continue running when tests complete!
    You must call ``instance.stop()`` inside your test to kill each SSH server
    if you want to free the port and prevent future connections.
    (This fixture assumes that you will be generating random ports for each server,
     to prevent collisions if a server doesn't terminate.)
    """
    instances = []

    def _create_mock_aerohive(*args, **kwargs):
        instance = mock_aerohive.MockAerohive(*args, **kwargs)
        instances.append(instance)
        return instance

    yield _create_mock_aerohive

    for instance in instances:
        if instance.reactor_running:
            try:
                raise instance.stopAll()
            except Exception as e:
                print("Issue stopping reactor: " + e)
            break
