import pytest
from kivy_dashboard import login
from pathlib import Path


@pytest.mark.parametrize("input", ["", "tests", "username", "."])
def test_invalid_username(input):
    assert not login.Credentials(input).validate_username()


def test_valid_username(tmpdir):
    with tmpdir.as_cwd():
        salt_file_path = tmpdir / "test_user"
        salt_file_path.mkdir()
        slat_file = salt_file_path / "salt.txt"
        slat_file.write_text("This is a test user", encoding="UTF-8")
        assert login.Credentials("test_user").validate_username()


def test_generate_salt():
    assert len(login.Credentials().generate_salt()) == 8


def test_create_user(tmpdir):
    with tmpdir.as_cwd():
        login.Credentials("test_user").create_user("password")
        assert Path(tmpdir / "test_user").exists()
        assert Path(tmpdir / "test_user" / "salt.txt").exists()
        assert Path(tmpdir / "test_user" / "password.txt").exists()
        assert login.Credentials("test_user").validate_user("password")
        assert not login.Credentials("test_user").validate_user("incorrect_password")