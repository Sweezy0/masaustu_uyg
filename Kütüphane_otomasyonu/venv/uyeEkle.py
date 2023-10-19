from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from veritabaniBaglan import *
import main

class UyeEkle(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Üye Ekle")
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

        baslik_alani=QLabel("Üye Ekle",ust_frame)
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
        self.uye_isim_alani.setPlaceholderText("Üye İsmi Giriniz..")

        self.telefon_alani = QLineEdit(alt_frame)
        self.telefon_alani.setPlaceholderText("Telefon Giriniz..")

        uye_ekle_buton = QPushButton("Ekle", alt_frame)
        uye_ekle_buton.clicked.connect(self.uye_ekle_fonksiyon)

        alt_layout.addRow(QLabel("Üye İsmi:"), self.uye_isim_alani)
        alt_layout.addRow(QLabel("Telefon:"), self.telefon_alani)
        alt_layout.addRow(QLabel(""), uye_ekle_buton)

        ana_layout.addWidget(alt_frame)
        self.setLayout(ana_layout)
    def uye_ekle_fonksiyon(self):
        isim=self.uye_isim_alani.text()
        telefon=self.telefon_alani.text()
        if (isim and telefon != "") :
            try:
                sorgu="insert into  'uyeler'  (uye_adi, uye_telefon) values (?,?)"
                cursor.execute(sorgu, (isim,telefon))
                con.commit()
                self.uye_isim_alani.setText("")
                self.telefon_alani.setText("")
                QMessageBox.information(self, "Uyarı!!!", "Üye Eklendi....")
            except:
                QMessageBox.information(self, "Uyarı!!!", "Üye Eklenmedi....")
        else:
            QMessageBox.information(self, "Uyarı!!!", "Alanlar boş Geçilemez....")
        self.mainpage = main.Main()
        self.mainpage.sekmeler.update()