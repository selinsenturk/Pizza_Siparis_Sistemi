from PyQt5.QtWidgets import *
from siparis import Ui_MainWindow
# Kütüphaneleri içe aktarıyoruz.
import csv
import datetime

# Pizza üst sınıfını oluşturalım. init metodu ile parametreleri tanımlıyoruz. Kapsülleme için get_description() 
# ve get_cost() yöntemlerini tanımlıyoruz.
class Pizza:
    def __init__(self, description, cost):
        self.description = description
        self.cost = cost

    def get_description(self):
        return self.description

    def get_cost(self):
        return self.cost

# Pizza alt sınıfını oluşturuyoruz.
class KlasikPizza(Pizza): 
    def __init__(self):
        super().__init__("Klasik Pizza", 30.00)

class MargaritaPizza(Pizza): 
    def __init__(self):
        super().__init__("Margarita Pizza", 28.50)
        
class TurkPizza(Pizza): 
    def __init__(self):
        super().__init__("Türk Pizza", 50.00)

class SadePizza(Pizza): 
    def __init__(self):
        super().__init__("Sade Pizza", 20.00)

# Decorator süper sınıfını oluşturuyoruz.
class Decorator(Pizza):
  def __init__(self, component, description, cost):
    self.component = component
    self.description  = description
    self.cost = cost

  def get_description(self):
    return self.component.get_description() + " " + Pizza.get_description(self)

  def get_cost(self):
    return self.component.get_cost() + Pizza.get_cost(self)

# Decoratorların alt sınıfını oluşturuyoruz.
class Zeytin(Decorator):
  def __init__(self, component):
    super().__init__(component, "Zeytin", 4.00)

class Mantar(Decorator):
  def __init__(self, component):
    super().__init__(component, "Mantar", 10.00)

class KeciPeyniri(Decorator):
  def __init__(self, component):
    super().__init__(component, "Keçi Peyniri", 12.00)

class Et(Decorator):
  def __init__(self, component):
    super().__init__(component, "Et", 15.00)

class Sogan(Decorator):
  def __init__(self, component):
    super().__init__(component, "Soğan", 5.00) 

class Misir(Decorator):
  def __init__(self, component):
    super().__init__(component, "Mısır", 6.00) 

class main(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.siparisTasarim = Ui_MainWindow()
        self.siparisTasarim.setupUi(self)
        self.siparisTasarim.btnOnayla.clicked.connect(self.siparisOnayla)
    
    def siparisOnayla(self):        
        pizza = 0
        pizza_choice = self.siparisTasarim.pizzaBox.currentIndex()
        if pizza_choice == 1:
            pizza = KlasikPizza()
        elif pizza_choice == 2:
            pizza = MargaritaPizza()
        elif pizza_choice == 3:
            pizza = TurkPizza()
        elif pizza_choice == 4:
            pizza = SadePizza()
        else:
            print("Lütfen geçerli bir seçim yapınız.")
            return

        sauce = 0
        sauce_choice = self.siparisTasarim.sosBox.currentIndex()
        if sauce_choice == 1:
            sauce = Zeytin(pizza)
        elif sauce_choice == 2:
            sauce = Mantar(pizza)
        elif sauce_choice == 3:
            sauce = KeciPeyniri(pizza)
        elif sauce_choice == 4:
            sauce = Et(pizza)
        elif sauce_choice == 5:
            sauce = Sogan(pizza)
        elif sauce_choice == 6:
            sauce = Misir(pizza)
        else:
            print("Lütfen geçerli bir seçim yapınız.")
            return

        toplam_tutar = sauce.get_cost()

        isim = self.siparisTasarim.lblAd.text()
        tc = self.siparisTasarim.lblTc.text()
        kart_no = self.siparisTasarim.lblKartNo.text()
        kart_sifre = self.siparisTasarim.lblKartSifre.text()

        print("isim: ", isim)
        print("tc: ", tc)
        print("no: ", kart_no)
        print("sifre: ", kart_sifre)


        # Dosya daha önce varsa "a" (append) modunda açılır, böylece mevcut veriler korunur ve yeni satır eklenir. 
        with open ("Orders_Database.csv", "a", newline='') as database:
                rows = ["İsmi", "TC" , "Kart Numarası", "Pizza Adı", "Toplam Tutar", "Sipariş Tarihi", "Kart Şifresi"]
                writer = csv.writer(database)
                writer.writerow(rows)
                writer.writerow([isim, tc, kart_no, sauce.get_description(), toplam_tutar , datetime.datetime.now(), kart_sifre])

        QMessageBox.about(self, "Siparişiniz Alındı", "Sipariş Detayları:\nAd: " + isim + "\nTC Kimlik Numarası: "+ tc + "\nKredi Kartı Numarası: "+ kart_no + "\nToplam tutar: " + str(toplam_tutar) + " TL.")


app = QApplication([])
pencere = main()
pencere.show()
app.exec_()