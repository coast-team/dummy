from collaborator.config_loader import ConfigLoader
from collaborator.dummy_error.configfile_error import ConfigfileError
import pytest
import os


@pytest.fixture
def get_well_formed_config_loader():
    # We assume the tests are launching from project's root
    dir_path_prefix = os.getcwd()
    path_prefix = '/config_files/config_test_success.ini'
    result_path = dir_path_prefix + path_prefix

    return ConfigLoader(result_path)


def test_load_default_config():
    config_loader = get_well_formed_config_loader()
    try:
        result = config_loader.getDefaultConfig()
    except ConfigfileError:
        assert False

    assert isinstance(result['port'], int)


def test_load_collaborator_config():
    config_loader = get_well_formed_config_loader()
    try:
        result = config_loader.getCollaboratorConfig()
    except ConfigfileError:
        assert False
    assert isinstance(result['waitingTime'], int)
    assert isinstance(result['loadingTime'], int)
    assert isinstance(result['noDisplay'], bool)


def test_load_mute_config():
    config_loader = get_well_formed_config_loader()
    try:
        result = config_loader.getMuteConfig()
    except ConfigfileError:
        assert False
    assert isinstance(result['refreshRate'], int)
    assert isinstance(result['writingSpeed'], int)
    assert isinstance(result['isBasicBehavior'], bool)
