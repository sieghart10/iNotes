import os
import tkinter as tk
from datetime import datetime
from iNotes_classes import Note
from tkinter import messagebox

class WindowBuilder:
    def __init__(self, master):
        self.master = master
    
    def set_title(self, title):
        self.master.title(title)
        return self
    
    def set_size(self, width, height):
        self.master.geometry(f"{width}x{height}")
        return self
    
    def set_resizable(self, resizable):
        self.master.resizable(*resizable)
        return self
    
    def build(self):
        return self.master

class WindowFacade:
    def __init__(self, master, title, width, height, resizable):
        self.builder = WindowBuilder(master)
        self.builder.set_title(title)
        self.builder.set_size(width, height)
        self.builder.set_resizable(resizable)
        self.frames = {}

    def build_window(self):
        return self.builder.build()

    def create_main_menu_frame(self):
        frame = tk.Frame(self.builder.master, bg="#0a014f")
        self.frames["main_menu"] = frame
        return frame

    def get_frame(self, frame_name):
        return self.frames.get(frame_name)

    def create_frame(self, parent, bg, width, height, relief):
        frame = tk.Frame(parent, width=width, height=height, relief=relief)    
        frame.config(bg=bg)
        return frame

    def create_label(self, parent, text, font, bg, fg):
        label = tk.Label(parent, text=text, font=font, bg=bg, fg=fg)
        return label

    def create_button(self, parent, text, width, relief, bg, fg, command):
        button = tk.Button(parent, text=text, width=width, relief=relief, bg=bg, fg=fg, command=command)
        return button

    def create_entry(self, parent, placeholder, show, width):
        entry = tk.Entry(parent, show=show, width=width)
        entry.insert(0, placeholder)
        return entry

    def create_radio_button(self, parent, text, variable, value, bg):
        radio = tk.Radiobutton(parent, text=text, variable=variable, value=value, bg=bg)
        return radio
    
    def create_top_level_window(self, title, size, bg_color):
        top_level_window = tk.Toplevel(self.builder.master)
        top_level_window.title(title)
        top_level_window.geometry(size)
        top_level_window.configure(bg=bg_color)
        top_level_window.resizable(False, False)
        return top_level_window
    
    def create_text_editor(self, parent, content, width, height):
        text_area = tk.Text(parent, width=width, height=height)
        text_area.insert(tk.END, content)
        return text_area

