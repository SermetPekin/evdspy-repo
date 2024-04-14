from pathlib import Path
import os
from evdspy.EVDSlocal.common.files import Write, Read
import base64

api_key_folder_name = Path() / "APIKEY_FOLDER"
api_key_file_name = api_key_folder_name / "api_key.txt"


def decode(base64_bytes) -> str:
    if isinstance(base64_bytes, str):
        base64_bytes = str.encode(base64_bytes)
    str_bytes = base64.b64decode(base64_bytes)
    decoded = str_bytes.decode("ascii")
    return decoded


def encode(text: str) -> bytes:
    t_bytes = text.encode("ascii")
    encoded = base64.b64encode(t_bytes)
    return encoded


def WriteBytes(file_name: str, content_bytes: bytes):
    with open(file_name, 'wb') as f:
        f.write(content_bytes)


def ReadBytes(file_name: str):
    with open(file_name, "rb") as f:
        return f.read()


from evdspy.EVDSlocal.config.apikey_class import ApikeyClass


# def check_key_before_saving(instance, api_key_answer: str):
#     ApikeyClass().now_testing_is_key_is_valid = api_key_answer
#     return instance.check_api_key_with_simple_Wrapper()


def save_api_key_to_file(instance, api_key_answer):
    instance.wait(1)

    if not api_key_folder_name.is_dir():
        os.makedirs(api_key_folder_name)
    # api_key_answer = instance.get_input("Your api key : ")
    # Write(api_key_file_name, str(encode(api_key_answer)), "")

    WriteBytes(str(api_key_file_name), encode(api_key_answer))
    # test for file api key for runtime (temp)
    ApikeyClass().set_api_key_filetype(value=api_key_answer)

    # ApikeyClass().now_testing_is_key_is_valid = api_key_answer
    print("your api file was saved...")
    instance.wait(1)
    # instance.set_apikey(api_key_answer)
    api_key_from_file = get_api_key_from_file_improved()
    return api_key_from_file


def get_api_key_from_file_improved():
    if not api_key_file_name.is_file():
        return False

    def read_api_file():
        content = ReadBytes(str(api_key_file_name))
        return content

    pot_key = read_api_file()
    if pot_key:
        return decode(pot_key)
    return False


def check_api_key_on_load():
    """ not compatible 3.8-"""
    # if api_key := get_api_key_from_file_improved():
    #     ApikeyClass().set_api_key_filetype(value=api_key)
    """changing to this"""
    api_key = get_api_key_from_file_improved()
    if api_key:
        ApikeyClass().set_api_key_filetype(value=api_key)
