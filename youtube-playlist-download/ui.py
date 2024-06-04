import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel,
                             QLineEdit, QPushButton, QFileDialog, QMessageBox, QProgressBar)
from PyQt5.QtCore import Qt
from pytube import Playlist, Stream


class YouTubePlaylistDownloader(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('YouTube Playlist Downloader')
        self.setGeometry(300, 300, 500, 250)

        layout = QVBoxLayout()

        # URL Label and Entry
        self.url_label = QLabel('Playlist URL:', self)
        layout.addWidget(self.url_label)

        self.url_entry = QLineEdit(self)
        layout.addWidget(self.url_entry)

        # Path Label and Entry
        self.path_label = QLabel('Download Path:', self)
        layout.addWidget(self.path_label)

        self.path_entry = QLineEdit(self)
        layout.addWidget(self.path_entry)

        # Browse Button
        self.browse_button = QPushButton('Browse', self)
        self.browse_button.clicked.connect(self.select_download_path)
        layout.addWidget(self.browse_button)

        # Download Button
        self.download_button = QPushButton('Download', self)
        self.download_button.clicked.connect(self.download_youtube_playlist)
        layout.addWidget(self.download_button)

        # Status Label
        self.status_label = QLabel('', self)
        self.status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.status_label)

        # Progress Bar
        self.progress_bar = QProgressBar(self)
        layout.addWidget(self.progress_bar)

        self.setLayout(layout)

    def select_download_path(self):
        path = QFileDialog.getExistingDirectory(
            self, 'Select Download Directory')
        if path:
            self.path_entry.setText(path)

    def download_youtube_playlist(self):
        playlist_url = self.url_entry.text()
        download_path = self.path_entry.text()

        if not playlist_url:
            QMessageBox.critical(self, 'Error', 'Please enter a playlist URL')
            return

        if not download_path:
            QMessageBox.critical(
                self, 'Error', 'Please select a download path')
            return

        try:
            playlist = Playlist(playlist_url)
            self.status_label.setText(f'Downloading: {playlist.title}')
            QApplication.processEvents()

            for video in playlist.videos:
                self.status_label.setText(f'Downloading {video.title}')
                QApplication.processEvents()

                # Get the highest resolution stream
                stream = video.streams.get_highest_resolution()

                # Register progress callback
                stream.register_on_progress_callback(self.progress_function)

                # Download video
                stream.download(output_path=download_path)

            self.status_label.setText('Download completed!')
            self.progress_bar.setValue(0)
        except Exception as e:
            QMessageBox.critical(self, 'Error', str(e))

    def progress_function(self, stream: Stream, chunk: bytes, bytes_remaining: int):
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        percentage_of_completion = bytes_downloaded / total_size * 100
        self.progress_bar.setValue(int(percentage_of_completion))
        self.status_label.setText(
            f'Downloading... {int(percentage_of_completion)}%')
        QApplication.processEvents()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = YouTubePlaylistDownloader()
    ex.show()
    sys.exit(app.exec_())
