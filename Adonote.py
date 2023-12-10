import tkinter as tk
from tkinter import simpledialog, font, messagebox
from datetime import datetime
import sqlite3


class Adonote:
    def __init__(self, master):
        self.master = master
        self.master.title("Adonote")
        self.master.geometry("1400x850")
        self.master.configure(bg="#F3E8D9")

        # Connect to the SQLite database
        self.conn = sqlite3.connect("notes.db")
        self.create_table()
        self.create_widgets()
        self.load_notes()

    # Create a table if it doesn't exist to save the notes
    def create_table(self):
        with self.conn:
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS notes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    content TEXT
                )
            ''')

    # Adds the title and the "new note" button to the screen
    def create_widgets(self):
        title_font = font.Font(family="Dosis", size=60, weight="bold")
        small_font = font.Font(family="Dosis", size=20)

        # Create a label at the top
        title_label = tk.Label(self.master, text="Adonote", font=title_font, bg="#F3E8D9", fg="grey", pady=10)
        title_label.pack()

        # Create a button to add a new note
        add_button = tk.Button(self.master, text="Add Note", command=self.add_note)
        add_button.pack(pady=10)

        # Create a frame to hold the notes
        self.notes_frame = tk.Frame(self.master)
        self.notes_frame.pack()
        self.notes_frame.option_add('*Font', small_font)

    # Prompt the user to enter a note
    def add_note(self):
        note_text = simpledialog.askstring(
            "Add Note",
            "Enter your note:",
            parent=self.master,
        )
        
        # Check if the user didn't cancel the input dialog, if not then the note is put into the database
        if note_text is not None:
            with self.conn:
                self.conn.execute("INSERT INTO notes (content) VALUES (?)", (note_text,))

            # Get the current date and time
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Dictionary to create a new note
            new_note = {"timestamp": timestamp, "content": note_text}
            self.display_note(new_note)

    # Query all notes from the database
    def load_notes(self):
        with self.conn:
            cursor = self.conn.execute("SELECT * FROM notes")
            for row in cursor.fetchall():
                # Create a new note dictionary for each note in the database
                note = {"timestamp": row[1], "content": row[2]}
                self.display_note(note, note_id=row[0])

    # Create a new frame to hold the note content and delete button
    def display_note(self, note, note_id=None):
        note_frame = tk.Frame(self.notes_frame)
        note_frame.pack(pady=10)

        # Create a new text box to display the note
        note_content = f"{note['timestamp']}\n{note['content']}\n"
        note_box = tk.Text(note_frame, height=8, width=120)
        note_box.insert(tk.END, note_content)
        note_box.pack(side=tk.LEFT)

        note_box.tag_configure("grey", foreground="#808080")
        note_box.tag_configure("white", foreground="#FFFFFF")

        note_box.tag_add("grey", "1.0", "1.end")
        note_box.tag_add("white", "1.end", tk.END)

        # Button to delete the note
        delete_button = tk.Button(note_frame, text="Delete",
                                  command=lambda nf=note_frame, note_id=note_id: self.show_delete_option(nf, note_id))
        delete_button.pack(side=tk.RIGHT)

    # Confirms if the user wants to delete the not 
    def show_delete_option(self, note_frame, note_id):
        try:
            confirm_delete = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this note?")

            # Remove the note from the database
            if confirm_delete:
                with self.conn:
                    self.conn.execute("DELETE FROM notes WHERE id=?", (note_id,))
                note_frame.destroy()

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")


if __name__ == "__main__":
    root = tk.Tk()
    app = Adonote(root)
    root.mainloop()


