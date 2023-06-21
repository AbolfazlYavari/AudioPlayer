# Import the necessary libraries
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
        # Initialize the pygame mixer
        pygame.mixer.init()

        # Set the initial state of the player (not paused)
        self.paused = False

        # Initialize the QMainWindow
        super(UI, self).__init__()

        # Load the UI from the "Audio Player.ui" file
        uic.loadUi("Audio Player.ui", self)

        # Access and store UI elements using findChild() method
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
        
        # Connect button click signals to their respective functions
        self.backward.clicked.connect(self.back_it)
        self.forward.clicked.connect(self.forward_it)
        self.play.clicked.connect(self.play_it)
        self.pause.clicked.connect(self.pause_it)
        self.stop.clicked.connect(self.stop_it)

        # Create an "Add song" action and connect it to the open_file_dialog() function
        open_action = QAction("Add song", self)
        open_action.triggered.connect(self.open_file_dialog)
        self.menusong.addAction(open_action)

        # Create a "Delete song" action and connect it to the delete_song() function
        delete_action = QAction("Delete song", self)
        delete_action.triggered.connect(self.delete_song)
        self.menusong.addAction(delete_action)

        # Show the main window
        self.show()

    def back_it(self):
        # Get the currently selected item and its row
        current_item = self.textedit.currentItem()
        current_row = self.textedit.row(current_item)

        # Calculate the previous row
        next_row = current_row - 1
        song = self.textedit.item(next_row)

        # Check if there is a song at the previous row
        if song:
            song_string = song.text()
            pygame.mixer.music.load(song_string)
            pygame.mixer.music.play(loops=0)

            self.textedit.setCurrentItem(song)

    def forward_it(self):
        # Get the currently selected item and its row
        current_item = self.textedit.currentItem()
        current_row = self.textedit.row(current_item)

        # Calculate the next row
        next_row = current_row + 1
        song = self.textedit.item(next_row)

        # Check if there is a song at the next row
        if song:
            song_string = song.text()
            pygame.mixer.music.load(song_string)
            pygame.mixer.music.play(loops=0)

            self.textedit.setCurrentItem(song)

    def update_time_label(self):
        global converted_current_time
        global current_time

        # Check if the music is currently playing
        if pygame.mixer.music.get_busy():
            current_time = pygame.mixer.music.get_pos() / 1000

             # Convert the current time to the format MM:SS
            converted_current_time = time.strftime('%M:%S', time.gmtime(current_time))
            self.timelabel.setText(str(converted_current_time))

            # Update the time label after 1 second using QTimer
            QTimer.singleShot(1000, self.update_time_label)
        else:
            self.timelabel.setText("")

        current_song = self.textedit.currentItem()

        if current_song:
            # Get the duration of the current song using mutagen.mp3
            song_mut = MP3(current_song.text())
            song_length = song_mut.info.length

            # Convert the song length to the format MM:SS
            converted_song_length = time.strftime('%M:%S', time.gmtime(song_length))

            # Update the time label with the current time and song length
            self.timelabel.setText(str(f' {converted_current_time} of {converted_song_length} '))

            # Set the range of the scrollbar according to the song length
            self.scrollbar.setRange(0, int(song_length))

            # Set the value of the scrollbar to the current time position
            self.scrollbar.setValue(int(current_time))

        else:
            self.timelabel.setText("")
            self.scrollbar.setRange(0, 0)

    def play_it(self):
        # Get the currently selected song
        song = self.textedit.currentItem()

        # Check if a song is selected
        if song:
            song_string = song.text()
            pygame.mixer.music.load(song_string)
            pygame.mixer.music.play(loops=0)

        # Update the time label after 1 second using QTimer
        QTimer.singleShot(1000, self.update_time_label)

    def pause_it(self):
        # Check if the music is paused or playing and toggle the state
        if self.paused:
            pygame.mixer.music.unpause()
            self.paused = False
        else:
            pygame.mixer.music.pause()
            self.paused = True

    def stop_it(self):
        # Stop the music playback and clear the textedit and time label
        pygame.mixer.music.stop()
        self.textedit.clear()
        self.timelabel.setText("")

    def open_file_dialog(self):
        # Create a file dialog to select audio files
        file_dialog = QFileDialog(self)
        file_path, _ = file_dialog.getOpenFileNames(self, "add Audio File", "", "Audio Files (*.mp3)")
        
        # Check if file paths are selected
        if file_path:
            self.textedit.addItems(file_path)
       

    def delete_song(self):
        # Get the currently selected item and remove it from the textedit
        selected_item = self.textedit.currentItem()

        if selected_item:
            self.textedit.takeItem(self.textedit.row(selected_item))

        # Stop the music playback
        pygame.mixer.music.stop()


app = QApplication(sys.argv)
UIWindow = UI()
app.exec_()
