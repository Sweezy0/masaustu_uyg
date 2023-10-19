from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from veritabaniBaglan import *
import main

class DuzenleUye(QWidget):
    def __init__(self,row, tablo_uyeler):
        super().__init__()
        self.setWindowTitle("Üye Düzenle")
        self.row= row
        self.tablo_uyeler = tablo_uyeler
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

        baslik_alani=QLabel("Üye Detay",ust_frame)
        baslik_alani.setStyleSheet("font:25pt Times Bold")

        ust_layout.addStretch()
        ust_layout.addWidget(kitap_resmi_alani)
        ust_layout.addWidget(baslik_alani)
        ust_layout.addStretch()

        ana_layout.addWidget(ust_frame)

        # ---------Alt Çerçeve-------------
        alt_frame = QFrame(self)
        alt_layout = QFormLayout(alt_frame)

        self.uye_isim_alani = QLineEdit(alt_frame)
        self.uye_isim_alani.setText(uye[0][1])

        self.telefon_isim_alani = QLineEdit(alt_frame)
        self.telefon_isim_alani.setText(uye[0][2])

        self.odunc_kitap_liste = QListWidget(alt_frame)
        if odunc_kitaplar != []:
            for kitap in odunc_kitaplar:
                self.odunc_kitap_liste.addItem(kitap[0])
        else:
            self.odunc_kitap_liste.addItem("Alınan Kitap Yok.......")

        uye_sil_buton = QPushButton("Sil", alt_frame)
        uye_sil_buton.clicked.connect(self.uye_sil_fonksiyon)

        alt_layout.addRow(QLabel("Üye İsmi:"), self.uye_isim_alani)
        alt_layout.addRow(QLabel("Üye Telefon:"), self.telefon_isim_alani)
        alt_layout.addRow(QLabel("Alınan Kitaplar:"), self.odunc_kitap_liste)
        alt_layout.addRow(QLabel(""), uye_sil_buton)

        ana_layout.addWidget(alt_frame)

        self.setLayout(ana_layout)
    def veri_doldur(self):
        liste_uye = []
        global uye_id
        global  uye
        global odunc_kitaplar
        for i in range(0, 3):
            text = self.tablo_uyeler.item(self.row, i).text()
            liste_uye.append(text)
        uye_id = liste_uye[0]
        uye = cursor.execute("select * from uyeler where uye_id=?", (uye_id,)).fetchall()
        odunc_kitaplar = cursor.execute("select kitaplar.kitap_adi from odunc left join kitaplar on kitaplar.kitap_id=odunc.oduncKitap_id where odunc.oduncUye_id=?",(uye_id,)).fetchall()
        print(odunc_kitaplar)
    def uye_sil_fonksiyon(self):
        global uye_id

        mesaj= QMessageBox.question(self, "Uyarı!!!!","Silmek İstediğinizden Emin misiniz...",QMessageBox.Yes|QMessageBox.No, QMessageBox.No)
        if mesaj == QMessageBox.Yes:
            try:
                cursor.execute("delete from uyeler where uye_id=?",(uye_id,))
                cursor.execute("delete from odunc where oduncUye_id=?", (uye_id,))
                con.commit()
                QMessageBox.information(self, "Uyarı!!!", "Üye Silindi....")

                self.mainpage = main.Main()
                self.mainpage.uye_al_fonksiyon()
            except:
                QMessageBox.information(self, "Uyarı!!!", "Üye Silinmedi....")