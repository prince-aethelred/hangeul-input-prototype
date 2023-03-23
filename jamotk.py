# -*- coding: utf-8 -*-
import tkinter as tk
import jamotools


def on_backspace_press(event):
    # Get the index of the character immediately preceding the cursor
    index = event.widget.index(tk.INSERT + "-1c")

    # Get the character at that index
    previous_char = event.widget.get(index)

    old_block_list = jamotools.string_to_block_list(previous_char)
    old_jamo_list = jamotools.block_list_to_jamo_list(old_block_list)

    new_jamo_list = jamotools.delete_jamo(old_jamo_list, 1)
    new_previous_char = jamotools.jamo_list_to_string(new_jamo_list)

    # Print the character that will be deleted
    print(f"Deleting character: {previous_char}")

    # Insert a string into the text widget
    event.widget.insert(tk.INSERT + "-1c", new_previous_char)


if __name__ == "__main__":
    # Create a new tkinter window with a text widget
    window = tk.Tk()
    text_widget = tk.Text(window)
    text_widget.pack()

    # Bind the on_backspace_press function to the <BackSpace> event for the text widget
    text_widget.bind("<BackSpace>", on_backspace_press)

    # Start the tkinter event loop
    window.mainloop()
