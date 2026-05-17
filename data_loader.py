# nama: alya dwi pangesti | nim: f1d02310104 | kelas: pemvis D

import pandas as pd

MATKUL_ORDER = ["Matematika", "Fisika", "Kimia", "Biologi", "Bahasa Inggris", "Pemrograman"]

def load_data(csv_path):
    df = pd.read_csv(csv_path)
    df["nilai"] = pd.to_numeric(df["nilai"])
    return df

def get_jurusan(df):
    return ["Semua"] + sorted(df["jurusan"].unique())

def filter_by_jurusan(df, jurusan):
    if jurusan == "Semua":
        return df
    return df[df["jurusan"] == jurusan]

def summarize_by_matkul(df):
    summary = df.groupby("matkul", sort=False)["nilai"].mean().reset_index()
    summary["nilai"] = summary["nilai"].round(1)
    order = [m for m in MATKUL_ORDER if m in summary["matkul"].values]
    summary["matkul"] = pd.Categorical(summary["matkul"], categories=order, ordered=True)
    return summary.sort_values("matkul")

def get_grade(nilai):
    if nilai >= 85: return "A"
    elif nilai >= 75: return "B"
    elif nilai >= 65: return "C"
    elif nilai >= 55: return "D"
    return "E"