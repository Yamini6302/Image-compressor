import sys
from PyQt5.QtWidgets import QApplication, QFileDialog,QInputDialog, QWidget, QMainWindow, QFrame, QLabel, QLineEdit, QPushButton, QComboBox
from PyQt5.QtGui import QIcon
from PIL import Image
from PyQt5.QtCore import Qt
import os
import PIL
import time
import sys, os
import numpy as np
import cv2
import zlib


class App(QMainWindow):

    def __init__(self):
        super().__init__()          
        self.title = 'Image Compressor'
        self.left = 10  
        self.top = 10
        self.width = 400
        self.height = 600
        self.statusBar().showMessage("Message:")
        self.statusBar().setObjectName("status")
        self.image_width = 0
        self.setFixedSize(self.width, self.height)
        self.setObjectName("main_window")
        stylesheet = ""
        with open("design.qss", "r") as f:
            stylesheet =  f.read()
        self.setStyleSheet(stylesheet)
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
       
         #------------------main window-------------------------- 
        
        self.single_bubble_expanded =QFrame(self)
        self.single_bubble_expanded.setObjectName("bubble_expanded")
        self.single_bubble_expanded.move(50, 100)
        self.single_bubble_expanded.setVisible(True)

        self.single_bubble_heading = QLabel(self.single_bubble_expanded)
        self.single_bubble_heading.setObjectName("bubble_heading")
        self.single_bubble_heading.setText("Compress Image")
        self.single_bubble_heading.move(90, 8)

        self.select_image_label = QLabel(self.single_bubble_expanded)
        self.select_image_label.setObjectName("bubble_para")
        self.select_image_label.setText("Choose Image")
        self.select_image_label.move(30,50)
        

        self.image_path = QLineEdit(self.single_bubble_expanded)
        self.image_path.setObjectName("path_text")
        self.image_path.move(60, 85)

        self.browse_button = QPushButton(self.single_bubble_expanded)
        self.browse_button.setText("...")
        self.browse_button.setObjectName("browse_button")
        self.browse_button.clicked.connect(self.select_file)
        self.browse_button.move(240,85)


        self.compress_image = QPushButton(self.single_bubble_expanded)
        self.compress_image.setText("Compress")
        self.compress_image.setObjectName("compress_button")
        self.compress_image.clicked.connect(self.resize_pic)
        self.compress_image.move(100,260)

        # -------------------end main window------------------------------

        self.show()


    #------------------------functions -----------------------------------

    def select_file(self):
       
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);; JPEG (*.jpeg)")
        if fileName:
            print(fileName, _)
            self.image_path.setText(fileName)
            img = Image.open(fileName)
 
    def resize_pic(self):
        old_pic = self.image_path.text()

        if old_pic == "":
            self.statusBar().showMessage("Message: Please choose an image")
            return
            
        print(old_pic)
        
        directories = self.image_path.text().split("/")
        print(directories)
        new_pic = ""
        new_pic_name, okPressed = QInputDialog.getText(self, "Save Image as","Image Name:", QLineEdit.Normal, "")
        if okPressed and new_pic_name != '':
            print(new_pic_name)

            if old_pic[-4:] == ".jpeg":
                new_pic_name+=".jpeg"           

            if old_pic[-4:] == ".png":
                new_pic_name+=".png"           

            if old_pic[-4:] == ".jpg":
                new_pic_name+=".jpg"    
            else:
                new_pic_name+=".jpeg"       
            
            for directory in directories[:-1]:
                new_pic = new_pic + directory + "/"

            new_pic+=new_pic_name
            print(new_pic)
        
        self.compreesion_code(old_pic, new_pic)
        self.statusBar().showMessage("Message: Compressed")

   
    
    def compreesion_code(self, old_pic, new_pic):
        try: 
            # Load image with PIL
            img_pil = Image.open(old_pic)
            img_pil.show()
            # Convert PIL image to numpy array
            img_np = np.array(img_pil)

            # Compress the image with OpenCV's imencode function
            retval, buffer = cv2.imencode('.jpg', img_np)

            # Convert the compressed buffer to a bytes object
            compressed_bytes = buffer.tobytes()

            # Compress the bytes object using the DEFLATE algorithm
            compressed_data = zlib.compress(compressed_bytes, level=9)

            # Write the compressed data to a file
            with open('input_image_compressed.deflate', 'wb') as f:
                f.write(compressed_data)


            # Load compressed data from file
            with open('input_image_compressed.deflate', 'rb') as f:
                compressed_data = f.read()

            # Decompress the data using the DEFLATE algorithm
            decompressed_data = zlib.decompress(compressed_data)

            # Convert the decompressed data to a buffer
            buffer = np.frombuffer(decompressed_data, dtype=np.uint8)

            # Decode the buffer using OpenCV's imdecode function
            img_np = cv2.imdecode(buffer, cv2.IMREAD_UNCHANGED)

            # Convert the numpy array to a PIL image
            img_pil = Image.fromarray(img_np)

            # Save the decompressed image as a file
            img_pil.save(new_pic)

        except Exception as e:
            self.statusBar().showMessage("Message: "+str(e))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
