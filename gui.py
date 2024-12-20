#from tkinter import Tk,Canvas,Button,Frame,filedialog,Message,Toplevel,StringVar,OptionMenu
from tkinter import Canvas,filedialog,Message,Toplevel,StringVar,messagebox,Scale,HORIZONTAL
import tkinter as tk
from tkinter import ttk, Text
from tkinter.ttk import Button,Frame,OptionMenu,Checkbutton
from ttkthemes import ThemedTk
from config import *
import json
import os
from canvas import ImageOnCanvas
from draw_poly import DrawPoly
from draw_rect import DrawRect
from PIL import Image,ImageTk
from log_debug import logger,debug
from tight_box import TightBox
from tkinter import Scrollbar,HORIZONTAL,BOTTOM,RIGHT,VERTICAL,X,Y

class GUI():
    def __init__(self):
        self.root = ThemedTk(theme="radiance")
        INIT_WIDTH,INIT_HEIGHT = self.root.winfo_screenwidth(),self.root.winfo_screenheight()
        boldStyle = ttk.Style ()
        boldStyle.configure("Bold.TButton", font = ('Sans','12','bold'))
        #icon_loc = os.path.join(os.getcwd(),ICON_NAME)
        #img = ImageTk.PhotoImage(master = self.root, file=icon_loc)
        #self.root.wm_iconbitmap(img)
        #self.root.ttk.call('wm', 'iconphoto', self.root._w, img)
        self.root.title("Form Labeller")
        self.root.maxsize(INIT_WIDTH,INIT_HEIGHT)
        self.supported_formats = SUPPORTED_FORMATS

        self.root.bind("<Escape>", self.deselect_all_keybind)
        self.root.bind("<Control-a>", self.select_all_keybind)
        self.root.bind("<t>", self.make_tight_keybind)
        self.root.bind("<y>", self.save_tight_keybind)
        self.root.bind("<r>", self.discard_tight_keybind)
        

        self.left_frame = Frame(self.root,width = BUTTON_WIDTH)
        self.top_frame1 = Frame(self.left_frame,width = BUTTON_WIDTH,height = int(INIT_HEIGHT/2))
        self.top_frame = Frame(self.left_frame,width = BUTTON_WIDTH,height = INIT_HEIGHT - int(INIT_HEIGHT/2))
        self.bottom_frame = Frame(self.root,width = INIT_WIDTH - BUTTON_WIDTH,height=INIT_HEIGHT)

        self.load_image_directory_button = Button(self.top_frame1,text = 'Open Folder',command=self.load_directory,width = int(BUTTON_WIDTH), style ="Bold.TButton")
        self.load_image_directory_button.grid(row = OPEN_FOLDER_ROW,columnspan = 2,sticky = tk.W+tk.E)

        self.prev_img_button = Button(self.top_frame1,text = '← Prev',command=self.previous_img,state = tk.DISABLED,width = int(BUTTON_WIDTH/2), style ="Bold.TButton")
        self.prev_img_button.grid(row= PREV_ROW, column = 0,sticky = tk.W+tk.E)

        self.next_img_button = Button(self.top_frame1,text = 'Next → ',command=self.next_img,width = int(BUTTON_WIDTH/2), style ="Bold.TButton")
        self.next_img_button.grid(row=NEXT_COL,column=1,sticky = tk.W+tk.E)

        self.save_image_button = Button(self.top_frame1, text = 'Save ', command = self.saver,width = int(BUTTON_WIDTH), style ="Bold.TButton")
        self.save_image_button.grid(row = SAVE_ROW, columnspan = 2,sticky = tk.W+tk.E)
        
        self.delete_poly_button = Button(self.top_frame,text = 'Delete Selected',command = self.delete_selected,width = int(BUTTON_WIDTH), style ="Bold.TButton")
        self.delete_poly_button.grid(row=DEL_SELECTED_ROW,columnspan =2,sticky = tk.W+tk.E)

        self.type_choices = TYPE_CHOICES
        self.variable = StringVar(self.top_frame)
        self.variable.set(self.type_choices[0])
        self.type_options = OptionMenu(self.top_frame,self.variable,*self.type_choices,style ="Bold.TButton")
        self.type_options.config(width = int(BUTTON_WIDTH/2))
        self.type_options.grid(row = DROP_DOWN_ROW,column = 0)

        self.save_type_button = Button(self.top_frame, text = 'Save Type', command = self.save_type,width = int(BUTTON_WIDTH/2), style ="Bold.TButton")
        self.save_type_button.grid(row = SAVE_TYPE_ROW, column = 1,sticky = tk.W+tk.E)

        self.deselect_all_button = Button(self.top_frame,text = 'Deselect All',command = self.deselect_all,width = BUTTON_WIDTH, style ="Bold.TButton")
        self.deselect_all_button.grid(row = DESELECT_ALL_ROW,columnspan = 2,sticky = tk.W+tk.E)

        self.select_all_button = Button(self.top_frame,text = 'Select All', command = self.select_all, width = BUTTON_WIDTH, style ="Bold.TButton")
        self.select_all_button.grid(row = SELECT_ALL_ROW,columnspan = 2,sticky = tk.W+tk.E)

        self.draw_poly_button = Button(self.top_frame,text = 'Draw Poly',command = self.draw_poly_func,width = BUTTON_WIDTH, style ="Bold.TButton")
        self.draw_poly_button.grid(row = DRAW_POLY_ROW,columnspan = 2,sticky = tk.W+tk.E)

        self.draw_rect_button = Button(self.top_frame,text = 'Draw Rectangle',command = self.draw_rect_func,width = BUTTON_WIDTH, style ="Bold.TButton")
        self.draw_rect_button.grid(row = DRAW_RECT_ROW,columnspan = 2,sticky = tk.W+tk.E)

        self.delete_all_button = Button(self.top_frame,text = 'Delete All',command = self.delete_all,width = BUTTON_WIDTH, style ="Bold.TButton")

        self.save_poly_button = Button(self.top_frame,text = 'Save Poly',command = self.save_drawing,width = int(BUTTON_WIDTH/2), style ="Bold.TButton")

        self.discard_poly_button = Button(self.top_frame,text = 'Discard Poly',command = self.discard_drawing,width = int(BUTTON_WIDTH/2), style ="Bold.TButton")

        self.save_rect_button = Button(self.top_frame,text = 'Save Rect',command = self.save_drawing,width = int(BUTTON_WIDTH/2), style ="Bold.TButton")

        self.discard_rect_button = Button(self.top_frame,text = 'Discard Rect',command = self.discard_drawing,width = int(BUTTON_WIDTH/2), style ="Bold.TButton")

        self.show_type_button = Button(self.top_frame, text = 'Show Type', command = self.show_type, width = int(BUTTON_WIDTH/2), style = "Bold.TButton")
        self.show_type_button.grid(row = SHOW_TYPE_ROW, column =0, columnspan = 1, sticky = tk.W+tk.E)
        
        self.hide_type_button = Button(self.top_frame, text = 'Hide Type', command = self.hide_type, width = int(BUTTON_WIDTH/2), style = "Bold.TButton")
        self.hide_type_button.grid(row = HIDE_TYPE_ROW, columnspan = 1, column = 1, sticky = tk.W+tk.E)
        
        self.make_tight_button = Button(self.top_frame, text = 'Make Tight', command = self.make_tight, width = int(BUTTON_WIDTH/2), style = "Bold.TButton")
        self.make_tight_button.grid(row = MAKE_TIGHT_ROW, columnspan = 2, column = 0, sticky = tk.W + tk.E)

        self.threshold_scale = Scale(self.top_frame, from_ = 0, to = 255, orient = HORIZONTAL, width = int(BUTTON_WIDTH/2), label = "Binary Threshold")
        self.threshold_scale.set(128)
        self.threshold_scale.grid(row = THRESHOLD_ROW, columnspan = 2, column = 0, sticky = tk.W + tk.E)
        self.label_text = Text(self.top_frame, width = int(BUTTON_WIDTH), height=int(1))
        self.label_text.insert(tk.END, "LABEL_CONTENT")
        self.label_text.grid(row = LABEL_TEXT_ROW, columnspan = 2, column = 0, sticky = tk.W + tk.E)
        self.show_label_text_button = Button(self.top_frame, text = 'Show Label Text', command = self.show_label_text, width = int(BUTTON_WIDTH/2), style = "Bold.TButton")
        self.show_label_text_button.grid(row = LABEL_TEXT_ROW + 1, columnspan = 1, column = 0, sticky = tk.W + tk.E)
        self.save_label_text_button = Button(self.top_frame, text = 'Save Label Text', command = self.save_label_text, width = int(BUTTON_WIDTH/2), style = "Bold.TButton")
        self.save_label_text_button.grid(row = LABEL_TEXT_ROW + 1, columnspan = 1, column = 1, sticky = tk.W + tk.E)
        self.auto_tight_poly = False
        self.auto_tight_poly_checkbutton = Checkbutton(self.top_frame, text="Auto Tighten new Polys", variable=self.auto_tight_poly, command=self.toggle_auto_tight)
        self.auto_tight_poly_checkbutton.grid(row = LABEL_TEXT_ROW + 2, columnspan = 2, column = 0, sticky = tk.W + tk.E)

        self.tight_save_button = Button(self.top_frame, text = 'Accept Tight', command = self.save_tight)

        self.tight_discard_button = Button(self.top_frame, text = 'Discard Tight', command = self.discard_tight)

        self.canvas = Canvas(self.bottom_frame,width = INIT_WIDTH - BUTTON_WIDTH, height = INIT_HEIGHT, borderwidth = 1)
        self.canvas.bind('<Escape>', self.deselect_all)
        self.image_name = None
        #self.image_path = os.path.join('imgs','img1.jpg')
        self.image_dir = None
        self.images_in_dir = None
        self.curr_idx = None
        self.img_cnv = None
        #self.img_cnv = ImageOnCanvas(self.root,self.canvas,self.image_path)
        self.drawing_obj = None
        self.tight_box_obj = None

        self.left_frame.pack(side = tk.LEFT)
        self.top_frame1.pack(side = tk.TOP)
        self.top_frame.pack(side = tk.BOTTOM)
        self.bottom_frame.pack(side = tk.LEFT)
        max_w,max_h = self.canvas.winfo_screenwidth(), self.canvas.winfo_screenheight()
        self.hbar=Scrollbar(self.bottom_frame,orient=HORIZONTAL)
        self.hbar.pack(side=BOTTOM,fill=X)
        self.hbar.config(command=self.canvas.xview)
        self.vbar=Scrollbar(self.bottom_frame,orient=VERTICAL)
        self.vbar.pack(side=RIGHT,fill=Y)
        self.vbar.config(command=self.canvas.yview)
        max_w,max_h = self.canvas.winfo_width(), self.canvas.winfo_height()
        self.canvas.configure(
            #scrollregion=self.canvas.bbox('all'),
            scrollregion=(0,0,max_w-BUTTON_WIDTH,max_h),
            yscrollcommand=self.vbar.set, 
            xscrollcommand=self.hbar.set)
        self.canvas.pack()
        self.hide_buttons()
        self.load_image_directory_button.config(state = "normal")
        

    def select_all_keybind(self, event=None, **kwargs):
        for poly in self.img_cnv.polygons:
            poly.select_polygon()
    
    def deselect_all_keybind(self, event=None, **kwargs):
        for poly in self.img_cnv.polygons:
            poly.deselect_poly()
    
    def make_tight_keybind(self, event=None, **kwargs):
        self.make_tight()
    
    def save_tight_keybind(self, event=None, **kwargs):
        self.save_tight()
    
    def discard_tight_keybind(self, event=None, **kwargs):
        self.discard_tight()
    
    def save_tight(self):
        self.tight_box_obj.save_tight_box()
        self.tight_save_button.grid_forget()
        self.tight_discard_button.grid_forget()
        self.make_tight_button.grid(row = MAKE_TIGHT_ROW, columnspan=2, sticky = tk.W+tk.E)
        self.show_buttons()
        self.tight_box_obj = None
        self.deselect_all()
    
    def toggle_auto_tight(self):
        self.auto_tight_poly = not self.auto_tight_poly

    def discard_tight(self):
        self.tight_box_obj.discard_tight_box()
        self.tight_save_button.grid_forget()
        self.tight_discard_button.grid_forget()
        self.make_tight_button.grid(row = MAKE_TIGHT_ROW, columnspan=2, sticky = tk.W+tk.E)
        self.show_buttons()
        self.tight_box_obj = None

    def show_type(self):
        for poly in self.img_cnv.polygons:
            if poly.select_poly:
                poly.show_type()

    def hide_type(self):
        for poly in self.img_cnv.polygons:
            poly.unshow_type()

    def hide_buttons(self):
        self.load_image_directory_button.config(state=tk.DISABLED)
        self.save_image_button.config(state=tk.DISABLED)
        self.delete_poly_button.config(state=tk.DISABLED)
        self.save_type_button.config(state=tk.DISABLED)
        self.deselect_all_button.config(state=tk.DISABLED)
        self.select_all_button.config(state=tk.DISABLED)
        self.delete_all_button.config(state = tk.DISABLED)
        self.show_type_button.config(state = tk.DISABLED)
        self.hide_type_button.config(state = tk.DISABLED)
        self.make_tight_button.config(state = tk.DISABLED)

    def show_buttons(self):
        self.load_image_directory_button.config(state="normal")
        self.save_image_button.config(state="normal")
        self.delete_poly_button.config(state="normal")
        self.save_type_button.config(state="normal")
        self.deselect_all_button.config(state="normal")
        self.select_all_button.config(state="normal")
        self.delete_all_button.config(state = "normal")
        self.show_type_button.config(state = "normal")
        self.hide_type_button.config(state = "normal")
        self.draw_poly_button.config(state = "normal")
        self.draw_rect_button.config(state = "normal")
        self.make_tight_button.config(state = "normal")

    def select_all(self):
        for poly in self.img_cnv.polygons:
            poly.select_polygon()

    def deselect_all(self): 
        self.hide_type()
        for poly in self.img_cnv.polygons:
            poly.deselect_poly()

    def delete_all(self): 
        result =  messagebox.askyesno("Confirm Delete All","Delete All Annotations?")
        if not result:
            return
        self.select_all()
        self.delete_selected()
        #self.img_cnv.polygons_mutex.acquire()
        #for poly in self.img_cnv.polygons:
        #    poly.delete_self()        
        #self.img_cnv.polygons_mutex.release()

    def save_type(self):
        selected_option = self.variable.get()
        self.img_cnv.polygons_mutex.acquire()
        for poly in self.img_cnv.polygons:
            if poly.select_poly == True:
                if selected_option == "None":
                    poly.poly_type = None
                else:
                    poly.poly_type = selected_option
                #poly.unshow_type()
                #poly.show_type()
        self.img_cnv.polygons_mutex.release()
        self.variable.set(self.type_choices[0])
        #self.deselect_all()
    
    def show_label_text(self):
        selected_poly = [poly for poly in self.img_cnv.polygons if poly.select_poly]
        if len(selected_poly) == 1:
            self.label_text.delete("1.0", "end")
            selected_poly = selected_poly[0]
            self.label_text.insert(tk.END, selected_poly.text)
    
    def save_label_text(self):
        selected_poly = [poly for poly in self.img_cnv.polygons if poly.select_poly]
        self.img_cnv.polygons_mutex.acquire()
        if len(selected_poly) == 1:
            new_label = self.label_text.get("1.0", tk.END)
            print(new_label)
            selected_poly[0].text = new_label.strip()
        self.img_cnv.polygons_mutex.release()

    def load_new_img(self):
        self.canvas.delete('all')
        self.img_cnv = None
        path = os.path.join(self.image_dir, self.image_name)
        self.img_cnv = ImageOnCanvas(self.root,self.bottom_frame,self.canvas,path)
        logger("LOADED: "+self.img_cnv.image_path)

    def load_directory(self):
        while True:
            selection = filedialog.askdirectory()
            if selection == () or selection == '':
                return
            self.root.directory = selection
            self.image_dir = self.root.directory
            file_names = os.listdir(self.image_dir)
            self.images_in_dir = [] 
            self.curr_idx = None
            self.image_name = None
            for name in file_names:
                if name.split('.')[-1] in self.supported_formats:
                    self.images_in_dir.append(name)
            if len(self.images_in_dir) == 0:
                self.pop_up("No supported images in the selected directory")
            else:
                break
        self.show_buttons()
        self.next_img()

    def pop_up(self,text):
        top = Toplevel()
        top.title("ERROR")
        msg = Message(top, text = text)
        msg.pack()
        button = Button(top,text="Dismiss", command = top.destroy)
        button.pack()
       
    def next_img(self):
        if self.curr_idx == None:
            self.curr_idx = -1
        self.curr_idx = self.curr_idx + 1
        if self.curr_idx >= len(self.images_in_dir):
            self.pop_up("Done with Images in this directory")
            self.curr_idx = self.curr_idx -1
            return
        if self.curr_idx > 0:
            self.prev_img_button.config(state = "normal")
        self.image_name = self.images_in_dir[self.curr_idx]
        self.load_new_img()
        self.root.title("Form Labeller - "+self.image_name+"("+str(self.curr_idx+1)+"/"+str(len(self.images_in_dir))+")")

    def previous_img(self):
        if self.curr_idx == 1:
            self.curr_idx = -1
            self.prev_img_button.config(state= tk.DISABLED)
        else:
            self.curr_idx = self.curr_idx -2
        self.next_img()

    def delete_selected(self):
        to_be_deleted = []
        for i,poly in enumerate(self.img_cnv.polygons):
            if poly.select_poly == True:
                poly.delete_self()
                to_be_deleted.append(i)
        j = 0
        for idx in to_be_deleted:
            self.img_cnv.polygons.pop(idx-j)
            self.img_cnv.bbs.pop(idx-j)
            self.img_cnv.poly_type.pop(idx-j)
            j = j + 1

    def start_gui(self):
        self.root.mainloop()

    def saver(self):
        logger("Saving: "+self.img_cnv.image_path)
        self.save_image_button.config(state= tk.DISABLED)
        self.img_cnv.save_json(self.root.directory)
        self.save_image_button.config(state= "normal")

    def draw_poly_func(self):
        self.deselect_all()
        self.img_cnv.drawing_polygon = True
        self.draw_poly_button.grid_forget()
        self.save_poly_button.grid(row = DRAW_POLY_ROW, column = 0,sticky = tk.W+tk.E)
        self.discard_poly_button.grid(row = DRAW_POLY_ROW, column = 1,sticky = tk.W+tk.E)
        self.hide_buttons()
        self.draw_rect_button.config(state=tk.DISABLED)
        self.drawing_obj = DrawPoly(self.bottom_frame,self.canvas,self.img_cnv,RADIUS, self.save_drawing)

    def draw_rect_func(self):
        self.deselect_all()
        self.img_cnv.drawing_polygon = True
        self.draw_rect_button.grid_forget()
        self.save_rect_button.grid(row = DRAW_RECT_ROW, column = 0,sticky = tk.W+tk.E)
        self.discard_rect_button.grid(row = DRAW_RECT_ROW, column = 1,sticky = tk.W+tk.E)
        self.hide_buttons()
        self.draw_poly_button.config(state=tk.DISABLED)
        self.drawing_obj = DrawRect(self.bottom_frame,self.canvas,self.img_cnv,RADIUS)

    def save_drawing(self):
        self.show_buttons()
        self.img_cnv.drawing_polygon = False
        new_poly_pts = self.drawing_obj.pt_coords
        print ("Trying to save polygon with pts:",str(new_poly_pts))
        for pt in self.drawing_obj.points:
            self.canvas.delete(pt) 
        if self.img_cnv.scale_factor != None:
            for i in range(len(new_poly_pts)):
                for j in range(2):
                    new_poly_pts[i][j] = new_poly_pts[i][j] / self.img_cnv.scale_factor
        self.img_cnv.add_poly(new_poly_pts)
        #self.img_cnv.bbs.append(new_poly_pts)
        #self.img_cnv.draw_bbs([self.img_cnv.bbs[-1]])
        #debug (1, str(type(self.drawing_obj))) 
        if isinstance(self.drawing_obj,DrawRect):
            self.save_rect_button.grid_forget()
            self.discard_rect_button.grid_forget()
            self.draw_rect_button.grid(row = DRAW_RECT_ROW, columnspan = 2, sticky = tk.W + tk.E)
        elif isinstance(self.drawing_obj,DrawPoly):
            self.save_poly_button.grid_forget()
            self.discard_poly_button.grid_forget()
            self.draw_poly_button.grid(row = DRAW_POLY_ROW, columnspan = 2, sticky = tk.W + tk.E)
        self.drawing_obj.delete_self()        
        self.drawing_obj = None
        print(f"Auto Tighten: {self.auto_tight_poly}")
        if self.auto_tight_poly:
            poly = self.img_cnv.polygons[-1]
            for polyg in self.img_cnv.polygons:
                polyg.select_poly = False
            poly.select_poly = True
            self.make_tight()
            self.save_tight()
            poly.select_poly = False

    def discard_drawing(self):
        self.show_buttons()
        self.img_cnv.drawing_polygon = False
        #for pt in self.drawing_obj.points:
        #    self.canvas.delete(pt)
        self.drawing_obj.delete_self()
        if isinstance(self.drawing_obj,DrawRect):
            self.save_rect_button.grid_forget()
            self.discard_rect_button.grid_forget()
            self.draw_rect_button.grid(row = DRAW_RECT_ROW, columnspan = 2, sticky = tk.W + tk.E)
        elif isinstance(self.drawing_obj,DrawPoly):
            self.save_poly_button.grid_forget()
            self.discard_poly_button.grid_forget()
            self.draw_poly_button.grid(row = DRAW_POLY_ROW, columnspan = 2, sticky = tk.W + tk.E)
        self.drawing_obj = None

    def make_tight(self):
        self.hide_buttons()
        self.tight_box_obj = TightBox(self.root,self.img_cnv,self.threshold_scale.get())
        self.tight_box_obj.tight_box()
        self.make_tight_button.grid_forget()
        self.tight_save_button.grid(row = MAKE_TIGHT_ROW,column=0,columnspan=1, sticky = tk.W + tk.E)
        self.tight_discard_button.grid(row = MAKE_TIGHT_ROW,column=1,columnspan=1, sticky = tk.W + tk.E)
    
gui = GUI()
gui.start_gui()
