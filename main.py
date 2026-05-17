# nama: alya dwi pangesti | nim: f1d02310104 | kelas: pemvis D

import sys
from PySide6.QtWidgets import QApplication
from dashboard_window import DashboardWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DashboardWindow()
    window.show()
    sys.exit(app.exec())