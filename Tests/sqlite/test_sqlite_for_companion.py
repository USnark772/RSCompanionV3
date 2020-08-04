import sqlite3
from sqlite3 import Error
from datetime import datetime
from time import sleep


def _get_db_conn(db_name: str):
    try:
        return sqlite3.connect(db_name, detect_types=sqlite3.PARSE_DECLTYPES)
    except Error as e:
        print(e)
        return None


def get_table_column_names(db_name: str, table_name: str):
    db_conn = _get_db_conn(db_name)
    cursor = db_conn.cursor()
    cursor.execute("SELECT * FROM " + table_name)
    names = [description[0] for description in cursor.description]
    db_conn.close()
    return names


def check_make_table(db_name: str, table_name: str, column_names: tuple):
    db_conn = _get_db_conn(db_name)
    cursor = db_conn.cursor()
    command = "CREATE TABLE IF NOT EXISTS " + table_name + "{}".format(column_names).replace("'", "")
    cursor.execute(command)
    db_conn.commit()
    db_conn.close()


def drop_table(db_name: str, table_name: str):
    db_conn = _get_db_conn(db_name)
    cursor = db_conn.cursor()
    cursor.execute("DROP TABLE " + table_name)
    db_conn.commit()
    db_conn.close()


def insert_values(db_name: str, table_name: str, values: tuple):
    db_conn = _get_db_conn(db_name)
    if len(values) < 1:
        return
    if len(values) != len(get_table_column_names(db_name, table_name)):
        return
    cursor = db_conn.cursor()
    placeholder = "("
    placeholder += "?," * len(values)
    placeholder = placeholder.rstrip(",")
    placeholder += ")"
    command = "INSERT INTO " + table_name + " VALUES " + placeholder
    cursor.execute(command, values)
    db_conn.commit()
    db_conn.close()


def main():
    db_name = r"C:/RSDev/Testdb/test_experiment.db"

    start_range = datetime.now()
    sleep(.5)

    drt_table_name = "DRT"
    drt_columns = ('ID INTEGER', 'Timestamp timestamp', 'Probe Num INTEGER', 'Clicks INTEGER', 'Mills Passed INTEGER', 'RT INTEGER')
    drt_values = (1, datetime.now(), 1, 0, 3057, 1)
    sleep(.08)

    vog_table_name = "VOG"
    vog_columns = ('ID INTEGER', 'Timestamp timestamp', 'Trial INTEGER', 'Open INTEGER', 'Close INTEGER')
    vog_values = (2, datetime.now(), 1, 33000, 32083)
    sleep(.05)

    notes_table_name = "Notes"
    notes_columns = ('Timestamp timestamp', 'Note STRING')
    notes_values = (datetime.now(), "Hello world!")
    sleep(.2)

    flags_table_name = "Flags"
    flags_columns = ('Timestamp timestamp', 'Flag STRING')
    flags_values = (datetime.now(), 'b')
    sleep(.1)

    end_range = datetime.now()

    check_make_table(db_name, drt_table_name, drt_columns)
    check_make_table(db_name, vog_table_name, vog_columns)
    check_make_table(db_name, notes_table_name, notes_columns)
    check_make_table(db_name, flags_table_name, flags_columns)

    insert_values(db_name, drt_table_name, drt_values)
    insert_values(db_name, vog_table_name, vog_values)
    insert_values(db_name, notes_table_name, notes_values)
    insert_values(db_name, flags_table_name, flags_values)

    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM " + drt_table_name)
    # drt_output = cursor.fetchall()
    # print(drt_output)
    for line in cursor:
        print(line)
    print()
    cursor.execute("SELECT * FROM " + vog_table_name)
    # vog_output = cursor.fetchall()
    # print(vog_output)
    for line in cursor:
        print(line)
    print()
    cursor.execute("SELECT * FROM " + notes_table_name)
    # notes_output = cursor.fetchall()
    # print(notes_output)
    for line in cursor:
        print(line)
    print()
    # print(get_table_column_names(db_name, flags_table_name))
    # command = "SELECT * FROM " + flags_table_name + " WHERE Timestamp BETWEEN DATETIME('" + str(start_range) + "') AND DATETIME('" + str(end_range) + "')"
    # other_command = "SELECT strftime('%Y-%m-%d %H:%M:%f','" + str(start_range) + "')"
    # print(other_command)
    # cursor.execute(other_command)
    # for line in cursor:
    #     print(line)
    # flags_output = cursor.fetchall()
    # print(flags_output)
    # cursor.execute("SELECT * FROM " + drt_table_name + " LEFT JOIN " + vog_table_name)
    # for line in cursor:
    #     print(line)
    drop_table(db_name, drt_table_name)
    drop_table(db_name, vog_table_name)
    drop_table(db_name, notes_table_name)
    drop_table(db_name, flags_table_name)

    conn.close()


if __name__ == '__main__':
    main()
