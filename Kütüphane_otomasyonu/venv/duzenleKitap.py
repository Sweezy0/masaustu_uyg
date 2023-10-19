from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from veritabaniBaglan import *
import main

class DuzenleKitap(QWidget):
    def __init__(self,row, tablo_kitaplar):
        super().__init__()
        self.setWindowTitle("Kitap Düzenle")
        self.row= row
        self.tablo_kitaplar = tablo_kitaplar
        self.setGeometry(300,80, 500, 600)
        self.setWindowIcon(QIcon('../icons/icon.ico'))
        self.setFixedSize(self.size())
        self.UI()
        self.show()
    def UI(self):
        self.veri_doldur()

        # ---------Ana Layout-------------
        ana_layout= QVBoxLayout()

        # ---------Ust Çerçeve-------------
        ust_frame= QFrame(self)

        ust_layout=QHBoxLayout(ust_frame)

        kitap_resmi_alani= QLabel(ust_frame)
        kitap_resmi=QPixmap("../icons/addbook.png")
        kitap_resmi_alani.setPixmap(kitap_resmi)

        baslik_alani=QLabel("Kitap Detay",ust_frame)
        baslik_alani.setStyleSheet("font:25pt Times Bold")

        ust_layout.addStretch()
        ust_layout.addWidget(kitap_resmi_alani)
        ust_layout.addWidget(baslik_alani)
        ust_layout.addStretch()

        ana_layout.addWidget(ust_frame)

        # ---------Alt Çerçeve-------------
        alt_frame = QFrame(self)
        alt_layout = QFormLayout(alt_frame)

        self.kitap_isim_alani = QLineEdit(alt_frame)
        self.kitap_isim_alani.setText(kitap[0][1])

        self.yazar_isim_alani = QLineEdit(alt_frame)
        self.yazar_isim_alani.setText(kitap[0][2])

        self.sayfa_sayisi_isim_alani = QLineEdit(alt_frame)
        self.sayfa_sayisi_isim_alani.setText(kitap[0][3])

        self.dil_isim_alani = QLineEdit(alt_frame)
        self.dil_isim_alani.setText(kitap[0][4])

        self.kitap_aciklama = QTextEdit(alt_frame)
        self.kitap_aciklama.setText(kitap[0][5])

        kitap_sil_buton = QPushButton("Sil", alt_frame)
        kitap_sil_buton.clicked.connect(self.kitap_sil_fonksiyon)

        alt_layout.addRow(QLabel("Kitap İsmi:"), self.kitap_isim_alani)
        alt_layout.addRow(QLabel("Yazar İsmi:"), self.yazar_isim_alani)
        alt_layout.addRow(QLabel("Kitap Sayfa Sayısı:"), self.sayfa_sayisi_isim_alani)
        alt_layout.addRow(QLabel("Kitap Dili:"), self.dil_isim_alani)
        alt_layout.addRow(QLabel("Kitap Açıklama:"), self.kitap_aciklama)
        alt_layout.addRow(QLabel(""), kitap_sil_buton)

        ana_layout.addWidget(alt_frame)

        self.setLayout(ana_layout)

    def veri_doldur(self):
        liste_kitap = []
        global kitap_id
        global  kitap
        for i in range(0, 6):
            text = self.tablo_kitaplar.item(self.row, i).text()
            liste_kitap.append(text)
        kitap_id = liste_kitap[0]
        kitap = cursor.execute("select * from kitaplar where kitap_id=?", (kitap_id,)).fetchall()
    def kitap_sil_fonksiyon(self):
        global kitap_id
        mesaj= QMessageBox.question(self, "Uyarı!!!!","Silmek İstediğinizden Emin misiniz...",QMessageBox.Yes|QMessageBox.No, QMessageBox.No)
        if mesaj == QMessageBox.Yes:
            try:
                cursor.execute("delete from kitaplar where kitap_id=?",(kitap_id,))
                cursor.execute("delete from odunc where oduncKitap_id=?", (kitap_id,))
                con.commit()
                QMessageBox.information(self, "Uyarı!!!", "Kitap Silindi....")

                self.mainpage = main.Main()
                self.mainpage.kitap_al_fonksiyon()
            except:
                QMessageBox.information(self, "Uyarı!!!", "Kitap Silinmedi....")