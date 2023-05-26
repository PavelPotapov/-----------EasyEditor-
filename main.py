#создай тут фоторедактор Easy Editor!
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QListWidget,QHBoxLayout,QVBoxLayout, QFileDialog
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import os
from PIL import Image, ImageFilter

app = QApplication([])
win = QWidget()
win.resize(900, 700)
win.setWindowTitle('Easy Editor')

#создание виджетов
lb_image = QLabel('Картинка')
btn_dir = QPushButton('Папка')
lw_files = QListWidget()

btn_left = QPushButton('Лево')
btn_right = QPushButton('Право')
btn_flip = QPushButton('Зеркало')
btn_sharp = QPushButton('Резкость')
btn_bw = QPushButton('Ч/Б')

#лейауты
row = QHBoxLayout() #Основная строка
col1 = QVBoxLayout()
col2 = QVBoxLayout()
row_tools = QHBoxLayout()#строка кнопок

#добавление виджетов в лейауты
col1.addWidget(btn_dir)
col1.addWidget(lw_files)

row_tools.addWidget(btn_left)
row_tools.addWidget(btn_right)
row_tools.addWidget(btn_flip)
row_tools.addWidget(btn_sharp)
row_tools.addWidget(btn_bw)

col2.addWidget(lb_image, 95)
col2.addLayout(row_tools)

row.addLayout(col1, 20)
row.addLayout(col2, 80)

win.setLayout(row)

workdir = ''

class ImageProcessor():
    def __init__(self):
        self.filename = None #храним название картинки
        self.image = None #объект картинки
        self.save_folder = 'Modified'
    
    def loadImage(self, filename):
        self.filename = filename #в свойство класса запомнили название картинки
        file_path = os.path.join(workdir, filename) #сформировали полный путь до картинки. соединили путь до папки (workdir) с названием картинки (filename)
        try:
            self.image = Image.open(file_path) #сохарнили в свойство класса объект картинки, которую загружаем по пути до картинки
        except:
            print('Такой картинки нет')

    def showImage(self, path):
        lb_image.hide() #скрываем выджет на время выполнения тех.работ  
        pixmapimage = QPixmap(path) #создаем объект "специальной" картинки, которую можно вставлять в виджеты pyqt5
        w = lb_image.width() #определяем ширину виджета, куда будем вставлять картинку
        h = lb_image.height() #определяем высотку виджета, куда будем вставлять картинку
        scaled_image = pixmapimage.scaled(w, h, Qt.KeepAspectRatio) #изменяем размеры картинки под размеры виджета (w, h)
        lb_image.setPixmap(scaled_image) #устанавливаем измененную под размеры виджета картинку в этот самый виджет
        lb_image.show() #снова отображаем виджет на экране

    def saveImage(self):
        '''сохраняет копию файла в подпапке'''
        path = os.path.join(workdir, self.save_folder) #формируем путь до подпапки (путь до выбранной папки workdir, внутри этой папке будет создавать подпапка с именем Modified)
        if not(os.path.exists(path) and os.path.isdir(path)): #проверяем, есть ли по заданному пути папка Modified и является ли она папкой, если нет, то
            os.mkdir(path) #создаем ее
        image_path = os.path.join(path, self.filename) #формируем путь до картинки, которая сохранится в папку Modified
        self.image.save(image_path) #сохраняем изображение по сформированному пути
    #черно-белое
    def do_bw(self):
        self.image = self.image.convert('L') #преобразует картинку в черно-белый формат
        self.saveImage() #сохраняет ее
        image_path = os.path.join(workdir, self.save_folder, self.filename) #формируем путь до измененной картинки
        self.showImage(image_path) #показываем эту картинку на экране
    #зеркало
    def do_flip(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT) #зеркалит картинку
        self.saveImage() #сохраняет ее
        image_path = os.path.join(workdir, self.save_folder, self.filename) #формируем путь до измененной картинки
        self.showImage(image_path) #показываем эту картинку на экране
    #резкость
    def do_shrapen(self):
        self.image = self.image.filter(ImageFilter.SHARPEN) #увеличиваем резкость
        self.saveImage() #сохраняет ее
        image_path = os.path.join(workdir, self.save_folder, self.filename) #формируем путь до измененной картинки
        self.showImage(image_path) #показываем эту картинку на экране
    #поворот влево
    def do_left(self):
        self.image = self.image.transpose(Image.ROTATE_90)
        self.saveImage() #сохраняет ее
        image_path = os.path.join(workdir, self.save_folder, self.filename) #формируем путь до измененной картинки
        self.showImage(image_path) #показываем эту картинку на экране
    #поворот вправо
    def do_right(self):
        self.image = self.image.transpose(Image.ROTATE_270)
        self.saveImage() #сохраняет ее
        image_path = os.path.join(workdir, self.save_folder, self.filename) #формируем путь до измененной картинки
        self.showImage(image_path) #показываем эту картинку на экране

workimage = ImageProcessor()

def showChosenImage():
    if lw_files.currentRow() >= 0:
        filename = lw_files.currentItem().text() #получаем имя файла, по которому мы кликнули из списка
        workimage.loadImage(filename) #загружаю картинку по названию
        file_path = os.path.join(workdir, workimage.filename) #сформировали полный путь до картинки. соединили путь до папки (workdir) с названием картинки (filename)
        workimage.showImage(file_path)

def chooseWorkdir():
    global workdir
    workdir = QFileDialog.getExistingDirectory()
   
def showFilenameList():
    global workdir
    chooseWorkdir()
    files = os.listdir(workdir)

    extensions = ['.jpg', '.png', '.bmp', '.jpeg', '.gif']
    results = []
    for element in files:
        for ex in extensions:
            if ex in element:
                results.append(element)
    
    lw_files.addItems(results)

btn_dir.clicked.connect(showFilenameList)
lw_files.currentRowChanged.connect(showChosenImage)


btn_bw.clicked.connect(workimage.do_bw)
btn_flip.clicked.connect(workimage.do_flip)
btn_sharp.clicked.connect(workimage.do_shrapen)
btn_left.clicked.connect(workimage.do_left)
btn_right.clicked.connect(workimage.do_right)

win.show()
app.exec_()