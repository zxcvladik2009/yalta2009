import os
from PyQt5.QtWidgets import (
   QApplication, QWidget,
   QFileDialog,
   QLabel, QPushButton, QListWidget,
   QHBoxLayout, QVBoxLayout
)
from PyQt5.QtCore import Qt # потрібна константа Qt.KeepAspectRatio для зміни розмірів із збереженням пропорцій
from PyQt5.QtGui import QPixmap # оптимізована для показу на екрані картинка
 
from PIL import Image
from PIL.ImageQt import ImageQt # Для перенесення графіки з Pillow до QT
from PIL import ImageFilter
from PIL.ImageFilter import (
   BLUR, CONTOUR, DETAIL, EDGE_ENHANCE, EDGE_ENHANCE_MORE,
   EMBOSS, FIND_EDGES, SMOOTH, SMOOTH_MORE, SHARPEN,
   GaussianBlur, UnsharpMask
)
 
app = QApplication([])
win = QWidget()      
win.resize(700, 500)
win.setWindowTitle('Easy Editor')
lb_image = QLabel("Картинка")
btn_dir = QPushButton("Папка")
lw_files = QListWidget()
 
btn_left = QPushButton("Вліво")
btn_right = QPushButton("Вправо")
btn_flip = QPushButton("Відзеркалити")
btn_sharp = QPushButton("Різкість")
btn_bw = QPushButton("Ч/Б")
 
row = QHBoxLayout()          # Головна лінія
col1 = QVBoxLayout()         # ділиться на два стовпці
col2 = QVBoxLayout()
col1.addWidget(btn_dir)      # в першому - кнопка вибору каталогу
col1.addWidget(lw_files)     # і список файлов
col2.addWidget(lb_image, 95) # в другому - картинка
row_tools = QHBoxLayout()    # і ряд кнопок
row_tools.addWidget(btn_left)
row_tools.addWidget(btn_right)
row_tools.addWidget(btn_flip)
row_tools.addWidget(btn_sharp)
row_tools.addWidget(btn_bw)
col2.addLayout(row_tools)
 
row.addLayout(col1, 20)
row.addLayout(col2, 80)
win.setLayout(row)
 
win.show()
 
workdir = ''
 
def filter(files, extensions):
   result = []
   for filename in files:
       for ext in extensions:
           if filename.endswith(ext):
               result.append(filename)
   return result
 
def chooseWorkdir():
   global workdir
   workdir = QFileDialog.getExistingDirectory()
 
def showFilenamesList():
   extensions = ['.jpg','.jpeg', '.png', '.gif', '.bmp']
   chooseWorkdir()
   filenames = filter(os.listdir(workdir), extensions)
 
   lw_files.clear()
   for filename in filenames:
       lw_files.addItem(filename)
 
btn_dir.clicked.connect(showFilenamesList)
 
class ImageProcessor():
   def __init__(self):
      self.image = None
      self.dir = None
      self.filename = None
      self.save_dir = "юра_ковтик_лох"
 
   def loadImage(self, filename):
      self.filename = filename
      fullname = os.path.join(workdir, filename)
      self.image = Image.open(fullname)
 
   def saveImage(self):
      path = os.path.join(workdir, self.save_dir)
      if not(os.path.exists(path) or os.path.isdir(path)):
        os.mkdir(path)
      fullname = os.path.join(path, self.filename)
      self.image.save(fullname)

   def showImage(self, path):
      lb_image.hide()
      pixmapimage = QPixmap(path)
      w, h = lb_image.width(), lb_image.height()
      pixmapimage = pixmapimage.scaled(w, h, Qt.KeepAspectRatio)
      lb_image.setPixmap(pixmapimage)
      lb_image.show()

   def do_bw(self):
      self.image = self.image.convert("L")
      self.saveImage()
      image_path = os.path.join(workdir, self.save_dir, self.filename)
      self.showImage(image_path) 

   def do_mr(self):
      self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
      self.saveImage()   
      image_path = os.path.join(workdir, self.save_dir, self.filename)
      self.showImage(image_path)

   def do_sp(self):
      self.image = self.image.filter(SHARPEN)   
      self.saveImage()   
      image_path = os.path.join(workdir, self.save_dir, self.filename)
      self.showImage(image_path)

   def do_left(self):
      self.image = self.image.transpose(Image.ROTATE_90)   
      self.saveImage()   
      image_path = os.path.join(workdir, self.save_dir, self.filename)
      self.showImage(image_path)

   def do_right(self):
      self.image = self.image.transpose(Image.ROTATE_270)   
      self.saveImage()   
      image_path = os.path.join(workdir, self.save_dir, self.filename)
      self.showImage(image_path)

def showChosenImage():
   if lw_files.currentRow() >= 0:
      filename = lw_files.currentItem().text()
      loader.loadImage(filename)
      loader.showImage(os.path.join(workdir, loader.filename))
 
loader = ImageProcessor()
lw_files.currentRowChanged.connect(showChosenImage)

btn_bw.clicked.connect(loader.do_bw)  
btn_flip.clicked.connect(loader.do_mr)
btn_sharp.clicked.connect(loader.do_sp)
btn_left.clicked.connect(loader.do_left)
btn_right.clicked.connect(loader.do_right)

app.exec()
