import PySimpleGUI as sg
import os
import subprocess

# Шлях до папки з лабораторними роботами
LABS_DIR = 'labs/'

# Функція для отримання списку лабораторних робіт та їхніх описів
def get_lab_info():
    if not os.path.exists(LABS_DIR):
        sg.popup_error(f"Папка '{LABS_DIR}' не знайдена. Будь ласка, перевірте шлях.", title="Помилка")
        return []
    
    lab_folders = [f for f in os.listdir(LABS_DIR) if os.path.isdir(os.path.join(LABS_DIR, f))]
    lab_info = []
    
    for lab in lab_folders:
        lab_path = os.path.join(LABS_DIR, lab)
        description = "Опис відсутній"
        
        # Читаємо README.md, якщо він існує
        readme_path = os.path.join(lab_path, 'README.md')
        if os.path.isfile(readme_path):
            with open(readme_path, 'r', encoding='utf-8') as f:
                description = f.read()
        
        # Збираємо доступні .py файли
        py_files = [f for f in os.listdir(lab_path) if f.endswith('.py')]
        lab_info.append({"name": lab, "description": description, "files": py_files, "path": lab_path})
    
    return lab_info

# Функція для запуску обраного скрипта
def run_lab_script(script_path):
    if not os.path.isfile(script_path):
        sg.popup_error(f"Файл '{script_path}' не знайдено!", title="Помилка")
        return
    try:
        subprocess.run(['python', script_path], check=True)
        sg.popup("Скрипт успішно виконано!", title="Успіх")
    except subprocess.CalledProcessError as e:
        sg.popup_error(f"Помилка виконання скрипта:\n{e}", title="Помилка")

# Основний інтерфейс
def main():
    labs = get_lab_info()
    if not labs:
        return

    lab_names = [lab['name'] for lab in labs]

    layout = [
        [sg.Text("Виберіть лабораторну роботу:", font=("Helvetica", 10))],
        [sg.Listbox(values=lab_names, size=(40, 10), key='-LAB_SELECTED-', enable_events=True)],
        [sg.Text("Опис лабораторної роботи:", font=("Helvetica", 10))],
        [sg.Multiline(size=(50, 10), key='-DESCRIPTION-', disabled=True)],
        [sg.Text("Оберіть файл для запуску:", font=("Helvetica", 10))],
        [sg.Combo([], size=(40, 1), key='-FILE_SELECTED-')],
        [sg.Button("Запустити", key='-RUN-'), sg.Button("Вихід")]
    ]

    window = sg.Window("Запуск лабораторних робіт", layout)

    while True:
        event, values = window.read()
        
        if event in (sg.WINDOW_CLOSED, "Вихід"):
            break

        # Вибір лабораторної роботи
        if event == '-LAB_SELECTED-' and values['-LAB_SELECTED-']:
            selected_lab = values['-LAB_SELECTED-'][0]
            for lab in labs:
                if lab['name'] == selected_lab:
                    window['-DESCRIPTION-'].update(lab['description'])
                    window['-FILE_SELECTED-'].update(values=lab['files'])
                    break

        # Запуск вибраного файлу
        if event == '-RUN-' and values['-FILE_SELECTED-']:
            selected_lab = values['-LAB_SELECTED-'][0]
            script_to_run = os.path.join(LABS_DIR, selected_lab, values['-FILE_SELECTED-'])
            run_lab_script(script_to_run)
    
    window.close()

if __name__ == "__main__":
    main()
