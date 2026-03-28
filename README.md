# iNotes

A simple note-taking desktop application built with Python and Tkinter.

## Features

- **Create, edit, and save** text notes (stored as `.txt` files in your Documents folder)
- **Search** across all notes to find matching words
- **Find** text within an open note with highlighting
- **Sort** notes by name, date modified, or file size (ascending/descending)
- **Rename** and **delete** notes
- **Dark mode** toggle for the text editor

## Design Patterns

- **Builder Pattern** — `WindowBuilder` for constructing the main application window
- **Facade Pattern** — `WindowFacade` for simplified creation of UI components (frames, labels, buttons, entries, etc.)
- **Abstract Base Class** — `File` ABC in `models.py` with a concrete `Note` subclass

## Algorithms

- **Bubble Sort** — used for sorting notes by name, date, or size
- **Edit Distance (Levenshtein)** — used for search matching

## User Interface
<img width="1011" height="793" alt="image" src="https://github.com/user-attachments/assets/e1af8a4c-79b1-4303-be41-01fab070dc56" />
<img width="1018" height="800" alt="image" src="https://github.com/user-attachments/assets/9b3fc3ab-fe41-426c-9f4b-b21051c626f1" />
<img width="1017" height="799" alt="image" src="https://github.com/user-attachments/assets/89ff84cd-34ac-47b3-8dfb-be63675f1413" />
<img width="1022" height="807" alt="image" src="https://github.com/user-attachments/assets/d7576041-42d0-4552-962e-91c7f73df2a2" />
<img width="1013" height="807" alt="image" src="https://github.com/user-attachments/assets/0e7050e5-e7f6-4c0e-9f3c-b39d92cf0efa" />

## How to Run

```bash
python main.py
```

## Requirements

- Python 3
- Tkinter (included with standard Python installations)
