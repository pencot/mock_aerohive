import pytest

import mock_aerohive.MockAerohive

@pytest.fixture(scope="session")
def MockAerohive():
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
