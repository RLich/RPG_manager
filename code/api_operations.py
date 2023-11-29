from config.private_data import table_possible_sessions, potential_sessions_worksheet
from code.application import today

from datetime import datetime


def potential_sessions_operations():
    clean_potential_sessions_worksheet()


def clean_potential_sessions_worksheet():
    counter = 2
    for row in table_possible_sessions:
        date = row["Termin"]
        date_format = "%d.%m.%Y %H:%M"
        date_potential_session = datetime.strptime(date, date_format)
        if date_potential_session < today:
            counter = str(counter)
            cell_list = potential_sessions_worksheet.range("A%s:E%s" % (counter, counter))
            for cell in cell_list:
                cell.value = ""
            potential_sessions_worksheet.update_cells(cell_list)
        counter = int(counter)
        counter += 1


potential_sessions_operations()