from datetime import datetime, timedelta
from config.private_data import *
from colorama import Fore, Style
from code.desktop_operations import *
from code.gui_operations import GUIHandler
from miscellaneous.messages import *

today = datetime.today()
today_formatted = today.strftime("%d.%m.%Y")
print("Application started:", today_formatted)

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


def prepare_and_deliver_notifications_missing_declarations(declarations_file):
    print("Preparing notifications about missing declarations")
    if len(declarations_file) == 0:
        print("Nothing to send. Skipping this step")
    else:
        notifications_dict = {}
        for participant in participants:
            dates_range_list = []
            for item in declarations_file:
                i = item[0].split(":")
                recipient = i[0]
                day = i[1]
                if recipient == participant:
                    dates_range_list.append(day)
            messages_list = [
                messages_dict["message_welcome_declarations"] % participant,
                string_appender(strings_list=dates_range_list)
            ]
            if len(dates_range_list) == 0:
                pass
            else:
                receiver = {"%s" % facebook_users_dict[participant]: messages_list}
                notifications_dict.update(receiver)
        send_notifications_via_messenger(notifications_dict=notifications_dict)


def prepare_and_deliver_notifications_session_is_coming():
    next_session_content = return_content_of_json_file(json_file=file_next_session)
    next_session = next_session_content[0]["Termin"]
    date_format = "%d.%m.%Y %H:%M"
    date_next_session = datetime.strptime(next_session, date_format)
    print("Preparing notifications about incoming session")
    if date_next_session + timedelta(days=1) == today + timedelta(days=1):
        notifications_dict = {}
        for participant in participants:
            messages_list = [
                messages_dict["message_welcome_session_incoming"] % (participant,
                                                                     next_session[slice(10, 16)])
            ]
            receiver = {"%s" % facebook_users_dict[participant]: messages_list}
            notifications_dict.update(receiver)
        send_notifications_via_messenger(notifications_dict=notifications_dict)
    else:
        print("Next session is too far into the future to notify about it at the moment")


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


def print_result_of_checks_if_any(title, content_list):
    if len(content_list) == 0:
        pass
    else:
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
    print("Possible session candidates check completed. Found:", len(list_possible_candidates))
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
    print("Missing declarations check completed. Found:", len(list_missing_declarations))
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
        answer = day[participant]
        if answer == "nie":
            return True


def is_declaration_in_acceptable_format(declaration):
    if declaration not in ["tak", "nie"]:
        return False


def return_missing_declarations(day):
    not_declared = []
    for participant in participants:
        declaration = day[participant]
        if len(declaration) == 0:
            print(Fore.RED + "%s did not declare their availability" % participant +
                  Style.RESET_ALL)
            not_declared.append("%s:%s" % (participant, day["Termin"]))
        elif is_declaration_in_acceptable_format(declaration=declaration) is False:
            print(Fore.RED + "%s provided declaration in unacceptable format: %s" %
                  (participant, declaration) + Style.RESET_ALL)
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


def send_notifications_via_messenger(notifications_dict):
    if len(notifications_dict) == 0:
        pass
    else:
        notificator = GUIHandler()
        notificator.log_into_messenger()
        for facebook_user in notifications_dict:
            print("Sending notification to", facebook_user)
            notificator.select_user_via_sidebar(username=facebook_user)
            notificator.send_messages(messages_list=notifications_dict[facebook_user])
            notificator.quit()
    print("All notifications sent")
