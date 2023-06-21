import sys
import time

import pygame
from PyQt5 import uic
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QPushButton, QMenuBar, QStatusBar, QWidget, \
    QListWidget, QMenu, QSlider, QScrollBar, QAction, QFileDialog
from mutagen.mp3 import MP3


class UI(QMainWindow):
    def __init__(self):
        pygame.mixer.init()

        self.paused = False

        super(UI, self).__init__()

        uic.loadUi("Audio Player.ui", self)

        self.menu = self.findChild(QMenuBar, "menubar")
        self.menusong = self.findChild(QMenu, "menuSong")
        self.status = self.findChild(QStatusBar, "statusbar")
        self.textedit = self.findChild(QListWidget, "listWidget")
        self.play = self.findChild(QPushButton, "pushButton")
        self.pause = self.findChild(QPushButton, "pushButton_2")
        self.forward = self.findChild(QPushButton, "pushButton_3")
        self.backward = self.findChild(QPushButton, "pushButton_7")
        self.stop = self.findChild(QPushButton, "pushButton_5")
        self.scrollbar = self.findChild(QSlider, "horizontalSlider")
        self.slidersong = self.findChild(QScrollBar, "verticalScrollBar")
        self.widget = self.findChild(QWidget, "centralwidget")
        self.timelabel = self.findChild(QLabel, "label_3")

        self.backward.clicked.connect(self.back_it)
        self.forward.clicked.connect(self.forward_it)
        self.play.clicked.connect(self.play_it)
        self.pause.clicked.connect(self.pause_it)
        self.stop.clicked.connect(self.stop_it)

        open_action = QAction("Add song", self)
        open_action.triggered.connect(self.open_file_dialog)
        self.menusong.addAction(open_action)

        delete_action = QAction("Delete song", self)
        delete_action.triggered.connect(self.delete_song)
        self.menusong.addAction(delete_action)

        self.show()

    def back_it(self):
        current_item = self.textedit.currentItem()
        current_row = self.textedit.row(current_item)

        next_row = current_row - 1
        song = self.textedit.item(next_row)

        if song:
            song_string = song.text()
            pygame.mixer.music.load(song_string)
            pygame.mixer.music.play(loops=0)

            self.textedit.setCurrentItem(song)

    def forward_it(self):
        current_item = self.textedit.currentItem()
        current_row = self.textedit.row(current_item)

        next_row = current_row + 1
        song = self.textedit.item(next_row)

        if song:
            song_string = song.text()
            pygame.mixer.music.load(song_string)
            pygame.mixer.music.play(loops=0)

            self.textedit.setCurrentItem(song)

    def update_time_label(self):
        global converted_current_time
        global current_time
        if pygame.mixer.music.get_busy():
            current_time = pygame.mixer.music.get_pos() / 1000

            converted_current_time = time.strftime('%M:%S', time.gmtime(current_time))
            self.timelabel.setText(str(converted_current_time))
            QTimer.singleShot(1000, self.update_time_label)
        else:
            self.timelabel.setText("")

        current_song = self.textedit.currentItem()

        if current_song:
            song_mut = MP3(current_song.text())
            song_length = song_mut.info.length

            converted_song_length = time.strftime('%M:%S', time.gmtime(song_length))

            self.timelabel.setText(str(f' {converted_current_time} of {converted_song_length} '))

            self.scrollbar.setRange(0, int(song_length))

            self.scrollbar.setValue(int(current_time))

        else:
            self.timelabel.setText("")
            self.scrollbar.setRange(0, 0)

    def play_it(self):
        song = self.textedit.currentItem()
        if song:
            song_string = song.text()
            pygame.mixer.music.load(song_string)
            pygame.mixer.music.play(loops=0)

        QTimer.singleShot(1000, self.update_time_label)

    def pause_it(self):
        if self.paused:
            pygame.mixer.music.unpause()
            self.paused = False
        else:
            pygame.mixer.music.pause()
            self.paused = True

    def stop_it(self):
        pygame.mixer.music.stop()
        self.textedit.clear()
        self.timelabel.setText("")

    def open_file_dialog(self):
        file_dialog = QFileDialog(self)
        file_path, _ = file_dialog.getOpenFileNames(self, "add Audio File", "", "Audio Files (*.mp3)")
        if file_path:
            self.textedit.addItems(file_path)
        # check out for strip out to correct the file name

    def delete_song(self):
        selected_item = self.textedit.currentItem()

        if selected_item:
            self.textedit.takeItem(self.textedit.row(selected_item))

        pygame.mixer.music.stop()


app = QApplication(sys.argv)
UIWindow = UI()
app.exec_()
