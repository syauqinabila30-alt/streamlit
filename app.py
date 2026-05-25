import streamlit as st

class KategoriNode:
    def __init__(self, nama_kategori):
        self.nama = nama_kategori
        self.sub_kategori = []

    def tambah_sub(self, node_kategori):
        self.sub_kategori.append(node_kategori)

    def dapatkan_tree_string(self, level=0):
        indentasi = "    " * level
        simbol = "↳ " if level > 0 else " + "
        hasil = f"{indentasi}{simbol}{self.nama}\n"
        
        for sub in self.sub_kategori:
            hasil =f"{indentasi}{simbol}{self.nama}"
        return hasil

    def cari_node(self, target_nama):
        # Mencari node spesifik untuk menambahkan anak di bawahnya
        if self.nama.lower() == target_nama.lower():
            return self
            
        for sub in self.sub_kategori:
            hasil = sub.cari_node(target_nama)
            if hasil:
                return hasil
                
        return None

    def cari_jalur(self, target, path=""):
        # Mencari jalur lengkap (breadcrumb) seperti studi kasus sebelumnya
        jalur_saat_ini = path + " > " + self.nama if path else self.nama
        
        if self.nama.lower() == target.lower():
            return jalur_saat_ini
            
        for sub in self.sub_kategori:
            hasil = sub.cari_jalur(target, jalur_saat_ini)
            if hasil:
                return hasil
                
        return None

# ==========================================
# PROGRAM UTAMA (INTERAKTIF)
# ==========================================

st.set_page_config(page_title="struktur kategori", page_icon=" + ")

st.title("pembuat struktur kategori")
st. write("aplikasi interaktif untuk menstimulasikan stuktu data tree.")

if 'root' not in st.session_state:
    st.session_state.root = None

if st.session_state.root is None:
    st.info("sistem belum memiliki kategori utama. silahkan buat terlebih dahulu.")
    nama_root = st.text_input("masukkan nama kategori utama (root):",
value="toko saya")

    if st.button("buat kategori utama", type="primary"):
        st.session_state.root = KategoriNode(nama_root)
        st.rerun()

else:
    root = st.session_state.root

    tab1, tab2, tab3, = st.tabs(["lihat struktur", "+ tambah sub-kategori", " cari jalur"])

    #tab1
    with tab1:
        st.subheader("struktur kategori saat ini")
        tree_teks = root.dapatkan_tree_string()

        st.code(tree_teks, language="text")

    #tab2
    with tab2:
        st.subheader("tambah cabang baru")
        induk_nama = st.text_input("nama kategori induk tempat cabang ditambahkan:")
        anak_nama = st.text_input("nama sub-kategori baru:")

        if st.button("tambah kategori"):
            if induk_nama and anak_nama:
                induk_node = root.cari_node(induk_nama)
                if induk_node:
                    induk_node.tambah_sub(KategoriNode(anak_nama))
                    st.success(f"berhasil menambahkan '{anak_nama}' di bawah '{induk_node.nama}'!")
                else:
                    st.error(f"kategori '{induk_nama}' tidak ditemukan! pastikan ejaannya benar.")
            else:
                st.warning("harap isi kedua kolom diatas.")

    #tab3
    with tab3:
        st.subheader("pencarian breadcrumb")
        target_cari = st.text_input("nama kategori yang ingin dicari jalurnya")

        if st.button("cari jalur"):
            if target_cari:
                hasil = root.cari_jalur(target_cari)
                if hasil:
                    st.success("ditemukan!")
                    st.info(f" jalur: {hasil}")
                else:
                    st.error(f"kategori '{target_cari}' tidak ditemukan dalam sistem.")
            else:
                st.warning("harap isi nama kategori yang dicari.")

    #tombol reset
    st.divider()
    if st.button("reset sistem / mulai dari awal"):
        st.session_state.root = None
        st.rerun()
