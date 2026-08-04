import sys
import os
import fitz
import io
from PIL import Image
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                            QPushButton, QLabel, QFileDialog, QMessageBox, QGraphicsView,
                            QGraphicsScene, QGraphicsPixmapItem, QGraphicsRectItem, QSizePolicy,
                            QTabWidget, QScrollArea, QCheckBox)
from PyQt5.QtCore import Qt, QRectF, QPointF, QMimeData, QTimer
from PyQt5.QtGui import QPixmap, QImage, QBrush, QPen, QColor, QDrag
from PyPDF2 import PdfReader, PdfWriter

# Helper pour ajouter des boutons à un layout
def add_to_layout(self, layout):
    layout.addWidget(self)
    return self
QPushButton.add_to_layout = add_to_layout

# ==========================================================
# IMAGE REDIMENSIONNABLE
# ==========================================================
class ResizablePixmapItem(QGraphicsPixmapItem):
    def __init__(self, pixmap, img_data):
        super().__init__()
        self.img_data = img_data
        self.original_pixmap = pixmap
        self.setPixmap(self.original_pixmap)
        self.setFlag(QGraphicsPixmapItem.ItemIsMovable)
        self.setFlag(QGraphicsPixmapItem.ItemIsSelectable)
        self.handle_size = 12
        self.is_resizing = False
        self.handle = QGraphicsRectItem(self)
        self.handle.setBrush(QBrush(Qt.red))
        self.handle.setPen(QPen(Qt.black))
        self.handle.setRect(0, 0, self.handle_size, self.handle_size)
        self.update_handle()

    def update_handle(self):
        self.handle.setPos(
            self.pixmap().width() - self.handle_size,
            self.pixmap().height() - self.handle_size
        )

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            handle_rect = QRectF(
                self.pixmap().width() - self.handle_size,
                self.pixmap().height() - self.handle_size,
                self.handle_size,
                self.handle_size
            )
            if handle_rect.contains(event.pos()):
                self.is_resizing = True
                self.resize_origin = event.scenePos()
                self.original_width = self.pixmap().width()
                self.original_height = self.pixmap().height()
                event.accept()
                return
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.is_resizing:
            delta = event.scenePos() - self.resize_origin
            scale = (self.original_width + delta.x()) / self.original_width
            if scale < 0.10:
                scale = 0.10
            new_width = int(self.original_pixmap.width() * scale)
            new_height = int(self.original_pixmap.height() * scale)
            scaled = self.original_pixmap.scaled(
                new_width, new_height,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            self.setPixmap(scaled)
            self.img_data["width"] = new_width
            self.img_data["height"] = new_height
            self.update_handle()
            return
        super().mouseMoveEvent(event)
        self.img_data["x"] = self.pos().x()
        self.img_data["y"] = self.pos().y()

    def mouseReleaseEvent(self, event):
        self.is_resizing = False
        super().mouseReleaseEvent(event)

# ==========================================================
# ONGLET AJOUT D'IMAGES
# ==========================================================
class ImageEditorTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.pdf_path = None
        self.current_page = 0
        self.pdf_doc = None
        self.pdf_pages = []
        self.images = []
        self.fixed_pages = set()
        self.background_item = None
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        buttons = QHBoxLayout()
        QPushButton("Ouvrir PDF", clicked=self.open_pdf).add_to_layout(buttons)
        QPushButton("Importer image", clicked=self.import_image).add_to_layout(buttons)
        QPushButton("Fixer cette page", clicked=self.fix_page).add_to_layout(buttons)
        QPushButton("Page ←", clicked=self.prev_page).add_to_layout(buttons)
        QPushButton("Page →", clicked=self.next_page).add_to_layout(buttons)
        QPushButton("Enregistrer PDF", clicked=self.save_pdf).add_to_layout(buttons)
        QPushButton("Supprimer image", clicked=self.delete_selected_image).add_to_layout(buttons)
        QPushButton("Aide", clicked=self.show_help).add_to_layout(buttons)
        layout.addLayout(buttons)

        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        self.view.setAlignment(Qt.AlignCenter)
        self.view.setRenderHints(self.view.renderHints())
        self.view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        layout.addWidget(self.view)

        self.page_label = QLabel()
        layout.addWidget(self.page_label)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self.background_item:
            self.view.fitInView(self.background_item, Qt.KeepAspectRatio)

    def open_pdf(self):
        path, _ = QFileDialog.getOpenFileName(self, "Ouvrir PDF", "", "PDF (*.pdf)")
        if not path:
            return
        self.pdf_path = path
        self.pdf_doc = fitz.open(path)
        self.current_page = 0
        self.images.clear()
        self.fixed_pages.clear()
        self.display_page()

    def display_page(self):
        self.scene.clear()
        self.background_item = None
        if self.pdf_doc is None:
            return

        page = self.pdf_doc.load_page(self.current_page)
        pix = page.get_pixmap(dpi=150)
        qimg = QImage(pix.samples, pix.width, pix.height, pix.stride, QImage.Format_RGB888)
        pdf_pixmap = QPixmap.fromImage(qimg)
        self.background_item = self.scene.addPixmap(pdf_pixmap)
        self.scene.setSceneRect(self.background_item.boundingRect())
        self.view.fitInView(self.background_item, Qt.KeepAspectRatio)

        for img_data in self.images:
            if img_data["page"] != self.current_page:
                continue
            item = ResizablePixmapItem(img_data["pixmap"], img_data)
            item.setPos(img_data["x"], img_data["y"])
            self.scene.addItem(item)
            img_data["item"] = item

        self.page_label.setText(f"Page {self.current_page+1}/{len(self.pdf_doc)}")

    def import_image(self):
        if self.pdf_doc is None:
            return
        if self.current_page in self.fixed_pages:
            QMessageBox.warning(self, "Attention", "Cette page est verrouillée.")
            return

        path, _ = QFileDialog.getOpenFileName(self, "Choisir une image", "", "Images (*.png *.jpg *.jpeg *.bmp)")
        if not path:
            return

        img = Image.open(path)
        img.thumbnail((300, 300), Image.LANCZOS)
        if img.mode != "RGB":
            img = img.convert("RGB")

        qimg = QImage(img.tobytes(), img.width, img.height, img.width*3, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qimg)

        page_rect = self.background_item.boundingRect()
        x = (page_rect.width() - pixmap.width()) / 2
        y = (page_rect.height() - pixmap.height()) / 2

        data = {
            "path": path,
            "pixmap": pixmap,
            "x": x,
            "y": y,
            "width": pixmap.width(),
            "height": pixmap.height(),
            "page": self.current_page,
            "item": None
        }
        self.images.append(data)
        self.display_page()

    def prev_page(self):
        if self.current_page == 0:
            return
        self.current_page -= 1
        self.display_page()

    def next_page(self):
        if self.current_page >= len(self.pdf_doc)-1:
            return
        self.current_page += 1
        self.display_page()

    def fix_page(self):
        if self.current_page in self.fixed_pages:
            self.fixed_pages.remove(self.current_page)
        else:
            self.fixed_pages.add(self.current_page)

    def delete_selected_image(self):
        if self.current_page in self.fixed_pages:
            QMessageBox.warning(self, "Attention", "Cette page est verrouillée.")
            return
        for img_data in self.images[:]:
            if img_data["page"] == self.current_page and img_data["item"].isSelected():
                self.scene.removeItem(img_data["item"])
                self.images.remove(img_data)
                break

    def save_pdf(self):
        if self.pdf_doc is None:
            QMessageBox.warning(self, "Erreur", "Aucun PDF ouvert.")
            return

        output_path, _ = QFileDialog.getSaveFileName(self, "Enregistrer le PDF", "", "PDF (*.pdf)")
        if not output_path:
            return

        try:
            doc = fitz.open(self.pdf_path)
            for page_number in range(len(doc)):
                page = doc.load_page(page_number)
                pdf_width = page.rect.width
                pdf_height = page.rect.height
                scene_width = self.scene.sceneRect().width()
                scene_height = self.scene.sceneRect().height()
                ratio_x = pdf_width / scene_width
                ratio_y = pdf_height / scene_height

                for img_data in self.images:
                    if img_data["page"] != page_number:
                        continue
                    image = Image.open(img_data["path"])
                    if image.mode != "RGB":
                        image = image.convert("RGB")
                    image = image.resize((int(img_data["width"]), int(img_data["height"])), Image.LANCZOS)
                    buffer = io.BytesIO()
                    image.save(buffer, format="PNG")
                    buffer.seek(0)
                    x = img_data["x"] * ratio_x
                    y = img_data["y"] * ratio_y
                    w = img_data["width"] * ratio_x
                    h = img_data["height"] * ratio_y
                    rect = fitz.Rect(x, y, x + w, y + h)
                    page.insert_image(rect, stream=buffer)
            doc.save(output_path)
            doc.close()
            QMessageBox.information(self, "Succès", "PDF enregistré.")
        except Exception as e:
            QMessageBox.critical(self, "Erreur", str(e))

    def show_help(self):
        help_text = """
        <b>📖 Aide - Éditeur d'images PDF</b><br><br>
        <b>Fonctionnalités :</b><br>
        • Ouvrir PDF : Charge un PDF<br>
        • Importer image : Ajoute une image<br>
        • Fixer cette page : Verrouille les images<br>
        • Page ←/→ : Navigue entre les pages<br>
        • Enregistrer PDF : Exporte le PDF modifié<br>
        • Supprimer image : Supprime l'image sélectionnée<br><br>
        <b>Manipulation :</b><br>
        • Déplacer : Cliquez et glissez l'image<br>
        • Redimensionner : Cliquez sur le ■ rouge (coin bas-droit) et glissez<br>
        """
        QMessageBox.information(self, "Aide", help_text)

# ==========================================================
# ONGLET ORGANISATION DES PAGES
# ==========================================================
class PDFPage(QWidget):
    def __init__(self, page_number, pixmap, pdf_path, parent=None):
        super().__init__(parent)
        self.page_number = page_number
        self.pdf_path = pdf_path
        self.original_column = None
        layout = QVBoxLayout(self)
        self.checkbox = QCheckBox()
        layout.addWidget(self.checkbox)
        self.label = QLabel()
        self.label.setPixmap(pixmap)
        self.label.setFixedSize(200, 280)
        self.label.setScaledContents(True)
        self.label.setFrameStyle(QLabel.Panel | QLabel.Raised)
        layout.addWidget(self.label)
        self.setFixedSize(220, 330)

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            self.drag_start_position = e.pos()

    def mouseMoveEvent(self, e):
        if not (e.buttons() & Qt.LeftButton):
            return
        if (e.pos() - self.drag_start_position).manhattanLength() < QApplication.startDragDistance():
            return
        drag = QDrag(self)
        mime_data = QMimeData()
        mime_data.setText(f"{self.pdf_path}|{self.page_number}|0|{id(self.original_column)}")
        drag.setMimeData(mime_data)
        drag.setPixmap(self.label.pixmap().scaled(100, 140, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        drag.exec_(Qt.MoveAction)

class PDFColumn(QWidget):
    def __init__(self, pdf_path, parent=None):
        super().__init__(parent)
        self.pdf_path = pdf_path
        self.pages = []
        self.is_scrolling = False
        self.scroll_speed = 0
        self.scroll_acceleration = 0.5
        self.max_scroll_speed = 20
        layout = QVBoxLayout(self)

        self.scroll_up_button = QPushButton("▲")
        self.scroll_up_button.setStyleSheet("background-color: lightblue; font-size: 20px;")
        layout.addWidget(self.scroll_up_button)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        layout.addWidget(self.scroll_area)

        content_widget = QWidget()
        self.page_layout = QVBoxLayout(content_widget)
        self.scroll_area.setWidget(content_widget)

        self.scroll_down_button = QPushButton("▼")
        self.scroll_down_button.setStyleSheet("background-color: lightblue; font-size: 20px;")
        layout.addWidget(self.scroll_down_button)

        self.load_pdf_pages(pdf_path)

        button_layout = QHBoxLayout()
        QPushButton("Enregistrer cette colonne", clicked=self.save_column, parent=self).add_to_layout(button_layout)
        QPushButton("Supprimer la sélection", clicked=self.delete_selected_pages, parent=self).add_to_layout(button_layout)
        QPushButton("Sélectionner tout", clicked=self.select_all_pages, parent=self).add_to_layout(button_layout)
        QPushButton("Désélectionner tout", clicked=self.deselect_all_pages, parent=self).add_to_layout(button_layout)
        QPushButton("Aide", clicked=self.show_help, parent=self).add_to_layout(button_layout)
        layout.addLayout(button_layout)

        self.setAcceptDrops(True)
        self.scroll_timer = QTimer(self)
        self.scroll_timer.timeout.connect(self.auto_scroll)
        self.scroll_timer.setInterval(16)

    def dragEnterEvent(self, event):
        event.accept()
        self.is_scrolling = True
        self.scroll_timer.start()

    def dragLeaveEvent(self, event):
        self.is_scrolling = False
        self.scroll_timer.stop()
        self.scroll_speed = 0

    def dragMoveEvent(self, event):
        cursor_pos = event.pos()
        scroll_area_rect = self.scroll_area.geometry()
        if cursor_pos.y() < scroll_area_rect.top() + 50:
            self.scroll_speed = max(-self.max_scroll_speed, self.scroll_speed - self.scroll_acceleration)
        elif cursor_pos.y() > scroll_area_rect.bottom() - 50:
            self.scroll_speed = min(self.max_scroll_speed, self.scroll_speed + self.scroll_acceleration)
        else:
            self.scroll_speed = 0

    def dropEvent(self, event):
        self.is_scrolling = False
        self.scroll_timer.stop()
        self.scroll_speed = 0
        pos = event.pos()
        mime_data = event.mimeData()
        if mime_data.hasText():
            pdf_path, page_number, _, original_column_id = mime_data.text().split('|')
            page_number = int(page_number)
            original_column_id = int(original_column_id)
            scroll_pos = self.scroll_area.mapFrom(self, pos)
            content_pos = self.scroll_area.widget().mapFrom(self.scroll_area, scroll_pos)
            if original_column_id == id(self):
                self.move_page(page_number, content_pos)
            else:
                self.copy_page(pdf_path, page_number, content_pos)

    def auto_scroll(self):
        if self.is_scrolling:
            scrollbar = self.scroll_area.verticalScrollBar()
            scrollbar.setValue(int(scrollbar.value() + self.scroll_speed))

    def load_pdf_pages(self, pdf_path):
        pdf_document = fitz.open(pdf_path)
        for i in range(len(pdf_document)):
            page = pdf_document.load_page(i)
            pix = page.get_pixmap(matrix=fitz.Matrix(1, 1))
            qimg = QImage(pix.samples, pix.width, pix.height, pix.stride, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(qimg)
            pdf_page = PDFPage(i + 1, pixmap, pdf_path)
            pdf_page.original_column = self
            self.page_layout.addWidget(pdf_page)
            self.pages.append(pdf_page)

    def move_page(self, page_number, pos):
        moving_page = None
        for i, page in enumerate(self.pages):
            if page.page_number == page_number:
                moving_page = page
                self.page_layout.removeWidget(page)
                self.pages.remove(page)
                break
        if moving_page:
            insert_index = self.get_insert_index(pos)
            self.page_layout.insertWidget(insert_index, moving_page)
            self.pages.insert(insert_index, moving_page)

    def copy_page(self, pdf_path, page_number, pos):
        pdf_document = fitz.open(pdf_path)
        page = pdf_document.load_page(page_number - 1)
        pix = page.get_pixmap(matrix=fitz.Matrix(1, 1))
        qimg = QImage(pix.samples, pix.width, pix.height, pix.stride, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qimg)
        new_page = PDFPage(page_number, pixmap, pdf_path)
        new_page.original_column = self
        insert_index = self.get_insert_index(pos)
        self.page_layout.insertWidget(insert_index, new_page)
        self.pages.insert(insert_index, new_page)

    def get_insert_index(self, pos):
        for i, page in enumerate(self.pages):
            if page.geometry().contains(pos):
                return i
        return len(self.pages)

    def save_column(self):
        output_path, _ = QFileDialog.getSaveFileName(self, "Enregistrer le PDF de cette colonne", "", "PDF Files (*.pdf)")
        if output_path:
            writer = PdfWriter()
            for page in self.pages:
                reader = PdfReader(page.pdf_path)
                writer.add_page(reader.pages[page.page_number - 1])
            with open(output_path, "wb") as output_file:
                writer.write(output_file)

    def delete_selected_pages(self):
        pages_to_remove = [page for page in self.pages if page.checkbox.isChecked()]
        for page in pages_to_remove:
            self.page_layout.removeWidget(page)
            self.pages.remove(page)
            page.deleteLater()

    def select_all_pages(self):
        for page in self.pages:
            page.checkbox.setChecked(True)

    def deselect_all_pages(self):
        for page in self.pages:
            page.checkbox.setChecked(False)

    def show_help(self):
        help_text = """
        <b>📖 Aide - Organisateur de pages PDF</b><br><br>
        <b>Fonctionnalités :</b><br>
        • Charger PDF : Charge un ou plusieurs PDFs<br>
        • Décharger PDF : Supprime les PDFs sélectionnés<br>
        • Enregistrer PDF Fusionné : Fusionne toutes les pages<br>
        • Enregistrer cette colonne : Exporte cette colonne<br><br>
        <b>Manipulation :</b><br>
        • Glissez-déposez les pages pour les réorganiser<br>
        • Utilisez les checkboxes pour sélectionner plusieurs pages<br>
        """
        QMessageBox.information(self, "Aide", help_text)

class PageArrangerTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.pdf_columns = []
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        control_layout = QHBoxLayout()
        layout.addLayout(control_layout)

        QPushButton("Charger PDF", clicked=self.load_pdf, parent=self).add_to_layout(control_layout)
        QPushButton("Décharger PDF", clicked=self.unload_pdf, parent=self).add_to_layout(control_layout)
        self.save_all_button = QPushButton("Enregistrer PDF Fusionné Global", clicked=self.save_merged_pdf, parent=self)
        self.save_all_button.setEnabled(False)
        control_layout.addWidget(self.save_all_button)

        self.pdf_layout = QHBoxLayout()
        layout.addLayout(self.pdf_layout)

    def load_pdf(self):
        file_dialog = QFileDialog()
        pdf_paths, _ = file_dialog.getOpenFileNames(self, "Sélectionner un ou plusieurs PDF", "", "PDF Files (*.pdf)")
        for pdf_path in pdf_paths:
            pdf_column = PDFColumn(pdf_path)
            self.pdf_columns.append(pdf_column)
            self.pdf_layout.addWidget(pdf_column)
        if len(self.pdf_columns) >= 1:
            self.save_all_button.setEnabled(True)

    def unload_pdf(self):
        if not self.pdf_columns:
            QMessageBox.warning(self, "Aucun PDF", "Aucun PDF chargé.")
            return
        selected_columns = []
        for column in self.pdf_columns:
            if any(page.checkbox.isChecked() for page in column.pages):
                selected_columns.append(column)
        if not selected_columns:
            QMessageBox.warning(self, "Aucune sélection", "Aucune page sélectionnée.")
            return
        for column in selected_columns:
            self.pdf_columns.remove(column)
            self.pdf_layout.removeWidget(column)
            column.deleteLater()
        if len(self.pdf_columns) < 1:
            self.save_all_button.setEnabled(False)

    def save_merged_pdf(self):
        output_path, _ = QFileDialog.getSaveFileName(self, "Enregistrer le PDF fusionné", "", "PDF Files (*.pdf)")
        if output_path:
            writer = PdfWriter()
            for column in self.pdf_columns:
                for page in column.pages:
                    reader = PdfReader(page.pdf_path)
                    writer.add_page(reader.pages[page.page_number - 1])
            with open(output_path, "wb") as output_file:
                writer.write(output_file)
            QMessageBox.information(self, "Succès", f"PDF enregistré sous: {output_path}")

# ==========================================================
# FENÊTRE PRINCIPALE
# ==========================================================
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("📄 Éditeur PDF Complet")
        self.setGeometry(100, 100, 1200, 800)
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        self.image_editor = ImageEditorTab()
        self.tabs.addTab(self.image_editor, "🖼️ Ajout d'images")
        self.page_arranger = PageArrangerTab()
        self.tabs.addTab(self.page_arranger, "📑 Organiser les pages")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
