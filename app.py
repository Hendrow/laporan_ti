import os
from datetime import datetime
from flask import Flask, render_template, redirect, url_for, flash, make_response, request, jsonify
from flask_migrate import Migrate
from models import db, Laporan
from forms import LaporanForm
from weasyprint import HTML

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 32 * 1024 * 1024
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
            foto2_base64=form.foto2_base64.data,
            foto3_base64=form.foto3_base64.data,
            foto4_base64=form.foto4_base64.data,
            foto5_base64=form.foto5_base64.data,
            foto6_base64=form.foto6_base64.data
        )
        db.session.add(laporan)
        db.session.commit()
        flash('Laporan berhasil disimpan ke database!', 'success')
        return redirect(url_for('index'))
    
    # Query dasar
    query = Laporan.query

    # Fitur Pencarian Keyword (Nama Petugas atau Perangkat)
    q = request.args.get('q', '').strip()
    if q:
        query = query.filter(
            Laporan.nama.ilike(f'%{q}%') | Laporan.perangkat.ilike(f'%{q}%')
        )

    # Fitur Filter Rentang Tanggal
    tgl_mulai = request.args.get('tgl_mulai', '').strip()
    tgl_selesai = request.args.get('tgl_selesai', '').strip()

    if tgl_mulai:
        query = query.filter(
            Laporan.tanggal >= datetime.strptime(tgl_mulai, '%Y-%m-%d').date()
        )
    if tgl_selesai:
        query = query.filter(
            Laporan.tanggal <= datetime.strptime(tgl_selesai, '%Y-%m-%d').date()
        )

    # Ambil riwayat laporan terurut dari yang terbaru
    riwayat_laporan = query.order_by(Laporan.created_at.desc()).all()

    return render_template(
        'index.html',
        form=form,
        laporan_list=riwayat_laporan,
        q=q,
        tgl_mulai=tgl_mulai,
        tgl_selesai=tgl_selesai,
    )

@app.route('/cetak-pdf/<int:id>')
def cetak_pdf(id):
    laporan = Laporan.query.get_or_404(id)
    rendered_html = render_template('pdf_template.html', data=laporan)
    pdf = HTML(string=rendered_html).write_pdf()
    
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'inline; filename=Laporan_{laporan.id}.pdf'
    return response

# app.py (tambahkan route ini di bawah route lainnya)
@app.route('/hapus-laporan/<int:id>', methods=['POST', 'DELETE'])
def hapus_laporan(id):
    laporan = Laporan.query.get_or_404(id)
    db.session.delete(laporan)
    db.session.commit()
    
    # Jika diakses lewat AJAX / Fetch
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({'status': 'success', 'message': 'Laporan berhasil dihapus.'})
    
    flash('Laporan berhasil dihapus!', 'success')
    return redirect(url_for('index'))


# Route api ajax untuk pagination dan pencarian
@app.route('/api/laporan', methods=['GET'])
def get_laporan_api():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 7, type=int) # Limit 7 laporan per halaman
    search_query = request.args.get('q', '', type=str).strip()

    # Query Dasar
    query = Laporan.query

    # Filter Pencarian (Nama Petugas, Perangkat, Kategori, atau Tanggal)
    if search_query:
        query = query.filter(
            (Laporan.perangkat.ilike(f'%{search_query}%')) |
            (Laporan.nama.ilike(f'%{search_query}%')) |
            (Laporan.kategori.ilike(f'%{search_query}%'))
        )

    # Urutkan dari yang terbaru dan terapkan Pagination SQLAlchemy
    pagination = query.order_by(Laporan.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
        )

    items = []
    for item in pagination.items:
        items.append({
            'id': item.id,
            'perangkat': item.perangkat,
            'nama': item.nama,
            'kategori': item.kategori,
            'tanggal': item.tanggal.strftime('%H:%M, %d %b %Y')
        })

    return jsonify({
        'items': items,
        'total': pagination.total,
        'page': pagination.page,
        'pages': pagination.pages,
        'has_prev': pagination.has_prev,
        'has_next': pagination.has_next,
        'prev_num': pagination.prev_num,
        'next_num': pagination.next_num
    })

if __name__ == '__main__':
    app.run(debug=True)