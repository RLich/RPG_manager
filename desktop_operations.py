from json import loads, dumps
import os

work_dir = os.getcwd()
file_possible_sessions_json = work_dir + "\\possible_sessions.json"
file_dates_without_declarations = work_dir + "\\dates_without_declarations.json"


def update_json_file(json_file, content):
    with open(json_file, "w+") as file:
        try:
            file_content = loads(file.read())
        except BaseException:
            file_content = content
        dict_list = file_content
        file_content = dumps(dict_list, indent=4)
        file.write(file_content)
        print("File updated:", json_file)
