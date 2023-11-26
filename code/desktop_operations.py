from json import loads, dumps
import os
import logging

desktop = os.path.join(os.path.join(os.environ["UserPROFILE"]), "Desktop")
file_possible_sessions_json = desktop + "\\json_files\\possible_sessions.json"
file_dates_without_declarations = desktop + "\\json_files\\dates_without_declarations.json"
file_next_session = desktop + "\\json_files\\next_session.json"
file_logs = desktop + "\\logs\\RPG_manager.log"


def update_json_file(json_file, content):
    create_json_files_directory_if_needed()
    with open(json_file, "w+") as file:
        try:
            file_content = loads(file.read())
        except BaseException:
            file_content = content
        dict_list = file_content
        file_content = dumps(dict_list, indent=4)
        file.write(file_content)
        print("File updated:", json_file)


def return_content_of_json_file(json_file):
    print("Reading the content of", json_file)
    try:
        with open(json_file, "r") as file:
            file_content = loads(file.read())
            return file_content
    except FileNotFoundError:
        print("File was not found")


def update_log_file():
    logging.basicConfig(filename="RPG_Manager.log", level=logging.DEBUG)
    logging.info("Starting the logging process")


def create_json_files_directory_if_needed():
    path = desktop + "\\json_files"
    is_exists = os.path.exists(path)
    print(is_exists)
    if is_exists is True:
        pass
    else:
        os.mkdir(path)
