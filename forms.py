from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SelectField, TextAreaField, HiddenField
from wtforms.validators import DataRequired

class LaporanForm(FlaskForm):
    nama = StringField('Nama Petugas', validators=[DataRequired()])
    nip = StringField('NIP', validators=[DataRequired()])
    jabatan = StringField('Jabatan', validators=[DataRequired()])
    tanggal = DateField('Tanggal Pelaksanaan', format='%Y-%m-%d', validators=[DataRequired()])
    
    perangkat = StringField('Perangkat / Unit Kerja', validators=[DataRequired()])
    kategori = SelectField('Kategori Pemeliharaan', choices=[
        ('Pilih Kategori', 'Pilih Kategori'),
        ('Install Aplikasi / Perangkat', 'Instalasi Aplikasi / Perangkat'),
        ('Pemeliharaan Rutin / Preventif', 'Pemeliharaan Rutin / Preventif'),
        ('Perbaikan / Korektif', 'Perbaikan / Korektif'),
        ('Pengolahan Data', 'Pengolahan Data'),
        ('Penggandaan Data', 'Penggandaan Data')      
    ], validators=[DataRequired()])
    uraian = TextAreaField('Uraian Pekerjaan', validators=[DataRequired()])
    penjelasan = TextAreaField('Penjelasan Detail Pekerjaan', validators=[DataRequired()])
    
    nama_atasan = StringField('Nama Atasan', validators=[DataRequired()])
    nip_atasan = StringField('NIP Atasan', validators=[DataRequired()])
    
    # Hidden fields untuk 4 Foto Base64
    foto1_base64 = HiddenField('Foto 1')
    foto2_base64 = HiddenField('Foto 2')
    foto3_base64 = HiddenField('Foto 3')
    foto4_base64 = HiddenField('Foto 4')