import tkinter as tk
from tkinter import *
from tkinter import filedialog
from tkinter import ttk

import PIL
from PIL import ImageTk, Image

from model.model import Model


class UI(Frame):

    def __init__(self):
        super().__init__()
        self.place(relwidth=0.8, relheight=0.8, relx=0.1, rely=0.1)
        self.filename = Image
        self.model = Model()
        self.initializeUI()

    def initializeUI(self):
        # Initial State of Frame
        self.master.title("Passport Application/Renewal App")
        self.pack(fill=BOTH, expand=True)
        self.configure(bg="#263D42")

        # Title
        lbl = Label(self, text="Fill in the details below", bg="#263D42", fg="white", pady=10)
        lbl.pack()

        # Main Content Pane
        rootCanvas = Canvas(self, height=700, width=700, bg="#263D42", highlightthickness=0)
        rootCanvas.pack()
        rootCanvas.columnconfigure(1, weight=1)

        # Form Labels
        self.fullNameLabel = Label(rootCanvas, text="Full Name:", bg="#263D42", fg="white")
        self.fullNameLabel.grid(row=1, column=0, sticky=W, padx=100, pady=10)

        self.emailLabel = Label(rootCanvas, text="Email Address:", bg="#263D42", fg="white")
        self.emailLabel.grid(row=2, column=0, sticky=W, padx=100, pady=10)

        self.dobLabel = Label(rootCanvas, text="Date of Birth (dd/mm/yyyy)", bg="#263D42", fg="white")
        self.dobLabel.grid(row=3, column=0, sticky=W, padx=100, pady=10)

        self.nationalInsuranceLabel = Label(rootCanvas, text="National Insurance ID:", bg="#263D42", fg="white")
        self.nationalInsuranceLabel.grid(row=4, column=0, sticky=W, padx=100, pady=10)

        self.genderLabel = Label(rootCanvas, text="Gender:", bg="#263D42", fg="white")
        self.genderLabel.grid(row=5, column=0, sticky=W, padx=100, pady=10)

        self.applicationResultLabel = Label(rootCanvas, text="", bg="#263D42", fg="white")
        self.applicationResultLabel.grid(row=8, column=1, sticky=E, padx=10, pady=10)

        # Form Input Fields
        self.fullNameTextField = Entry(rootCanvas)
        self.fullNameTextField.grid(row=1, column=1, sticky=W, padx=20, pady=10)

        self.emailTextField = Entry(rootCanvas)
        self.emailTextField.grid(row=2, column=1, sticky=W, padx=20, pady=10)

        self.dobTextField = Entry(rootCanvas)
        self.dobTextField.grid(row=3, column=1, sticky=W, padx=20, pady=10)

        self.nationalInsuranceTextField = Entry(rootCanvas)
        self.nationalInsuranceTextField.grid(row=4, column=1, sticky=W, padx=20, pady=10)

        genderComboBox = ttk.Combobox(rootCanvas, values=["Select a Gender", "M", "F"], state='readonly')
        genderComboBox.grid(row=5, column=1, sticky=W, padx=20, pady=10)
        genderComboBox.current(0)

        # Images
        self.imageHolder = Canvas(rootCanvas, bg='white', width=150, height=150)
        self.imageHolder.grid(row=1, column=2, sticky=E, padx=100, rowspan=5)
        self.uploadedImage = Label(self.imageHolder, text="Upload an Image", bg="white")
        self.uploadedImage.place(x=20, y=65)

        self.passportImage = PIL.Image.open("images/passport.png")
        size = (150, 150)
        self.resized = self.passportImage.resize(size, Image.ANTIALIAS)
        self.passportPhoto = ImageTk.PhotoImage(self.resized)
        self.passportPhotoHolder = Label(rootCanvas, image=self.passportPhoto, bg="#263D42")
        self.passportPhotoHolder.grid(row=7, column=0, sticky=W, padx=100, pady=10)

        # Buttons
        uploadImageButton = tk.Button(rootCanvas, text="Upload Image", padx=10, pady=10,
                                      fg="white", bg="#263D42", command=self.launchFileBrowser)
        uploadImageButton.grid(row=6, column=0, padx=100, sticky=W, pady=10)
        processApplicationButton = tk.Button(rootCanvas, text="Send Application", padx=10, pady=10,
                                             fg="white", bg="#263D42", command=lambda: self.validateImage())
        processApplicationButton.grid(row=7, column=2, sticky=E, padx=100, pady=50)
        mainloop()

    def launchFileBrowser(self):
        # Upload the Image from File System
        filename = filedialog.askopenfilename(
            initialdir="/home/dan/Documents/University/AI/AssignmentStuff/RealTesting/testing",
            title="Select an Image",
            filetypes=(("Image files",
                        ".jpg .png .bmp .jpeg"),
                       ("all files",
                        "*.*")))

        # Load, save and resize Image
        img = Image.open(filename)
        img = img.resize((150, 150), Image.ANTIALIAS)
        img.save("images/self_portrait.jpg")
        photo = ImageTk.PhotoImage(img)

        # Update Image Placeholder to Display Loaded Image
        self.uploadedImage.configure(image=photo)
        self.uploadedImage.image = photo
        self.uploadedImage.grid(row=7, column=1, sticky=W, padx=0, pady=10)

        mainloop()

    def validateImage(self):
        # Predict the Image provided and store the result.
        predictionResult = self.model.predictEmotion("images/self_portrait.jpg")

        # Checks the result of the prediction and prompts the user of the result.
        if "angry" in predictionResult:
            self.applicationResultLabel.config(text="You are displaying signs of anger, please upload another photo")
        elif "fear" in predictionResult:
            self.applicationResultLabel.config(text="You are displaying signs of fear, please upload another photo")
        elif "happy" in predictionResult:
            self.applicationResultLabel.config(text="You are displaying signs of happiness, please upload another photo")
        elif "sad" in predictionResult:
            self.applicationResultLabel.config(text="You are displaying signs of sadness, please upload another photo")
        elif "surprise" in predictionResult:
            self.applicationResultLabel.config(text="You are displaying signs of surprise, please upload another photo")
        elif "neutral" in predictionResult:
            self.applicationResultLabel.config(text="Application Successful!")
            self.clearInputFields()

    # Clears input forms.
    def clearInputFields(self):
        self.fullNameTextField.delete("0", "end")
        self.emailTextField.delete("0", "end")
        self.dobTextField.delete("0", "end")
        self.nationalInsuranceTextField.delete("0", "end")


# Entry point.
def main():
    root = tk.Tk()
    root.resizable(False, False)
    UI()
    root.mainloop()


if __name__ == '__main__':
    main()
