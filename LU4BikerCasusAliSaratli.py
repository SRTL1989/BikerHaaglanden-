"""

LU4 Ontwerp van een desktopapplicatie
Student: A.Saratli
Studentnummer:25147897
Biker Haaglanden - Fietsverhuur applicatie


Doel van deze applicatie:
- Medewerker logt in.
- Medewerker vult klantgegevens, fietsen, accessoires en huurperiode in.
- Applicatie berekent prijs, borg en korting.
- Reservering wordt opgeslagen in een CSV-bestand.
- Reserveringen kunnen bekeken en geannuleerd worden.
-Versie 5
"""

import csv
from datetime import datetime, timedelta
from decimal import Decimal
import os
import re
import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import DateEntry


class LoginWindow:
    """Venster voor het inloggen van medewerkers."""

    def __init__(self, root):
        self.root = root
        self.root.title("Biker Haaglanden - Inloggen")
        self.root.geometry("450x350")
        self.root.resizable(False, False)

        # Huisstijl kleuren toepassen op de achtergrond van het venster
        self.root.configure(bg="#26384A")  # Donkerblauwe De Haagse hogeschool-achtergrond voor login #000000 (dient als test)

        # Centraal frame (White content surface)
        login_frame = tk.Frame(self.root, bg="#FFFFFF", padx=30, pady=30)
        login_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)  # type: ignore

        # Grote Typografie - Titel
        ttk.Label(login_frame, text="Medewerker Portaal", font=('Source Sans Pro', 22, 'bold'),
                  foreground='#26384A', background='#FFFFFF').pack(anchor=tk.W, pady=(0, 20))  # type: ignore

        # Invoervelden met strakke styling
        ttk.Label(login_frame, text="Gebruikersnaam", font=('Source Sans Pro', 11, 'bold'),
                  foreground='#26384A', background='#FFFFFF').pack(anchor=tk.W, pady=(5, 2))  # type: ignore
        self.username_var = tk.StringVar()
        self.username_entry = ttk.Entry(login_frame, textvariable=self.username_var, font=('Source Sans Pro', 12),
                                        width=30)
        self.username_entry.pack(fill=tk.X, pady=(0, 10))  # type: ignore
        self.username_entry.focus_set()

        ttk.Label(login_frame, text="Wachtwoord", font=('Source Sans Pro', 11, 'bold'), #test Verdana
                  foreground='#26384A', background='#FFFFFF').pack(anchor=tk.W, pady=(5, 2))  # type: ignore
        self.password_var = tk.StringVar()
        self.password_entry = ttk.Entry(login_frame, textvariable=self.password_var, show="*",
                                        font=('Source Sans Pro', 12), width=30)
        self.password_entry.pack(fill=tk.X, pady=(0, 20))  # type: ignore

        # De Haagse Hogeschool Grijze/Blauwe Button - relief="flat" lost de Literal warning op
        self.login_btn = tk.Button(login_frame, text="INLOGGEN", command=self.check_login,
                                   font=('Source Sans Pro', 12, 'bold'), bg='#5A7188', fg='#FFFFFF',
                                   activebackground='#26384A', activeforeground='#FFFFFF',
                                   relief="flat", bd=0, cursor='hand2', pady=8)
        self.login_btn.pack(fill=tk.X)  # type: ignore

        self.root.bind('<Return>', lambda event: self.check_login())

    def check_login(self):
        """Controleert of de inloggegevens juist zijn."""
        username = self.username_var.get().strip()
        password = self.password_var.get().strip()

        if username == "admin" and password == "biker2026":
            self.root.destroy()
            self.start_main_app()
        else:
            messagebox.showerror("Fout", "Onjuiste gebruikersnaam of wachtwoord!")
            self.password_entry.delete(0, tk.END)

    @staticmethod
    def start_main_app():
        """Start de hoofdapplicatie na succesvol inloggen."""
        main_root = tk.Tk()
        try:
            main_root.wm_iconbitmap('jouw_logo.ico')
        except (tk.TclError, IOError):
            pass
        BikerRentalApp(main_root)
        main_root.mainloop()


