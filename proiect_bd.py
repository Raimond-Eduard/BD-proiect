import tkinter as tk
from tkinter import messagebox
from tkcalendar import Calendar
import cx_Oracle
import datetime
import re


class Deschidere(tk.Tk):
    def __init__(self, user, passwd, dsn):
        super().__init__()
        self.username = user
        self.password = passwd
        self.dsn = dsn
        self.connection = cx_Oracle.connect(self.username, self.password, self.dsn)
        self.title("Aplicatie hoteliera")
        self.geometry("800x600")
        self.create_widets()

    def create_widets(self):
        self.ghostLabel = tk.Label(self, text="\t")
        self.ghostLabel.grid(row=0, column=0)
        # Afisarea tabelelor
        self.labelAfisare = tk.Label(self, text="Afisare")
        self.labelAfisare.grid(row=0, column=1)

        self.afisareClientiButton = tk.Button(self, text="Clienti", command=self.afisare_clienti)
        self.afisareClientiButton.grid(row=1, column=1)

        self.afisareCamereButton = tk.Button(self, text="Camere", command=self.afisare_camere)
        self.afisareCamereButton.grid(row=2, column=1)

        self.detaliiCameraButton = tk.Button(self, text="Detalii camera", command=self.detalii_camera)
        self.detaliiCameraButton.grid(row=3, column=1)

        self.afisareRezervariButton = tk.Button(self, text="Rezervari", command=self.afisare_rezervare)
        self.afisareRezervariButton.grid(row=4, column=1)

        # Adaugarea in tabele
        self.ghostLabel1 = tk.Label(self, text="\t")
        self.ghostLabel1.grid(row=0, column=2)

        self.labelAdaugare = tk.Label(self, text="Adaugare")
        self.labelAdaugare.grid(row=0, column=3)

        self.adaugareClientiButton = tk.Button(self, text="Clienti", command=self.add_client)
        self.adaugareClientiButton.grid(row=1, column=3)

        self.adaugareCamereButton = tk.Button(self, text="Camere", command=self.add_camera)
        self.adaugareCamereButton.grid(row=2, column=3)

        self.adaugareRezervariButton = tk.Button(self, text="Rezervervari", command=self.add_rezervare)
        self.adaugareRezervariButton.grid(row=3, column=3)

        # Modificare
        self.ghostLabel2 = tk.Label(self, text="\t")
        self.ghostLabel2.grid(row=0, column=4)

        self.modificareLabel = tk.Label(self, text="Modificare")
        self.modificareLabel.grid(row=0, column=5)

        self.modificareClientiButton = tk.Button(self, text="Clienti", command=self.modificare_clienti)
        self.modificareClientiButton.grid(row=1, column=5)

        self.modificareCameraButton = tk.Button(self, text="Camera", command=self.modificare_camera)
        self.modificareCameraButton.grid(row=2, column=5)

        self.modificareRezervariButton = tk.Button(self, text="Rezervervari", command=self.modificare_rezervari)
        self.modificareRezervariButton.grid(row=3, column=5)

        # Stergere inregistrari
        self.ghostLabel3 = tk.Label(self, text="\t")
        self.ghostLabel3.grid(row=0, column=6)

        self.stergereInregistrare = tk.Button(self, text="Stergere", command=self.sterge)
        self.stergereInregistrare.grid(row=2, column=7)

        self.ghostLabel4 = tk.Label(self, text="\n \n")
        self.ghostLabel4.grid(row=4, column=0)

        self.labelDeAfisare = tk.Label(self, text="")
        self.labelDeAfisare.grid(row=5, column=0, columnspan=7, sticky="ew")

    def modificare_rezervari(self):
        modificareRezervare = tk.Toplevel(self)
        modificareRezervare.title("Modificare rezervare")

        idRezervareLabel = tk.Label(modificareRezervare, text="Introduceti ID-ul rezervarii pentru a o cauta:")
        idRezervareLabel.pack()

        idRezervareEntry = tk.Entry(modificareRezervare)
        idRezervareEntry.pack()

        def cautare():
            update = tk.Toplevel(modificareRezervare)
            update.title("Modificare Rezervare")
            cursor = self.connection.cursor()
            cursor.execute("SELECT ID_REZERVARE FROM REZERVARE")
            rezervare = cursor.fetchall()
            cursor.close()
            id = idRezervareEntry.get()
            validare = any(int(id) == int(tuplu[0]) for tuplu in rezervare)
            if not validare:
                messagebox.showwarning("Atentie", "Nu exista rezervarea cu ID-ul funrizat")
                return None

            cursor = self.connection.cursor()
            cursor.execute(
                "SELECT ID_CLIENT, ID_CAMERA, DATA_REZERVARE, DATA_ELEIBERARE FROM REZERVARE WHERE ID_REZERVARE = \'{}\'"
                .format(id))
            intrariOFF = cursor.fetchall()
            cursor.close()
            intrari = intrariOFF[0]

            idClientLabel = tk.Label(update, text="Id Client: ")
            idClientLabel.pack()

            str_IdClient = tk.StringVar()
            str_IdClient.set(intrari[0])
            idClientEntry = tk.Entry(update, textvariable=str_IdClient)
            idClientEntry.pack()

            idCameraLabel = tk.Label(update, text="Id Camera: ")
            idCameraLabel.pack()

            str_IdCamera = tk.StringVar()
            str_IdCamera.set(intrari[1])
            idCameraEntry = tk.Entry(update, textvariable=str_IdCamera)
            idCameraEntry.pack()

            data1Label = tk.Label(update, text="Data Check-in: ")
            data1Label.pack()

            checkin = intrari[2]
            an = int(checkin.year)
            luna = int(checkin.month)
            ziua = int(checkin.day)
            dataInput = Calendar(update, selectmode='day',
                                 year=an, month=luna,
                                 day=ziua)
            dataInput.pack()

            data2Label = tk.Label(update, text="Data Check-out: ")
            data2Label.pack()

            checkout = intrari[3]
            an1 = int(checkout.year)
            luna1 = int(checkout.month)
            ziua1 = int(checkout.day)
            data2Input = Calendar(update, selectmode='day',
                                  year=an1, month=luna1,
                                  day=ziua1)
            data2Input.pack()

            def salvare():
                str_checkIn = dataInput.get_date()
                checkIn = datetime.datetime.strptime(str_checkIn, "%m/%d/%y").date()
                str_checkOut = data2Input.get_date()
                checkOut = datetime.datetime.strptime(str_checkOut, "%m/%d/%y").date()
                idClient = idClientEntry.get()

                if checkIn <= datetime.date.today():
                    messagebox.showwarning("Atentie", "Nu puteti faceti rezervari in trecut")
                    return None

                if checkOut <= checkIn:
                    messagebox.showwarning("Atentie",
                                           "Nu puteti face checkout inainte de checkin\nNici nu puteti face rezervari mai scurte de o zi")
                    return None

                zile = checkOut - checkIn
                zile = int(zile.days)
                checkInA = datetime.datetime(checkIn.year,checkIn.month, checkIn.day)
                checkOutA = datetime.datetime(checkOut.year, checkOut.month, checkOut.day)

                cursor = self.connection.cursor()
                cursor.execute('SELECT ID_CAMERA FROM CAMERA')
                result = cursor.fetchall()
                cursor.close()
                idCamera = idCameraEntry.get()
                cameraValida = any(int(idCamera) == tuplu[0] for tuplu in result)

                if not cameraValida:
                    messagebox.showwarning("Atentionare", "Camera cu ID-ul specificat nu exista")
                    return None

                cursor = self.connection.cursor()
                cursor.execute("SELECT ID_CLIENT FROM CLIENTI")
                result = cursor.fetchall()
                cursor.close()
                exista_client = any(int(idClient) == tuplu[0] for tuplu in result)
                if not exista_client:
                    messagebox.showwarning("Atentie", "Clientul cu ID-ul specificat nu exista")
                    return None

                cursor = self.connection.cursor()
                cursor.execute("SELECT ID_CAMERA, DATA_REZERVARE, DATA_ELEIBERARE FROM REZERVARE WHERE ID_CAMERA= \'{}\'".format(idCamera))
                result = cursor.fetchall()
                cursor.close()

                for row in result:
                    if int(row[0]) == int(idCamera):
                        if row[1] <= checkInA <= row[2] :
                            messagebox.showwarning("Atentionare",
                                                   "Camera selectata este ocupata pe acea data, selectati alta data de check-in")
                            return None
                        if row[2] >= checkOutA >= row[1]:
                            messagebox.showwarning("Atentionare",
                                                   "Camera trebuie sa fie eliberata pana la data specificata deoarece exista alta rezervare in acea perioada")
                            return None

                cursor = self.connection.cursor()
                cursor.execute("SELECT ID_CAMERA, PRET_NOAPTE, CAPACITATE FROM DETALII_CAMERA")
                result = cursor.fetchall()
                cursor.close()
                pretFinal = 0
                for row in result:
                    if int(row[0]) == int(idCamera):
                        pretFinal = int(row[1]) * int(zile)

                cursor = self.connection.cursor()
                cursor.execute("SELECT * FROM REZERVARE WHERE ID_REZERVARE = \'{}\'".format(id))
                chestii = cursor.fetchall()
                verificari = chestii[0]
                cursor.close()
                if idClient != int(verificari[1]):
                    try:
                        cursor = self.connection.cursor()
                        print("Se ajunge la primul update")
                        cursor.execute("UPDATE REZERVARE SET ID_CLIENT = \'{}\' WHERE ID_REZERVARE = \'{}\'"
                                       .format(idClient, id))
                        print("Se termina primul update")
                        cursor.close()
                    except cx_Oracle.DatabaseError as exc:
                        error, = exc.args
                        print("Oracle-Error-Code: ", error.code)
                        print("Oracle-Error-Message: ", error.message)
                        messagebox.showerror(title="Eraore",message="Inregistrarea nu exista sau nu poate fi modificata")
                if idCamera != int(verificari[2]):
                    try:
                        cursor = self.connection.cursor()
                        cursor.execute("UPDATE REZERVARE SET ID_CAMERA = \'{}\' WHERE ID_REZERVARE = \'{}\'"
                                       .format(idCamera, id))
                        cursor.close()
                    except cx_Oracle.DatabaseError as exc:
                        error, = exc.args
                        print("Oracle-Error-Code: ", error.code)
                        print("Oracle-Error-Message: ", error.message)
                        messagebox.showerror(title="Eraore",
                                             message="Inregistrarea nu exista sau nu poate fi modificata")
                if zile != int(verificari[3]):
                    try:
                        cursor = self.connection.cursor()
                        cursor.execute("UPDATE REZERVARE SET NUMAR_NOPTI = \'{}\' WHERE ID_REZERVARE = \'{}\'"
                                       .format(zile, id))
                        cursor.close()
                    except cx_Oracle.DatabaseError as exc:
                        error, = exc.args
                        print("Oracle-Error-Code: ", error.code)
                        print("Oracle-Error-Message: ", error.message)
                        messagebox.showerror(title="Eraore",
                                             message="Inregistrarea nu exista sau nu poate fi modificata")
                if pretFinal != int(verificari[4]):
                    try:
                        cursor = self.connection.cursor()
                        cursor.execute("UPDATE REZERVARE SET TOTAL_PLATA = \'{}\' WHERE ID_REZERVARE = \'{}\'"
                                       .format(pretFinal, id))
                        cursor.close()
                    except cx_Oracle.DatabaseError as exc:
                        error, = exc.args
                        print("Oracle-Error-Code: ", error.code)
                        print("Oracle-Error-Message: ", error.message)
                        messagebox.showerror(title="Eraore",
                                             message="Inregistrarea nu exista sau nu poate fi modificata")
                cursor = self.connection.cursor()
                cursor.execute(
                    "SELECT ID_CAMERA, DATA_REZERVARE, DATA_ELEIBERARE FROM REZERVARE WHERE ID_CAMERA= \'{}\' AND ID_CLIENT != \'{}\'".format(
                        idCamera, idClient))
                result = cursor.fetchall()

                cursor.close()


                if checkInA != verificari[5].date():
                    try:
                        cursor = self.connection.cursor()
                        cursor.execute("UPDATE REZERVARE SET DATA_REZERVARE = TO_DATE(\'{}\', \'YYYY-MM-DD\') WHERE ID_REZERVARE = \'{}\'"
                                       .format(checkIn, id))
                        cursor.close()
                    except cx_Oracle.DatabaseError as exc:
                        error, = exc.args
                        print("Oracle-Error-Code: ", error.code)
                        print("Oracle-Error-Message: ", error.message)
                        messagebox.showerror(title="Eraore",
                                             message="Inregistrarea nu exista sau nu poate fi modificata")
                if checkOutA != verificari[6].date():
                    try:
                        cursor = self.connection.cursor()
                        cursor.execute("UPDATE REZERVARE SET DATA_ELEIBERARE = TO_DATE(\'{}\', \'YYYY-MM-DD\') WHERE ID_REZERVARE = \'{}\'"
                                       .format(checkOut, id))
                        cursor.execute("commit")
                    except cx_Oracle.DatabaseError as exc:
                        error, = exc.args
                        print("Oracle-Error-Code: ", error.code)
                        print("Oracle-Error-Message: ", error.message)
                        messagebox.showerror(title="Eraore",
                                             message="Inregistrarea nu exista sau nu poate fi modificata")
                #messagebox.showinfo("Gata", "Modificarea s-a incheiat cu succes")



                update.destroy()

            buton = tk.Button(update, text="Salveaza", command=salvare)
            buton.pack()

        cautareInregistrare = tk.Button(modificareRezervare, text="Cauta", command=cautare)
        cautareInregistrare.pack()

    def modificare_camera(self):
        modificareCamera = tk.Toplevel(self)
        modificareCamera.title("Modificare camera")

        label = tk.Label(modificareCamera, text="Introduceti ID-ul camerei")
        label.pack()

        entry = tk.Entry(modificareCamera)
        entry.pack()

        def scriere():
            idCamera = entry.get()
            if not idCamera or not idCamera.isdigit():
                messagebox.showerror("Eroare", "Parametru numar camera invalid")
                return None
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM DETALII_CAMERA WHERE ID_CAMERA = :numar", {'numar': idCamera})
            intrareMare = cursor.fetchall()
            intrare = intrareMare[0]
            cursor.close()
            if not intrare:
                messagebox.showerror("Eroare", "Nu exista camera cu ID-ul acesta")
                return None
            modificare = tk.Toplevel(modificareCamera)
            modificare.title("Modificare Camera")
            pretCameraLabel = tk.Label(modificare, text="Pret/Noapte: ")
            pretCameraLabel.pack()

            str_pretCamera = tk.StringVar()
            str_pretCamera.set(intrare[1])
            pretCameraInput = tk.Entry(modificare, textvariable=str_pretCamera)
            pretCameraInput.pack()

            etajLabel = tk.Label(modificare, text="Etaj: ")
            etajLabel.pack()

            str_etaj = tk.StringVar()
            str_etaj.set(intrare[2])
            etajInput = tk.Entry(modificare, textvariable=str_etaj)
            etajInput.pack()

            options = ["Deluxe", "Apartament", "Executiv", "Standard"]
            displayed = tk.StringVar()
            displayed.set(intrare[3])
            tipCameraInput = tk.OptionMenu(modificare, displayed, *options)
            tipCameraInput.pack()

            capacitateLabel = tk.Label(modificare, text="Capacitate")
            capacitateLabel.pack()

            options1 = ["1", "2", "3", "4"]
            displayed2 = tk.StringVar()
            displayed2.set(intrare[4])
            dropdown2 = tk.OptionMenu(modificare, displayed2, *options1)
            dropdown2.pack()

            vedereLabel = tk.Label(modificare, text="Vedere la mare")
            vedereLabel.pack()

            vedere = tk.IntVar()
            vedere.set(0)
            if intrare[5] == "DA":
                vedere.set(1)
            vedereButton = tk.Checkbutton(modificare, variable=vedere, onvalue=1, offvalue=0)
            vedereButton.pack()

            balconOpt = ["PROPRIU", "COMUN"]
            balconDisp = tk.StringVar()
            balconDisp.set(intrare[6])
            balcon = tk.OptionMenu(modificare, balconDisp, *balconOpt)
            balcon.pack()

            def salvare():
                pretCamera = pretCameraInput.get()
                etaj = etajInput.get()
                tipCamera = displayed.get()
                capacitate = displayed2.get()
                vedereLaMare = "NU"
                if vedere == 1:
                    vedereLaMare = "DA"

                balconTip = balconDisp.get()

                cursor = self.connection.cursor()
                try:
                    cursor.execute("UPDATE DETALII_CAMERA SET PRET_NOAPTE = \'{}\',"
                                   "ETAJ = \'{}\', TIP_CAMERA = \'{}\',"
                                   "CAPACITATE = \'{}\', VEDERE_LA_MARE = \'{}\',"
                                   "BALCON = \'{}\' WHERE ID_CAMERA = \'{}\'"
                                   .format(pretCamera, etaj, tipCamera,
                                           capacitate, vedereLaMare, balconTip, idCamera))
                    cursor.execute("commit")
                    messagebox.showinfo("Succes", "Ai modificat camera cu succes")
                except cx_Oracle.DatabaseError as exc:
                    error, = exc.args
                    print("Oracle-Error-Code: ", error.code)
                    print("Oracle-Error-Message: ", error.message)
                    messagebox.showerror(title="Eraore", message="Inregistrarea nu exista sau nu poate fi modificata")

                cursor.close()

                modificare.destroy()

            salvareButton = tk.Button(modificare, text="Salvare modificari", command=salvare)
            salvareButton.pack()

        buton = tk.Button(modificareCamera, text="Cauta", command=scriere)
        buton.pack()

    def modificare_clienti(self):
        modificareClienti = tk.Toplevel(self)
        modificareClienti.title("Modificare clienti")

        label = tk.Label(modificareClienti, text="Introduceti numele clientului: ")
        label.pack()

        entry = tk.Entry(modificareClienti)
        entry.pack()

        def scriere_clienti():
            nume = entry.get()
            if not nume:
                messagebox.showwarning("Atentie", "Nu ati introdus niciun nume")
                return None
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM CLIENTI WHERE NUME = :nume", {'nume': nume})
            intrareMare = cursor.fetchall()
            intrare = intrareMare[0]
            cursor.close()
            if not intrare:
                messagebox.showerror("Eroare", "Nu exista inregistrari sub acest nume")
                return None

            modificare = tk.Toplevel(modificareClienti)
            modificare.title("Modificare clienti")
            numeLabel = tk.Label(modificare, text="Nume: ")
            numeLabel.grid(row=0, column=0)

            str_numeEntry = tk.StringVar()
            str_numeEntry.set(intrare[1])
            numeEntry = tk.Entry(modificare, textvariable=str_numeEntry)
            numeEntry.grid(row=0, column=1)

            prenumeLabel = tk.Label(modificare, text="Prenume: ")
            prenumeLabel.grid(row=1, column=0)

            str_prenumeEntry = tk.StringVar()
            str_prenumeEntry.set(intrare[2])
            prenumeEntry = tk.Entry(modificare, textvariable=str_prenumeEntry)
            prenumeEntry.grid(row=1, column=1)

            telefonLabel = tk.Label(modificare, text="Telefon")
            telefonLabel.grid(row=2, column=0)

            str_telefonEntry = tk.StringVar()
            str_telefonEntry.set(intrare[3])
            telefonEntry = tk.Entry(modificare, textvariable=str_telefonEntry)
            telefonEntry.grid(row=2, column=1)

            emailLabel = tk.Label(modificare, text="Email: ")
            emailLabel.grid(row=3, column=0)

            str_emailEntry = tk.StringVar()
            str_emailEntry.set(intrare[4])
            emailEntry = tk.Entry(modificare, textvariable=str_emailEntry, width=35)
            emailEntry.grid(row=3, column=1)

            varstaLabel = tk.Label(modificare, text="Varsta: ")
            varstaLabel.grid(row=4, column=0)

            str_varstaEntry = tk.StringVar()
            str_varstaEntry.set(intrare[5])
            varstaEntry = tk.Entry(modificare, textvariable=str_varstaEntry)
            varstaEntry.grid(row=4, column=1)

            def salvare_modificare():
                idNou = intrare[0]
                if numeEntry.get():
                    numeNou = numeEntry.get()
                else:
                    numeNou = intrare[1]
                if prenumeEntry.get():
                    prenumeNou = prenumeEntry.get()
                else:
                    prenumeNou = intrare[2]
                cursor = self.connection.cursor()
                cursor.execute("SELECT TELEFON FROM CLIENTI")
                rows = cursor.fetchall()
                for row in rows:
                    if telefonEntry.get() == row[0]:
                        messagebox.showerror("Eroare", "Numarul de telefon introdus este deja folosit")
                        return None
                if telefonEntry.get():
                    telefonNou = telefonEntry.get()
                else:
                    telefonNou = intrare[3]
                pattern = r'^\w+@\w+\.\w+$'
                match = re.match(pattern, emailEntry.get())
                if not bool(match):
                    messagebox.showerror("Eroare", "Adresa de email invalida")
                    return None
                if emailEntry.get():
                    emailNou = emailEntry.get()
                else:
                    emailNou = str(intrare[4])
                if int(varstaEntry.get()) < 18:
                    messagebox.showerror("Eroare", "Varsta minima trebuie sa fie 18")
                    return None
                if not varstaEntry.get().isdigit():
                    messagebox.showwarning("Atentie", "Va rog incercati doar numere")
                    return None
                if varstaEntry.get():
                    varstaNou = varstaEntry.get()
                else:
                    varstaNou = intrare[5]
                try:
                    cursor = self.connection.cursor()
                    cursor.execute(
                        "UPDATE CLIENTI SET NUME = \'{}\', PRENUME = \'{}\', TELEFON = \'{}\', EMAIL = \'{}\', VARSTA = \'{}\' WHERE ID_CLIENT = {}"
                        .format(numeNou, prenumeNou, telefonNou, emailNou, varstaNou, idNou))
                    cursor.execute("commit")
                    cursor.close()
                except cx_Oracle.DatabaseError as exc:
                    error, = exc.args
                    print("Oracle-Error-Code: ", error.code)
                    print("Oracle-Error-Message: ", error.message)
                    messagebox.showerror(title="Eraore", message="Inregistrarea nu exista sau nu poate fi modificata")
                modificareClienti.destroy()

            modifica = tk.Button(modificare, text="Salvare modificare", command=salvare_modificare)
            modifica.grid(row=5, column=1)

        button = tk.Button(modificareClienti, text="Cauta", command=scriere_clienti)
        button.pack()

    def afisare_rezervare(self):
        cursor = self.connection.cursor()

        cursor.execute('SELECT * FROM REZERVARE')
        rows = cursor.fetchall()
        cursor.close()

        printRecords = "ID REZERVARE || ID CLIENT || ID CAMERA || NUMAR NOPTI || TOTAL DE PLATA || DATA CHECK-IN || DATA CHECK-OUT\n\n"
        for row in rows:
            for item in row:
                if isinstance(item, datetime.datetime):
                    item = item.strftime("%d-%m-%Y")
                printRecords += str(item) + "\t||\t"
            printRecords += '\n'

        self.labelDeAfisare.config(text=printRecords)

    def afisare_clienti(self):
        cursor = self.connection.cursor()

        cursor.execute('SELECT * FROM CLIENTI')
        rows = cursor.fetchall()
        cursor.close()
        printRecords = "ID\t NUME\t PRENUME\t TELEFON\t EMAIL\t VARSTA\n\n"
        for row in rows:
            for item in row:
                printRecords += str(item) + " || "
            printRecords += "\n\n"

        self.labelDeAfisare.config(text=printRecords)



    def afisare_camere(self):
        cursor = self.connection.cursor()

        cursor.execute('SELECT * FROM CAMERA')
        rows = cursor.fetchall()
        printRecords = "ID\t NUMAR CAMERA\n\n"
        for row in rows:
            for item in row:
                printRecords += str(item) + " \t||\t "
            printRecords += '\n'

        self.labelDeAfisare.config(text=printRecords)

        cursor.close()

    def detalii_camera(self):
        cursor = self.connection.cursor()

        cursor.execute('SELECT * FROM DETALII_CAMERA')
        rows = cursor.fetchall()
        printRecords = "ID CAMERA || PRET/NOAPTE || ETAJ || TIP CAMERA || CAPACITATE PERSOANE || VEDERE LA MARE || TIP BALCON ||\n\n"
        for row in rows:
            for item in row:
                printRecords += str(item) + " || "
            printRecords += '\n'

        self.labelDeAfisare.config(text=printRecords)

        cursor.close()

    def sterge(self):
        stergereInregistrare = tk.Toplevel(self)
        stergereInregistrare.title("Stergere")

        tabelaInregistrare = tk.Label(stergereInregistrare, text="Din ce tabela: ")
        tabelaInregistrare.grid(row=0, column=0)

        optiuni = ["CAMERA", "CLIENTI", "REZERVARE"]
        optiuneCurenta = tk.StringVar()
        optiuneCurenta.set("CAMERA")
        inregistrare = tk.OptionMenu(stergereInregistrare, optiuneCurenta, *optiuni)
        inregistrare.grid(row=0, column=1)

        idLabel = tk.Label(stergereInregistrare, text="ID inregistrare (Numar): ")
        idLabel.grid(row=1, column=0)

        idInput = tk.Entry(stergereInregistrare)
        idInput.grid(row=1, column=1)

        def delete_row():
            id = idInput.get()
            if not id:
                messagebox.showwarning("Eroare", "Id-ul nu poate fi null")
                return None
            if optiuneCurenta.get() == "CAMERA":
                try:
                    cursor = self.connection.cursor()
                    cursor.execute("DELETE FROM CAMERA WHERE ID_CAMERA = {}".format(id))
                    cursor.execute("commit")
                    cursor.close()

                    cursor = self.connection.cursor()
                    cursor.execute("DELETE FROM DETALII_CAMERA WHERE ID_CAMERA = {}".format(id))
                    cursor.execute("commit")
                    cursor.close()
                except cx_Oracle.DatabaseError as exc:
                    error, = exc.args
                    print("Oracle-Error-Code: ", error.code)
                    print("Oracle-Error-Message: ", error.message)
                    messagebox.showerror(title="Eraore", message="Nu exista inregistrarea")

            elif optiuneCurenta.get() == "CLIENTI":
                try:
                    cursor = self.connection.cursor()
                    cursor.execute("DELETE FROM CLIENTI WHERE ID_CLIENT = {}".format(id))
                    cursor.execute("commit")
                    cursor.close()

                except cx_Oracle.DatabaseError as exc:
                    error, = exc.args
                    print("Oracle-Error-Code: ", error.code)
                    print("Oracle-Error-Message: ", error.message)
                    messagebox.showerror(title="Eraore", message="Nu exista inregistrarea")

            elif optiuneCurenta.get() == "REZERVARE":
                try:
                    cursor = self.connection.cursor()
                    cursor.execute("DELETE FROM REZERVARE WHERE ID_REZERVARE = {}".format(id))
                    cursor.execute("commit")
                    cursor.close()

                except cx_Oracle.DatabaseError as exc:
                    error, = exc.args
                    print("Oracle-Error-Code: ", error.code)
                    print("Oracle-Error-Message: ", error.message)
                    messagebox.showerror(title="Eraore", message="Nu exista inregistrarea")
            messagebox.showinfo(title="Succes!", message="Inregistrare stearsa cu succes!")

        finish = tk.Button(stergereInregistrare, text="Sterge", command=delete_row)
        finish.grid(row=2, column=1)

    # Functie de adaugare client
    def add_client(self):
        addClient = tk.Toplevel(self)
        addClient.title("Adaugare client")

        numeLabel = tk.Label(addClient, text="Nume: ")
        numeLabel.grid(row=0, column=2)

        numeInput = tk.Entry(addClient)
        numeInput.grid(row=0, column=3)

        prenumeLabel = tk.Label(addClient, text="Prenume: ")
        prenumeLabel.grid(row=0, column=4)

        prenumeInput = tk.Entry(addClient)
        prenumeInput.grid(row=0, column=5)

        telefonLabel = tk.Label(addClient, text="Telefon (Numar): ")
        telefonLabel.grid(row=0, column=6)

        telefonInput = tk.Entry(addClient)
        telefonInput.grid(row=0, column=7)

        emailLabel = tk.Label(addClient, text="Email: ")
        emailLabel.grid(row=0, column=8)

        emailInput = tk.Entry(addClient)
        emailInput.grid(row=0, column=9)

        varstaLabel = tk.Label(addClient, text="Varsta: ")
        varstaLabel.grid(row=0, column=10)

        varstaInput = tk.Entry(addClient)
        varstaInput.grid(row=0, column=11)

        def realizeaza_adaugare():
            nume = numeInput.get()
            prenume = prenumeInput.get()
            telefon = telefonInput.get()
            cursor = self.connection.cursor()
            cursor.execute("SELECT TELEFON FROM CLIENTI")
            rows = cursor.fetchall()
            cursor.close()
            for row in rows:
                if row[0] == telefon:
                    messagebox.showerror("Eroare", "Numarul de telefon introdus exista deja")
                    return None
            email = emailInput.get()
            pattern = r'^\w+@\w+\.\w+$'
            match = re.match(pattern, email)
            if not bool(match):
                messagebox.showerror("Eroare", "Adresa de email invalida")
                return None
            varsta = varstaInput.get()
            if int(varsta) < 18:
                messagebox.showerror("Eroare", "Varsta minima trebuie sa fie 18")
                return None
            if not varsta.isdigit():
                messagebox.showwarning("Atentie", "Va rog incercati doar numere")
                return None
            cursor = self.connection.cursor()
            cursor.execute("SELECT MAX(ID_CLIENT) FROM CLIENTI")
            max_id = 0
            for result in cursor:
                max_id = result[0]
            max_id += 1
            cursor.close()
            cursor = self.connection.cursor()
            cursor.execute(
                "INSERT INTO CLIENTI VALUES (\'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\')"
                .format(max_id, nume, prenume, telefon, email, varsta)
            )
            cursor.execute("commit")
            cursor.close()
            addClient.destroy()

        submit = tk.Button(addClient, text="Adauga", command=realizeaza_adaugare)
        submit.grid(row=1, column=5)

    def add_camera(self):
        addCamera = tk.Toplevel(self)
        addCamera.title("Adaugare camera")

        nrCameraLabel = tk.Label(addCamera, text="Numarul camerei (Numar): ")
        nrCameraLabel.grid(row=1, column=0)

        nrCameraInput = tk.Entry(addCamera)
        nrCameraInput.grid(row=1, column=1)

        pretCameraLabel = tk.Label(addCamera, text="Pret per noapte (Numar): ")
        pretCameraLabel.grid(row=2, column=0)

        pretCameraInput = tk.Entry(addCamera)
        pretCameraInput.grid(row=2, column=1)

        etajLabel = tk.Label(addCamera, text="Etajul (Numar): ")
        etajLabel.grid(row=3, column=0)

        etajInput = tk.Entry(addCamera)
        etajInput.grid(row=3, column=1)

        tip_cameraLabel = tk.Label(addCamera, text="Tipul Camerei: ")
        tip_cameraLabel.grid(row=4, column=0)

        options = ["Deluxe", "Apartament", "Executiv", "Standard"]
        displayed = tk.StringVar()
        displayed.set("Deluxe")
        tipCameraInput = tk.OptionMenu(addCamera, displayed, *options)
        tipCameraInput.grid(row=4, column=1)

        capacitateLabel = tk.Label(addCamera, text="Capacitate: ")
        capacitateLabel.grid(row=5, column=0)

        options1 = ["1", "2", "3", "4"]
        displayed2 = tk.StringVar()
        displayed2.set("1")
        dropdown2 = tk.OptionMenu(addCamera, displayed2, *options1)
        dropdown2.grid(row=5, column=1)

        vedereLabel = tk.Label(addCamera, text="Vedere la mare? ")
        vedereLabel.grid(row=6, column=0)

        vedere = tk.IntVar()
        vedereButton = tk.Checkbutton(addCamera, variable=vedere, onvalue=1, offvalue=0)
        vedereButton.grid(row=6, column=1)

        balconLabel = tk.Label(addCamera, text="Tip balcon: ")
        balconLabel.grid(row=7, column=0)

        balconOpt = ["PROPRIU", "COMUN"]
        balconDisp = tk.StringVar()
        balconDisp.set("PROPRIU")
        balcon = tk.OptionMenu(addCamera, balconDisp, *balconOpt)
        balcon.grid(row=7, column=1)

        def salvare():
            numarCamera = nrCameraInput.get()
            cursor = self.connection.cursor()
            cursor.execute("SELECT NUMAR_CAMERA FROM CAMERA")
            rows = cursor.fetchall()
            cursor.close()
            for row in rows:
                if row[0] == numarCamera:
                    messagebox.showerror("Eroare", "Camera deja exista")
                    return None
            pretCamera = pretCameraInput.get()
            etaj = etajInput.get()
            tipCamera = displayed.get()
            capacitate = displayed2.get()
            vedereLaMare = "NU"
            if vedere == 1:
                vedereLaMare = "DA"

            balconTip = balconDisp.get()
            max_id = 0
            cursor = self.connection.cursor()
            cursor.execute("SELECT MAX(ID_CAMERA) FROM CAMERA")

            for result in cursor:
                max_id = result[0]
            max_id += 1
            cursor.close()

            cursor = self.connection.cursor()
            cursor.execute("INSERT INTO CAMERA VALUES(\'{}\', \'{}\')".format(max_id, numarCamera))
            cursor.execute("commit")
            cursor.close()

            cursor = self.connection.cursor()
            cursor.execute("INSERT INTO DETALII_CAMERA VALUES(\'{}\', \'{}\',\'{}\', \'{}\', \'{}\', \'{}\', \'{}\')"
                           .format(max_id, pretCamera, etaj, tipCamera, capacitate, vedereLaMare, balconTip))

            cursor.execute("commit")
            cursor.close()
            addCamera.destroy()

        submit = tk.Button(addCamera, text="Adauga", command=salvare)
        submit.grid(row=8, column=1)

    def add_rezervare(self):
        addRezervare = tk.Toplevel(self)
        addRezervare.title("Adaugare rezervare")

        idClientLabel = tk.Label(addRezervare, text="ID client (Nuamr): ")
        idClientLabel.grid(row=1, column=0)

        idClientInput = tk.Entry(addRezervare)
        idClientInput.grid(row=1, column=1)

        idCameraLabel = tk.Label(addRezervare, text="ID Camera (Numar): ")
        idCameraLabel.grid(row=2, column=0)

        idCameraInput = tk.Entry(addRezervare)
        idCameraInput.grid(row=2, column=1)

        nrNoptiLabel = tk.Label(addRezervare, text="Numar de nopti rezervate (Numar): ")
        nrNoptiLabel.grid(row=3, column=0)

        nrNoptiInput = tk.Entry(addRezervare, state="disabled")
        nrNoptiInput.grid(row=3, column=1)

        plataLabel = tk.Label(addRezervare, text="Total de plata (Numar): ")
        plataLabel.grid(row=4, column=0)

        plataInput = tk.Entry(addRezervare)
        plataInput.config(state="disabled")
        plataInput.grid(row=4, column=1)

        dataLabel = tk.Label(addRezervare, text="Data check-in: ")
        dataLabel.grid(row=5, column=0)

        # dataInput = tk.Entry(addRezervare)
        dataInput = Calendar(addRezervare, selectmode='day',
                             year=2024, month=1,
                             day=1)
        dataInput.grid(row=5, column=1)

        data2Label = tk.Label(addRezervare, text="Data checkout: ")
        data2Label.grid(row=6, column=0)

        # data2Input = tk.Entry(addRezervare)
        data2Input = Calendar(addRezervare, selectmode='day',
                              year=2024, month=1,
                              day=8)
        data2Input.grid(row=6, column=1)

        def adaugare():
            str_checkIn = dataInput.get_date()
            checkIn = datetime.datetime.strptime(str_checkIn, "%m/%d/%y").date()

            str_checkOut = data2Input.get_date()
            checkOut = datetime.datetime.strptime(str_checkOut, "%m/%d/%y").date()
            idClient = idClientInput.get()

            if checkIn <= datetime.date.today():
                messagebox.showwarning("Atentie", "Nu puteti faceti rezervari in trecut")
                return None

            if checkOut <= checkIn:
                messagebox.showwarning("Atentie",
                                       "Nu puteti face checkout inainte de checkin\nNici nu puteti face rezervari mai scurte de o zi")
                return None

            zile = checkOut - checkIn
            zile = int(zile.days)
            cursor = self.connection.cursor()
            cursor.execute('SELECT ID_CAMERA FROM CAMERA')
            result = cursor.fetchall()
            cursor.close()
            idCamera = idCameraInput.get()
            cameraValida = any(int(idCamera) == tuplu[0] for tuplu in result)

            if not cameraValida:
                messagebox.showwarning("Atentionare", "Camera cu ID-ul specificat nu exista")
                return None

            cursor = self.connection.cursor()
            cursor.execute("SELECT ID_CLIENT FROM CLIENTI")
            result = cursor.fetchall()
            cursor.close()
            exista_client = any(int(idClient) == tuplu[0] for tuplu in result)
            if not exista_client:
                messagebox.showwarning("Atentie", "Clientul cu ID-ul specificat nu exista")
                return None

            cursor = self.connection.cursor()
            cursor.execute("SELECT ID_CAMERA, DATA_REZERVARE, DATA_ELEIBERARE FROM REZERVARE WHERE ID_CAMERA = \'{}\'".format(idCamera))
            result = cursor.fetchall()
            cursor.close()
            checkInA = datetime.datetime(checkIn.year, checkIn.month, checkIn.day)
            checkOutA = datetime.datetime(checkOut.year, checkOut.month, checkOut.day)

            for row in result:
                if row[1] <= checkInA <= row[2]:
                    messagebox.showwarning("Atentionare",
                                               "Camera selectata este ocupata pe acea data, selectati alta data de check-in")
                    return None
                if row[1] <= checkOutA <= row[2]:
                    messagebox.showwarning("Atentionare",
                                               "Camera trebuie sa fie eliberata pana la data specificata deoarece exista alta rezervare in acea perioada")
                    return None
            cursor = self.connection.cursor()
            cursor.execute("SELECT ID_CAMERA, PRET_NOAPTE, CAPACITATE FROM DETALII_CAMERA")
            result = cursor.fetchall()
            cursor.close()
            pretFinal = 0
            for row in result:
                if int(row[0]) == int(idCamera):
                    pretFinal = int(row[1]) * int(zile)
            max_id = 0
            cursor = self.connection.cursor()
            cursor.execute("SELECT MAX(ID_REZERVARE) FROM REZERVARE")

            for result in cursor:
                max_id = result[0]
            max_id += 1
            cursor.close()

            cursor = self.connection.cursor()
            cursor.execute("INSERT INTO REZERVARE VALUES("
                           "\'{}\',\'{}\', \'{}\',\'{}\', \'{}\',"
                           "TO_DATE(\'{}\', \'YYYY-MM-DD\'),"
                           "TO_DATE(\'{}\', \'YYYY-MM-DD\'))"
                           .format(max_id, idClient, idCamera, zile, pretFinal,
                                   checkIn, checkOut))
            cursor.execute("commit")
            cursor.close()
            messagebox.showwarning("Succes", f"Aveti rezervare pe {zile} zile.\nPretul total este {pretFinal}.")
            addRezervare.destroy()

        submit = tk.Button(addRezervare, text="Adaugare rezervare", command=adaugare)
        submit.grid(row=7, column=1)

    def __del__(self):
        self.connection.close()


if __name__ == "__main__":
    cx_Oracle.init_oracle_client(lib_dir="E:\Facultate\BD\instantclient_21_12")

    username = "bd014"
    password = "bd014"
    dsn = "bd-dc.cs.tuiasi.ro:1539/orcl"
    deschidere = Deschidere(username, password, dsn)
    deschidere.mainloop()
