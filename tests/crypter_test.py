"""The collections of the tests for the crypter.py module"""
import builtins
import os

from tools.crypter import Crypter
from tools.file_management import File
from tools.protection import Protection


def test_encrypt_file(mocker):
    """Check that the data from the unencrypted file is encrypted and saved correctly"""
    example_file_path = 'example_folder/file.txt'
    fake_encrypted_data = 'gAABj0YLPHaoW=='
    example_read_data = ' data1@./? '
    crypter = Crypter('password')

    mocker.patch.object(Protection, 'encrypt', return_value=fake_encrypted_data)
    mocker.patch.object(File, 'load', return_value=example_read_data)
    mocker.patch.object(File, 'save')

    crypter.encrypt(example_file_path)

    Protection.encrypt.assert_called_once_with(example_read_data)
    File.load.assert_called_once()
    File.save.assert_called_once_with(fake_encrypted_data)


def test_file_extension_after_encrypt(mocker):
    """Check that the extension file is changed to '.cr' after encrypt"""
    example_file_path = 'example_folder/file.txt'
    crypter = Crypter('password')

    mocker.patch.object(builtins, 'open', new=mocker.mock_open())
    mocker.patch.object(Protection, 'encrypt')
    mocker.patch.object(File, 'load')

    crypter.encrypt(example_file_path)

    builtins.open.assert_called_once_with(
        example_file_path + '.cr',
        'w',
        encoding='utf-8',
    )
    Protection.encrypt.assert_called_once()
    File.load.assert_called_once()


def test_file_extension_after_decrypt(mocker):
    """Check that the '.cr' extension is removed after decrypt"""
    example_file_path = 'example_folder/file.txt.cr'
    crypter = Crypter('password')

    mocker.patch.object(builtins, 'open', new=mocker.mock_open())
    mocker.patch.object(Protection, 'decrypt')
    mocker.patch.object(File, 'load')

    crypter.decrypt(example_file_path)

    builtins.open.assert_called_once_with(
        example_file_path[:-3],
        'w',
        encoding='utf-8',
    )
    Protection.decrypt.assert_called_once()
    File.load.assert_called_once()


def test_append_new_data_to_encrypted_file(mocker):
    """Check that the data from the encrypted file is decrypted,
    append new data, encrypt again and save to the encrypted file"""
    example_encrypted_file = 'encrypted.txt.cr'
    example_unencrypted_file = 'unencrypted.txt'
    crypter = Crypter('pAss12@;!')

    mocker.patch.object(Protection, 'encrypt', return_value='abced==')
    mocker.patch.object(Protection, 'decrypt', return_value='decrypted data')
    mocker.patch.object(File, 'load', side_effect=(
        'some text',
        'gAABPHaoW==',
    ))
    mocker.patch.object(File, 'save')

    crypter.append(example_encrypted_file, example_unencrypted_file)

    Protection.encrypt.assert_called_once_with('decrypted data' + 'some text')
    Protection.decrypt.assert_called_once_with('gAABPHaoW==')
    File.save.assert_called_once_with('abced==')
    assert File.load.call_count == 2


def test_parent_file_has_been_removed_after_encrypt(mocker):
    """Check that the parent file is removed after encrypting
    when the remove option is chosen"""
    example_file_path = 'example_folder/file.txt'
    crypter = Crypter('password', remove_parent_file=True)

    mocker.patch.object(Protection, 'encrypt')
    mocker.patch.object(File, 'load')
    mocker.patch.object(File, 'save')
    mocker.patch.object(os, 'remove')

    crypter.encrypt(example_file_path)

    Protection.encrypt.assert_called_once()
    File.load.assert_called_once()
    File.save.assert_called_once()
    os.remove.assert_called_once_with(example_file_path)


def test_parent_file_has_been_removed_after_decrypt(mocker):
    """Check that the parent file is removed after decrypting
    when the remove option is chosen"""
    example_file_path = 'example_folder/file.txt.cr'
    crypter = Crypter('password', remove_parent_file=True)

    mocker.patch.object(Protection, 'decrypt')
    mocker.patch.object(File, 'load')
    mocker.patch.object(File, 'save')
    mocker.patch.object(os, 'remove')

    crypter.decrypt(example_file_path)

    Protection.decrypt.assert_called_once()
    File.load.assert_called_once()
    File.save.assert_called_once()
    os.remove.assert_called_once_with(example_file_path)


def test_parent_file_has_been_removed_after_append(mocker):
    """Check that the unencrypted file is removed after append new data
    when the remove option is chosen"""
    example_encrypted_file = 'encrypted.txt.cr'
    example_unencrypted_file = 'unencrypted.txt'
    crypter = Crypter('password', remove_parent_file=True)

    mocker.patch.object(Protection, 'decrypt')
    mocker.patch.object(Protection, 'encrypt')
    mocker.patch.object(File, 'load', return_data='some text')
    mocker.patch.object(File, 'save')
    mocker.patch.object(os, 'remove')

    crypter.append(example_encrypted_file, example_unencrypted_file)

    Protection.encrypt.assert_called_once()
    Protection.decrypt.assert_called_once()
    File.save.assert_called_once()
    os.remove.assert_called_once_with(example_unencrypted_file)
    assert File.load.call_count == 2


def test_parent_file_has_not_been_removed_after_encrypt(mocker):
    """Check that the parent file isn't removed after encrypting
    when the remove option is chosen as False"""
    example_file_path = 'example_folder/file.txt'
    crypter = Crypter('password', remove_parent_file=False)

    mocker.patch.object(Protection, 'encrypt')
    mocker.patch.object(File, 'load')
    mocker.patch.object(File, 'save')
    mocker.patch.object(os, 'remove')

    crypter.encrypt(example_file_path)

    Protection.encrypt.assert_called_once()
    File.load.assert_called_once()
    File.save.assert_called_once()
    os.remove.assert_not_called()


def test_parent_file_has_not_been_removed_after_decrypt(mocker):
    """Check that the parent file isn't removed after decrypting
    when the remove option is chosen as False"""
    example_file_path = 'example_folder/file.txt'
    crypter = Crypter('password', remove_parent_file=False)

    mocker.patch.object(Protection, 'decrypt')
    mocker.patch.object(File, 'load')
    mocker.patch.object(File, 'save')
    mocker.patch.object(os, 'remove')

    crypter.decrypt(example_file_path)

    Protection.decrypt.assert_called_once()
    File.load.assert_called_once()
    File.save.assert_called_once()
    os.remove.assert_not_called()


def test_parent_file_has_not_been_removed_after_append(mocker):
    """Check that the unencrypted file isn't removed after append new data
    when the remove option is chosen as False"""
    example_encrypted_file = 'encrypted.txt.cr'
    example_unencrypted_file = 'unencrypted.txt'
    crypter = Crypter('password', remove_parent_file=False)

    mocker.patch.object(Protection, 'encrypt')
    mocker.patch.object(Protection, 'decrypt')
    mocker.patch.object(File, 'load', return_data='some text')
    mocker.patch.object(File, 'save')
    mocker.patch.object(os, 'remove')

    crypter.append(example_encrypted_file, example_unencrypted_file)

    Protection.encrypt.assert_called_once()
    Protection.decrypt.assert_called_once()
    File.save.assert_called_once()
    os.remove.assert_not_called()
    assert File.load.call_count == 2
