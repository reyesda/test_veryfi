from .receipt import Receipt
from .read_file import get_all_files_by_extension


from PIL import Image, ImageDraw, ImageFont, ImageTk
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog


def graph_receipt(receipt: object)-> object:
    max_min = receipt.get_max()
    main_blocks = receipt.get_all_list_info_blocks()

    width = max_min[0] + 5
    height = max_min[1] + 5

    white = (250, 250, 250)
    black = (0, 0, 0)
    gray = (70, 70, 70)

    img  = Image.new( mode = "RGB", size = (width, height) , color= white)
    draw = ImageDraw.Draw(img)

    color=[gray, black, gray]
    size = 29

    for n in range(3):
        for i in main_blocks[n]:
            # draw.rectangle((i[0], i[1], i[4], i[5]), outline=black)

            font = ImageFont.truetype("arial.ttf", size)
            draw.text((i[0], i[1]),i[-1],font=font, fill=color[n])

            size = 17

    return img

class GuiMain:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.configure(padx=5, pady=5)
        self.height = 680
        self.setup_screen(self.height)
        # ====================================================
        self.background_color_opcion = "#f8f8f8"
        self.frame_options = tk.Frame(self.root,width=250 ,bg=self.background_color_opcion,
                                      relief="flat", padx=5, pady=5)
        self.frame_options.pack_propagate(False)
        self.frame_options.pack(side="right", fill='y', expand=False)
        # ====================================================
        self.background_color_opcion = "#f0f0f0"
        self.frame_json = tk.Frame(self.root, width=350, bg=self.background_color_opcion,
                                      relief="flat", padx=5, pady=5)
        self.frame_json.pack_propagate(False)
        self.frame_json.pack(side="right", fill='y', expand=False)
        # ====================================================
        self.background_color_opcion = "#f8f8f8"
        self.frame_ime = tk.Frame(self.root, bg=self.background_color_opcion,
                                      relief="flat", padx=5, pady=5)
        self.frame_ime.pack_propagate(False)
        self.frame_ime.pack(side="right", fill='both', expand=True)
        # ====================================================

        OptionContainer(self)

    def setup_screen(self, height):
        self.root.title("Receipts")

        w = int(height * 1.6)
        ws = self.root.winfo_screenwidth()
        hs = self.root.winfo_screenheight()

        self.root.geometry(f'{w}x{height}+{int(round((ws - w) * 0.5, 0))}+{int(round((hs - height) * 0.5, 0))}')
        self.root.wm_minsize(w, height)
        self.root.wm_maxsize(w, height)


class OptionContainer:
    def __init__(self, main_frame):
        self.filename = ''
        self.open_button = ttk.Button(main_frame.frame_options, text="Choose a file to upload",
                                      cursor="hand2", width=25, command=lambda: self.bottom_function(main_frame))
        self.open_button.pack(side="top", fill='x', expand=False)

        self.label_var = tk.StringVar()
        self.open_label = tk.Label(main_frame.frame_json, textvariable=self.label_var, wraplength=250, justify='left')
        

        self.canvas = tk.Canvas(main_frame.frame_ime)


        self.open_button_directory = ttk.Button(main_frame.frame_options, text="Choose a directory",
                                      cursor="hand2", width=25, command=lambda: self.bottom_function_directory(main_frame))
        self.open_button_directory.pack(side="top", fill='x', expand=False)

        self.files_from_directory = {}

        self.labels_request = ['Files']

        self.current_var_drop_request = tk.StringVar()
        self.drop_request = ttk.Combobox(main_frame.frame_options, values=self.labels_request,
                                         textvariable=self.current_var_drop_request,
                                         state="disabled", width=23)
        self.drop_request.current(0)
        self.drop_request.pack(side="top", fill='x', expand=False)

        self.drop_request.bind('<<ComboboxSelected>>',  lambda event: self.selected(event, main_frame))

        


    def bottom_function(self, main_frame):
        self.open_file(main_frame)

    def open_file(self, main_frame):
        try:
            self.filename = filedialog.askopenfile(title="Open File", filetypes=(("jtl files", "*.txt"), ("all files", "*.*")))
            type(self.filename.name)

            self.show_data(main_frame, Receipt(self.filename.name))

            self.drop_request.configure(state='disable')
            self.labels_request = [self.filename.name.split("/")[-1]]
            self.drop_request['values'] = self.labels_request 
            self.drop_request.current(0)

        except AttributeError:
            self.read_document_error = True

    def show_data(self, main_frame, receipt):
        self.open_label.pack(side="top", fill='x', expand=True)

        self.label_var.set(receipt)
        

        newsize = (main_frame.frame_ime.winfo_width() - 5, main_frame.frame_ime.winfo_height()- 5)
        photo = ImageTk.PhotoImage(graph_receipt(receipt).resize(newsize))

        self.canvas.delete("all")
        self.canvas.pack(side="top", fill='both', expand=True)
        
        self.canvas.photo = photo
        self.canvas.create_image(0, 0, image=photo, anchor='nw')

    def bottom_function_directory(self, main_frame):
        self.open_file_directory(main_frame)

    def open_file_directory(self, main_frame):
        try:
            self.directory_name = filedialog.askdirectory()
            type(self.directory_name)

            self.files_from_directory = get_all_files_by_extension(self.directory_name, '.txt')
            self.drop_request.configure(state='readonly')
            self.labels_request = list(self.files_from_directory.keys())
            self.drop_request['values'] = self.labels_request 
            self.drop_request.current(0)
            self.selected(None, main_frame)

        except AttributeError:
            self.read_document_error = True

    def selected(self, event, main_frame):
        path = self.files_from_directory[self.drop_request.get()]
        self.show_data(main_frame, Receipt(path))