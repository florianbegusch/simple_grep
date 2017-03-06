import os
import tempfile
import pytest


global temp_dir, fd, temp_path
temp_dir = tempfile.mkdtemp()
fd, temp_path = tempfile.mkstemp(dir=temp_dir, suffix='.txt', text=True)


@pytest.fixture(scope='session', autouse=True)
def remove_tempdir():
    yield None
    os.close(fd)
    os.remove(temp_path)
    os.removedirs(temp_dir)


@pytest.fixture(scope='function')
def with_f_read():
    f = open(temp_path, 'r')
    yield f
    f.close()


@pytest.fixture(scope='function')
def with_f_bread():
    f = open(temp_path, 'rb')
    yield f
    f.close()


@pytest.fixture(scope='function')
def with_f_write():
    f = open(temp_path, 'w')
    yield f
    f.close()


@pytest.fixture(scope='function')
def with_f_bwrite():
    f = open(temp_path, 'wb')
    yield f
    f.close()


@pytest.fixture(scope='function')
def with_permission_denied():
    f = open(temp_path, 'r')
    # Leading zero ensures int is treated as octal
    os.chmod(f.name, 0000)
    yield f.name

    # Leading zero ensures int is treated as octal
    os.chmod(f.name, 0777)
