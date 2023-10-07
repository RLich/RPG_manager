from code.api_operations import *
from config import config
from code.desktop_operations import *


def run_weekly():
    days = config.number_of_days_to_check
    rows_list = return_rows_given_days_from_today(days=days)
    prepared_data = remove_redundant_columns_and_unify_responses(data=rows_list,
                                                                 fields_to_remove=["Termin?"])
    possible_sessions = create_possible_session_candidates(dates_range=prepared_data)
    update_json_file(json_file=file_possible_sessions_json, content=possible_sessions)
    missing_declarations = create_missing_declarations(dates_range=prepared_data)
    update_json_file(json_file=file_dates_without_declarations, content=missing_declarations)
    print_result_of_checks_if_any(title="Missing declarations:", content_list=missing_declarations)
    print_result_of_checks_if_any(title="Session candidates:", content_list=possible_sessions)
    prepare_and_deliver_notifications_missing_declarations(
        declarations_file=return_content_of_json_file(
            json_file=file_dates_without_declarations))


run_weekly()
