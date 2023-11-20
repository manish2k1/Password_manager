import tkinter as tk
import random
import string
import ttkbootstrap as ttk
import backend
import crypt_1
from datetime import datetime
import re
    
    
# GLOBALVARIABLE FOR TO DEFINE LENGTH OF PASSWORD
global_length = 8
random_string = ''

def add_record():

    # CLOSE BUTTON ACTION 
    def close_window():
        root.destroy()

    # APPLY BUTTON ACTION
    def push_data():
        
        # title,username,notes=" "*3
        # FETCH DATA TO INSERT IN TABLE
        title = input_field_title.get()
        username = input_field_uname.get()
        password = input_field_password.get()
        notes = input_field_notes.get("1.0", "end-1c")
        now =datetime.now()
        formatted_date = now.strftime("%Y-%m-%d %H:%M:%S")
        last_modified =  formatted_date
        
        if not title:
            title =" "
        if not username:
            username =" "
        if not notes:
            notes =" "
        
        
        # ENCRYPT DATA BEFORE ENTRY
        title_en =  crypt_1.encrypt_text(title)
        username_en =  crypt_1.encrypt_text(username)
        password_en =  crypt_1.encrypt_text(password)
        notes_en =  crypt_1.encrypt_text(notes)
        last_modified_en =  crypt_1.encrypt_text(last_modified)
        
        # INSERT DATA
        backend.insert_data(title_en, username_en, password_en, notes_en, last_modified_en)
        root.destroy()


    # GENERATE PASSWORD FUNCTION
    def gen():
        
        # GENERATE STRING
        def generate_random_string(length, lst):
            
            #PASSWORD CRITERIA
            def valid_pass(password, lst):
                if 'L' in lst and not re.search(r'[a-z]', password):
                    return False
                
                if 'U' in lst and not re.search(r'[A-Z]', password):
                    return False
                
                if 'N' in lst and not re.search(r'[0-9]', password):
                    return False

                if 'S' in lst and not re.search(r'[!@#$%^&*()-_+=<>?]', password):
                    return False
                return True
            
            characters = ''

            if 'U' in lst:
                characters += string.ascii_uppercase

            if 'L' in lst:
                characters += string.ascii_lowercase

            if 'N' in lst:
                characters += string.digits

            if 'S' in lst:
                characters += string.punctuation

            while True:
                random_string = ''.join(random.choices(characters, k=length))
                if valid_pass(random_string,lst):
                    break
            return random_string

        # GENERATE BUTTON FUNCTION
        def generate_random_string_button_clicked():
            length = global_length

            charsets = []

            if uppercase_var.get():
                charsets.append('U')
            if lowercase_var.get():
                charsets.append('L')
            if digits_var.get():
                charsets.append('N')
            if punctuation_var.get():
                charsets.append('S')
            global random_string
            random_string = generate_random_string(length, charsets)
            result_label.delete(0, tk.END)
            result_label.insert(0, str(random_string))

        # READ FROM SCALE_WIDGET
        def update_label(value):
            
            label.config(text=f"Length: {value}")

        # CLOSE BUTTOH WIDGET
        def close_modal_window():
            modal_window.destroy()

        # APPLY BUTTON WIDGET
        def apply_modal_window():
            input_field_password.delete(0, tk.END)
            input_field_password.insert(0, random_string)
            modal_window.destroy()


        # GENERATE PASSWORD WINDOW
        modal_window = ttk.Toplevel(root)
        modal_window.title("Password Generator")
        modal_window.grab_set()

        width, height = 1200, 800
        modal_window.minsize(width=width, height=height)
        modal_window.maxsize(width=width, height=height)

        frame = ttk.Frame(modal_window)
        frame.pack(padx=100, pady=200)

        frame2 = ttk.Frame(frame)
        frame2.pack(padx=10, pady=10)

        frame3 = ttk.Frame(frame)
        frame3.pack(padx=10, pady=10)

        frame4 = ttk.Frame(frame)
        frame4.pack(padx=10, pady=10)

        frame5 = ttk.Frame(frame)
        frame5.pack(padx=10, pady=10)

        frame6 = ttk.Frame(frame)
        frame6.pack(padx=10, pady=10)

        custom_style = ttk.Style()
        custom_style.configure("Custom.TCheckbutton", font=("Aptos", 12))

        scale = tk.Scale(frame2, from_=8, to=32, orient="horizontal", length=500, showvalue=10,
                        command=update_label)
        scale.pack(pady=20)

        label = ttk.Label(frame2,
                        font=("Aptos", 15),
                        text=f"Value: {global_length}")
        label.pack()

        uppercase_var = tk.BooleanVar()
        Ucb = ttk.Checkbutton(frame3, text="Uppercase", style="Custom.TCheckbutton", variable=uppercase_var)
        Ucb.pack(side="left", padx=5, pady=5)

        lowercase_var = tk.BooleanVar()
        Lcb = ttk.Checkbutton(frame3, text="Lowercase", style="Custom.TCheckbutton", variable=lowercase_var)
        Lcb.pack(side="left", padx=5, pady=5)

        digits_var = tk.BooleanVar()
        Dcb = ttk.Checkbutton(frame3, text="Digits", style="Custom.TCheckbutton", variable=digits_var)
        Dcb.pack(side="left", padx=5, pady=5)

        punctuation_var = tk.BooleanVar()
        Pcb = ttk.Checkbutton(frame3, text="Punctuation", style="Custom.TCheckbutton", variable=punctuation_var)
        Pcb.pack(side="left", padx=5, pady=5)

        generate_button = ttk.Button(frame4, text="Generate", command=generate_random_string_button_clicked)
        generate_button.pack(side="left", padx=5, pady=5)

        result_label = ttk.Entry(frame5,
                                font=("Aptos", 15),
                                width=35)

        result_label.pack(side="left", padx=5, pady=5)

        apply = ttk.Button(frame6, text="Apply", command=apply_modal_window)
        apply.pack(side="left", padx=5, pady=5)

        cancel = ttk.Button(frame6, text="Cancel", command=close_modal_window)
        cancel.pack(side="right", padx=5, pady=5)

        modal_window.wait_window(modal_window)

    # ENTER DATA WINDOW
    root = ttk.Window(themename='flatly')
    root.title("Enter New Record")
    root.geometry("600x400")
    

    entry_frame = tk.Frame(root, height=600)
    entry_frame.pack(padx=90)

    button_frame = tk.Frame(root, height=400)
    button_frame.pack(pady=60)

    label = tk.Label(entry_frame, text="Title:", font=("Aptos", 12))
    label.grid(row=1, column=0, padx=10, pady=10, sticky="e")

    input_field_title = tk.Entry(entry_frame, font=("Aptos", 12), width=110)
    input_field_title.grid(row=1, column=1, padx=10, pady=10, sticky="w", columnspan=2)

    label = tk.Label(entry_frame, text="Username:", font=("Aptos", 12))
    label.grid(row=2, column=0, padx=10, pady=10, sticky="e")

    input_field_uname = tk.Entry(entry_frame, font=("Aptos", 12), width=110)
    input_field_uname.grid(row=2, column=1, padx=10, pady=10, sticky="w", columnspan=2)

    label = tk.Label(entry_frame, text="Password:", font=("Aptos", 12))
    label.grid(row=3, column=0, padx=10, pady=10, sticky="e")

    input_field_password = tk.Entry(entry_frame, font=("Aptos", 12), width=100)
    input_field_password.grid(row=3, column=1, padx=10, pady=10, sticky="w")

    password_generate = tk.Button(entry_frame, text="Generate", font=("Aptos", 10), command=gen)
    password_generate.grid(row=3, column=2, pady=10, sticky="w")

    label = tk.Label(entry_frame, text="Notes : ",font=("Aptos",   12))
    label.grid(row=4, column=0, padx=10, pady=10, sticky="e")   

    input_field_notes = tk.Text(entry_frame,font=("Aptos",   12),width=109)
    input_field_notes.grid(row=4, column=1, padx=10, pady=10, sticky="w",columnspan=2) 

    apply = tk.Button(button_frame, text=" Apply", font=("Aptos", 15),pady=10, command=push_data)
    apply.pack(side="left", padx=30, pady=50)

    cancel = tk.Button(button_frame, text="Cancel", font=("Aptos", 15),pady=10, command=close_window)
    cancel.pack(side="right", padx=30, pady=50)


    root.state('zoomed')
    root.mainloop()
    return 0  

