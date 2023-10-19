from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from veritabaniBaglan import *
import main

class KitapEkle(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kitap Ekle")
        self.setGeometry(300,80, 500, 600)
        self.setWindowIcon(QIcon('../icons/icon.ico'))
        self.setFixedSize(self.size())
        self.UI()
        self.show()
    def UI(self):
        # ---------Ana Layout-------------
        ana_layout= QVBoxLayout()

        # ---------Ust Çerçeve-------------
        ust_frame= QFrame(self)

        ust_layout=QHBoxLayout(ust_frame)

        kitap_resmi_alani= QLabel(ust_frame)
        kitap_resmi=QPixmap("../icons/addbook.png")
        kitap_resmi_alani.setPixmap(kitap_resmi)

        baslik_alani=QLabel("Kitap Ekle",ust_frame)
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
        self.kitap_isim_alani.setPlaceholderText("Kitap İsmi Giriniz..")

        self.yazar_isim_alani = QLineEdit(alt_frame)
        self.yazar_isim_alani.setPlaceholderText("Yazar Adını Giriniz..")

        self.sayfa_sayisi_isim_alani = QLineEdit(alt_frame)
        self.sayfa_sayisi_isim_alani.setPlaceholderText("Sayfa Sayısını Giriniz..")

        self.dil_isim_alani = QLineEdit(alt_frame)
        self.dil_isim_alani.setPlaceholderText("Kitap Dilini Giriniz...")
      
        self.kitap_aciklama = QTextEdit(alt_frame)

        kitap_ekle_buton = QPushButton("Ekle", alt_frame)
        kitap_ekle_buton.clicked.connect(self.kitap_ekle_fonksiyon)

        alt_layout.addRow(QLabel("Kitap İsmi:"), self.kitap_isim_alani)
        alt_layout.addRow(QLabel("Yazar İsmi:"), self.yazar_isim_alani)
        alt_layout.addRow(QLabel("Kitap Sayfa Sayısı:"), self.sayfa_sayisi_isim_alani)
        alt_layout.addRow(QLabel("Kitap Dili:"), self.dil_isim_alani)
        alt_layout.addRow(QLabel("Kitap Açıklama:"), self.kitap_aciklama)
        alt_layout.addRow(QLabel(""), kitap_ekle_buton)

        ana_layout.addWidget(alt_frame)
        self.setLayout(ana_layout)
    def kitap_ekle_fonksiyon(self):
        isim=self.kitap_isim_alani.text()
        yazar=self.yazar_isim_alani.text()
        sayfasayisi=self.sayfa_sayisi_isim_alani.text()
        dil=self.dil_isim_alani.text()
        aciklama= self.kitap_aciklama.toPlainText()

        if (isim and yazar and sayfasayisi and dil and aciklama != "") :
            try:
                sorgu="insert into  'kitaplar'  (kitap_adi, kitap_yazari, kitap_sayfa_sayisi, kitap_dil,kitap_detay) values (?,?,?,?,?)"
                cursor.execute(sorgu, (isim,yazar,sayfasayisi,dil,aciklama))
                con.commit()
                self.kitap_isim_alani.setText("")
                self.yazar_isim_alani.setText("")
                self.sayfa_sayisi_isim_alani.setText("")
                self.dil_isim_alani.setText("")
                self.kitap_aciklama.setText("")
                QMessageBox.information(self, "Uyarı!!!", "Kitap Eklendi....")
            except:
                QMessageBox.information(self, "Uyarı!!!", "Kitap Eklenmedi....")
        else:
            QMessageBox.information(self, "Uyarı!!!", "Alanlar boş Geçilemez....")