class INotesApplication(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.facade = WindowFacade(self, "iNotes", 800, 600, (False, False))
        self.window = self.facade.build_window()
        self.notes = Note("My Notes", datetime.now(), datetime.now(), 0, [])
        self.text_files = []
        self.file_names = []
        self.file_dates = []
        self.file_sizes = []
        self.text_area = None
        self.current_sort_method = None
        self.main_menu_frame = None
        self.main_menu_frame = self.facade.create_frame(self.master, "#0a014f", 800, 600, relief=tk.RAISED)
        self.main_menu_frame.pack(fill=tk.BOTH, expand=True)
        self.display_main_menu(sort_key=lambda x: x[1], is_reversed=False)
        
    def display_main_menu(self, sort_key=lambda x: x[1], is_reversed=False):
        self.clear_widgets(self.main_menu_frame)
        self.current_sort_method = sort_key.__name__.replace('_', ' ')
        self.file_names.clear()
        self.file_dates.clear()
        self.file_sizes.clear()

        self.navigation_frame = self.facade.create_frame(self.main_menu_frame, "#060c44", 800, 95, relief=tk.RAISED)
        self.navigation_frame.place(x=0, y=0)

        self.search_frame = self.facade.create_frame(self.navigation_frame, "#060c44", 320, 30, relief=tk.RAISED)
        self.search_frame.place(x=460, y=20)

        self.title_label = self.facade.create_label(self.navigation_frame, "iNotes", ("Arial", 20), "#060c44", "white")
        self.title_label.place(x=20, y=22)
        self.tagline_label = self.facade.create_label(self.navigation_frame, "Your memory keeper.", ("Noto Sans", 8), "#060c44", "white")
        self.tagline_label.place(x=24, y=54)

        self.search_input_entry = self.facade.create_entry(self.search_frame, "Search your notes...", "", 50)
        self.search_input_entry.pack(padx=8, pady=8)
        self.search_input_entry.bind("<Return>", lambda event: self.search_word())
        self.search_input_entry.focus_set()

        self.search_button = self.facade.create_button(self.navigation_frame, "Search", 7, "flat", "#043edc", "white", command=lambda: self.search_word())
        self.search_button.place(x=713, y=60)

        self.side_frame = self.facade.create_frame(self.main_menu_frame, "#000066", 160, 600, relief=tk.RAISED)
        self.side_frame.place(x=0, y=95)

        self.credits_label = self.facade.create_label(self.side_frame, "© iNotes by Izyne Gallardo", ("Arial", 8), "#000066", "white")
        self.credits_label.place(x=12, y=475)

        self.name_asc_button = self.facade.create_button(self.main_menu_frame, "Name     ↑", 7, "flat", "#0a014f", "white", command=lambda: self.sort_menu(lambda x: x[0], True))
        self.name_asc_button.place(x=245, y=100)

        self.date_asc_button = self.facade.create_button(self.main_menu_frame, "Date modified   ↑", 11, "flat", "#0a014f", "white", command=lambda: self.sort_menu(lambda x: x[1], True))
        self.date_asc_button.place(x=425, y=100)

        self.size_asc_button = self.facade.create_button(self.main_menu_frame, "Size   ↑", 4, "flat", "#0a014f", "white", command=lambda: self.sort_menu(lambda x: x[2], True))
        self.size_asc_button.place(x=655, y=100)

        self.name_desc_button = self.facade.create_button(self.main_menu_frame, "↓", 1, "flat", "#0a014f", "white", command=lambda: self.sort_menu(lambda x: x[0], False))
        self.name_desc_button.place(x=300, y=100)

        self.date_desc_button = self.facade.create_button(self.main_menu_frame, "↓", 1, "flat", "#0a014f", "white", command=lambda: self.sort_menu(lambda x: x[1], False))
        self.date_desc_button.place(x=512, y=100)

        self.size_desc_button = self.facade.create_button(self.main_menu_frame, "↓", 1, "flat", "#0a014f", "white", command=lambda: self.sort_menu(lambda x: x[2], False))
        self.size_desc_button.place(x=690, y=100)

        self.add_note_button = self.facade.create_button(self.main_menu_frame, "+", 3, "raised", "#043edc", "#fae0e4", command=self.create_new_note)
        self.add_note_button.config(font=("Arial", 20))
        self.add_note_button.place(x=714, y=520)

        self.documents_folder = os.path.expanduser("~/Documents")
        files = os.listdir(self.documents_folder)
        self.text_files = [file for file in files if file.endswith('.txt')]

        num_notes = len(self.text_files)
        
        print("Number of existing notes:", num_notes)
        print("Number of new notes:", len(self.notes.get_memo()))
        for note in self.notes.get_memo():
            print("Note:", note.get_name())
            print("Date:", note.get_date_modified())
            print("Size:", note.get_size())

        for file_name in self.text_files:
            file_path = os.path.join(self.documents_folder, file_name)
            file_date_modified = datetime.fromtimestamp(os.path.getmtime(file_path)).strftime("%m/%d/%Y %I:%M %p")
            file_size = os.path.getsize(file_path)
            self.file_names.append(file_name[:-4])
            self.file_dates.append(file_date_modified)
            self.file_sizes.append(file_size)

        files_info = [(name, date, size) for name, date, size in zip(self.file_names, self.file_dates, self.file_sizes)]

        if is_reversed:
            sorted_files_info = self.bubble_sort(files_info, key=sort_key)
        else:
            sorted_files_info = self.bubble_sort_reversed(files_info, key=sort_key)

        for file_no, (file_name, file_date, file_size) in enumerate(sorted_files_info):
            file_size_kb = file_size / 1024.0
            file_size_str = f"{file_size_kb:.2f} KB"
            new_note_button = self.facade.create_button(self.main_menu_frame, file_name, 26, "flat", "#060c44", "white", command=lambda note_name=file_name: self.display_text_editor(note_name))
            new_note_button.place(x=175, y=130 + file_no * 30)
            date_modified_label = self.facade.create_label(self.main_menu_frame, file_date, ("Arial", 10), "#0a014f", "white")
            date_modified_label.place(x=410, y=130 + file_no * 30)
            file_size_label = self.facade.create_label(self.main_menu_frame, file_size_str, ("Arial", 10), "#0a014f", "white")
            file_size_label.place(x=650, y=130 + file_no * 30)

    def search_word(self):
        self.clear_widgets(self.side_frame)
        self.credits_label = self.facade.create_label(self.side_frame, "© iNotes by Izyne Gallardo", ("Arial", 8), "#000066", "white")
        self.credits_label.place(x=12, y=475)

        search_text = self.search_input_entry.get().strip().lower()
        result_found = False

        for file_name in self.text_files:
            # Read the content of the text file
            file_path = os.path.join(self.documents_folder, file_name)
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()

            words = content.split()

            for word in words:
                word_stripped = word.strip().strip().lower()
                edit_distance = self.edit_distance(search_text, word_stripped)

                if edit_distance == 0:  # Set a threshold for edit distance
                    # Found a match, do something (e.g., highlight the word, display the file name, etc.)
                    self.reuslt_label = self.facade.create_label(self.side_frame, f"Match found: {word_stripped}", ("Arial", 10), "#000066", "white")
                    self.reuslt_label.place(x=4, y=50)
                    self.reuslt_location_label = self.facade.create_label(self.side_frame, f"In file: {file_name}", ("Arial", 10), "#000066", "white")
                    self.reuslt_location_label.place(x=4, y=70)
                    result_found = True
                    break

                if result_found:
                    break

        if not result_found:
            self.reuslt_label = self.facade.create_label(self.side_frame, f"No items match your search.", ("Arial", 8), "#000066", "white")
            self.reuslt_label.place(x=4, y=50)

    def create_new_note(self):
        self.new_note_window = self.facade.create_top_level_window("Create new note", "400x300", "#0a014f")
        self.new_note_window.grab_set()

        self.note_name_label = self.facade.create_label(self.new_note_window, "Note Name:", ("Arial",  10), "#0a014f", "white")
        self.note_name_label.place(x=20, y=50)

        self.note_name_entry = self.facade.create_entry(self.new_note_window, "Input title here...", "", 30)
        self.note_name_entry.place(x=150, y=50)

        self.create_button = self.facade.create_button(self.new_note_window, "Create", "10", "raised", "#043edc", "white", command=lambda: [self.display_text_editor(self.note_name_entry.get()), self.new_note_window.destroy()])
        self.create_button.place(x=160, y=250)

    def display_text_editor(self, note_name):
        self.clear_widgets(self.main_menu_frame)
        
        self.note_title_label = self.facade.create_label(self.main_menu_frame, f"{note_name}.txt", ("Arial", 10), "#0a014f", "white")
        self.note_title_label.pack(pady=10)

        self.documents_folder = os.path.expanduser("~/Documents")
        self.file_path = os.path.join(self.documents_folder, f"{note_name}.txt")

        if os.path.exists(self.file_path):
            with open(self.file_path, "r", encoding="utf-8") as file:
                content = file.read()
        else:
            content = ""

        self.find_input_entry = self.facade.create_entry(self.main_menu_frame, "Find...", "", 20)
        self.find_input_entry.place(x=590, y=12)
        self.find_input_entry.bind("<Return>", lambda event: find_word())
        self.find_input_entry.focus_set()

        self.find_button = self.facade.create_button(self.main_menu_frame, "Find", "8", "raised", "#043edc", "white", command=lambda: find_word())
        self.find_button.place(x=718, y=8)

        self.text_area = self.facade.create_text_editor(self.main_menu_frame, content, 96, 32)
        self.text_area.place(x=12, y=40)

        self.cancel_button = self.facade.create_button(self.main_menu_frame, "←Back—", "8", "raised", "#043edc", "white", command=lambda:[self.display_main_menu(sort_key=lambda x: x[1], is_reversed=False)])
        self.cancel_button.place(x=12, y=8)

        self.theme_button = self.facade.create_button(self.main_menu_frame, "Dark Mode", "10", "solid", "#212529", "white", command=lambda:[self.text_area.configure(bg="black"), self.text_area.configure(fg="white")])
        self.theme_button.place(x=12, y=565)

        self.save_button = self.facade.create_button(self.main_menu_frame, "Save", "10", "raised", "#043edc", "white", command=lambda:[self.save_note(note_name), self.display_main_menu(sort_key=lambda x: x[1], is_reversed=False)])
        self.save_button.place(x=360, y=565)

        self.rename_button = self.facade.create_button(self.main_menu_frame, "Rename", "10", "ridge", "#73e7aa", "black", command=lambda: self.rename_note_dialog(note_name))
        self.rename_button.place(x=600, y=565)

        self.delete_button = self.facade.create_button(self.main_menu_frame, "Delete", "10", "ridge", "#dc3545", "white", command=lambda: self.delete_note_file(note_name))
        self.delete_button.place(x=704, y=565)

        def find_word():
            search_text = self.find_input_entry.get().strip().lower()
            result_found = False

            if search_text:
                start = "1.0"
                end = "end"
                self.text_area.tag_remove("highlight", start, end)

                while True:
                    start = self.text_area.search(search_text, start, stopindex=end, nocase=True)
                    if not start:
                        break

                    end_index = self.text_area.index(f"{start}+{len(search_text)}c")
                    word = self.text_area.get(start, end_index)
                    if self.edit_distance(search_text, word.strip().lower()) == 0:
                        self.text_area.tag_add("highlight", start, end_index)
                        result_found = True

                    start = end_index

                if result_found:
                    self.text_area.tag_configure("highlight", background="red")
                else:
                    messagebox.showinfo("Search", "No results found.")

    def save_note(self, note_name):
        print("Saving note...")
        print("File path:", self.file_path)
        print("Content to save:", self.text_area.get("1.0", tk.END))
        
        if os.path.exists(self.file_path):
            with open(self.file_path, "w", encoding="utf-8") as file:
                file.write(self.text_area.get("1.0", tk.END))
        else:
            with open(self.file_path, "w", encoding="utf-8") as file:
                file.write(self.text_area.get("1.0", tk.END))

        existing_note = next((note for note in self.notes.get_memo() if note.get_name() == note_name), None)
        if existing_note:
            existing_note.set_date_modified(datetime.now())
        else:
            new_note = Note(note_name, datetime.now(), datetime.now(), 0, [])
            self.notes.add_note(new_note)

    def rename_note_dialog(self, old_name):
        self.rename_window = self.facade.create_top_level_window("Rename Note", "400x150", "#0a014f")
        self.rename_window.grab_set()

        self.note_name_label = self.facade.create_label(self.rename_window, "New Note Name:", ("Arial",  10), "#0a014f", "white")
        self.note_name_label.place(x=20, y=50)

        self.note_name_entry = self.facade.create_entry(self.rename_window, "Input new title here...", "", 30)
        self.note_name_entry.place(x=150, y=50)

        self.rename_button = self.facade.create_button(self.rename_window, "Rename", "10", "raised", "#043edc", "white", command=lambda: [self.rename_note_file(old_name, self.note_name_entry.get()), self.rename_window.destroy()])
        self.rename_button.place(x=160, y=100)

    def rename_note_file(self, old_name, new_name):
        old_file_path = os.path.join(self.documents_folder, f"{old_name}.txt")
        new_file_path = os.path.join(self.documents_folder, f"{new_name}.txt")
        
        if os.path.exists(old_file_path):
            os.rename(old_file_path, new_file_path)
            self.text_files = [new_name + ".txt" if file_name == old_name + ".txt" else file_name for file_name in self.text_files]
            
            # Check if the note is in the memo and update its name
            note = next((note for note in self.notes.get_memo() if note.get_name() == old_name), None)
            if note:
                note.update_name(new_name)
            
            self.display_main_menu(sort_key=lambda x: x[1], is_reversed=False)
            messagebox.showinfo("Rename Note", "Note renamed successfully.")
        else:
            messagebox.showwarning("Rename Note", "Note file not found.")

    def delete_note_file(self, note_name):
        file_path = os.path.join(self.documents_folder, f"{note_name}.txt")
        if os.path.exists(file_path):
            os.remove(file_path)
            messagebox.showinfo("Delete Note", "Note deleted successfully.")
            self.display_main_menu(sort_key=lambda x: x[1], is_reversed=False)
            if note_name in self.notes.get_memo():
                self.notes.delete_note(note_name)  # Utilize the delete_note method here
        else:
            messagebox.showwarning("Delete Note", "Note file not found.")
    
    def sort_menu(self, sort_key, is_reversed):
        self.display_main_menu(sort_key=sort_key, is_reversed=is_reversed)

    def sort_name_asc(self):
        self.sort_menu(lambda x: x[0], True)

    def sort_date_asc(self):
        self.sort_menu(lambda x: x[1], True)

    def sort_size_asc(self):
        self.sort_menu(lambda x: x[2], True)

    def sort_name_desc(self):
        self.sort_menu(lambda x: x[0], False)

    def sort_date_desc(self):
        self.sort_menu(lambda x: x[1], False)

    def sort_size_desc(self):
        self.sort_menu(lambda x: x[2], False)

    def clear_widgets(self, frame):
        if not frame:
            return 
        for child in frame.winfo_children():
            child.destroy()

    def run(self):
        self.mainloop()

    ### ALGORITHMS ##
    def bubble_sort(self, arr, key=lambda x: x[2]):
        n = len(arr)
        i = 0
        while i < n:
            j = 0
            while j < n-i-1:
                if key(arr[j]) > key(arr[j+1]):
                    arr[j], arr[j+1] = arr[j+1], arr[j]
                j += 1
            i += 1
        return arr
    
    def bubble_sort_reversed(self, arr, key=lambda x: x[2]):
        n = len(arr)
        i = 0
        while i < n:
            j = 0
            while j < n-i-1:
                if key(arr[j]) < key(arr[j+1]):
                    arr[j], arr[j+1] = arr[j+1], arr[j]
                j += 1
            i += 1
        return arr

    def edit_distance(self, s1, s2):
        m, n = len(s1), len(s2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]

        for i in range(m + 1):
            dp[i][0] = i

        for j in range(n + 1):
            dp[0][j] = j

        for i in range(1, m + 1):
            for j in range(1, n + 1):
                cost = 0 if s1[i - 1] == s2[j - 1] else 1
                dp[i][j] = min(dp[i - 1][j] + 1,
                            dp[i][j - 1] + 1,
                            dp[i - 1][j - 1] + cost)

        return dp[m][n]

if __name__ == '__main__':
    os.system("cls")
    app = INotesApplication()
    app.run()
