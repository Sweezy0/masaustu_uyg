import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from veritabaniBaglan import *
from PyQt5.QtChart import QChart, QChartView, QPieSeries, QPieSlice
import kitapEkle, uyeEkle, kitapVer, duzenleKitap,duzenleUye
class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kütüphane Otomasyonu")
        self.setGeometry(50,50, 1200, 600)
        self.setWindowIcon(QIcon('../icons/icon.ico'))
        self.setFixedSize(self.size())

        # Zamanı güncellemek için bir QTimer kullanalım
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.tarih_saat_fonksiyon)
        self.timer.start(1000)  # Her 1 saniyede bir güncelle

        self.UI()
        self.show()
    def UI(self):
        self.toolbar()
        self.tasarim()
        self.kitap_al_fonksiyon()
        self.uye_al_fonksiyon()
        self.istatistik_al_fonksiyon()
        self.apply_style()
    def toolbar(self):
        self.tool_bar= self.addToolBar("Tool Bar")
        self.tool_bar.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

        #-------Kitap Ekle-------------
        self.kitap_ekle= QAction(QIcon("../icons/bookadd.png"),"Kitap Ekle",self)
        self.tool_bar.addAction((self.kitap_ekle))
        self.kitap_ekle.triggered.connect(self.kitap_ekle_fonksiyon)
        self.tool_bar.addSeparator()

        # -------Üye Ekle--------------
        self.uye_ekle = QAction(QIcon("../icons/users.png"), "Üye Ekle", self)
        self.tool_bar.addAction((self.uye_ekle))
        self.uye_ekle.triggered.connect(self.uyle_ekle_fonksiyon)
        self.tool_bar.addSeparator()

        # -------Kitap Ver--------------
        self.kitap_ver = QAction(QIcon("../icons/givebook.png"), "Kitap Ver", self)
        self.tool_bar.addAction((self.kitap_ver))
        self.kitap_ver.triggered.connect(self.kitap_ver_fonksiyon)
        self.tool_bar.addSeparator()

        # -------Esnek Boşluk--------------
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.tool_bar.addWidget(spacer)

        # -------Tema Değişikliği----------
        self.style_combobox = QComboBox(self)
        for file in os.listdir('../style'):
            #if file.endswith(".qss"):
                self.style_combobox.addItem(file)

        #self.style_combobox.addItem("AMOLED")
        #self.style_combobox.addItem("AQUA")
        #self.style_combobox.addItem("CONSOLE")
        #self.style_combobox.addItem("DARKBLUE")
        #self.style_combobox.addItem("ELEGANTDARK")
        #self.style_combobox.addItem("MACOS")
        #self.style_combobox.addItem("MANJAROMIX")
        #self.style_combobox.addItem("MATERIALDARK")
        #self.style_combobox.addItem("NEON")
        #self.style_combobox.addItem("UBUNTU")

        self.style_combobox.currentIndexChanged.connect(self.apply_style)
        self.tool_bar.addWidget((self.style_combobox))
        self.tool_bar.addSeparator()

        #--------Tarih ve zaman-----------------
        self.datetime_label = QLabel(self)
        self.tool_bar.addWidget(self.datetime_label)

        self.datetime_label = QLabel(self)
        self.tool_bar.addWidget(self.datetime_label)

        self.tool_bar.setMovable(False)
        self.tool_bar.toggleViewAction().setEnabled(False)
        self.tool_bar.setOrientation(1)

        self.tool_bar.addSeparator()

    def tasarim(self):
        #---------Ana Layout-------------
        ana_layout= QHBoxLayout()

        # -------Sağ ve Sol Layout-------
        sol_layout= QVBoxLayout()
        sag_layout= QVBoxLayout()

        ana_layout.addLayout(sol_layout,80)
        ana_layout.addLayout(sag_layout, 20)

        self.sekmeler=QTabWidget(self)
        self.setCentralWidget(self.sekmeler)

        self.sekme_kitaplar= QWidget()
        self.sekme_uyeler = QWidget()
        self.sekme_istatistik = QWidget()

        self.sekmeler.addTab(self.sekme_kitaplar, "kitaplar")
        self.sekmeler.addTab(self.sekme_uyeler, "Üyeler")
        self.sekmeler.addTab(self.sekme_istatistik, "İstatistik")

        #--------Sol Layout-------
        #---------Kitap Sekmesi----------
        self.tablo_kitaplar= QTableWidget()
        self.tablo_kitaplar.setColumnCount(6)
        self.tablo_kitaplar.setColumnHidden(0,True)
        self.tablo_kitaplar.setHorizontalHeaderItem(0,QTableWidgetItem("Kitap ID"))
        self.tablo_kitaplar.setHorizontalHeaderItem(1,QTableWidgetItem("Kitap Adı"))
        self.tablo_kitaplar.setHorizontalHeaderItem(2, QTableWidgetItem("Kitap Yazarı"))
        self.tablo_kitaplar.setHorizontalHeaderItem(3, QTableWidgetItem("Kitap Sayfası"))
        self.tablo_kitaplar.setHorizontalHeaderItem(4, QTableWidgetItem("Kitap Detay"))
        self.tablo_kitaplar.setHorizontalHeaderItem(5, QTableWidgetItem("Kitap Dili"))
        self.tablo_kitaplar.cellDoubleClicked.connect(self.secilen_kitap_fonksiyon)
        self.tablo_kitaplar.horizontalHeader().setStretchLastSection(True)
        sol_layout.addWidget(self.tablo_kitaplar)

        #---------Sağ Layout-------------
        #---------Arama Çerçevesi----------
        sag_ust_frame= QGroupBox(self)
        sag_ust_frame.setTitle("Kitap Ara")
        sag_ust_frame.setObjectName("arama_kutusu")

        sag_ust_frame_box=QHBoxLayout(sag_ust_frame)

        yazi_arama= QLabel("Ara",sag_ust_frame)
        self.arama_yazi_alani= QLineEdit(sag_ust_frame)
        arama_butonu= QPushButton("Kitap Ara",sag_ust_frame)
        arama_butonu.clicked.connect(self.kitap_ara_fonksiyonu)

        sag_ust_frame_box.addStretch()
        sag_ust_frame_box.addWidget(yazi_arama)
        sag_ust_frame_box.addWidget(self.arama_yazi_alani)
        sag_ust_frame_box.addWidget(arama_butonu)

        sag_ust_frame_box.addStretch()
        sag_layout.addWidget(sag_ust_frame,20)

        # ---------Sağ Layout---------------
        # ---------Listeleme Çerçevesi------
        sag_orta_frame= QGroupBox( self)
        sag_orta_frame.setTitle("Kitap Listele")
        sag_orta_frame.setObjectName("listele_kutusu")

        self.radio_buton_bir=QRadioButton("Hepsi", sag_orta_frame)
        self.radio_buton_iki=QRadioButton("Mevcut", sag_orta_frame)
        self.radio_buton_uc=QRadioButton("Ödünç", sag_orta_frame)
        self.liste_buton= QPushButton("Kitap Listele", sag_orta_frame)
        self.liste_buton.clicked.connect(self.kitap_listele_fonksiyon)

        sag_orta_frame_box= QHBoxLayout(sag_orta_frame)
        sag_orta_frame_box.addStretch()
        sag_orta_frame_box.addWidget(self.radio_buton_bir)
        sag_orta_frame_box.addWidget(self.radio_buton_iki)
        sag_orta_frame_box.addWidget(self.radio_buton_uc)
        sag_orta_frame_box.addWidget(self.liste_buton)

        sag_orta_frame_box.addStretch()
        sag_layout.addWidget(sag_orta_frame,20)

        # ---------Sağ Layout---------------
        # ---------Resim Çerçevesi----------
        sag_alt_frame_box=QVBoxLayout()
        baslik_yazisi= QLabel("Hoşgeldiniz")
        baslik_yazisi.setContentsMargins(160,0,0,0)

        baslik_yazisi.setFont(QFont("Times",20))
        sag_alt_frame_box.addWidget(baslik_yazisi)

        resim_kutuphane_alani=QLabel("")
        resim_kutuphane=QPixmap("../icons/library.jpg")

        resim_kutuphane_alani.setPixmap(resim_kutuphane)
        resim_kutuphane_alani.setContentsMargins(10, 0, 0, 0)
        sag_alt_frame_box.addWidget(resim_kutuphane_alani)

        sag_layout.addLayout(sag_alt_frame_box,60)

        self.sekme_kitaplar.setLayout(ana_layout)

        # --------Sol Layout-------
        # ---------Uyeler Sekmesi----------
        uyeler_ana_layout=QHBoxLayout()

        uyeler_sag_layout=QVBoxLayout()
        uyeler_sol_layout=QHBoxLayout()

        uyeler_ana_layout.addLayout(uyeler_sol_layout, 65)
        uyeler_ana_layout.addLayout(uyeler_sag_layout,35)

        self.tablo_uyeler = QTableWidget()
        self.tablo_uyeler.setColumnCount(3)

        self.tablo_uyeler.setColumnHidden(0, True)
        self.tablo_uyeler.setHorizontalHeaderItem(0, QTableWidgetItem("Üye ID"))
        self.tablo_uyeler.setHorizontalHeaderItem(1, QTableWidgetItem("Üye Adı"))
        self.tablo_uyeler.setHorizontalHeaderItem(2, QTableWidgetItem("Üye Telefon"))
        self.tablo_uyeler.cellDoubleClicked.connect(self.secilen_uye_fonksiyon)
        self.tablo_uyeler.horizontalHeader().setStretchLastSection(True)
        uyeler_sol_layout.addWidget(self.tablo_uyeler)

        # ---------Sağ Layout--------------
        # ---------Uyeler Sekmesi----------
        uyeler_sag_frame = QGroupBox(self)
        uyeler_sag_frame.setTitle("Üye Ara")
        uyeler_sag_frame.setObjectName("uye_listele_kutusu")

        uyeler_sag_frame_box = QHBoxLayout(uyeler_sag_frame)

        uyeler_yazi_arama = QLabel("Ara", uyeler_sag_frame)

        self.uyeler_arama_yazi_alani = QLineEdit(uyeler_sag_frame)

        uyeler_arama_butonu = QPushButton("Üye Ara", uyeler_sag_frame)
        uyeler_arama_butonu.clicked.connect(self.uyeler_ara_fonksiyonu)

        uyeler_sag_frame_box.addStretch()
        uyeler_sag_frame_box.addWidget(uyeler_yazi_arama)
        uyeler_sag_frame_box.addWidget(self.uyeler_arama_yazi_alani)
        uyeler_sag_frame_box.addWidget(uyeler_arama_butonu)
        uyeler_sag_frame_box.addStretch()
        uyeler_sag_layout.addWidget(uyeler_sag_frame)
        uyeler_sag_layout.addLayout(uyeler_sag_frame_box,20)
        uyeler_sag_layout.addStretch()

        self.sekme_uyeler.setLayout(uyeler_ana_layout)


        # ---------İstatistik Sekmesi----------
        istatistik_ana_layout=QHBoxLayout()

        istatistik_sag_layout = QVBoxLayout()
        istatistik_sol_layout = QVBoxLayout()

        istatistik_ana_layout.addLayout(istatistik_sag_layout,65)
        istatistik_ana_layout.addLayout(istatistik_sol_layout,35)

        self.istatistik_group= QGroupBox("İstatistik")
        self.istatistik_form_layout= QFormLayout()

        self.toplam_kitaplar= QLabel("")
        self.toplam_uyeler= QLabel("")
        self.verilen_kitaplar= QLabel("")
        self.mevcut_kitaplar= QLabel("")

        self.istatistik_form_layout.addChildWidget(self.istatistik_group)
        self.istatistik_form_layout.addRow(QLabel("Toplam Kitaplar : "),self.toplam_kitaplar)
        self.istatistik_form_layout.addRow(QLabel("Toplam Üyeler : "),self.toplam_uyeler)
        self.istatistik_form_layout.addRow(QLabel("Verilen Kitaplar : "),self.verilen_kitaplar)
        self.istatistik_form_layout.addRow(QLabel("Mevcut Kitaplar : "),self.mevcut_kitaplar)

        self.istatistik_group.setLayout(self.istatistik_form_layout)
        istatistik_sol_layout.addWidget(self.istatistik_group)

        # Kitap istatistikleri
        kitap_series = QPieSeries()
        mevcut_kitap_sayisi =cursor.execute("select count(kitap_durumu) from kitaplar where kitap_durumu='Mevcut' ").fetchone()[0]
        verilen_kitap_sayisi =cursor.execute("select count(kitap_durumu) from kitaplar where kitap_durumu='Mevcut Değil' ").fetchone()[0]

        kitap_series.append("Mevcut Kitaplar", mevcut_kitap_sayisi)
        kitap_series.append("Verilen Kitaplar", verilen_kitap_sayisi)

        kitap_chart = QChart()
        kitap_chart.addSeries(kitap_series)
        kitap_chart.setTitle("Kitap İstatistikleri")

        self.kitap_chart_view = QChartView(kitap_chart)
        istatistik_sag_layout.addWidget(self.kitap_chart_view)

        self.sekme_istatistik.setLayout(istatistik_ana_layout)
    def kitap_ekle_fonksiyon(self):
        self.kitapEkle=kitapEkle.KitapEkle()

    def uyle_ekle_fonksiyon(self):
        self.uyeEkle=uyeEkle.UyeEkle()

    def kitap_ver_fonksiyon(self):
        self.kitapVer = kitapVer.KitapVer()

    def kitap_al_fonksiyon(self):
        for i in reversed(range(self.tablo_kitaplar.rowCount())):
            self.tablo_kitaplar.removeRow(i)
        sorgu=cursor.execute("select kitap_id, kitap_adi, kitap_yazari, kitap_sayfa_sayisi,kitap_detay, kitap_dil, kitap_durumu From kitaplar")
        for satir_verisi in sorgu:
            satir_numarasi= self.tablo_kitaplar.rowCount()
            self.tablo_kitaplar.insertRow(satir_numarasi)
            for sutun_numarasi, veri in enumerate(satir_verisi):
                self.tablo_kitaplar.setItem(satir_numarasi, sutun_numarasi,QTableWidgetItem(str(veri)))

        #QTimer.singleShot(1000, self.kitap_al_fonksiyon)
        self.tablo_kitaplar.setEditTriggers(QAbstractItemView.NoEditTriggers)

    def secilen_kitap_fonksiyon(self):
        self.duzenleKitap = duzenleKitap.DuzenleKitap(self.tablo_kitaplar.currentRow(),self.tablo_kitaplar )

    def tarih_saat_fonksiyon(self):
        simdiki = QDateTime.currentDateTime()
        tarih_saat_text= simdiki.toString("yyyy-MM-dd\nhh:mm")
        self.datetime_label.setText(tarih_saat_text)

    def kitap_ara_fonksiyonu(self):
        deger=self.arama_yazi_alani.text()
        if deger == "":
            QMessageBox.information(self, "Uyarı!!", "Arama Alanına Boş Değer Girmeyiniz.")
        else:
            sorgu=cursor.execute("select *  from kitaplar where  kitap_adi like ? or kitap_yazari like ? ",
                                 ('%' +deger + '%', '%' +deger + '%')).fetchall()

            if sorgu== []:
                QMessageBox.information(self, "Uyarı!!", "Kayıt Bulunamadı")
            else:
                for i in reversed(range(self.tablo_kitaplar.rowCount())):
                    self.tablo_kitaplar.removeRow(i)
                for satir_verisi in sorgu:
                    satir_numarasi = self.tablo_kitaplar.rowCount()
                    self.tablo_kitaplar.insertRow(satir_numarasi)
                    for sutun_numarasi, veri in enumerate(satir_verisi):
                        self.tablo_kitaplar.setItem(satir_numarasi, sutun_numarasi, QTableWidgetItem(str(veri)))

    def kitap_listele_fonksiyon(self):
        if self.radio_buton_bir.isChecked() == True:
            sorgu= cursor.execute("select kitap_id, kitap_adi, kitap_yazari, kitap_sayfa_sayisi,kitap_detay, kitap_dil, kitap_durumu  from kitaplar")
            for i in reversed(range(self.tablo_kitaplar.rowCount())):
                self.tablo_kitaplar.removeRow(i)
            for satir_verisi in sorgu:
                satir_numarasi = self.tablo_kitaplar.rowCount()
                self.tablo_kitaplar.insertRow(satir_numarasi)
                for sutun_numarasi, veri in enumerate(satir_verisi):
                    self.tablo_kitaplar.setItem(satir_numarasi, sutun_numarasi, QTableWidgetItem(str(veri)))

        elif self.radio_buton_iki.isChecked() == True:
            sorgu = cursor.execute("select  kitap_id, kitap_adi, kitap_yazari, kitap_sayfa_sayisi,kitap_detay, kitap_dil, kitap_durumu  "
                                   "From kitaplar where kitap_durumu= ?", ("Mevcut",))
            for i in reversed(range(self.tablo_kitaplar.rowCount())):
                self.tablo_kitaplar.removeRow(i)
            for satir_verisi in sorgu:
                satir_numarasi = self.tablo_kitaplar.rowCount()
                self.tablo_kitaplar.insertRow(satir_numarasi)
                for sutun_numarasi, veri in enumerate(satir_verisi):
                    self.tablo_kitaplar.setItem(satir_numarasi, sutun_numarasi, QTableWidgetItem(str(veri)))

        elif self.radio_buton_uc.isChecked() == True:
            sorgu = cursor.execute("select  kitap_id, kitap_adi, kitap_yazari, kitap_sayfa_sayisi,kitap_detay, kitap_dil, kitap_durumu  "
                                   "From kitaplar where kitap_durumu= ?", ("Mevcut Değil",))
            for i in reversed(range(self.tablo_kitaplar.rowCount())):
                self.tablo_kitaplar.removeRow(i)
            for satir_verisi in sorgu:
                satir_numarasi = self.tablo_kitaplar.rowCount()
                self.tablo_kitaplar.insertRow(satir_numarasi)
                for sutun_numarasi, veri in enumerate(satir_verisi):
                    self.tablo_kitaplar.setItem(satir_numarasi, sutun_numarasi, QTableWidgetItem(str(veri)))

    def uyeler_ara_fonksiyonu(self):
        deger=self.uyeler_arama_yazi_alani.text()
        if deger == "":
            QMessageBox.information(self, "Uyarı!!", "Arama Alanına Boş Değer Girmeyiniz.")
        else:
            sorgu=cursor.execute("select * from uyeler where  uye_adi like ? or uye_telefon like ? ",
                                 ('%' +deger + '%', '%' +deger + '%')).fetchall()
            if sorgu== []:
                QMessageBox.information(self, "Uyarı!!", "Kayıt Bulunamadı")
            else:
                for i in reversed(range(self.tablo_uyeler.rowCount())):
                    self.tablo_uyeler.removeRow(i)
                for satir_verisi in sorgu:
                    satir_numarasi = self.tablo_uyeler.rowCount()
                    self.tablo_uyeler.insertRow(satir_numarasi)
                    for sutun_numarasi, veri in enumerate(satir_verisi):
                        self.tablo_uyeler.setItem(satir_numarasi, sutun_numarasi, QTableWidgetItem(str(veri)))

    def uye_al_fonksiyon(self):
        for i in reversed(range(self.tablo_uyeler.rowCount())):
            self.tablo_uyeler.removeRow(i)
        sorgu = cursor.execute("select  uye_id, uye_adi, uye_telefon From uyeler")
        for satir_verisi in sorgu:
            satir_numarasi = self.tablo_uyeler.rowCount()
            self.tablo_uyeler.insertRow(satir_numarasi)
            for sutun_numarasi, veri in enumerate(satir_verisi):
                self.tablo_uyeler.setItem(satir_numarasi, sutun_numarasi, QTableWidgetItem(str(veri)))

        #QTimer.singleShot(1000, self.uye_al_fonksiyon)
        self.tablo_uyeler.setEditTriggers(QAbstractItemView.NoEditTriggers)

    def secilen_uye_fonksiyon(self):
        self.duzenleUye = duzenleUye.DuzenleUye(self.tablo_uyeler.currentRow(),self.tablo_uyeler )
    def istatistik_al_fonksiyon(self):
        kitap_sayisi= cursor.execute("select count(kitap_id) from kitaplar").fetchall()
        uye_sayisi= cursor.execute("select count(uye_id) from uyeler").fetchall()
        verilen_kitap_sayisi= cursor.execute("select count(kitap_durumu) from kitaplar where kitap_durumu='Mevcut Değil' ").fetchall()
        mevcut_kitap_sayisi= cursor.execute("select count(kitap_durumu) from kitaplar where kitap_durumu='Mevcut' ").fetchall()

        self.toplam_kitaplar.setText(str(kitap_sayisi[0][0]))
        self.toplam_uyeler.setText(str(uye_sayisi[0][0]))
        self.mevcut_kitaplar.setText(str(mevcut_kitap_sayisi[0][0]))
        self.verilen_kitaplar.setText(str(verilen_kitap_sayisi[0][0]))
        #QTimer.singleShot(1000, self.istatistik_al_fonksiyon)

    def apply_style(self):
        selected_style = self.style_combobox.currentText()
        if selected_style == "aqua.qss":
            self.load_stylesheet("../style/aqua.qss")
        elif selected_style == "ConsoleStyle.qss":
            self.load_stylesheet("../style/ConsoleStyle.qss")
        elif selected_style == "ElegantDark.qss":
            self.load_stylesheet("../style/ElegantDark.qss")
        elif selected_style == "NeonButtons.qss":
            self.load_stylesheet("../style/NeonButtons.qss")
        elif selected_style == "MacOS.qss":
            self.load_stylesheet("../style/MacOS.qss")
        elif selected_style == "ManjaroMix.qss":
            self.load_stylesheet("../style/ManjaroMix.qss")
        elif selected_style == "AMOLED.qss":
            self.load_stylesheet("../style/AMOLED.qss")
        elif selected_style == "MaterialDark.qss":
            self.load_stylesheet("../style/MaterialDark.qss")
        elif selected_style == "Ubuntu.qss":
            self.load_stylesheet("../style/Ubuntu.qss")
        elif selected_style == "darkBlue.qss":
            self.load_stylesheet("../style/darkBlue.qss")

    def load_stylesheet(self, filename):
        style = QFile(filename)
        if style.open(QFile.ReadOnly | QFile.Text):
            stream = QTextStream(style)
            stylesheet = stream.readAll()
            QApplication.instance().setStyleSheet(stylesheet)
            style.close()
def main():
    App= QApplication(sys.argv)
    window= Main()
    sys.exit(App.exec_())

if __name__ == '__main__':
    main()