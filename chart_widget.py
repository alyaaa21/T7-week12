# nama: alya dwi pangesti | nim: f1d02310104 | kelas: pemvis D

from PySide6.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

PINK       = "#e91e8c"
PINK_LIGHT = "#f48fb1"
PINK_DARK  = "#880e4f"
PINK_BG    = "#fce4ec"
ACCENT     = "#f06292"
PIE_COLORS = ["#e91e8c", "#f48fb1", "#f06292", "#880e4f", "#f8bbd0", "#ec407a"]

class NilaiChartWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        self.figure = Figure(figsize=(6, 4), tight_layout=True, facecolor=PINK_BG)
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

    def plot(self, summary, chart_type, title):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.set_facecolor("#fff0f6")

        matkul = summary["matkul"].astype(str).tolist()
        nilai  = summary["nilai"].tolist()

        if chart_type == "Bar Chart":
            bars = ax.bar(matkul, nilai, color=PINK, edgecolor=PINK_DARK, linewidth=0.8)
            ax.set_ylim(0, 105)
            for bar in bars:
                h = bar.get_height()
                ax.text(bar.get_x() + bar.get_width() / 2, h + 0.5,
                        str(h), ha="center", va="bottom",
                        fontsize=8, color=PINK_DARK, fontweight="bold")

        elif chart_type == "Line Chart":
            ax.plot(matkul, nilai, marker="o", linewidth=2.5,
                    color=PINK, markerfacecolor=PINK_DARK, markersize=8)
            ax.fill_between(range(len(matkul)), nilai, alpha=0.15, color=PINK)
            ax.set_xticks(range(len(matkul)))
            ax.set_xticklabels(matkul)
            ax.set_ylim(0, 105)

        elif chart_type == "Pie Chart":
            ax.pie(nilai, labels=matkul, autopct="%1.1f%%",
                   startangle=90, colors=PIE_COLORS[:len(matkul)],
                   textprops={"color": PINK_DARK, "fontsize": 9})
            ax.axis("equal")

        ax.set_title(title, color=PINK_DARK, fontsize=12, fontweight="bold", pad=10)

        if chart_type != "Pie Chart":
            ax.set_xlabel("Mata Kuliah", color=PINK_DARK, fontsize=9)
            ax.set_ylabel("Rata-rata Nilai", color=PINK_DARK, fontsize=9)
            ax.tick_params(colors=PINK_DARK, labelsize=8)
            ax.tick_params(axis="x", rotation=15)
            ax.grid(True, alpha=0.3, color=PINK_LIGHT, linestyle="--")
            for spine in ax.spines.values():
                spine.set_edgecolor(PINK_LIGHT)

        self.canvas.draw()