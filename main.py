import tkinter as tk
from tkinter import filedialog
import cv2,os
from PIL import Image, ImageTk
from pathlib import Path

class global_variable:
    upload_file_label = None

    upload_file_preview_lbl = None
    upload_file_title_lbl = None 
    convert_file_preview_lbl = None
    convert_file_title_lbl = None
    def __init__(self) -> None:
        pass
gv = global_variable()

class Action:
    upload_file_name=""
    image_path=None
    input_directory=Path("./output/uploaded_image/")
    input_file=""
    output_directory=Path("./output/converted_image/")
    output_file=""
    def __init__(self) -> None:
        pass
    
    def saveImage(self, directory, file_name, image):
        location = os.path.join(directory,file_name)
        cv2.imwrite(location, image)
        
    def setImage(self, setToImage, lbl):
        pil_image = Image.fromarray(setToImage)
        
        image_width, image_height = pil_image.size
        image_ratio = image_width/image_height
        
        label_height = min(image_height,max(100,lbl.winfo_height()))
        label_width = (int)(image_ratio*label_height)
        pil_image = pil_image.resize((label_width, label_height), Image.ANTIALIAS)
        
        pil_image = ImageTk.PhotoImage(pil_image)
        
        lbl.config(image=pil_image)
        lbl.image = pil_image  # Keep a reference to the image to prevent garbage collection

    def upload(self):
        self.image_path = filedialog.askopenfilename(initialdir=os.path.abspath("./color-to-gray-scale-image-conversion/original_images"))
        try:
            self.upload_file_name=os.path.basename(self.image_path)
            
            uploaded_image = cv2.imread(self.image_path)
            uploaded_image_rgb = cv2.cvtColor(uploaded_image, cv2.COLOR_BGR2RGB)  # Convert image to RGB format
            upload_file_label.config(text=self.upload_file_name)
            self.setImage(uploaded_image_rgb,upload_file_preview_lbl)
            
            self.upload_file_name = (str)(1+len(list(self.input_directory.glob("*"))))+".jpg"
            
        except Exception as e:
            print("Error while uploading:",e)
    def convert_to_grayscale(self):
        try:
            if self.image_path:
                image = cv2.imread(self.image_path)
                height, width, channels = image.shape
                grayscale_image = image.copy()
                
                for y in range(height):
                    for x in range(width):
                        
                        blue = int(image[y, x, 0])
                        green = int(image[y, x, 1])
                        red = int(image[y, x, 2])
                        
                        gray = (red+green+blue)/3 
                        gray1 = (red * 0.299) + (green * 0.587) + (blue * 0.114)
                    
                        grayscale_image[y, x] = [gray1, gray1, gray1]
                
                self.setImage(grayscale_image,convert_file_preview_lbl)
                self.saveImage(self.output_directory,self.upload_file_name,grayscale_image)
                self.saveImage(self.input_directory,self.upload_file_name,image)
                self.update_recent_act()
            else:
                print("Please upload an image first.")
        except Exception as e:
            print("Error while converting: ",e)
    def update_recent_act(self):
        j = len(list(self.input_directory.glob("*")))
        for i in range(4):
            image_path = os.path.join(obj.input_directory,(str)(j)+".jpg")
            image = cv2.imread(image_path)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) 
            obj.setImage(image,real_images[i])
            
            image_path = os.path.join(obj.output_directory,(str)(j)+".jpg")
            image = cv2.imread(image_path)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) 
            obj.setImage(image,gray_images[i])
            j-=1

obj=Action()

root = tk.Tk()
root.title("Digital Image Processing")
root.geometry('1350x700+0+0')
root.minsize(1350,700)

main_frame = tk.Frame(root,bg="white")
main_frame.pack(fill=tk.BOTH,expand=1)
def on_enter(e, btn,clr="#a9d1df"):
    btn.config(bg=clr)

def on_leave(e, btn,clr="#f8f5f5"):
    btn.config(bg=clr)
    
def on_press(e, btn):
    obj.upload_file_name = btn.cget('text')+".jpg"
    obj.image_path = os.path.join(obj.input_directory,obj.upload_file_name)
    image = cv2.imread(obj.image_path);
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    obj.setImage(image,upload_file_preview_lbl)
    
title_frame = tk.Frame(main_frame,bg="#fafafa")
title_frame.place(relx=0,rely=0,relheight=0.1,relwidth=1)
title_label = tk.Label(title_frame,fg="black", bg="#fafafa", font=("Arial", 20, "bold"),
            text="Color Image To Gray Scale Convertion")
