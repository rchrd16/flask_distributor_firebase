from flask import Flask, render_template, request, redirect, url_for
import firebase_admin
from firebase_admin import credentials, firestore

# Inisialisasi Firebase Admin SDK
cred = credentials.Certificate("ladju_distributor.json")
firebase_admin.initialize_app(cred)

# Firestore database instance
db = firestore.client()

app = Flask(__name__)

# Status pesanan yang bisa diubah
STATUS_LIST = [
    "Pesanan sedang diproses",
    "Kurir mengambil paket",
    "Kurir mengirim paket",
    "Barang masuk Gudang sortir A",
    "Barang masuk Gudang sortir B",
    "Barang masuk Gudang sortir C",
    "Kurir menuju ke toko lokasi anda",
    "Pesanan Selesai"
]

@app.route('/')
def index():
    # Ambil data dari Firestore collection 'tb_pesanan' dan 'tb_ongkos_kirim'
    pesanan_docs = db.collection('tb_pesanan').stream()
    ongkos_docs = db.collection('tb_ongkos_kirim').stream()

    pesanan_list = [doc.to_dict() for doc in pesanan_docs]
    ongkos_list = [doc.to_dict() for doc in ongkos_docs]

    return render_template('index.html', pesanan=pesanan_list, ongkos=ongkos_list, status_list=STATUS_LIST)

@app.route('/update_status', methods=['POST'])
def update_status():
    if request.method == 'POST':
        doc_id = request.form['doc_id']
        new_status = request.form['status']
        
        # Update Firestore
        db.collection('tb_ongkos_kirim').document(doc_id).update({
            'id_status': new_status
        })
    return redirect(url_for('index'))

@app.route('/add_order', methods=['GET', 'POST'])
def add_order():
    if request.method == 'POST':
        alamat_retail = request.form['alamat_retail']
        alamat_supplier = request.form['alamat_supplier']
        berat = int(request.form['id_berat'])
        jumlah = int(request.form['id_jumlah'])

        # Perhitungan ongkos kirim (jarak dan berat)
        JARAK_KOTA = {
            ('ngawi', 'solo'): 102,
            ('bali', 'solo'): 335,
            ('surabaya', 'solo'): 262,
            ('bali', 'madura'): 274,
            ('ngawi', 'madura'): 269,
            ('surabaya', 'madura'): 32,
            ('bali', 'batam'): 623,
            ('ngawi', 'batam'): 488,
            ('surabaya', 'batam'): 503,
        }
        
        jarak = JARAK_KOTA.get((alamat_retail.lower(), alamat_supplier.lower()), 0)
        ongkos_kirim = jarak * 500 + berat * 1000

         # Generate ID baru
        existing_orders = db.collection('tb_ongkos_kirim').stream()
        existing_ids = [doc.id for doc in existing_orders if doc.id.startswith('LOGDIS')]
        
        if existing_ids:
            # Ambil nomor terakhir dari ID yang ada
            last_id = sorted(existing_ids)[-1]  # Ambil ID terakhir
            last_number = int(last_id[7:])  # Ambil nomor di belakang 'LOGDIS'
            new_number = last_number + 1  # Tambah 1
        else:
            new_number = 1  # Jika tidak ada ID, mulai dari 1

        new_id = f'LOGDIS{str(new_number).zfill(5)}'  # Format ID baru

        # Mapping kode kota
        supplier_codes = {
            'madura': 'S01',
            'solo': 'S02',
            'batam': 'S03'
        }
        
        retail_codes = {
            'ngawi': 'R01',
            'denpasar': 'R02',
            'surabaya': 'R03'
        }

        # Mendapatkan kode supplier dan retail
        supplier_code = supplier_codes.get(alamat_supplier.lower(), 'S00')  # Default jika tidak ditemukan
        retail_code = retail_codes.get(alamat_retail.lower(), 'R00')  # Default jika tidak ditemukan

        # Hitung urutan pesanan
        existing_resi = db.collection('tb_ongkos_kirim').where('alamat_retail', '==', alamat_retail)\
            .where('alamat_supplier', '==', alamat_supplier).stream()
        
        pk_count = sum(1 for _ in existing_resi) + 1  # Hitung pesanan sebelumnya dan tambah 1

        # Generate id_resi
        id_resi = f'LES{supplier_code}{retail_code}PK{str(pk_count).zfill(3)}'

        # Simpan ke Firestore
        db.collection('tb_ongkos_kirim').add({
            'alamat_retail': alamat_retail,
            'alamat_supplier': alamat_supplier,
            'harga': str(ongkos_kirim),
            'id_berat': berat,
            'id_jumlah': jumlah,
            'id_resi': id_resi,
            'id_status': 'Pesanan sedang diproses'
        }, document_id=new_id)

        return redirect(url_for('index'))

    return render_template('add_order.html')

if __name__ == '__main__':
    app.run(debug=True)
