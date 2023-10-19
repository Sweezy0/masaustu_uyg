from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from veritabaniBaglan import *
import  main
class KitapVer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kitap Ödünç Ver")
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

        self.kitap_combo=QComboBox(alt_frame)
        kitaplar=cursor.execute("select * from kitaplar where kitap_durumu='Mevcut'").fetchall()

        for kitap in kitaplar:
            self.kitap_combo.addItem(str(kitap[0])+"-"+kitap[1])

        self.uye_combo = QComboBox(alt_frame)
        uyeler = cursor.execute("select * from uyeler").fetchall()
        for uye in uyeler:
            self.uye_combo.addItem(str(uye[0])+"-"+uye[1])

        kitap_ver_buton = QPushButton("Ekle", alt_frame)
        kitap_ver_buton.clicked.connect(self.kitap_ver_fonksiyon)
        alt_layout.addRow(QLabel("Kitap:"), self.kitap_combo)
        alt_layout.addRow(QLabel("Üye:"), self.uye_combo)
        alt_layout.addRow(QLabel(""), kitap_ver_buton)
        ana_layout.addWidget(alt_frame)
        self.setLayout(ana_layout)
    def kitap_ver_fonksiyon(self):
        kitap=self.kitap_combo.currentText()
        kitap_id=kitap.split("-")[0]
        uye=self.uye_combo.currentText()
        uye_id = uye.split("-")[0]

        try:
            sorgu="insert into 'odunc' (oduncKitap_id, oduncUye_id) values(?,?)"
            cursor.execute(sorgu, (kitap_id,uye_id))
            con.commit()

            cursor.execute("update kitaplar  set kitap_durumu=? where kitap_id= ?", ('Mevcut Değil', kitap_id ))
            con.commit()
            QMessageBox.information(self, "Uyarı!!!", "Kitap Başarılı bir şekilde Ödünç Verildi....")

        except:
            QMessageBox.warning(self, "Uyarı!!!", "Kitap Ödünç Verilemedi........")

        self.mainpage= main.Main()
        self.mainpage.sekmeler.update()