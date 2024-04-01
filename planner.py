import PySimpleGUI as sg
import sqlite3


def init_database():
    conn = sqlite3.connect('postit.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS postits (
            id INTEGER PRIMARY KEY,
            title TEXT,
            text TEXT,
            font TEXT,
            alpha REAL,
            location_x INTEGER,
            location_y INTEGER
        )
    ''')
    conn.commit()

    conn.close()


def save_data(title, text, font, alpha, location):
    conn = sqlite3.connect('postit.db')
    cursor = conn.cursor()

    cursor.execute(
        'INSERT OR REPLACE INTO postits (id, title, text, font, alpha, location_x, location_y) VALUES (1, ?, ?, ?, ?, ?, ?)',
        (title, text, font, alpha, location[0], location[1]))
    conn.commit()

    conn.close()


def load_data():
    conn = sqlite3.connect('postit.db')
    cursor = conn.cursor()

    cursor.execute('SELECT title, text, font, alpha, location_x, location_y FROM postits WHERE id=1')
    result = cursor.fetchone()

    conn.close()

    return result if result else (None, '', '_ 20', 1.0, None)


def make_window(title, text, loc):
    text_font = sg.user_settings_get_entry('-font-', '_ 20')
    alpha = sg.user_settings_get_entry('-alpha-', 1.0)

    layout = [[sg.T(title, text_color='black', background_color='#FFFF88', k='-TITLE-')],
              [sg.ML(text, size=(30, 5), background_color='#FFFF88', no_scrollbar=True, k='-ML-', border_width=0,
                     expand_y=True, expand_x=True, font=text_font),
               sg.Sizegrip(background_color='#FFFF88')],
              [sg.Button('Save', key='-SAVE-'), sg.Button('Exit', key='-EXIT-')]]

    window = sg.Window('Postit', layout,
                       no_titlebar=True, grab_anywhere=True, margins=(0, 0), background_color='#FFFF88',
                       element_padding=(0, 0), location=loc, keep_on_top=True,
                       right_click_menu=[[''], ['Edit Me', 'Change Font', 'Alpha', [str(x) for x in range(1, 11)],
                                                'Choose Title', 'Exit', ]],
                       font='_ 20', right_click_menu_font=text_font, resizable=True, finalize=True, alpha_channel=alpha)
    window.set_min_size(window.size)

    return window


def main():
    init_database()
    data = load_data()

    # Используем data[4:] для получения кортежа с координатами (x, y) или None, если координаты не существуют
    window = make_window(data[0], data[1], data[4:] if data[4] is not None else (None, None))

    while True:
        event, values = window.read()
        print(event, values)

        if event in (sg.WIN_CLOSED, '-EXIT-'):
            save_data(window['-TITLE-'].Get(), window['-ML-'].Get().rstrip(),
                      sg.user_settings_get_entry('-font-', '_ 20'),
                      sg.user_settings_get_entry('-alpha-', 1.0), window.current_location())
            break
        elif event == '-SAVE-':
            save_data(window['-TITLE-'].Get(), window['-ML-'].Get().rstrip(),
                      sg.user_settings_get_entry('-font-', '_ 20'),
                      sg.user_settings_get_entry('-alpha-', 1.0), window.current_location())

        # ... (ваш оригинальный код)

    window.close()


if __name__ == '__main__':
    main()
