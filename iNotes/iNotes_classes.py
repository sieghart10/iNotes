from abc import ABC, abstractmethod
import os

class File(ABC):
    def __init__(self, name, date_created, date_modified, size, type) -> None:
        self.__name = name
        self.__date_created = date_created
        self.__date_modified = date_modified
        self.__size = size
        self.__type = type

    @abstractmethod
    def get_name(self):
        return self.__name
    
    @abstractmethod
    def get_date_created(self):
        return self.__date_created
    
    @abstractmethod
    def get_date_modified(self):
        return self.__date_modified
    
    @abstractmethod
    def get_size(self):
        return self.__size
    
    @abstractmethod
    def get_type(self):
        return self.__type

    @abstractmethod
    def add_note(self, name, date_created):
        pass
   
    @abstractmethod
    def delete_note(self, name):
        pass

class Note(File):
    def __init__(self, name, date_created, date_modified, size, memo) -> None:
        super().__init__(name, date_created, date_modified, size, "txt")
        self.__memo = memo if memo else []

    def get_name(self):
        return super().get_name()
    
    def set_name(self, name):
        self.__name = name
    
    def get_date_created(self):
        return super().get_date_created()
    
    def set_date_modified(self, date):
        self.__date_modified = date
    
    def get_date_modified(self):
        return super().get_date_modified()
    
    def get_size(self):
        return super().get_size()
    
    def get_type(self):
        return super().get_type()
    
    def get_memo(self):
        return self.__memo
    
    def set_memo(self, memo):
        self.__memo = memo

    def add_note(self, note):
        self.get_memo().append(note)
        # for note in self.get_memo():
        #     print(f"Name: {note.get_name()}, Date Created: {note.get_date_created()}")

    def delete_note(self, name):
        #self.get_memo()[:] = [note for note in self.get_memo() if note.get_name() != name]
        self.get_memo().pop(-1)
        
    def update_name(self, new_name):
        old_name = self.get_name()
        
        # Check if the note is in the application's notes list and update its name
        note_in_memo = next((note for note in self.get_memo() if self.get_name() == old_name), None)
        if note_in_memo:
            note_in_memo.set_name(new_name)
        else:
            file_path_old = os.path.join(os.path.expanduser("~/Documents"), f"{old_name}.txt")
            file_path_new = os.path.join(os.path.expanduser("~/Documents"), f"{new_name}.txt")
            os.rename(file_path_old, file_path_new)

        self.set_name(new_name)