class BikerRentalApp:
    """De hoofdklasse voor het Fietsverhuur Systeem."""

    def __init__(self, root):
        self.root = root
        self.root.title("Biker Haaglanden - Fietsverhuur Systeem")
        self.root.geometry("1200x850")
        self.root.configure(bg="#F4F4F4")  # Lichtgrijze De Haagse Hogeschool Achtergrond

        # Initialiseer alle instance attributes vooraf om linter warnings te voorkomen
        self.naam_var = None
        self.naam_entry = None
        self.email_var = None
        self.email_entry = None
        self.aantal_stad_dames = None
        self.spin_stad_dames = None
        self.aantal_stad_heren = None
        self.spin_stad_heren = None
        self.aantal_elek_dames = None
        self.spin_elek_dames = None
        self.aantal_elek_heren = None
        self.spin_elek_heren = None
        self.helm_var = None
        self.kinderzitje_var = None
        self.start_datum = None
        self.eind_datum = None
        self.terugkerend_var = None
        self.betaalmethode_var = None
        self.btn_res = None
        self.btn_reset = None
        self.btn_list = None
        self.prijs_label = None
        self.prijs_details_label = None
        self.borg_label = None
        self.dagen_label = None

        self.prijzen = {
            'stadfiets': Decimal('15.00'), 'elektrisch': Decimal('25.00'),
            'helm': Decimal('3.00'), 'kinderzitje': Decimal('4.00')
        }
        self.borg = {'stadfiets': Decimal('50.00'), 'elektrisch': Decimal('100.00')}
        self.csv_bestand = 'verhuur_data.csv'
        self.init_csv()

        # Configureer Tkinter TTK Styles voor Haagse Hogeschool uitstraling
        self.setup_styles()
        self.create_widgets()

    @staticmethod
    def setup_styles():
        """Configureer fonts en stijlen gebaseerd op de HHS-ontwerpfilosofie."""
        style = ttk.Style()
        style.theme_use('clam')

        # Algemene fonts en achtergronden
        style.configure('.', font=('Source Sans Pro', 11), background='#F4F4F4', foreground='#26384A')

        # Formulier styling (Wit contentblok)
        style.configure('Content.TFrame', background='#FFFFFF')
        style.configure('THHSR.TLabel', background='#FFFFFF', foreground='#26384A')
        style.configure('THHSR_Sub.TLabel', background='#FFFFFF', foreground='#5A7188')
        style.configure('THHSR_Check.TCheckbutton', background='#FFFFFF', foreground='#26384A')
        style.configure('THHSR_Radio.TRadiobutton', background='#FFFFFF', foreground='#26384A')

        # Treeview (Reserveringen overzicht)
        style.configure('Treeview', font=('Source Sans Pro', 10), background='#FFFFFF', foreground='#26384A',
                        rowheight=25)
        style.configure('Treeview.Heading', font=('Source Sans Pro', 10, 'bold'), background='#26384A',
                        foreground='#FFFFFF')

    def init_csv(self):
        """Initialiseert het databasebestand als het nog niet bestaat."""
        if not os.path.exists(self.csv_bestand):
            try:
                with open(self.csv_bestand, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(
                        ['ReserveringsID', 'Datum', 'Naam', 'Email', 'StadDames', 'StadHeren', 'ElekDames', 'ElekHeren',
                         'Helm', 'Kinderzitje', 'Startdatum', 'Einddatum', 'Dagen', 'Terugkerend', 'Betaalmethode',
                         'Borg', 'Totaalprijs', 'BetalingStatus', 'Status'])
            except IOError as err:
                messagebox.showerror("Fout", f"Kan CSV niet initialiseren: {err}")
                self.root.destroy()

    def create_widgets(self):
        """Bouwt de interface-elementen op."""
        # Asymmetrische Hoofdcontainer: Veel witruimte en padding als integer (30)
        container = ttk.Frame(self.root, padding=30, style='TFrame')
        container.pack(fill=tk.BOTH, expand=True)  # type: ignore
        container.columnconfigure(0, weight=3)  # Linker kolom breder voor rustige layout
        container.columnconfigure(1, weight=1)  # Rechter kolom smaller (Asymmetrisch)

        # ================= LINKER KOLOM: HET WITTE CONTENTBLOK =================
        main_frame = ttk.Frame(container, style='Content.TFrame', padding=40)
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 20))  # type: ignore

        # Grote Typografie (Titel conform De Haagse Hogeschool stijl: 28px krachtig)
        title_label = ttk.Label(main_frame, text="Biker Haaglanden", font=('Source Sans Pro', 28, 'bold'),
                                style='THHSR.TLabel')
        title_label.pack(anchor=tk.W, pady=(0, 2))  # type: ignore

        subtitle_label = ttk.Label(main_frame, text="Fietsverhuur Den Haag",
                                   font=('Source Sans Pro', 12), style='THHSR_Sub.TLabel')
        subtitle_label.pack(anchor=tk.W, pady=(0, 30))  # type: ignore

        # --- Klantgegevens ---
        ttk.Label(main_frame, text="Klantgegevens", font=('Source Sans Pro', 16, 'bold'), style='THHSR.TLabel').pack(
            anchor=tk.W, pady=(10, 10))  # type: ignore

        row_klant = ttk.Frame(main_frame, style='Content.TFrame')
        row_klant.pack(fill=tk.X, pady=(0, 20))  # type: ignore

        ttk.Label(row_klant, text="Naam:", style='THHSR.TLabel').pack(side=tk.LEFT, padx=(0, 10))  # type: ignore
        self.naam_var = tk.StringVar()
        self.naam_entry = ttk.Entry(row_klant, textvariable=self.naam_var, font=('Source Sans Pro', 11), width=25)
        self.naam_entry.pack(side=tk.LEFT, padx=(0, 20))  # type: ignore

        ttk.Label(row_klant, text="Email:", style='THHSR.TLabel').pack(side=tk.LEFT, padx=(0, 10))  # type: ignore
        self.email_var = tk.StringVar()
        self.email_entry = ttk.Entry(row_klant, textvariable=self.email_var, font=('Source Sans Pro', 11), width=25)
        self.email_entry.pack(side=tk.LEFT)  # type: ignore

        # --- Aantal Fietsen ---
        ttk.Label(main_frame, text="Aantal Fietsen", font=('Source Sans Pro', 16, 'bold'), style='THHSR.TLabel').pack(
            anchor=tk.W, pady=(10, 10))  # type: ignore

        grid_fietsen = ttk.Frame(main_frame, style='Content.TFrame')
        grid_fietsen.pack(fill=tk.X, pady=(0, 20))  # type: ignore

        # Stadsfietsen rij
        ttk.Label(grid_fietsen, text="Stadsfiets Dames:", style='THHSR.TLabel').grid(row=0, column=0, sticky=tk.W,  # type: ignore
                                                                                     pady=5, padx=(0, 10))
        self.aantal_stad_dames = tk.IntVar(value=0)
        self.spin_stad_dames = ttk.Spinbox(grid_fietsen, from_=0, to=10, textvariable=self.aantal_stad_dames, width=5,
                                           command=self.update_prijs)
        self.spin_stad_dames.grid(row=0, column=1, pady=5, padx=(0, 40))

        ttk.Label(grid_fietsen, text="Stadsfiets Heren:", style='THHSR.TLabel').grid(row=0, column=2, sticky=tk.W,  # type: ignore
                                                                                     pady=5, padx=(0, 10))
        self.aantal_stad_heren = tk.IntVar(value=0)
        self.spin_stad_heren = ttk.Spinbox(grid_fietsen, from_=0, to=10, textvariable=self.aantal_stad_heren, width=5,
                                           command=self.update_prijs)
        self.spin_stad_heren.grid(row=0, column=3, pady=5)

        # E-bikes rij
        ttk.Label(grid_fietsen, text="Elektrische Dames:", style='THHSR.TLabel').grid(row=1, column=0, sticky=tk.W,  # type: ignore
                                                                                      pady=5, padx=(0, 10))
        self.aantal_elek_dames = tk.IntVar(value=0)
        self.spin_elek_dames = ttk.Spinbox(grid_fietsen, from_=0, to=10, textvariable=self.aantal_elek_dames, width=5,
                                           command=self.update_prijs)
        self.spin_elek_dames.grid(row=1, column=1, pady=5, padx=(0, 40))

        ttk.Label(grid_fietsen, text="Elektrische Heren:", style='THHSR.TLabel').grid(row=1, column=2, sticky=tk.W,  # type: ignore
                                                                                      pady=5, padx=(0, 10))
        self.aantal_elek_heren = tk.IntVar(value=0)
        self.spin_elek_heren = ttk.Spinbox(grid_fietsen, from_=0, to=10, textvariable=self.aantal_elek_heren, width=5,
                                           command=self.update_prijs)
        self.spin_elek_heren.grid(row=1, column=3, pady=5)

        # --- Accessoires & Datums ---
        row_opties = ttk.Frame(main_frame, style='Content.TFrame')
        row_opties.pack(fill=tk.X, pady=(10, 20))  # type: ignore

        # Accessoires links
        acc_frame = ttk.Frame(row_opties, style='Content.TFrame')
        acc_frame.pack(side=tk.LEFT, anchor=tk.N, padx=(0, 50))  # type: ignore
        ttk.Label(acc_frame, text="Accessoires", font=('Source Sans Pro', 14, 'bold'), style='THHSR.TLabel').pack(
            anchor=tk.W, pady=(0, 5))  # type: ignore
        self.helm_var = tk.BooleanVar()
        ttk.Checkbutton(acc_frame, text="Helm (€3.00/dg)", variable=self.helm_var, command=self.update_prijs,
                        style='THHSR_Check.TCheckbutton').pack(anchor=tk.W, pady=2)  # type: ignore
        self.kinderzitje_var = tk.BooleanVar()
        ttk.Checkbutton(acc_frame, text="Kinderzitje (€4.00/dg)", variable=self.kinderzitje_var,
                        command=self.update_prijs, style='THHSR_Check.TCheckbutton').pack(anchor=tk.W, pady=2)  # type: ignore

        # Datums rechts
        date_frame = ttk.Frame(row_opties, style='Content.TFrame')
        date_frame.pack(side=tk.LEFT, anchor=tk.N)  # type: ignore
        ttk.Label(date_frame, text="Huurperiode", font=('Source Sans Pro', 14, 'bold'), style='THHSR.TLabel').pack(
            anchor=tk.W, pady=(0, 5))  # type: ignore

        self.start_datum = DateEntry(date_frame, width=15, background='#26384A', foreground='white', borderwidth=2,
                                     date_pattern='dd-mm-yyyy', mindate=datetime.now())
        self.start_datum.pack(side=tk.LEFT, padx=(0, 10))  # type: ignore
        self.start_datum.bind("<<DateEntrySelected>>", lambda event: self.update_prijs())

        self.eind_datum = DateEntry(date_frame, width=15, background='#26384A', foreground='white', borderwidth=2,
                                    date_pattern='dd-mm-yyyy', mindate=datetime.now() + timedelta(days=1))
        self.eind_datum.pack(side=tk.LEFT)  # type: ignore
        self.eind_datum.bind("<<DateEntrySelected>>", lambda event: self.update_prijs())

        # --- Korting & Betaling ---
        self.terugkerend_var = tk.BooleanVar()
        ttk.Checkbutton(main_frame, text="Terugkerende klant / Student (10% korting)",
                        variable=self.terugkerend_var, command=self.update_prijs,
                        style='THHSR_Check.TCheckbutton').pack(anchor=tk.W, pady=(10, 15))  # type: ignore

        ttk.Label(main_frame, text="Betaalmethode:", font=('Source Sans Pro', 12, 'bold'), style='THHSR.TLabel').pack(
            anchor=tk.W, pady=(5, 2))  # type: ignore
        pay_frame = ttk.Frame(main_frame, style='Content.TFrame')
        pay_frame.pack(anchor=tk.W, pady=(0, 30))  # type: ignore
        self.betaalmethode_var = tk.StringVar(value='ideal')
        ttk.Radiobutton(pay_frame, text="iDEAL", variable=self.betaalmethode_var, value='ideal',
                        style='THHSR_Radio.TRadiobutton').pack(side=tk.LEFT, padx=(0, 20))  # type: ignore
        ttk.Radiobutton(pay_frame, text="PIN", variable=self.betaalmethode_var, value='pin',
                        style='THHSR_Radio.TRadiobutton').pack(side=tk.LEFT)  # type: ignore

        # --- Actieknoppen ---
        btn_frame = ttk.Frame(main_frame, style='Content.TFrame')
        btn_frame.pack(anchor=tk.W)  # type: ignore

        self.btn_res = tk.Button(btn_frame, text="RESERVEER", command=self.reserveer,
                                 font=('Source Sans Pro', 11, 'bold'), bg='#5A7188', fg='#FFFFFF', relief="flat", bd=0,
                                 cursor='hand2', padx=20, pady=8)
        self.btn_res.grid(row=0, column=0, padx=(0, 10))

        self.btn_reset = tk.Button(btn_frame, text="RESET", command=self.reset_form,
                                   font=('Source Sans Pro', 11, 'bold'), bg='#F4F4F4', fg='#26384A', relief="flat",
                                   bd=0, cursor='hand2', padx=20, pady=8)
        self.btn_reset.grid(row=0, column=1, padx=(0, 10))

        self.btn_list = tk.Button(btn_frame, text="BEKIJK RESERVERINGEN", command=self.toon_reserveringen,
                                  font=('Source Sans Pro', 11, 'bold'), bg='#26384A', fg='#FFFFFF', relief="flat", bd=0,
                                  cursor='hand2', padx=20, pady=8)
        self.btn_list.grid(row=0, column=2)

        # ================= RECHTER KOLOM: DE LIMEGROENE SIDEBAR =================
        sidebar_frame = tk.Frame(container, bg="#A3AD00", padx=25, pady=40)
        sidebar_frame.grid(row=0, column=1, sticky=(tk.N, tk.E, tk.W, tk.S))  # type: ignore

        tk.Label(sidebar_frame, text="TOTAALPRIJS", font=('Source Sans Pro', 14, 'bold'), fg='#26384A',
                 bg='#A3AD00').pack(anchor=tk.W, pady=(0, 10))  # type: ignore

        # Enorm prijzen label conform de grote typografie wens van De Haagse Hogeschool
        self.prijs_label = tk.Label(sidebar_frame, text="€0.00", font=('Source Sans Pro', 36, 'bold'), fg='#26384A',
                                    bg='#A3AD00')
        self.prijs_label.pack(anchor=tk.W, pady=(0, 20))  # type: ignore

        # Wit informatievlak binnen de sidebar voor ademruimte - relief="flat" toegevoegd
        details_box = tk.Frame(sidebar_frame, bg='#FFFFFF', padx=15, pady=15, relief="flat")
        details_box.pack(fill=tk.X, pady=(0, 20))  # type: ignore

        self.prijs_details_label = tk.Label(details_box, text="", font=('Source Sans Pro', 10), fg='#26384A',
                                            bg='#FFFFFF', justify=tk.LEFT, anchor=tk.W)  # type: ignore
        self.prijs_details_label.pack(fill=tk.BOTH)  # type: ignore

        self.borg_label = tk.Label(sidebar_frame, text="", font=('Source Sans Pro', 11, 'bold'), fg='#26384A',
                                   bg='#A3AD00', justify=tk.LEFT)  # type: ignore
        self.borg_label.pack(anchor=tk.W)  # type: ignore

        self.dagen_label = tk.Label(sidebar_frame, text="Aantal dagen: 1", font=('Source Sans Pro', 12), fg='#26384A',
                                    bg='#A3AD00')
        self.dagen_label.pack(anchor=tk.W, pady=(20, 0))  # type: ignore

        self.update_prijs()

    def bereken_prijs_values(self):
        """Interne berekening zonder type checker issues."""
        try:
            start = self.start_datum.get_date()
            eind = self.eind_datum.get_date()
            dagen = (eind - start).days
            if dagen < 1:
                dagen = 1
                self.eind_datum.set_date(start + timedelta(days=1))
        except (ValueError, TypeError):
            dagen = 1

        self.dagen_label.config(text=f"Aantal huurdagen: {dagen}")

        s_dames = max(0, self.aantal_stad_dames.get())
        s_heren = max(0, self.aantal_stad_heren.get())
        e_dames = max(0, self.aantal_elek_dames.get())
        e_heren = max(0, self.aantal_elek_heren.get())

        totaal_stadsfietsen = Decimal(s_dames + s_heren)
        totaal_elektrisch = Decimal(e_dames + e_heren)
        totaal_fietsen = totaal_stadsfietsen + totaal_elektrisch

        prijs_stads = totaal_stadsfietsen * self.prijzen['stadfiets'] * Decimal(dagen)
        prijs_elek = totaal_elektrisch * self.prijzen['elektrisch'] * Decimal(dagen)
        verhuur_totaal = prijs_stads + prijs_elek

        details = []
        if totaal_stadsfietsen > 0:
            details.append(f"Stadsfietsen: {totaal_stadsfietsen}x\n  ↳ €{prijs_stads:.2f}")
        if totaal_elektrisch > 0:
            details.append(f"E-bikes: {totaal_elektrisch}x\n  ↳ €{prijs_elek:.2f}")
        if totaal_fietsen == 0:
            details.append("Geen fietsen geselecteerd.")

        if self.helm_var.get() and totaal_fietsen > 0:
            helm_totaal = self.prijzen['helm'] * Decimal(dagen)
            verhuur_totaal += helm_totaal
            details.append(f"Helm: €{helm_totaal:.2f}")

        if self.kinderzitje_var.get() and totaal_fietsen > 0:
            zitje_totaal = self.prijzen['kinderzitje'] * Decimal(dagen)
            verhuur_totaal += zitje_totaal
            details.append(f"Kinderzitje: €{zitje_totaal:.2f}")

        if self.terugkerend_var.get() and verhuur_totaal > 0:
            korting = verhuur_totaal * Decimal('0.10')
            verhuur_totaal -= korting
            details.append(f"Korting (10%): -€{korting:.2f}")

        borg_stads = totaal_stadsfietsen * self.borg['stadfiets']
        borg_elek = totaal_elektrisch * self.borg['elektrisch']
        borg_bedrag = borg_stads + borg_elek

        totaal_met_borg = verhuur_totaal + borg_bedrag
        return totaal_met_borg, details, dagen, borg_bedrag, verhuur_totaal, totaal_fietsen

    def update_prijs(self):
        """Updatet de interface-elementen met de actuele berekende prijzen."""
        totaal_met_borg, details, _, borg_bedrag, _, _ = self.bereken_prijs_values()
        self.prijs_label.config(text=f"€{totaal_met_borg:.2f}")
        self.prijs_details_label.config(text="\n".join(details))
        self.borg_label.config(text=f"Borgsom (Inbegrepen):\n€{borg_bedrag:.2f}")

    def reserveer(self):
        """Valideert en slaat de reservering op in de database."""
        naam = self.naam_var.get().strip()
        if not naam:
            messagebox.showerror("Fout", "Voer een naam in")
            self.naam_entry.focus_set()
            return

        email = self.email_var.get().strip()
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,7}$'

        if not email or not re.fullmatch(email_pattern, email):
            messagebox.showerror("Fout", "Voer een geldig emailadres in.")
            self.email_entry.focus_set()
            return

        totaal_met_borg, _, dagen, borg_bedrag, _, totaal_fietsen = self.bereken_prijs_values()
        if totaal_fietsen == 0:
            messagebox.showerror("Fout", "Selecteer minimaal 1 fiets.")
            return

        start = self.start_datum.get_date()
        eind = self.eind_datum.get_date()

        reserverings_id = f"RES{datetime.now().strftime('%Y%m%d%H%M%S')}"
        betaalmethode = self.betaalmethode_var.get()
        betaalmethode_tekst = "iDEAL" if betaalmethode == 'ideal' else "PIN"
        betaling_status = "Betaald" if betaalmethode == 'ideal' else "Bij afhalen"

        datum = datetime.now().strftime("%Y-%m-%d %H:%M")
        start_str = start.strftime("%d-%m-%Y")
        eind_str = eind.strftime("%d-%m-%Y")

        try:
            with open(self.csv_bestand, 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([
                    reserverings_id, datum, naam, email,
                    self.aantal_stad_dames.get(), self.aantal_stad_heren.get(),
                    self.aantal_elek_dames.get(), self.aantal_elek_heren.get(),
                    'Ja' if self.helm_var.get() else 'Nee', 'Ja' if self.kinderzitje_var.get() else 'Nee',
                    start_str, eind_str, str(dagen), 'Ja' if self.terugkerend_var.get() else 'Nee',
                    betaalmethode_tekst, f"{borg_bedrag:.2f}", f"{totaal_met_borg:.2f}", betaling_status, 'Actief'
                ])
        except IOError as err:
            messagebox.showerror("Fout", f"Kan reservering niet opslaan: {err}")
            return

        bevestiging_tekst = f"Succesvol Gereserveerd!\n\nID: {reserverings_id}\nNaam: {naam}\nAantal fietsen: " \
                            f"{int(totaal_fietsen)}\nPeriode: {start_str} tot {eind_str}\nTotaalbedrag (incl. borg): " \
                            f"€{totaal_met_borg:.2f}"
        messagebox.showinfo("Reservering Bevestigd", bevestiging_tekst)
        self.reset_form()

    def reset_form(self):
        """Zet alle velden in het formulier terug naar de standaardwaarde."""
        self.naam_var.set('')
        self.email_var.set('')
        self.aantal_stad_dames.set(0)
        self.aantal_stad_heren.set(0)
        self.aantal_elek_dames.set(0)
        self.aantal_elek_heren.set(0)
        self.helm_var.set(False)
        self.kinderzitje_var.set(False)
        self.start_datum.set_date(datetime.now())
        self.eind_datum.set_date(datetime.now() + timedelta(days=1))
        self.terugkerend_var.set(False)
        self.betaalmethode_var.set('ideal')
        self.update_prijs()

    def toon_reserveringen(self):
        """Toont een overzichtsvenster met alle opgeslagen reserveringen."""
        if not os.path.exists(self.csv_bestand):
            messagebox.showinfo("Info", "Geen reserveringen gevonden")
            return

        window = tk.Toplevel(self.root)
        window.title("Reserveringen - Overzicht")
        window.geometry("1400x600")
        window.configure(bg="#F4F4F4")

        frame = ttk.Frame(window, padding=15)
        frame.pack(fill=tk.BOTH, expand=True)  # type: ignore

        columns = ('ReserveringsID', 'Datum', 'Naam', 'Email', 'StadDames', 'StadHeren', 'ElekDames', 'ElekHeren',
                   'Helm', 'Kinderzitje', 'Startdatum', 'Einddatum', 'Dagen', 'Terugkerend', 'Betaalmethode', 'Borg',
                   'Totaalprijs', 'BetalingStatus', 'Status')
        tree = ttk.Treeview(frame, columns=columns, show='headings', height=18)  # type: ignore

        for col in columns:
            tree.heading(col, text=col)
            if col == 'Email':
                tree.column(col, width=140)
            elif col in ['StadDames', 'StadHeren', 'ElekDames', 'ElekHeren', 'Dagen']:
                tree.column(col, width=65, anchor=tk.CENTER)  # type: ignore
            else:
                tree.column(col, width=85)

        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=tree.yview)  # type: ignore
        tree.configure(yscrollcommand=scrollbar.set)
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)  # type: ignore
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)  # type: ignore

        try:
            with open(self.csv_bestand, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                next(reader)
                for db_row in reader:
                    if len(db_row) == len(columns):
                        tree.insert('', tk.END, values=db_row)  # type: ignore
        except IOError as err:
            messagebox.showerror("Fout", f"Fout bij inlezen: {err}")
            window.destroy()
            return

        btn_win_frame = ttk.Frame(window, padding=10)
        btn_win_frame.pack()

        def annuleer_reservering():
            selection = tree.selection()
            if not selection:
                messagebox.showwarning("Waarschuwing", "Selecteer een reservering")
                return

            item = tree.item(selection[0])
            values = item['values']

            if values[18] == 'Geannuleerd':
                messagebox.showinfo("Info", "Al geannuleerd")
                return

            target_id = values[0]
            startdatum_str = values[10]

            try:
                startdatum = datetime.strptime(startdatum_str, "%d-%m-%Y")
            except ValueError:
                messagebox.showerror("Fout", "Datumfout")
                return

            if (startdatum - datetime.now()).total_seconds() / 3600 < 24:
                messagebox.showerror("Fout", "Annuleren moet minimaal 24 uur van tevoren.")
                return

            if not messagebox.askyesno("Bevestig", f"Annuleer {target_id}?"):
                return

            try:
                with open(self.csv_bestand, 'r', encoding='utf-8') as file_in:
                    rows = list(csv.reader(file_in))
                for file_row in rows:
                    if file_row[0] == target_id:
                        file_row[18] = 'Geannuleerd'
                        break
                with open(self.csv_bestand, 'w', newline='', encoding='utf-8') as file_out:
                    csv.writer(file_out).writerows(rows)
                window.destroy()
                self.toon_reserveringen()
            except IOError as inner_err:
                messagebox.showerror("Fout", f"Fout bij annuleren: {inner_err}")

        # Ook hier relief="flat" toegepast voor de overzichtsknoppen
        tk.Button(btn_win_frame, text="ANNULEER RESERVERING", command=annuleer_reservering,
                  font=('Source Sans Pro', 10, 'bold'), bg='#5A7188', fg='#FFFFFF', relief="flat", pady=6,
                  padx=15).grid(row=0, column=0, padx=5)
        tk.Button(btn_win_frame, text="SLUITEN", command=window.destroy, font=('Source Sans Pro', 10, 'bold'),
                  bg='#26384A', fg='#FFFFFF', relief="flat", pady=6, padx=15).grid(row=0, column=1, padx=5)


def main():
    """Main startpunt van de applicatie."""
    root = tk.Tk()
    try:
        root.wm_iconbitmap('jouw_logo.ico')
    except (tk.TclError, IOError):
        pass
    LoginWindow(root)
    root.mainloop()


if __name__ == "__main__":
    main()
