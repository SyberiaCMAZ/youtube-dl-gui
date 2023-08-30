import customtkinter
from pytube import YouTube
from download_manager import download_vids
from file_manager import load_settings, save_setting


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("YoutubeDL")
        self.geometry("700x325")
        self.grid_columnconfigure((0, 1), weight=1)
        self.resolution, self.file_type, self.path = load_settings()

        self.entry = customtkinter.CTkEntry(self, placeholder_text="Paste link here!! (CTRL+V)")
        self.entry.grid(row=0, column=0, padx=20, pady=20, sticky="ew", columnspan=2)

        self.button = customtkinter.CTkButton(self, text="Download", command=lambda: download_vids(self.entry.get()))
        self.button.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="ew", columnspan=2)

        self.frame_1 = MyCheckboxFrame(self, "Options", values=[" Resolution:", "File type: ", "Path: "])
        self.frame_1.grid(row=2, column=1, padx=(10, 20), pady=(10, 0), sticky="ew")
        self.grid_columnconfigure(1, weight=1)

        self.frame_2 = MyCheckboxFrame(self, "Video", values=["Title: ", "Lenght: ", "Views: "])
        self.frame_2.grid(row=2, column=0, padx=(20, 10), pady=(10, 0), sticky="ew")
        self.grid_columnconfigure(0, weight=2)

        self.options_button = customtkinter.CTkButton(self, text="Options", command=self.open_settings)
        self.options_button.grid(row=3, column=1, padx=(10, 20), pady=(10, 0), sticky="nsew")

        self.author = customtkinter.CTkLabel(self, text="Michał Syberia")
        self.author.grid(row=3, column=0, padx=(20, 10), pady=(10, 0), sticky="sw")

        self.toplevel_window = None
        self.update()
        self.entry.bind("<<Paste>>", self.on_paste)

    def update(self):
        self.resolution, self.file_type, self.path = load_settings()
        self.frame_1.update_label_text(0, f"Resolution: {self.resolution}")
        self.frame_1.update_label_text(1, f"File type: {self.file_type}")
        self.frame_1.update_label_text(2, f"Path: {self.path}")
         

    def on_paste(self, event):
        yt = YouTube(event.widget.clipboard_get())
        title_length = len(yt.title)
        
        # Calculate the desired minsize based on title length
        min_width = 300 + title_length * 5
        min_height = 300
        
        # Use .after() to adjust the minsize with a slight delay
        self.after(100, lambda: self.minsize(min_width, min_height))

        # Update frame_2
        self.frame_2.update_label_text(0, f"Title: {yt.title}")
        self.frame_2.update_label_text(1, f"Lenght: {yt.length}s")
        self.frame_2.update_label_text(2, f"Author: {yt.author}")
    def open_settings(self):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = ToplevelWindow(self)  # create window if its None or destroyed
        else:
            self.toplevel_window.focus()  # if window exists focus it

class ToplevelWindow(customtkinter.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)
        self.geometry("400x450")
        self.title("Options")

        self.radiobutton_frame1 = MyRadiobuttonFrame(self, "Resolution", values=["Highest", "Lowest"])
        self.radiobutton_frame1.grid(row=0, padx=10, pady=(10, 0), sticky="ewn", columnspan=2)

        self.radiobutton_frame2 = MyRadiobuttonFrame(self, "File type", values=["MP4", "MP3"])
        self.radiobutton_frame2.grid(row=1, padx=10, pady=(10, 0), sticky="ewn", columnspan=2)
        
        self.radiobutton_frame3 = MyRadiobuttonFrame(self, "Path", values=["Desktop", "Downloads", "Custom(WIP)"])
        self.radiobutton_frame3.grid(row=2, padx=10, pady=(10, 0), sticky="ewn", columnspan=2)
        
        self.submit_button = customtkinter.CTkButton(self, text="Submit", command=self.submit_options)
        self.submit_button.grid(row=3, column=0, padx=(20, 10), pady=(10, 0), sticky="ewn", columnspan=2)
        
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.grab_set()

        # Set the values of the radio buttons
        self.radiobutton_frame1.set(self.master.resolution)
        self.radiobutton_frame2.set(self.master.file_type)
        self.radiobutton_frame3.set(self.master.path)        

    def submit_options(self):
        #get
        resolution = self.radiobutton_frame1.get()
        file_type = self.radiobutton_frame2.get()
        path = self.radiobutton_frame3.get()
        #update 
        self.master.resolution = resolution
        self.master.file_type = file_type
        self.master.path = path
        #save
        save_setting(resolution, file_type, path)
        self.master.update()
        self.destroy()


        
    
        

class MyRadiobuttonFrame(customtkinter.CTkFrame):
    def __init__(self, master, title, values):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        self.values = values
        self.title = title
        self.radiobuttons = []
        self.variable = customtkinter.StringVar(value="")

        self.title = customtkinter.CTkLabel(self, text=self.title, fg_color="gray30", corner_radius=6)
        self.title.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="ew")

        for i, value in enumerate(self.values):
            radiobutton = customtkinter.CTkRadioButton(self, text=value, value=value, variable=self.variable)
            radiobutton.grid(row=i + 1, column=0, padx=10, pady=(10, 0), sticky="w")
            self.radiobuttons.append(radiobutton)

    def get(self):
        return self.variable.get()

    def set(self, value):
        self.variable.set(value)


class MyCheckboxFrame(customtkinter.CTkFrame):
    def __init__(self, master, title, values):
        super().__init__(master)
        self.values = values
        self.title = title
        self.info = []

        self.title = customtkinter.CTkLabel(self, text=self.title, fg_color="gray30", corner_radius=6)
        self.title.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="ew")
        self.columnconfigure(0, weight=1)

        for i, value in enumerate(self.values):
            checkbox = customtkinter.CTkLabel(self, text=value)
            checkbox.grid(row=i+1, column=0, padx=10, pady=(10, 0), sticky="w")
            self.info.append(checkbox)
    def update_label_text(self, index, new_text):
        self.info[index].configure(text=new_text)


