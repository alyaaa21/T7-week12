# nama: alya dwi pangesti | nim: f1d02310104 | kelas: pemvis D

from pathlib import Path
from PySide6.QtWidgets import (
    QComboBox, QHBoxLayout, QLabel, QMainWindow,
    QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QFrame
)
from PySide6.QtCore import Qt

from chart_widget import NilaiChartWidget
from data_loader import get_jurusan, filter_by_jurusan, load_data, summarize_by_matkul, get_grade

STYLE = """
QMainWindow, QWidget#central {
    background-color: #fff0f6;
}
QLabel#title {
    color: #880e4f;
    font-size: 20px;
    font-weight: bold;
    padding: 6px 0;
}
QLabel {
    color: #880e4f;
    font-size: 12px;
}
QComboBox {
    background: #ffffff;
    border: 2px solid #f48fb1;
    border-radius: 8px;
    padding: 4px 10px;
    color: #880e4f;
    font-size: 12px;
    min-width: 140px;
}
QComboBox::drop-down { border: none; }
QComboBox QAbstractItemView {
    background: #fff0f6;
    border: 1px solid #f48fb1;
    color: #880e4f;
}
QTableWidget {
    background: #ffffff;
    border: 2px solid #f48fb1;
    border-radius: 10px;
    gridline-color: #fce4ec;
    color: #4a0030;
    font-size: 11px;
}
QHeaderView::section {
    background-color: #e91e8c;
    color: white;
    font-weight: bold;
    padding: 6px;
    border: none;
}
QFrame#kpi_card {
    background: #ffffff;
    border: 2px solid #f48fb1;
    border-radius: 12px;
}
"""

class KpiCard(QFrame):
    def __init__(self, label):
        super().__init__()
        self.setObjectName("kpi_card")
        self.setFixedHeight(72)
        layout = QVBoxLayout(self)
        layout.setSpacing(2)
        layout.setContentsMargins(12, 8, 12, 8)

        self.lbl = QLabel(label)
        self.lbl.setAlignment(Qt.AlignCenter)
        self.lbl.setStyleSheet("color: #f48fb1; font-size: 11px;")

        self.val = QLabel("-")
        self.val.setAlignment(Qt.AlignCenter)
        self.val.setStyleSheet("color: #880e4f; font-size: 16px; font-weight: bold;")

        layout.addWidget(self.lbl)
        layout.addWidget(self.val)

    def update(self, value):
        self.val.setText(value)


class DashboardWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dashboard Nilai Mahasiswa 🌸")
        self.resize(1100, 680)
        self.setStyleSheet(STYLE)

        csv_path = Path(__file__).parent / "data" / "nilai_mahasiswa.csv"
        self.df = load_data(csv_path)

        self._setup_ui()
        self._update_dashboard()

    def _setup_ui(self):
        central = QWidget()
        central.setObjectName("central")
        main = QVBoxLayout(central)
        main.setContentsMargins(16, 16, 16, 16)
        main.setSpacing(12)
        self.setCentralWidget(central)

        # judul
        title = QLabel("🌸 Dashboard Nilai Mahasiswa")
        title.setObjectName("title")
        main.addWidget(title)

        # filter
        filter_row = QHBoxLayout()
        filter_row.setSpacing(12)

        filter_row.addWidget(QLabel("Jurusan:"))
        self.jurusan_box = QComboBox()
        self.jurusan_box.addItems(get_jurusan(self.df))
        self.jurusan_box.currentTextChanged.connect(self._update_dashboard)
        filter_row.addWidget(self.jurusan_box)

        filter_row.addWidget(QLabel("Chart:"))
        self.chart_box = QComboBox()
        self.chart_box.addItems(["Bar Chart", "Line Chart", "Pie Chart"])
        self.chart_box.currentTextChanged.connect(self._update_dashboard)
        filter_row.addWidget(self.chart_box)

        filter_row.addStretch()
        main.addLayout(filter_row)

        # kpi cards
        kpi_row = QHBoxLayout()
        kpi_row.setSpacing(12)
        self.kpi_avg    = KpiCard("Rata-rata Nilai")
        self.kpi_total  = KpiCard("Jumlah Mahasiswa")
        self.kpi_lulus  = KpiCard("Lulus (≥ 65)")
        self.kpi_top    = KpiCard("Nilai Tertinggi")
        for card in [self.kpi_avg, self.kpi_total, self.kpi_lulus, self.kpi_top]:
            kpi_row.addWidget(card)
        main.addLayout(kpi_row)

        # tabel + chart
        content = QHBoxLayout()
        content.setSpacing(12)

        self.table = QTableWidget()
        content.addWidget(self.table, stretch=2)

        self.chart = NilaiChartWidget()
        content.addWidget(self.chart, stretch=3)

        main.addLayout(content)

    def _update_dashboard(self):
        jurusan    = self.jurusan_box.currentText()
        chart_type = self.chart_box.currentText()

        filtered = filter_by_jurusan(self.df, jurusan)
        summary  = summarize_by_matkul(filtered)

        self._update_kpi(filtered)
        self._update_table(filtered)
        self.chart.plot(summary, chart_type, f"Rata-rata Nilai per Matkul — {jurusan}")

    def _update_kpi(self, df):
        avg   = df["nilai"].mean()
        lulus = len(df[df["nilai"] >= 65])
        top   = df["nilai"].max()

        self.kpi_avg.update(f"{avg:.1f}")
        self.kpi_total.update(str(len(df)))
        self.kpi_lulus.update(f"{lulus} ({lulus/len(df)*100:.0f}%)")
        self.kpi_top.update(str(top))

    def _update_table(self, df):
        cols   = ["nama", "jurusan", "matkul", "nilai", "grade"]
        labels = ["Nama", "Jurusan", "Mata Kuliah", "Nilai", "Grade"]

        # tambahkan kolom grade dari data_loader
        display_df = df.copy()
        display_df["grade"] = display_df["nilai"].apply(get_grade)
        display_df = display_df.reset_index(drop=True)

        self.table.setRowCount(len(display_df))
        self.table.setColumnCount(len(cols))
        self.table.setHorizontalHeaderLabels(labels)

        for r, (_, row) in enumerate(display_df.iterrows()):
            for c, col in enumerate(cols):
                item = QTableWidgetItem(str(row[col]))
                item.setTextAlignment(Qt.AlignCenter)
                # warna baris berdasarkan grade
                if col == "grade":
                    grade = row[col]
                    color = {"A": "#f8bbd0", "B": "#fce4ec", "C": "#fff9c4",
                             "D": "#ffe0b2", "E": "#ffcdd2"}.get(grade, "white")
                    item.setBackground(__import__("PySide6.QtGui", fromlist=["QColor"]).QColor(color))
                self.table.setItem(r, c, item)

        self.table.resizeColumnsToContents()