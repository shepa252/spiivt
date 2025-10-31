import sys
import cv2
import numpy as np
from PySide6 import QtWidgets
from PySide6.QtCore import Qt
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import QFileDialog, QMessageBox

from tracker_ui import Ui_MainWindow
from tracker import TemplateTracker


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.tracker = TemplateTracker()
        self.tracker.change_pixmap_signal.connect(self.update_image)
        self.tracker.status_signal.connect(self.update_status)

        self.current_frame = None
        self.selecting_roi = False

        self.connect_signals()

        self.ui.start_tracking_btn.setEnabled(False)

    def connect_signals(self):
        self.ui.select_from_video_btn.clicked.connect(self.select_object_from_video)
        self.ui.start_tracking_btn.clicked.connect(self.start_tracking)
        self.ui.stop_tracking_btn.clicked.connect(self.stop_tracking)
        self.ui.reset_btn.clicked.connect(self.reset_all)
        self.ui.start_video_btn.clicked.connect(self.start_video)
        self.ui.stop_video_btn.clicked.connect(self.stop_video)
        self.ui.browse_btn.clicked.connect(self.browse_video_file)

    def update_status(self, message):
        self.statusBar().showMessage(message)

    def select_object_from_video(self):
        if self.current_frame is None:
            QMessageBox.warning(self, "Ошибка", "Сначала запустите видео!")
            return

        # Входим в режим выбора ROI
        self.selecting_roi = True
        self.ui.select_from_video_btn.setEnabled(False)
        self.ui.start_tracking_btn.setEnabled(False)

        # Создаем копию текущего кадра для выбора ROI
        frame_copy = self.current_frame.copy()

        # Показываем кадр в отдельном окне для выбора ROI
        roi = cv2.selectROI("Select Object", frame_copy)
        cv2.destroyWindow("Select Object")

        # Выходим из режима выбора ROI
        self.selecting_roi = False
        self.ui.select_from_video_btn.setEnabled(True)

        # Проверяем, что ROI выбран (не отменен)
        if roi[2] > 0 and roi[3] > 0:  # width и height > 0
            x, y, w, h = roi
            template = self.current_frame[y:y + h, x:x + w]

            # Устанавливаем выбранный объект как шаблон
            if self.tracker.set_template_from_image(template, roi):
                self.ui.start_tracking_btn.setEnabled(True)
                QMessageBox.information(self, "Успех", "Объект выбран для трекинга!")
            else:
                QMessageBox.warning(self, "Ошибка", "Не удалось установить шаблон!")
        else:
            QMessageBox.information(self, "Информация", "Выбор объекта отменен")

    def update_image(self, image):
        if not self.selecting_roi:  # Не обновляем во время выбора ROI
            self.ui.video_label.setPixmap(QPixmap.fromImage(image))

            # Сохраняем текущий кадр для выбора ROI
            self.current_frame = self.convert_qimage_to_cv(image)

    def convert_qimage_to_cv(self, qimage):
        try:
            if qimage.format() != QImage.Format_RGB888:
                qimage = qimage.convertToFormat(QImage.Format_RGB888)

            width = qimage.width()
            height = qimage.height()
            bytes_per_line = qimage.bytesPerLine()

            buffer = qimage.bits()
            if hasattr(buffer, 'tobytes'):
                buffer_bytes = buffer.tobytes()
            else:
                buffer_bytes = bytes(buffer)

            if bytes_per_line != width * 3:
                arr = np.frombuffer(buffer_bytes, dtype=np.uint8)
                if bytes_per_line % 4 == 0:
                    arr = arr.reshape((height, bytes_per_line))
                    arr = arr[:, :width * 3]
                    arr = arr.reshape(height, width, 3)
                else:
                    arr = arr[:height * width * 3].reshape(height, width, 3)
            else:
                arr = np.frombuffer(buffer_bytes, dtype=np.uint8).reshape(height, width, 3)

            return cv2.cvtColor(arr, cv2.COLOR_RGB2BGR)

        except Exception as e:
            print(f"Ошибка конвертации: {e}")
            return None

    def browse_video_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Выберите видеофайл", "", "Video Files (*.mp4 *.avi *.mov *.mkv *.wmv)")
        if file_path:
            self.ui.video_path_edit.setText(file_path)

    def start_video(self):
        source = self.ui.video_path_edit.text()
        if not source:
            QMessageBox.warning(self, "Ошибка", "Выберите видеофайл!")
            return

        # Сбрасываем позицию видео в начало
        self.tracker.reset_video_position()

        self.tracker.set_video_source(source)
        self.tracker.start()
        # Включаем кнопку выбора объекта после запуска видео
        self.ui.select_from_video_btn.setEnabled(True)

    def stop_video(self):
        self.tracker.stop()
        # Отключаем кнопки, требующие запущенного видео
        self.ui.select_from_video_btn.setEnabled(False)
        self.ui.start_tracking_btn.setEnabled(False)

    def start_tracking(self):
        if self.tracker.template is None:
            QMessageBox.warning(self, "Ошибка", "Сначала выберите объект на видео!")
            return
        self.tracker.start_tracking()

    def stop_tracking(self):
        self.tracker.stop_tracking()

    def reset_all(self):
        self.tracker.reset_tracker()
        self.current_frame = None
        self.ui.video_label.setText("Видео предпросмотр")
        self.ui.select_from_video_btn.setEnabled(False)
        self.ui.start_tracking_btn.setEnabled(False)

    def closeEvent(self, event):
        self.tracker.stop()
        event.accept()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())