# tracker.py
import cv2
import numpy as np
import time
from PySide6.QtCore import QThread, Signal, Qt
from PySide6.QtGui import QImage


class TemplateTracker(QThread):

    change_pixmap_signal = Signal(QImage)
    status_signal = Signal(str)

    def __init__(self):
        super().__init__()
        self._run_flag = True
        self.video_source = ""
        self.tracking = False
        self.tracker = None
        self.template = None
        self.template_gray = None
        self.cap = None
        self.fps = 30
        self.frame_time = 1.0 / 30
        self.current_frame_position = 0
        self.bbox = None  # bounding box для трекера
        self.lost_frames = 0  # Счетчик кадров, когда объект потерян
        self.max_lost_frames = 30  # Увеличим максимальное количество кадров до сброса

    def reset_video_position(self):
        self.current_frame_position = 0

    def set_template_from_image(self, template_image, roi):
        try:
            self.template = template_image
            self.template_gray = cv2.cvtColor(self.template, cv2.COLOR_BGR2GRAY)
            # Сохраняем ROI для трекинга
            self.bbox = roi
            self.lost_frames = 0
            print(f"ROI установлен: {roi}")
            print(f"Размер шаблона: {self.template_gray.shape}")
            self.status_signal.emit("Шаблон установлен")
            return True
        except Exception as e:
            print(f"Ошибка установки шаблона: {e}")
            self.status_signal.emit(f"Ошибка установки шаблона: {e}")
            return False

    def get_template_preview(self):
        return self.template

    def set_video_source(self, source):
        self.video_source = source
        if self.cap:
            self.cap.release()
            self.cap = None

    def start_tracking(self):
        if self.template is not None and self.bbox is not None:
            self.tracking = True
            self.lost_frames = 0
            self.status_signal.emit("Трекинг запущен")
        else:
            self.status_signal.emit("Сначала выберите объект на видео!")

    def stop_tracking(self):
        self.tracking = False
        self.status_signal.emit("Трекинг остановлен")

    def reset_tracker(self):
        self.tracking = False
        self.template = None
        self.template_gray = None
        self.bbox = None
        self.current_frame_position = 0
        self.lost_frames = 0
        self.status_signal.emit("Трекер сброшен")

    def run(self):
        if not self.video_source:
            self.status_signal.emit("Ошибка: не выбран видеофайл")
            return

        self.cap = cv2.VideoCapture(self.video_source)
        if not self.cap.isOpened():
            self.status_signal.emit("Ошибка открытия видеофайла")
            return

        # Устанавливаем сохраненную позицию - всегда начинаем с начала
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        self.current_frame_position = 0

        # Получаем реальный FPS видео
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        if self.fps <= 0:
            self.fps = 30
        self.frame_time = 1.0 / self.fps

        self.status_signal.emit(f"Видео запущено ({self.fps:.1f} FPS)")

        self._run_flag = True

        while self._run_flag:
            start_time = time.time()

            ret, frame = self.cap.read()
            if not ret:
                # Достигнут конец видео - останавливаемся
                self.status_signal.emit("Конец видео")
                break

            # Сохраняем текущую позицию кадра
            self.current_frame_position = self.cap.get(cv2.CAP_PROP_POS_FRAMES)

            # Обрабатываем кадр если трекинг активен
            if self.tracking:
                try:
                    frame = self._track_object(frame)
                except Exception as e:
                    self.status_signal.emit(f"Ошибка трекинга: {str(e)}")
                    # Не останавливаем трекинг при ошибке, продолжаем попытки

            # Конвертируем кадр для Qt
            rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_image.shape
            bytes_per_line = ch * w
            convert_to_qt_format = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
            p = convert_to_qt_format.scaled(800, 600, Qt.AspectRatioMode.KeepAspectRatio)
            self.change_pixmap_signal.emit(p)

            # Контроль FPS
            elapsed = time.time() - start_time
            if elapsed < self.frame_time:
                time.sleep(self.frame_time - elapsed)

        if self.cap:
            self.cap.release()

    def _track_object(self, frame):
        try:
            # Если шаблон не установлен, ничего не делаем
            if self.template is None or self.template_gray is None:
                return frame

            # Используем метод нормализованной кросс-корреляции (NCC) для трекинга
            frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Определяем область поиска
            if self.bbox is not None and self.lost_frames == 0:
                # Если объект был найден в предыдущем кадре, ищем в области вокруг него
                x, y, w, h = self.bbox
                search_margin = 50
            else:
                # Если объект потерян, ищем во всем кадре
                x, y, w, h = 0, 0, frame_gray.shape[1], frame_gray.shape[0]
                search_margin = 0

            # Определяем область поиска
            search_x1 = max(0, x - search_margin)
            search_y1 = max(0, y - search_margin)
            search_x2 = min(frame_gray.shape[1], x + w + search_margin)
            search_y2 = min(frame_gray.shape[0], y + h + search_margin)

            # Извлекаем область поиска
            search_region = frame_gray[search_y1:search_y2, search_x1:search_x2]

            # Проверяем, что область поиска больше шаблона
            if search_region.shape[0] < self.template_gray.shape[0] or search_region.shape[1] < \
                    self.template_gray.shape[1]:
                # Если область поиска меньше шаблона, используем весь кадр
                search_region = frame_gray
                search_x1, search_y1 = 0, 0
                search_x2, search_y2 = frame_gray.shape[1], frame_gray.shape[0]

            # Используем несколько масштабов для поиска
            scales = [0.5, 0.75, 1.0, 1.25, 1.5]
            best_max_val = -1
            best_max_loc = None
            best_scale = 1.0
            best_size = (self.template_gray.shape[1], self.template_gray.shape[0])

            for scale in scales:
                # Масштабируем шаблон
                scaled_w = int(self.template_gray.shape[1] * scale)
                scaled_h = int(self.template_gray.shape[0] * scale)

                # Пропускаем слишком маленькие или большие шаблоны
                if scaled_w < 10 or scaled_h < 10 or scaled_w > search_region.shape[1] or scaled_h > \
                        search_region.shape[0]:
                    continue

                scaled_template = cv2.resize(self.template_gray, (scaled_w, scaled_h))

                # Применяем сопоставление шаблона
                result = cv2.matchTemplate(search_region, scaled_template, cv2.TM_CCOEFF_NORMED)
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

                # Сохраняем лучшее соответствие
                if max_val > best_max_val:
                    best_max_val = max_val
                    best_max_loc = max_loc
                    best_scale = scale
                    best_size = (scaled_w, scaled_h)

            # Если найдено хорошее соответствие
            confidence_threshold = 0.65  # Порог уверенности

            if best_max_val > confidence_threshold:
                # Вычисляем новое положение объекта
                new_x = search_x1 + best_max_loc[0]
                new_y = search_y1 + best_max_loc[1]
                new_w, new_h = best_size

                # Обновляем bounding box
                self.bbox = (new_x, new_y, new_w, new_h)
                self.lost_frames = 0  # Сбрасываем счетчик потерянных кадров

                # Рисуем bounding box
                cv2.rectangle(frame, (new_x, new_y), (new_x + new_w, new_y + new_h), (0, 255, 0), 2)

                # Центр объекта
                center_x = new_x + new_w // 2
                center_y = new_y + new_h // 2

                # Крест в центре
                cross_size = 10
                cv2.line(frame, (center_x - cross_size, center_y),
                         (center_x + cross_size, center_y), (0, 0, 255), 2)
                cv2.line(frame, (center_x, center_y - cross_size),
                         (center_x, center_y + cross_size), (0, 0, 255), 2)

                # Текст с координатами и уверенностью
                cv2.putText(frame, f'Tracked: {best_max_val:.2f}',
                            (new_x, new_y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

            else:
                # Объект не найден
                self.lost_frames += 1

                # Если объект потерян слишком долго, показываем предупреждение
                if self.lost_frames > self.max_lost_frames:
                    self.status_signal.emit("Объект потерян, продолжаем поиск...")

        except Exception as e:
            print(f"Ошибка трекинга: {e}")
            # Не останавливаем трекинг при ошибке

        return frame

    def stop(self):
        self._run_flag = False
        if self.cap:
            # Сохраняем текущую позицию перед освобождением
            self.current_frame_position = self.cap.get(cv2.CAP_PROP_POS_FRAMES)
            self.cap.release()
        self.wait()