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

## How to Run

```bash
python main.py
```

## Requirements

- Python 3
- Tkinter (included with standard Python installations)
