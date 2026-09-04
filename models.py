from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Laporan(db.Model):
  __tablename__ = 'laporan'

  id = db.Column(db.Integer, primary_key=True)
  nama = db.Column(db.String(100), nullable=False)
  nip = db.Column(db.String(50), nullable=False)
  jabatan = db.Column(db.String(100), nullable=False)
  tanggal = db.Column(db.Date, nullable=False)
  perangkat = db.Column(db.String(150), nullable=False)
  kategori = db.Column(db.String(100), nullable=False)
  uraian = db.Column(db.Text, nullable=False)
  penjelasan = db.Column(db.Text, nullable=False)
  nama_atasan = db.Column(db.String(100), nullable=False)
  nip_atasan = db.Column(db.String(50), nullable=False)
  foto1_base64 = db.Column(db.Text, nullable=True)
  foto2_base64 = db.Column(db.Text, nullable=True)
  created_at = db.Column(db.DateTime, default=datetime.utcnow)