import os
from flask import Flask, render_template, redirect, url_for, flash, make_response
from flask_migrate import Migrate
from models import db, Laporan
from forms import LaporanForm
from weasyprint import HTML

app = Flask(__name__)
app.config['SECRET_KEY'] = 'kunci-rahasia-aplikasi-ti'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///laporan.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

@app.route('/', methods=['GET', 'POST'])
def index():
    form = LaporanForm()
    if form.validate_on_submit():
        laporan = Laporan(
            nama=form.nama.data,
            nip=form.nip.data,
            jabatan=form.jabatan.data,
            tanggal=form.tanggal.data,
            perangkat=form.perangkat.data,
            kategori=form.kategori.data,
            uraian=form.uraian.data,
            penjelasan=form.penjelasan.data,
            nama_atasan=form.nama_atasan.data,
            nip_atasan=form.nip_atasan.data,
            foto1_base64=form.foto1_base64.data,
            foto2_base64=form.foto2_base64.data
        )
        db.session.add(laporan)
        db.session.commit()
        flash('Laporan berhasil disimpan ke database!', 'success')
        return redirect(url_for('index'))
    
    riwayat_laporan = Laporan.query.order_by(Laporan.created_at.desc()).all()
    return render_template('index.html', form=form, laporan_list=riwayat_laporan)

@app.route('/cetak-pdf/<int:id>')
def cetak_pdf(id):
    laporan = Laporan.query.get_or_404(id)
    rendered_html = render_template('pdf_template.html', data=laporan)
    pdf = HTML(string=rendered_html).write_pdf()
    
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'inline; filename=Laporan_{laporan.id}.pdf'
    return response

if __name__ == '__main__':
    app.run(debug=True)