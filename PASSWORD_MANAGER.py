from threading import Thread
from datetime import datetime
from tkinter import messagebox
import tkinter as tk
import ttkbootstrap as ttk
import pyperclip
import time
import crypt_1
import backend
import enter_new_record
import edit_record_window




def start():
    
        
    def user_not_exist():
    
        def logon():
            
            
            entered_value = password_entry.get()
            reentered_value = password_reentry.get()
            phrase = input_field_notes.get("1.0", "end-1c")
            if(not entered_value):
                messagebox.showerror("ERROR","Enter A Password")
            else:
                if(not phrase):
                    messagebox.showerror("ERROR","Enter A Phrase")
                    
                else:
                    if(entered_value==reentered_value):
                        
                        ciphertext = crypt_1.write_encrypt_password(phrase, reentered_value)
                        
                        backend.insert_user(ciphertext,phrase)
                        backend.create_table()
                        logonroot.destroy()
                        start()

                        
                    else:
                        messagebox.showerror("Login Failed", "Password dosen't match")
                    
                
        #---------------------------------------------------- LOGON PAGE ---------------------------------------------------
        
        def on_entry_click(event):
            if input_field_notes.get("1.0", "end-1c") == "Eg. Today is my lucky day":
                input_field_notes.delete("1.0", "end-1c")
                input_field_notes.config(fg="black")

        def on_focus_out(event):
            if not input_field_notes.get("1.0", "end-1c"):
                input_field_notes.insert("1.0", "")
                input_field_notes.config(fg="grey")    


        logonroot = ttk.Window(themename="flatly")
        logonroot.title("Password Logon`")
        logonroot.geometry("1150x800")

        frame = ttk.Frame(logonroot)
        frame.pack(padx=100, pady=100)

        frame2 = ttk.Frame(frame)
        frame2.pack(padx=50, pady=50)

        password_label = ttk.Label(frame2, text="Enter Master Password:", font=("Aptos", 15))
        password_label.pack(pady=5)
        password_entry = ttk.Entry(frame2, justify="center", width=30, font=("Aptos", 15))
        password_entry.pack(pady=5)
        reenter_label = ttk.Label(frame2, text="Re-Enter Master Password:", font=("Aptos", 15))
        reenter_label.pack(pady=5)
        password_reentry = ttk.Entry(frame2, justify="center", width=30, font=("Aptos", 15))
        password_reentry.pack(pady=5)
        reenter_label = ttk.Label(frame2, text="Enter key phrase (Can be used to recover passwords):", font=("Aptos", 15))
        reenter_label.pack(pady=5)
        input_field_notes = tk.Text(frame2, font=("Aptos", 15), width=50, height=10)

        input_field_notes.insert("1.0", "Eg. Today is my lucky day")
        input_field_notes.bind("<FocusIn>", on_entry_click)
        input_field_notes.bind("<FocusOut>", on_focus_out)
        input_field_notes.pack()

        reenter_label = ttk.Label(frame2, text="WARNING: Incase you forget this key phrase you will not be able to access your account.", font=("Aptos", 15))
        reenter_label.pack(pady=5)

        
        # LOGIN BUTTON FUNCTION
        login_button = ttk.Button(frame2, text="LOGON", command=logon)
        login_button.pack(pady = 10)

        logonroot.state('zoomed')



        logonroot.mainloop()
        
                

    
    
    # LOGIN FUNCTION
    def login():
        
        
        
        password = password_entry.get()
        
        value = crypt_1.logon(password)
        if value == 1:
            password_modal.destroy()
            root.deiconify()
            root.state('zoomed')  
            update_treeview()
            check_for_expiry()

        
            
        else:
            messagebox.showerror("Login Failed", "Invalid Password")
            password_entry.delete(0, ttk.END)
            
                

    def strTOdatetime(time_str):
        datetime_object = datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')
        return datetime_object
        
    
    # UPDATE TREEVIEW FUNCTION
    global expired_entry
    expired_entry=[]
    
    def update_treeview():
        data = backend.retrieve()


        for item in my_tree.get_children():
            my_tree.delete(item)
            
        if(data==None):
            return
        else:
            for value in data:       
                en = [x for x in list(map(crypt_1.decrypt_text,value[1:])) if x]    
                my_tree.insert(parent='', index='end', values=([value[0]]+en), tags=("custom_font",))


    # PASSWORD EXPIRED
    def check_for_expiry():
        
        data = backend.retrieve()
        
        if(data==None):
            return
        else:
            for value in data:       
                en = [x for x in list(map(crypt_1.decrypt_text,value[1:])) if x]    
                
                
                record_datetime = strTOdatetime(en[4])
                current_datetime = datetime.now()
                datetime_difference = current_datetime-record_datetime
                days_difference = datetime_difference.days
                
                if(days_difference > -1):
                    expired_entry.append([en[0],en[1]])
                    
                    
                
        if(len(expired_entry)==0):
            return
        else:
            
            def exit():
                alert_window.destroy()
                
            
            style = ttk.Style()
            style.configure("Bold.Treeview")

            
            alert_window = tk.Toplevel(root)
            alert_window.title("!!!!ATTENTION REQUIRED!!!!")
            alert_window.geometry("700x520")
            alert_window.grab_set()

            
            # Add a label for the message
            message_label = tk.Label(alert_window, text="Password(s) for the following entries haven't been Updated for 3 months or more.\n Its recommended to update the password")
            message_label.pack(pady=10)

            
            tree = ttk.Treeview(alert_window, columns=("TITLE", "USERNAME"), show="headings", style="Bold.Treeview")         
            tree.heading("TITLE", text="TITLE")
            tree.heading("USERNAME", text="USERNAME")
            for row in expired_entry:
                tree.insert("", "end", values=(row[0], row[1]))
            tree.pack()
            
            exit_button = ttk.Button(alert_window, text="        OK        ", padding=10, command=exit)
            exit_button.pack(side="top", expand=True, pady=40)
            
            
                

    # SCROLLBAR EVENT
    def set_scrollbar_height(event):
        num_visible_rows = int(event.height / style.lookup("Treeview", "rowheight"))
        my_tree.config(height=num_visible_rows)



    # ACTION ON TREEVIEW-WIDGET ENTRY CLICKED
    def on_treeview_click(event):

        selected_item = my_tree.selection()
        user_copybutton.pack(side="left", padx=50, pady=10)
        pass_copybutton.pack(side="left", padx=50, pady=10)
        
        # PRINT AT TEXT-WIDGET
        if selected_item:
        
            item_data = my_tree.item(selected_item)
            
            global clicked_data
            clicked_data=item_data['values']
            
            
            title = item_data['values'][1]
            global username
            username= item_data['values'][2]
            global password
            password = item_data['values'][3]
            last_modified = item_data['values'][5]
            notes = item_data['values'][4]
            
            
            output_text.config(state=ttk.NORMAL)
            output_text.delete(1.0, tk.END)
            output_text.insert(ttk.END, f"Title:\n {title}\n\n")
            output_text.insert(ttk.END, f"Username:\n {username}\n\n")
            output_text.insert(ttk.END, f"Password:\n {password}\n\n")
            output_text.insert(ttk.END, f"Last_modified:\n {last_modified}\n\n")
            output_text.insert(ttk.END, f"Notes:\n {notes}\n\n")
            output_text.config(state=ttk.DISABLED)

    # CREATE BUTTON FUNCTION
    def create():
        
        enter_new_record.add_record()
        update_treeview()

    # EDIT BUTTON FUNCTION
    def edit():
        
        edit_record_window.edit_record(clicked_data)
        update_treeview()

    # DELETE BUTTON FUNCTION
    def delete():
        selected_item = my_tree.selection()
        item_data = my_tree.item(selected_item)
        backend.delete_record(item_data['values'][0])
        output_text.delete(1.0, tk.END)
        update_treeview()
        
        
    # EXIT BUTTON FUNCTION
    def exit():
        root.destroy()
        
        
    #PROGRESSBAR
    def start_countdown_U():
        countdown_var.set("")
        progress_var.set(100.0)
        copy_text = username
        pyperclip.copy(copy_text)
        
        progressbar.pack(side="left", padx=50, pady=10)
        progressbar_status.pack(side="right", pady=10)


        countdown_thread = Thread(target=update_countdown)
        countdown_thread.start()

    def start_countdown_P():
        countdown_var.set("")
        progress_var.set(100.0)
        copy_text = password
        pyperclip.copy(copy_text)
                
        progressbar.pack(side="left", padx=50, pady=10)
        progressbar_status.pack(side="right", pady=10)

        countdown_thread = Thread(target=update_countdown)
        countdown_thread.start()


    def update_countdown():
        countdown_seconds = 7
        progress_step = 100 / 8

        for i in range(countdown_seconds, -1, -1):
            time.sleep(1)
            progress_var.set(progress_var.get() - progress_step)
            countdown_var.set(f"Clearing clipboard in {i}")

            root.update()

        countdown_var.set(" ")
        progress_var.set(0.0)
        pyperclip.copy('')
        progressbar.pack_forget()
        progressbar_status.pack_forget()
        
    def reset():
        
        def confirm():
            backend.delete_all()
            root.destroy()
            start()
        
        
        
        warning_window = tk.Toplevel(root)
        warning_window.title("Reset Confirmation")
        warning_window.geometry("800x600")
        
        warning_window.grab_set()




        warning_label = ttk.Label(warning_window, text="Are you sure you want to reset the application?\nThere is no way to recover the deleted passwords.")
        warning_label.pack(pady=10)

        reset_button = ttk.Button(warning_window, text="RESET", command=confirm)
        reset_button.pack(pady=10)
        
        
        
    # HARD RESET
    def hard_reset():
        
        def confirm():
            password = confirm_entry.get()
            
            value = crypt_1.logon(password)
            if value == 1:
                
                
                
                backend.delete_all() 

                warning_window.destroy()
                root.destroy()
                start()
            
                
            else:
                messagebox.showerror("Login Failed", "Invalid Password")
                password_entry.delete(0, ttk.END)
                
        
        # ------------------------------------------------ RESET CONFIRMATION ---------------------------------------
        
        warning_window = tk.Toplevel(root)
        warning_window.title("Reset Confirmation")
        warning_window.geometry("800x600")
        
        warning_window.grab_set()

        confirm_label = ttk.Label(warning_window, text="Enter Master Password:")
        confirm_label.pack(pady=10)

        confirm_entry = ttk.Entry(warning_window, justify="center", show="*", font=("Aptos", 16))
        confirm_entry.pack(pady=10)

        warning_label = ttk.Label(warning_window, text="Are you sure you want to reset the application?\nThere is no way to recover the deleted passwords.")
        warning_label.pack(pady=10)

        reset_button = ttk.Button(warning_window, text="RESET", command=confirm)
        reset_button.pack(pady=10)
        
        
    def change_masterpass():
        
        def confirm_change():
            
            password0 = change_entry0.get()
            password1 = change_entry1.get()
            password2 = change_entry2.get()
            
            
            if password0 !=crypt_1 .masterpassword:
                
                messagebox.showerror("Error", "Wrong Masterpassword")
                change_entry0.delete(0, ttk.END)
                change_entry1.delete(0, ttk.END)
                change_entry2.delete(0, ttk.END)
                
            else:
            
                if(password1 == ""):
                    messagebox.showerror("Error", "Enter a valid password")
                else:
                    if(password1 != password2):
                    
                        messagebox.showerror("Error", "New passwords didn't match")
                        change_entry0.delete(0, ttk.END)
                        change_entry1.delete(0, ttk.END)
                        change_entry2.delete(0, ttk.END)
                        
                    else:
                        crypt_1.replace(password1)
                        data = backend.retrieve_user()
                        for value in data:
                            
                            ciphertext = crypt_1.write_encrypt_password(value[2], password2)
                            
                            backend.update_user(ciphertext)
                            changePW_window.destroy()
                        
        
        # -----------------------------------------------CHANGE MASTERPASSWORD----------------------------------------------------------
        
        changePW_window = tk.Toplevel(root)
        changePW_window.title("Change Masterpassword")
        changePW_window.geometry("800x600")
        changePW_window.grab_set()


        change_label_Previous = ttk.Label(changePW_window, text="Enter Old Master Password:")
        change_label_Previous.pack(pady=10)

        change_entry0 = ttk.Entry(changePW_window, justify="center", font=("Aptos", 16))
        change_entry0.pack(pady=10)

        change_label = ttk.Label(changePW_window, text="Enter New Master Password:")
        change_label.pack(pady=10)

        change_entry1 = ttk.Entry(changePW_window, justify="center", font=("Aptos", 16))
        change_entry1.pack(pady=10)
        
        change_label = ttk.Label(changePW_window, text="Re-enter New Master Password:")
        change_label.pack(pady=10)

        change_entry2 = ttk.Entry(changePW_window, justify="center", font=("Aptos", 16))
        change_entry2.pack(pady=10)
        

        change_button = ttk.Button(changePW_window, text="CHANGE", command=confirm_change)
        change_button.pack(pady=10)
   
   
    #--------------------------------------------------FORGOT PASSWORD WINDOW-----------------------------------------------
        
    def forgot_password():
        def display():
            
            input = input_field_notes.get("1.0", "end-1c")
            
            data = backend.retrieve_user()
            for value in data:
                if (input == value[2]):
                    masterpassword = crypt_1.test_masterpassword(value[2],value[1])
                    
                    def copy():
                        
                        def copy_and_clear():
                            
                            pyperclip.copy(masterpassword)

                            time.sleep(5)

                            pyperclip.copy('')
                        
                        copy_and_clear()
                        
                        
                        
                        error_window.destroy()
                        phrase_modal.destroy()
                      
            
                    error_window = tk.Toplevel(phrase_modal)
                    error_window.title("Error")
                    error_window.geometry("600x400")
                    
                    label_error = ttk.Label(error_window, text=f"Your master password is {masterpassword}")
                    label_error.pack(padx=20, pady=10)
                    
                    ok_button = ttk.Button(error_window, text="Copy Password", command=copy)
                    ok_button.pack(pady=10)
                else:
                    messagebox.showerror("Login Failed", "Phrase dosen't match")



        phrase_modal = ttk.Toplevel(password_modal)
        phrase_modal.title("Test Phrase")
        phrase_modal.geometry("800x600")

        frame = ttk.Frame(phrase_modal)
        frame.pack(padx=100, pady=100)

        text_label = ttk.Label(frame, text="Enter Phrase:", font=("Aptos", 15))
        text_label.pack(pady=5)

        input_field_notes = tk.Text(frame, font=("Aptos", 15), width=50, height=10)
        input_field_notes.pack()

        error_button = ttk.Button(frame, text="ENTER", command=display)
        error_button.pack(pady=20)


        root.mainloop()

    #----------------------------------------------- MAIN WINDOW ------------------------------------------------------------

    root = ttk.Window(themename="flatly")
    root.title("Main_Window")
    root.geometry("1200x800")

    #FRAMES
    
    option_frame = ttk.Frame(root, width=400)
    option_frame.pack(side="left",padx=200)

    tree_frame = ttk.Frame(root, width=150, height=1000)
    tree_frame.pack(side="top", fill="both", expand=True)


    txtfield_frame = ttk.Frame(tree_frame, height=50)
    txtfield_frame.pack(side="bottom", fill="both" )

    dbutton_frame = ttk.Frame(txtfield_frame, height=50)
    dbutton_frame.pack(side="bottom", fill="both", padx=200)


    # TREE SECTION

    my_tree = ttk.Treeview(
        tree_frame,
        columns=("Serial_No","Title", "Username","Password","Notes", "Last_Modified")
    )

    my_tree.column("#0", width=0, stretch=ttk.NO)  
    my_tree.column("Serial_No", width=0, stretch=ttk.NO)
    my_tree.column("Title", anchor=ttk.W, width=500)
    my_tree.column("Username", anchor=ttk.W, width=500)
    my_tree.column("Password", width=0, stretch=ttk.NO)
    my_tree.column("Notes", width=0, stretch=ttk.NO)
    my_tree.column("Last_Modified", anchor=ttk.W, width=500)

    my_tree.heading("#0", text="", anchor=ttk.W)
    my_tree.heading("Serial_No", text='', anchor=ttk.W)
    my_tree.heading("Title", text="Title", anchor=ttk.W)
    my_tree.heading("Username", text="Username", anchor=ttk.W)
    my_tree.heading("Password", text='', anchor=ttk.W)
    my_tree.heading("Notes", text='', anchor=ttk.W)
    my_tree.heading("Last_Modified", text="Last_Modified", anchor=ttk.W)


    my_tree.tag_configure("custom_font", font=("Aptos", 12))  
    style = ttk.Style()
    style.configure("Treeview", rowheight=30)  



    # SCROLLBAR
    vsb = tk.Scrollbar(tree_frame, orient="vertical", command=my_tree.yview)
    vsb.pack(side="right", fill="y")


    # SCROLLBAR-WIDGET FUNCTIONALITY
    my_tree.configure(yscrollcommand=vsb.set)
    my_tree.pack(fill="both", expand=True)
    tree_frame.bind("<Configure>", set_scrollbar_height)
    my_tree.bind("<ButtonRelease-1>", on_treeview_click)


    # TEXTFIELD
    output_text = tk.Text(txtfield_frame, wrap=tk.WORD, state=tk.DISABLED)
    output_text.pack(fill="both", expand=True)

    custom_font = ("Aptos", 12)
    output_text.tag_configure("custom_tag", font=custom_font)



    # BUTTON_FRAME
    refresh_button = ttk.Button(option_frame, text="Refresh", padding=10, command=update_treeview)
    refresh_button.pack(side="top", fill="both", expand=True, pady=40)
    
    create_button = ttk.Button(option_frame, text="Add", padding=10, command=create)
    create_button.pack(side="top", fill="both", expand=True, pady=40)

    edit_button = ttk.Button(option_frame, text="  Edit  ", padding=10, command=edit)
    edit_button.pack(side="top", fill="both", expand=True, pady=40)

    delete_button = ttk.Button(option_frame, text="Delete", padding=10, command=delete)
    delete_button.pack(side="top", fill="both", expand=True, pady=40)

    reset_button = ttk.Button(option_frame, text="Hard_Reset", padding=10, command=hard_reset)
    reset_button.pack(side="top", fill="both", expand=True, pady=40)
    
    changePW_button = ttk.Button(option_frame, text="Change Master_Password", padding=10, command=change_masterpass)
    changePW_button.pack(side="top", fill="both", expand=True, pady=40)

    exit_button = ttk.Button(option_frame, text="  Exit  ", padding=10, command=exit)
    exit_button.pack(side="top", fill="both", expand=True, pady=40)

    # CLIPBOARD FRAME
    
    countdown_var = tk.StringVar()
    countdown_var.set("")
    

    progress_var = tk.DoubleVar()
    progress_var.set(100.0)



    user_copybutton = ttk.Button(dbutton_frame, text="Copy Username", command=start_countdown_U)

    pass_copybutton = ttk.Button(dbutton_frame, text="Copy Password", command=start_countdown_P)

    progressbar = ttk.Progressbar(dbutton_frame, variable=progress_var, length=200)
    progressbar_status = tk.Label(dbutton_frame, textvariable=countdown_var)
    
    



    #----------------------------------------------------------- LOGIN PAGE -------------------------------------------------------
    
    password_modal = ttk.Toplevel(root)
    

    password_modal.title("Password Login")
    password_modal.geometry("1200x800")

    main_frame = ttk.Frame(password_modal)
    main_frame.pack(fill=tk.BOTH, expand=True, padx=200, pady=(150,50))

    upper_frame = ttk.Frame(main_frame)
    upper_frame.pack(pady=(150, 50))

    password_label = ttk.Label(upper_frame, text="Master Password:", font=("Aptos", 25))
    password_label.pack(pady=5)

    password_entry = ttk.Entry(upper_frame, justify="center", show="*", width=30, font=("Aptos", 22))
    password_entry.pack(pady=5)


    login_button = ttk.Button(upper_frame, text="LOGIN", command=login)
    login_button.pack(pady =10)

    upper_frame = ttk.Frame(upper_frame)
    upper_frame.pack(pady=(50,0))

    login_button = ttk.Button(upper_frame, text="FORGOT PASSWORD", command=forgot_password)
    login_button.pack(pady =10)

    login_button = ttk.Button(upper_frame, text="RESET", command=reset)
    login_button.pack(pady =10)


  
    password_modal.state('zoomed')
    
    
    
    root.withdraw()
    
    user = backend.user_count()
    
    if user==0:
    
        password_modal.withdraw()
        user_not_exist()
    
    
    root.mainloop()
    


    



start()

