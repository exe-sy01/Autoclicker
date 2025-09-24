import sys
import json
import os
from PySide6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, 
                               QWidget, QPushButton, QLabel, QSpinBox, QComboBox, 
                               QRadioButton, QButtonGroup, QGroupBox, QCheckBox,
                               QLineEdit, QMessageBox, QFrame)
from PySide6.QtCore import QTimer, Qt, QThread, Signal, QSettings
from PySide6.QtGui import QKeySequence, QShortcut, QIcon, QFont
import pyautogui
import keyboard
import time
import threading

class ClickerThread(QThread):
    """Thread for handling the clicking operations"""
    def __init__(self):
        super().__init__()
        self.running = False
        self.interval = 100  # milliseconds
        self.click_type = 'left'
        self.click_mode = 'cursor'  # 'cursor' or 'fixed'
        self.fixed_x = 0
        self.fixed_y = 0
        self.max_clicks = 0  # 0 means infinite
        self.current_clicks = 0
        self.double_click = False
        self.triple_click = False
        
    def run(self):
        """Main clicking loop"""
        self.current_clicks = 0
        while self.running:
            if self.max_clicks > 0 and self.current_clicks >= self.max_clicks:
                self.running = False
                break
                
            try:
                if self.click_mode == 'fixed':
                    x, y = self.fixed_x, self.fixed_y
                else:
                    x, y = pyautogui.position()
                
                # Perform the click based on type
                if self.triple_click:
                    pyautogui.click(x, y, button=self.click_type)
                    time.sleep(0.01)
                    pyautogui.click(x, y, button=self.click_type)
                    time.sleep(0.01)
                    pyautogui.click(x, y, button=self.click_type)
                elif self.double_click:
                    pyautogui.doubleClick(x, y, button=self.click_type)
                else:
                    pyautogui.click(x, y, button=self.click_type)
                
                self.current_clicks += 1
                
            except Exception as e:
                print(f"Click error: {e}")
                
            # Wait for the specified interval
            time.sleep(self.interval / 1000.0)
    
    def stop_clicking(self):
        """Stop the clicking thread"""
        self.running = False

class AutoClickerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.clicker_thread = ClickerThread()
        self.settings = QSettings('AutoClicker', 'Settings')
        self.init_ui()
        self.setup_hotkeys()
        self.load_settings()
        
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle('Auto Clicker')
        self.setFixedSize(400, 600)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Title
        title = QLabel('Auto Clicker')
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont('Arial', 16, QFont.Bold))
        layout.addWidget(title)
        
        # Click interval section
        interval_group = QGroupBox('Click Interval')
        interval_layout = QHBoxLayout(interval_group)
        
        interval_layout.addWidget(QLabel('Interval (ms):'))
        self.interval_spinbox = QSpinBox()
        self.interval_spinbox.setRange(1, 10000)
        self.interval_spinbox.setValue(100)
        self.interval_spinbox.valueChanged.connect(self.update_interval)
        interval_layout.addWidget(self.interval_spinbox)
        
        layout.addWidget(interval_group)
        
        # Click options section
        options_group = QGroupBox('Click Options')
        options_layout = QVBoxLayout(options_group)
        
        # Click type
        click_type_layout = QHBoxLayout()
        click_type_layout.addWidget(QLabel('Click Type:'))
        self.click_type_combo = QComboBox()
        self.click_type_combo.addItems(['Left Click', 'Right Click', 'Middle Click'])
        self.click_type_combo.currentTextChanged.connect(self.update_click_type)
        click_type_layout.addWidget(self.click_type_combo)
        options_layout.addLayout(click_type_layout)
        
        # Click mode
        click_mode_layout = QHBoxLayout()
        click_mode_layout.addWidget(QLabel('Click Mode:'))
        self.click_mode_combo = QComboBox()
        self.click_mode_combo.addItems(['Cursor Location', 'Fixed Position'])
        self.click_mode_combo.currentTextChanged.connect(self.update_click_mode)
        click_mode_layout.addWidget(self.click_mode_combo)
        options_layout.addLayout(click_mode_layout)
        
        # Fixed position inputs
        self.fixed_pos_widget = QWidget()
        fixed_pos_layout = QHBoxLayout(self.fixed_pos_widget)
        fixed_pos_layout.addWidget(QLabel('X:'))
        self.x_spinbox = QSpinBox()
        self.x_spinbox.setRange(0, 9999)
        self.x_spinbox.valueChanged.connect(self.update_fixed_position)
        fixed_pos_layout.addWidget(self.x_spinbox)
        
        fixed_pos_layout.addWidget(QLabel('Y:'))
        self.y_spinbox = QSpinBox()
        self.y_spinbox.setRange(0, 9999)
        self.y_spinbox.valueChanged.connect(self.update_fixed_position)
        fixed_pos_layout.addWidget(self.y_spinbox)
        
        self.pick_position_btn = QPushButton('Pick Position')
        self.pick_position_btn.clicked.connect(self.pick_position)
        fixed_pos_layout.addWidget(self.pick_position_btn)
        
        self.fixed_pos_widget.setVisible(False)
        options_layout.addWidget(self.fixed_pos_widget)
        
        # Multiple click options
        multi_click_layout = QHBoxLayout()
        self.double_click_cb = QCheckBox('Double Click')
        self.double_click_cb.toggled.connect(self.update_multi_click)
        multi_click_layout.addWidget(self.double_click_cb)
        
        self.triple_click_cb = QCheckBox('Triple Click')
        self.triple_click_cb.toggled.connect(self.update_multi_click)
        multi_click_layout.addWidget(self.triple_click_cb)
        options_layout.addLayout(multi_click_layout)
        
        layout.addWidget(options_group)
        
        # Click count section
        count_group = QGroupBox('Click Count')
        count_layout = QVBoxLayout(count_group)
        
        self.infinite_clicks_rb = QRadioButton('Infinite Clicks')
        self.infinite_clicks_rb.setChecked(True)
        self.infinite_clicks_rb.toggled.connect(self.update_click_count_mode)
        count_layout.addWidget(self.infinite_clicks_rb)
        
        limited_layout = QHBoxLayout()
        self.limited_clicks_rb = QRadioButton('Limited Clicks:')
        self.limited_clicks_rb.toggled.connect(self.update_click_count_mode)
        limited_layout.addWidget(self.limited_clicks_rb)
        
        self.max_clicks_spinbox = QSpinBox()
        self.max_clicks_spinbox.setRange(1, 999999)
        self.max_clicks_spinbox.setValue(100)
        self.max_clicks_spinbox.setEnabled(False)
        self.max_clicks_spinbox.valueChanged.connect(self.update_max_clicks)
        limited_layout.addWidget(self.max_clicks_spinbox)
        
        count_layout.addLayout(limited_layout)
        layout.addWidget(count_group)
        
        # Control buttons
        control_group = QGroupBox('Controls')
        control_layout = QVBoxLayout(control_group)
        
        self.start_stop_btn = QPushButton('Start (F6)')
        self.start_stop_btn.clicked.connect(self.toggle_clicking)
        self.start_stop_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 10px;
                font-size: 14px;
                font-weight: bold;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
        """)
        control_layout.addWidget(self.start_stop_btn)
        
        # Status
        self.status_label = QLabel('Status: Ready')
        self.status_label.setAlignment(Qt.AlignCenter)
        control_layout.addWidget(self.status_label)
        
        layout.addWidget(control_group)
        
        # Hotkey info
        hotkey_info = QLabel('Hotkey: F6 to start/stop clicking')
        hotkey_info.setAlignment(Qt.AlignCenter)
        hotkey_info.setStyleSheet('color: #666; font-style: italic;')
        layout.addWidget(hotkey_info)
        
    def setup_hotkeys(self):
        """Setup global hotkeys"""
        try:
            keyboard.add_hotkey('f6', self.toggle_clicking)
        except Exception as e:
            print(f"Hotkey setup error: {e}")
    
    def toggle_clicking(self):
        """Toggle the clicking on/off"""
        if not self.clicker_thread.running:
            self.start_clicking()
        else:
            self.stop_clicking()
    
    def start_clicking(self):
        """Start the auto clicking"""
        if self.clicker_thread.isRunning():
            self.clicker_thread.stop_clicking()
            self.clicker_thread.wait()
        
        # Update thread settings
        self.clicker_thread.interval = self.interval_spinbox.value()
        self.clicker_thread.click_type = self.get_click_type()
        self.clicker_thread.click_mode = 'fixed' if self.click_mode_combo.currentText() == 'Fixed Position' else 'cursor'
        self.clicker_thread.fixed_x = self.x_spinbox.value()
        self.clicker_thread.fixed_y = self.y_spinbox.value()
        self.clicker_thread.max_clicks = 0 if self.infinite_clicks_rb.isChecked() else self.max_clicks_spinbox.value()
        self.clicker_thread.double_click = self.double_click_cb.isChecked()
        self.clicker_thread.triple_click = self.triple_click_cb.isChecked()
        
        self.clicker_thread.running = True
        self.clicker_thread.start()
        
        self.start_stop_btn.setText('Stop (F6)')
        self.start_stop_btn.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                border: none;
                padding: 10px;
                font-size: 14px;
                font-weight: bold;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #da190b;
            }
            QPushButton:pressed {
                background-color: #c1170a;
            }
        """)
        self.status_label.setText('Status: Clicking...')
    
    def stop_clicking(self):
        """Stop the auto clicking"""
        if self.clicker_thread.isRunning():
            self.clicker_thread.stop_clicking()
            self.clicker_thread.wait()
        
        self.start_stop_btn.setText('Start (F6)')
        self.start_stop_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 10px;
                font-size: 14px;
                font-weight: bold;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
        """)
        self.status_label.setText('Status: Ready')
    
    def get_click_type(self):
        """Get the current click type"""
        click_map = {
            'Left Click': 'left',
            'Right Click': 'right',
            'Middle Click': 'middle'
        }
        return click_map.get(self.click_type_combo.currentText(), 'left')
    
    def update_interval(self):
        """Update click interval"""
        pass  # Already handled by spinbox value
    
    def update_click_type(self):
        """Update click type"""
        pass  # Already handled by combo box
    
    def update_click_mode(self):
        """Update click mode"""
        is_fixed = self.click_mode_combo.currentText() == 'Fixed Position'
        self.fixed_pos_widget.setVisible(is_fixed)
    
    def update_fixed_position(self):
        """Update fixed position coordinates"""
        pass  # Already handled by spinbox values
    
    def update_multi_click(self):
        """Update multiple click options"""
        if self.double_click_cb.isChecked():
            self.triple_click_cb.setChecked(False)
        elif self.triple_click_cb.isChecked():
            self.double_click_cb.setChecked(False)
    
    def update_click_count_mode(self):
        """Update click count mode"""
        self.max_clicks_spinbox.setEnabled(self.limited_clicks_rb.isChecked())
    
    def update_max_clicks(self):
        """Update maximum clicks"""
        pass  # Already handled by spinbox value
    
    def pick_position(self):
        """Pick a position by clicking on screen"""
        self.hide()
        QMessageBox.information(None, 'Pick Position', 
                               'Click anywhere on the screen to set the fixed position.\n'
                               'The application will minimize and you have 3 seconds.')
        
        def get_position():
            time.sleep(3)
            x, y = pyautogui.position()
            self.x_spinbox.setValue(x)
            self.y_spinbox.setValue(y)
            self.show()
        
        threading.Thread(target=get_position, daemon=True).start()
    
    def save_settings(self):
        """Save current settings"""
        self.settings.setValue('interval', self.interval_spinbox.value())
        self.settings.setValue('click_type', self.click_type_combo.currentIndex())
        self.settings.setValue('click_mode', self.click_mode_combo.currentIndex())
        self.settings.setValue('fixed_x', self.x_spinbox.value())
        self.settings.setValue('fixed_y', self.y_spinbox.value())
        self.settings.setValue('infinite_clicks', self.infinite_clicks_rb.isChecked())
        self.settings.setValue('max_clicks', self.max_clicks_spinbox.value())
        self.settings.setValue('double_click', self.double_click_cb.isChecked())
        self.settings.setValue('triple_click', self.triple_click_cb.isChecked())
    
    def load_settings(self):
        """Load saved settings"""
        self.interval_spinbox.setValue(self.settings.value('interval', 100, int))
        self.click_type_combo.setCurrentIndex(self.settings.value('click_type', 0, int))
        self.click_mode_combo.setCurrentIndex(self.settings.value('click_mode', 0, int))
        self.x_spinbox.setValue(self.settings.value('fixed_x', 0, int))
        self.y_spinbox.setValue(self.settings.value('fixed_y', 0, int))
        self.infinite_clicks_rb.setChecked(self.settings.value('infinite_clicks', True, bool))
        self.limited_clicks_rb.setChecked(not self.infinite_clicks_rb.isChecked())
        self.max_clicks_spinbox.setValue(self.settings.value('max_clicks', 100, int))
        self.double_click_cb.setChecked(self.settings.value('double_click', False, bool))
        self.triple_click_cb.setChecked(self.settings.value('triple_click', False, bool))
        
        # Update UI based on loaded settings
        self.update_click_mode()
        self.update_click_count_mode()
    
    def closeEvent(self, event):
        """Handle application close"""
        self.stop_clicking()
        self.save_settings()
        try:
            keyboard.unhook_all()
        except:
            pass
        event.accept()

def main():
    app = QApplication(sys.argv)
    app.setApplicationName('Auto Clicker')
    
    # Disable pyautogui failsafe for better user experience
    pyautogui.FAILSAFE = False
    
    window = AutoClickerApp()
    window.show()
    
    sys.exit(app.exec())

if __name__ == '__main__':
    main()