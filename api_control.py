import gspread
from datetime import date
from private_data import *
import config
from colorama import Fore, Style
from desktop_operations import *
from gui_operations import GUIHandler

service_account = gspread.service_account()
sheet = service_account.open("Terminy RPG")

worksheet = sheet.worksheet("Dostepnosc")

today = date.today()
today_formatted = today.strftime("%d.%m.%Y")
print("Today is:", today_formatted)

table = worksheet.get_all_records()


def return_rows_given_days_from_today(days):
    temp_list = []
    day_counter = 0
    row_counter = 0
    for row in table:
        row_counter += 1
        if row["Termin"] == today_formatted:
            temp_list.append(row)
            while day_counter < days:
                temp_list.append(table[row_counter])
                row_counter += 1
                day_counter += 1
            break
    return temp_list


def application():
    days = config.number_of_days_to_check
    rows_list = return_rows_given_days_from_today(days=days)
    prepared_data = remove_redundant_columns_and_unify_responses(data=rows_list,
                                                                 fields_to_remove=["Termin?"])
    possible_sessions = create_possible_session_candidates(dates_range=prepared_data)
    update_json_file(json_file=file_possible_sessions_json, content=possible_sessions)
    missing_declarations = create_missing_declarations(dates_range=prepared_data)
    update_json_file(json_file=file_dates_without_declarations, content=missing_declarations)
    print_result_of_checks(title="Missing declarations:", content_list=missing_declarations)
    print_result_of_checks(title="Session candidates:", content_list=possible_sessions)
    prepare_and_deliver_notifications_missing_declarations(
        declarations_file=return_content_of_json_file(
            json_file=file_dates_without_declarations))


def prepare_and_deliver_notifications_missing_declarations(declarations_file):
    print("Preparing notifications")
    for participant in participants:
        dates_range_list = []
        for item in declarations_file:
            i = item[0].split(":")
            recipient = i[0]
            day = i[1]
            if recipient == participant:
                dates_range_list.append(day)
        message_welcome = "Cześć %s, tutaj twój ulubiony bot - binarny avatar RPG. " \
                          "Chciałbym przypomnieć o wpisaniu Twojej dostępności do arkusza. " \
                          "Terminy, których nie uzupełniłeś:" % participant
        message_dates = string_appender(strings_list=dates_range_list)
        if len(dates_range_list) == 0:
            pass
        else:
            send_notifications_via_messenger(facebook_usernames=[facebook_users_dict[participant]],
                                             text_list=[message_welcome, message_dates])


def string_appender(strings_list):
    final_string = ""
    counter = 0
    for string in strings_list:
        if counter == 0:
            final_string = final_string + string
        else:
            final_string = final_string + "; " + string
        counter += 1
    return final_string


def print_result_of_checks(title, content_list):
    print(title)
    for item in content_list:
        print(item)


def create_possible_session_candidates(dates_range):
    print("Checking possible session candidates for range: %s to %s" % (dates_range[0]["Termin"],
                                                                        dates_range[-1]["Termin"]))
    list_possible_candidates = []
    for row in dates_range:
        print("Checking:", row["Termin"])
        if is_session_possible_given_day_bool(day=row) is not False:
            list_possible_candidates.append(row)
    return list_possible_candidates


def create_missing_declarations(dates_range):
    print("Checking missing declarations for range: %s to %s" % (dates_range[0]["Termin"],
                                                                 dates_range[-1]["Termin"]))
    list_missing_declarations = []
    for row in dates_range:
        print("Checking:", row["Termin"])
        missing_declarations_from_given_day = return_missing_declarations(day=row)
        if len(missing_declarations_from_given_day) > 0:
            list_missing_declarations.append(missing_declarations_from_given_day)
        else:
            print("Missing declarations not found")
    return list_missing_declarations


def is_session_possible_given_day_bool(day):
    if is_there_at_least_one_no_bool(day=day) is True:
        return False
    elif len(return_missing_declarations(day=day)) > 0:
        print(Fore.RED + "No-one is opposing %s yet, but one or more participants "
                         "did not declare their availability" % day["Termin"] + Style.RESET_ALL)
        return False
    else:
        print(Fore.GREEN + "Possible session candidate:", day["Termin"] + Style.RESET_ALL)


def is_there_at_least_one_no_bool(day):
    for participant in participants:
        print(day[participant])
        answer = day[participant]
        if answer == "nie":
            return True


def return_missing_declarations(day):
    not_declared = []
    for participant in participants:
        if len(day[participant]) == 0:
            print(Fore.RED + "%s did not declare their availability" % participant +
                  Style.RESET_ALL)
            not_declared.append("%s:%s" % (participant, day["Termin"]))
    return not_declared


def remove_redundant_columns_and_unify_responses(data, fields_to_remove):
    for row in data:
        for field in fields_to_remove:
            try:
                row.pop(field)
            except BaseException:
                pass
        for participant in participants:
            declaration = row[participant]
            new_declaration = {'%s' % participant: '%s' % declaration.lower()}
            row.update(new_declaration)
    return data


def send_notifications_via_messenger(text_list, facebook_usernames):
    notificator = GUIHandler()
    notificator.log_into_messenger()
    for facebook_username in facebook_usernames:
        notificator.select_user_via_sidebar(username=facebook_username)
        notificator.send_messages(messages_list=text_list)
        notificator.quit()


application()
