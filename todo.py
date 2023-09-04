from tkinter import *
from tkinter.font import Font
from tkinter import filedialog
import pickle
import customtkinter

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")
root = customtkinter.CTk()
root.title('ToDo List Project')
root.geometry("500x625")


#Define font
my_font = Font(
    family="Helvetica",
    size=30,
    weight="bold"
)

#Create frame
my_frame = customtkinter.CTkFrame(root)
my_frame.pack(pady=0)

#Create Listbox
my_list = Listbox(my_frame,
        font=my_font,
        width=25,
        height=8,
        bg="#a4a6a6",
        bd=5,
        fg="#464646",
        highlightthickness=0,
        selectbackground="#a6a6a6",
        activestyle="none")

my_list.pack(side=LEFT, fill=BOTH)

#Create Dict
Items = {}

#Create scrollbar
my_scrollbar = Scrollbar(my_frame)
my_scrollbar.pack(side=RIGHT, fill=BOTH)

#Add scrollbar
my_list.config(yscrollcommand=my_scrollbar.set)
my_scrollbar.config(command=my_list.yview)

#Create entry box
my_entry = customtkinter.CTkEntry(root, font=("Roboto", 24), width=300, placeholder_text="Enter Task")
my_entry.pack(pady=20)

#Create btn frame
# button_frame = customtkinter.CTkFrame(root)
# button_frame.pack(pady=20)

#Functions
def delete_item():
    my_list.delete(ANCHOR)

def add_item():
    entry = my_entry.get()
    my_list.insert(END, entry)
    my_entry.delete(0, END)
    Items[entry] = ""  # Initialize the details as an empty string

def add_item_with_enter(event):
    my_list.insert(END, my_entry.get())
    my_entry.delete(0, END)

def cross_off_item():
    #Cross Off Item
    my_list.itemconfig(
        my_list.curselection(),
        fg="#dedede"
    )

    #Hide Highlight Bar
    my_list.select_clear(0, END)

def uncross_item():
    my_list.itemconfig(
        my_list.curselection(),
        fg="#464646"
    )

    #Hide Highlight Bar
    my_list.select_clear(0, END)

def cleanup_item():
    count = 0
    while count < my_list.size():
        if my_list.itemcget(count, "fg") == "#dedede":
            my_list.delete(my_list.index(count))
        
        else:
            count += 1

def save_list():
    file_name = filedialog.asksaveasfilename(
        initialdir="D:\Projects\ToDo List\Lists",
        title="Save List",
        filetypes=(
            ("Dat Files", "*.dat"), 
            ("All Files", "*.*"))
    )
    if file_name:
        if file_name.endswith(".dat"):
            pass
        else:
            file_name = f'{file_name}.dat'
        #Delete Cross Off Items before saving
        cleanup_item()

    #Get everything from list
    stuff = my_list.get(0, END)

    # Create a list of items with their details
    items_with_details = [(item, Items.get(item, "")) for item in stuff]

    #Open the File
    with open(file_name, 'wb') as output_file:
            # Actually add stuff to file
            pickle.dump(items_with_details, output_file)

def open_list():
    file_name = filedialog.askopenfilename(
        initialdir="D:\Projects\ToDo List\Lists",
        title="Save List",
        filetypes=(
            ("Dat Files", "*.dat"), 
            ("All Files", "*.*"))
    )
    if file_name:
        #Delete current list if there is one
        my_list.delete(0, END)

        #Open the file
        input_file = open(file_name, 'rb')

        # Load the data from the file
        stuff = pickle.load(input_file)

        #Output stuff to screen
        for i in stuff:
            my_list.insert(END, i)
    
def clear_list():
    my_list.delete(0, END)

def edit_item():
    pass

def edit_details(entry):
    selected = my_list.curselection()
    if selected:
        selected_item_text = my_list.get(selected)
        details = Items.get(selected_item_text, "")
        edit_window = Toplevel(root)
        edit_window.title("Edit Details")
        edit_window.geometry("500x500")

        Label(edit_window, text=f"Edit Details for {selected_item_text}").pack()

        edit_box = customtkinter.CTkTextbox(edit_window, font=("Roboto", 20), width=300, height=400)
        edit_box.pack()
        edit_box.insert("1.0", details)

        def save_details():
            new_details = edit_box.get("1.0", "end-1c")
            Items[selected_item_text] = new_details
            edit_window.destroy()

        save_button = customtkinter.CTkButton(edit_window, text="Save", command=save_details)
        save_button.pack(pady=10)

#Hotkeys
root.bind('<Return>', add_item_with_enter)
root.bind('<Double-1>', edit_details)

#Create Menu
my_menu = Menu(root)
root.config(menu=my_menu)

#Add items to menu
file_menu = Menu(my_menu, tearoff=False)
my_menu.add_cascade(label="File", menu=file_menu)

#Add Dropdown items
file_menu.add_command(label="Save List", command=save_list)
file_menu.add_command(label="Open List", command=open_list)
file_menu.add_separator()
file_menu.add_command(label="Clear List", command=clear_list)  

#Add some buttons
delete_btn = customtkinter.CTkButton(root, text="Delete Item", command=delete_item)
add_btn = customtkinter.CTkButton(root, text="Add Item", command=add_item)
cross_off_btn = customtkinter.CTkButton(root, text="Cross Off Item", command=cross_off_item)
uncross_btn = customtkinter.CTkButton(root, text="Uncross Off Item", command=uncross_item)
cleanup_btn = customtkinter.CTkButton(root, text="Clean Up List", command=cleanup_item)

#Btn positioning
delete_btn.pack(pady=10, padx=10)
delete_btn.place(y=460, x=250)
add_btn.pack(pady=10, padx=10)
add_btn.place(y=460, x=100)
cross_off_btn.pack(pady=10, padx=10)
cross_off_btn.place(y=500, x=100)
uncross_btn.pack(pady=10, padx=10)
uncross_btn.place(y=500, x=250)
cleanup_btn.pack(pady=10, padx=10)
cleanup_btn.place(y=540, x=175)


# delete_btn.grid(row=0, column=0)
# add_btn.grid(row=0, column=1, padx=20)
# cross_off_btn.grid(row=0, column=2)
# uncross_btn.grid(row=0, column=3, padx=20)
# cleanup_btn.grid(row=0, column=4)




root.mainloop()