title_label.pack(pady=15)

recent_act_frame = tk.Frame(main_frame,bg="#e5e5e5")
recent_act_frame.place(relx=0,rely=0.1,relheight=0.9,relwidth=0.2)
recent_act_title = tk.Label(recent_act_frame,bg="#e5e5e5",fg="black",font=("Arial", 12, "bold"),
                    text="Recent Activities")
recent_act_title.place(rely=0.001,relheight=0.08,relx=0.25)

recent_act_images_frames = [tk.Frame(recent_act_frame,bg="white") for i in range(4)]
real_images = [tk.Label(recent_act_images_frames[i],text=str(i+1)) for i in range(4)]
gray_images = [tk.Label(recent_act_images_frames[i],text=str(i+1)) for i in range(4)]
for i in range(4):
    recent_act_images_frames[i].place(relx=0.02,relwidth=0.96,rely=0.1+i*(0.22),relheight=0.2)
    recent_act_images_frames[i].bind("<Enter>", lambda e, btn=recent_act_images_frames[i],clr="black": on_enter(e, btn,clr))
    recent_act_images_frames[i].bind("<Leave>", lambda e, btn=recent_act_images_frames[i],clr="white": on_leave(e, btn,clr))
    
    real_images[i].place(relx=0.01,rely=0.01,relheight=.98,relwidth=0.48)
    real_images[i].bind("<Button-1>", lambda e, btn=real_images[i]: on_press(e, btn))
    gray_images[i].place(relx=.51,rely=0.01,relheight=.98,relwidth=0.48)
    gray_images[i].bind("<Button-1>", lambda e, btn=gray_images[i]: on_press(e, btn))
    
obj.update_recent_act()

action_frame = tk.Frame(main_frame,bg="#e5e5e5")
action_frame.place(relx=0.3,rely=0.12,relheight=0.1,relwidth=0.6)

upload_button_frame = tk.Frame(action_frame,bg="#b0a9a9")
upload_button_frame.pack(side=tk.LEFT, padx=10, pady=10)
convert_button_frame = tk.Frame(action_frame,bg="#b0a9a9")
convert_button_frame.pack(side=tk.RIGHT, padx=10, pady=10)


upload_button = tk.Button(upload_button_frame,bg="#f8f5f5", bd=0, text="Upload", height=20, width=20, font=('Arial',14))
upload_button.pack(fill=tk.BOTH, expand=True,padx=1,pady=1)
upload_button.bind("<Enter>",lambda e:on_enter(e,upload_button))
upload_button.bind("<Leave>",lambda e:on_leave(e,upload_button))

upload_file_label = tk.Label(action_frame,bg="#e5e5e5",font=('Arial',11))
upload_file_label.pack(side=tk.LEFT)
upload_button.bind("<Button-1>",lambda e:obj.upload())


convert_button = tk.Button(convert_button_frame,bg="#f8f5f5", bd=0, text="Convert", height=20, width=20, font=('Arial',14))
convert_button.pack(fill=tk.BOTH, expand=True,padx=1,pady=1)
convert_button.bind("<Enter>",lambda e:on_enter(e,convert_button))
convert_button.bind("<Leave>",lambda e:on_leave(e,convert_button))
convert_button.bind("<Button-1>",lambda e:obj.convert_to_grayscale())

image_frame = tk.Frame(main_frame,bg="");
image_frame.place(relx=0.2,rely=0.24,relheight=0.76,relwidth=0.8)

upload_file_preview_lbl = tk.Label(image_frame,text="Uploaded image preview", font=('Arial',10))
upload_file_preview_lbl.place(relx=0.05, rely=0.05,relwidth=0.4,relheight=0.7)
upload_file_title_lbl = tk.Label(image_frame,text="Original Image", font=('Arial',14))
upload_file_title_lbl.place(relx=0.05,rely=0.85, relwidth=0.4, relheight=0.1)

convert_file_preview_lbl = tk.Label(image_frame,text="Gray image preview", font=('Arial',10))
convert_file_preview_lbl.place(relx=.55, rely=0.05,relwidth=0.4,relheight=0.7)
convert_file_title_lbl = tk.Label(image_frame,text="Converted Image", font=('Arial',14))
convert_file_title_lbl.place(relx=0.55,rely=0.85, relwidth=0.4, relheight=0.1)

root.mainloop()