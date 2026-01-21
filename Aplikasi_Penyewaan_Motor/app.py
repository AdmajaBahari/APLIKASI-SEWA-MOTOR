from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
DB_NAME = 'database.db'


def get_db():
    return sqlite3.connect(DB_NAME)


@app.route('/')
def home():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
        SELECT motor.id, motor.nama, motor.merk, motor.plat_nomor,
               motor.status, penyewa.nama
        FROM motor
        LEFT JOIN penyewa ON motor.id_penyewa = penyewa.id
    """)
    data = cursor.fetchall()
    return render_template('home.html', data=data)


# ================= MOTOR =================
@app.route('/motor')
def motor():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM motor")
    data = cursor.fetchall()
    return render_template('motor.html', data=data)


@app.route('/motor/add', methods=['GET', 'POST'])
def add_motor():
    if request.method == 'POST':
        nama = request.form['nama']
        merk = request.form['merk']
        plat = request.form['plat']

        db = get_db()
        cursor = db.cursor()
        cursor.execute("""
            INSERT INTO motor (nama, merk, plat_nomor, status)
            VALUES (?, ?, ?, 'tersedia')
        """, (nama, merk, plat))
        db.commit()
        return redirect(url_for('motor'))

    return render_template('add_motor.html')


@app.route('/motor/edit/<int:id>', methods=['GET', 'POST'])
def edit_motor(id):
    db = get_db()
    cursor = db.cursor()

    if request.method == 'POST':
        nama = request.form['nama']
        merk = request.form['merk']
        plat = request.form['plat']
        cursor.execute("""
            UPDATE motor SET nama=?, merk=?, plat_nomor=?
            WHERE id=?
        """, (nama, merk, plat, id))
        db.commit()
        return redirect(url_for('motor'))

    cursor.execute("SELECT * FROM motor WHERE id=?", (id,))
    data = cursor.fetchone()
    return render_template('edit_motor.html', data=data)


@app.route('/motor/delete/<int:id>')
def delete_motor(id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM motor WHERE id=?", (id,))
    db.commit()
    return redirect(url_for('motor'))


# ================= PENYEWA =================
@app.route('/penyewa')
def penyewa():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM penyewa")
    data = cursor.fetchall()
    return render_template('penyewa.html', data=data)


@app.route('/penyewa/add', methods=['GET', 'POST'])
def add_penyewa():
    if request.method == 'POST':
        nama = request.form['nama']
        nik = request.form['nik']
        alamat = request.form['alamat']

        db = get_db()
        cursor = db.cursor()
        cursor.execute("""
            INSERT INTO penyewa (nama, nik, alamat)
            VALUES (?, ?, ?)
        """, (nama, nik, alamat))
        db.commit()
        return redirect(url_for('penyewa'))

    return render_template('add_penyewa.html')


@app.route('/penyewa/edit/<int:id>', methods=['GET', 'POST'])
def edit_penyewa(id):
    db = get_db()
    cursor = db.cursor()

    if request.method == 'POST':
        nama = request.form['nama']
        nik = request.form['nik']
        alamat = request.form['alamat']
        cursor.execute("""
            UPDATE penyewa SET nama=?, nik=?, alamat=?
            WHERE id=?
        """, (nama, nik, alamat, id))
        db.commit()
        return redirect(url_for('penyewa'))

    cursor.execute("SELECT * FROM penyewa WHERE id=?", (id,))
    data = cursor.fetchone()
    return render_template('edit_penyewa.html', data=data)


@app.route('/penyewa/delete/<int:id>')
def delete_penyewa(id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM penyewa WHERE id=?", (id,))
    db.commit()
    return redirect(url_for('penyewa'))


# ================= SEWA =================
@app.route('/sewa/<int:id>', methods=['GET', 'POST'])
def sewa_motor(id):
    db = get_db()
    cursor = db.cursor()

    if request.method == 'POST':
        id_penyewa = request.form['penyewa']
        cursor.execute("""
            UPDATE motor
            SET status='disewa', id_penyewa=?
            WHERE id=?
        """, (id_penyewa, id))
        db.commit()
        return redirect(url_for('home'))

    cursor.execute("SELECT * FROM penyewa")
    penyewa = cursor.fetchall()
    return render_template('sewa_motor.html', penyewa=penyewa)

@app.route('/kembalikan/<int:id>')
def kembalikan_motor(id):
    db = get_db()
    cursor = db.cursor()

    cursor.execute("""
        UPDATE motor
        SET status = 'tersedia',
            id_penyewa = NULL
        WHERE id = ?
    """, (id,))

    db.commit()
    return redirect(url_for('home'))


def init_db():
    db = sqlite3.connect(DB_NAME)
    cursor = db.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS penyewa (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nama TEXT,
        nik TEXT,
        alamat TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS motor (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nama TEXT,
        merk TEXT,
        plat_nomor TEXT,
        status TEXT,
        id_penyewa INTEGER DEFAULT NULL
    )
    """)

    db.commit()
    db.close()

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
