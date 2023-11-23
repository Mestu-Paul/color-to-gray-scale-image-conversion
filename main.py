import tkinter as tk
from tkinter import filedialog
import cv2,os
from PIL import Image, ImageTk

image_file_name=""

def setInLabel(imageToSet,img_lbl):
    # Convert OpenCV image to PIL format
    pil_image = Image.fromarray(imageToSet)
    # Get image dimensions (width and height)
    image_width, image_height = pil_image.size
    image_ratio = image_width/image_height
    

    # Resize image to fit label dimensions
    label_height = min(500,image_height)
    label_width = (int)(image_ratio*label_height)
    pil_image = pil_image.resize((label_width, label_height), Image.ANTIALIAS)
    
    # Convert resized PIL image to PhotoImage for display in Tkinter
    pil_image = ImageTk.PhotoImage(pil_image)
    
    # Update the label with the uploaded image
    img_lbl.config(image=pil_image)
    img_lbl.image = pil_image  # Keep a reference to the image to prevent garbage collection

    
def upload_image():
    global image_path
    image_path = filedialog.askopenfilename(initialdir=os.path.abspath("./color-to-gray-scale-image-conversion/original_images"))
    global image_file_name
    image_file_name=os.path.basename(image_path)
    
    print("Image uploaded:", image_path)
    
    # Read the uploaded image using OpenCV
    uploaded_image = cv2.imread(image_path)
    uploaded_image = cv2.cvtColor(uploaded_image, cv2.COLOR_BGR2RGB)  # Convert image to RGB format
    setInLabel(uploaded_image,img_lbl)
           
def convert_to_grayscale():
    global image_path
    if image_path:
        image = cv2.imread(image_path)
        # grayscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
         # Convert the image to grayscale manually
        height, width, channels = image.shape
        grayscale_image = image.copy()
        
        for y in range(height):
            for x in range(width):
                # Get RGB values
                blue = int(image[y, x, 0])
                green = int(image[y, x, 1])
                red = int(image[y, x, 2])
                
                # Calculate grayscale value (weighted sum)
                gray = (red+green+blue)/3 
                gray1 = (red * 0.299) + (green * 0.587) + (blue * 0.114)
               
                # Assign grayscale value to each channel (R, G, B)
                grayscale_image[y, x] = [gray, gray, gray]
        
        setInLabel(grayscale_image,img_lbl1)
        global image_file_name
        save_path = filedialog.asksaveasfile(initialdir=os.path.abspath("./color-to-gray-scale-image-conversion/converted_images")
                    ,defaultextension=".jpg", filetypes=[("JPEG files", "*.jpg")],initialfile=image_file_name)
        if save_path:
            cv2.imwrite(save_path.name, grayscale_image)
            print("Image converted to grayscale and saved.")
        print("Image converted to grayscale.")
    else:
        print("Please upload an image first.")

root = tk.Tk()
root.title("Image Processing")
root.geometry('1100x650+10+10')
root.minsize(1100,650)

tk.Label(root,text="Color Image To Gray Scale Image"
         ,font=("Arial", 14, "bold")).pack(side=tk.TOP)

frame = tk.Frame(root)
frame.place(relx=0.4, rely=0.05, relwidth=0.3, height=50)

upload_button = tk.Button(frame, text="Upload", command=upload_image)
upload_button.pack(side=tk.LEFT, padx=20, pady=10)

convert_button = tk.Button(frame, text="Convert to Grayscale", command=convert_to_grayscale)
convert_button.pack(side=tk.LEFT, padx=20, pady=10)

# Create a frame to display image
img_frame = tk.Frame(root)
img_frame.place(relx=0, rely=0.15, relheight=0.75, relwidth=1)

img_f1 = tk.Frame(img_frame)
img_f1.pack(side=tk.LEFT, padx=20, pady=10)
img_lbl = tk.Label(img_f1)
img_lbl.pack(side=tk.TOP, padx=20, pady=10)
img_txt = tk.Label(img_f1,text="Original Image",font=("Arial", 14, "bold"))
img_txt.pack(side=tk.BOTTOM, padx=20, pady=10)

img_f2 = tk.Frame(img_frame)
img_f2.pack(side=tk.RIGHT, padx=20, pady=10)
img_lbl1 = tk.Label(img_f2)
img_lbl1.pack(side=tk.TOP, padx=20, pady=10)
img_txt1 = tk.Label(img_f2,text="Converted image",font=("Arial", 14, "bold"))
img_txt1.pack(side=tk.BOTTOM, padx=20, pady=10)

root.mainloop()


