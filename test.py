import unittest
import tkinter as tk
from unittest.mock import patch
from tkinter import simpledialog, messagebox
from datetime import datetime
import sqlite3
from Adonote import Adonote 

class TestAdonote(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.app = Adonote(self.root)

    def tearDown(self):
        self.root.destroy()
        
    # Ensure the table is created in the database
    def test_create_table(self):
        with sqlite3.connect("notes.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='notes'")
            result = cursor.fetchone()
        self.assertIsNotNone(result, "Table 'notes' not found in the database")

    # Ensure a new note is added to the database
    @patch.object(simpledialog, 'askstring', return_value="Test Note")
    def test_add_note(self, mock_askstring):
        with sqlite3.connect("notes.db") as conn:
            cursor = conn.cursor()
            initial_count = cursor.execute("SELECT COUNT(*) FROM notes").fetchone()[0]

        self.app.add_note()

        with sqlite3.connect("notes.db") as conn:
            cursor = conn.cursor()
            final_count = cursor.execute("SELECT COUNT(*) FROM notes").fetchone()[0]

        self.assertEqual(final_count, initial_count + 1, "Note not added to the database")

    # Ensure that the display_note method creates a new frame
    def test_display_note(self):
        initial_frame_count = len(self.app.notes_frame.winfo_children())
        self.app.display_note({"timestamp": "2022-01-01 12:00:00", "content": "Test Content"})
        final_frame_count = len(self.app.notes_frame.winfo_children())
        self.assertEqual(final_frame_count, initial_frame_count + 1, "Frame not created")

    # Ensure that the show_delete_option method deletes a note
    @patch.object(messagebox, 'askyesno', return_value=True)
    def test_show_delete_option(self, mock_askyesno):
        with sqlite3.connect("notes.db") as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO notes (timestamp, content) VALUES (?, ?)", ("2022-01-01 12:00:00", "Test Content"))
            note_id = cursor.lastrowid

        initial_count = cursor.execute("SELECT COUNT(*) FROM notes").fetchone()[0]
        self.app.show_delete_option(tk.Frame(), note_id)
        final_count = cursor.execute("SELECT COUNT(*) FROM notes").fetchone()[0]

        self.assertEqual(final_count, initial_count - 1, "Note not deleted from the database")

if __name__ == '__main__':
    unittest.main()
