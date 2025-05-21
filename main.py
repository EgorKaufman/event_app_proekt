import tkinter as tk
from tkinter import messagebox, scrolledtext
from datetime import datetime
import os

EVENTS_FILE = "events.txt"


selected_index = None
events_list = []


def is_valid_date(date_str):
    try:
        datetime.strptime(date_str, "%d.%m.%Y")
        return True
    except ValueError:
        return False

def add_event():
    global selected_index
    name = name_entry.get().strip()
    date = date_entry.get().strip()
    description = desc_text.get("1.0", tk.END).strip()

    if not name or not date:
        messagebox.showwarning("Ошибка", "Название и дата обязательны.")
        return

    if not is_valid_date(date):
        messagebox.showerror("Неверная дата", "Введите дату в формате ДД.ММ.ГГГГ.")
        return

    new_event = (name, date, description)

    if selected_index is not None:
        events_list[selected_index] = new_event
        selected_index = None
    else:
        events_list.append(new_event)

    save_events()
    refresh_event_list()
    clear_inputs()


def save_events():
    with open(EVENTS_FILE, "w", encoding="utf-8") as f:
        for name, date, desc in events_list:
            line = f"{name} | {date} | {desc}\n"
            f.write(line)


def load_events():
    if os.path.exists(EVENTS_FILE):
        with open(EVENTS_FILE, "r", encoding="utf-8") as f:
            for line in f:
                parts = line.strip().split(" | ")
                if len(parts) >= 3:
                    name, date, desc = parts[0], parts[1], " | ".join(parts[2:])
                    events_list.append((name, date, desc))
    refresh_event_list()

def refresh_event_list():
    events_box.delete("1.0", tk.END)
    for i, (name, date, desc) in enumerate(events_list):
        events_box.insert(tk.END, f"{i+1}. {name} | {date} | {desc}\n")

def clear_inputs():
    name_entry.delete(0, tk.END)
    date_entry.delete(0, tk.END)
    desc_text.delete("1.0", tk.END)

def clear_events():
    global events_list
    confirm = messagebox.askyesno("Подтверждение", "Удалить все мероприятия?")
    if confirm:
        events_list = []
        save_events()
        refresh_event_list()
        clear_inputs()

def select_event(event):
    global selected_index
    index = events_box.index("@%s,%s" % (event.x, event.y))
    line_num = int(index.split('.')[0]) - 1

    if 0 <= line_num < len(events_list):
        selected_index = line_num
        name, date, desc = events_list[line_num]
        name_entry.delete(0, tk.END)
        name_entry.insert(0, name)

        date_entry.delete(0, tk.END)
        date_entry.insert(0, date)

        desc_text.delete("1.0", tk.END)
        desc_text.insert("1.0", desc)

root = tk.Tk()
root.title("Планировщик мероприятий с редактированием")
root.geometry("600x650")

tk.Label(root, text="Название мероприятия:").pack(anchor="w", padx=10, pady=(10, 0))
name_entry = tk.Entry(root, width=70)
name_entry.pack(padx=10, pady=5)

tk.Label(root, text="Дата (ДД.ММ.ГГГГ):").pack(anchor="w", padx=10)
date_entry = tk.Entry(root, width=70)
date_entry.pack(padx=10, pady=5)

tk.Label(root, text="Описание:").pack(anchor="w", padx=10)
desc_text = scrolledtext.ScrolledText(root, width=70, height=5)
desc_text.pack(padx=10, pady=5)

tk.Button(root, text="Добавить / Сохранить", command=add_event, bg="green", fg="white").pack(pady=5)
tk.Button(root, text="Очистить все мероприятия", command=clear_events, bg="red", fg="white").pack(pady=5)

tk.Label(root, text="Список мероприятий (нажмите, чтобы редактировать):").pack(anchor="w", padx=10)
events_box = scrolledtext.ScrolledText(root, width=70, height=20)
events_box.pack(padx=10, pady=10)
events_box.bind("<Button-1>", select_event)

load_events()
root.mainloop()
