"""
Biker Haaglanden - Fietsverhuur Applicatie
Versie met extra commentaar voor assessment/verdediging.

Doel van deze applicatie:
- Medewerker logt in.
- Medewerker vult klantgegevens, fietsen, accessoires en huurperiode in.
- Applicatie berekent prijs, borg en korting.
- Reservering wordt opgeslagen in een CSV-bestand.
- Reserveringen kunnen bekeken en geannuleerd worden.
"""

# Importeert de csv-module om reserveringen in een CSV-bestand op te slaan en uit te lezen.
import csv
# Importeert datetime en timedelta om datums, tijden en huurperiodes te berekenen.
from datetime import datetime, timedelta
# Importeert Decimal zodat geldbedragen nauwkeurig worden berekend zonder afrondingsfouten van floats.
from decimal import Decimal
# Importeert os om te controleren of het CSV-bestand al bestaat.
import os
# Importeert re om e-mailadressen met een reguliere expressie te valideren.
import re
# Importeert Tkinter als tk; dit is de basisbibliotheek voor de grafische interface.
import tkinter as tk
# Importeert extra Tkinter-onderdelen: messagebox voor meldingen en ttk voor moderne widgets.
from tkinter import messagebox, ttk
# Importeert DateEntry, een kalender-widget waarmee de gebruiker datums kan selecteren.
from tkcalendar import DateEntry


# Definieert de klasse voor het inlogscherm van de applicatie.
class LoginWindow:
    """Venster voor het inloggen van medewerkers."""

    # Constructor: wordt automatisch uitgevoerd zodra een object van deze klasse wordt aangemaakt.
    def __init__(self, root):
        # Slaat het hoofdvenster op in self.root zodat andere methodes dit venster kunnen gebruiken.
        self.root = root
        # Stelt de titel van het venster in zoals die bovenaan het scherm zichtbaar is.
        self.root.title("Biker Haaglanden - Inloggen")
        # Bepaalt de grootte van het venster in pixels.
        self.root.geometry("450x350")
        # Voorkomt dat de gebruiker het venster groter of kleiner kan maken.
        self.root.resizable(False, False)

        # Huisstijl kleuren toepassen op de achtergrond van het venster
        # Past eigenschappen van een widget aan, zoals achtergrondkleur of scrollbar-koppeling.
        self.root.configure(bg="#26384A")  # Donkerblauwe De Haagse hogeschool-achtergrond voor login

        # Centraal frame (White content surface)
        # Maakt een frame aan; dit is een container waarin widgets netjes gegroepeerd worden.
        login_frame = tk.Frame(self.root, bg="#FFFFFF", padx=30, pady=30)
        # Plaatst de widget in het venster met de pack-layoutmanager.
        login_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)  # type: ignore

        # Grote Typografie - Titel
        # Maakt een label aan; dit toont tekst in de interface.
        ttk.Label(login_frame, text="Medewerker Portaal", font=('Source Sans Pro', 22, 'bold'),
                  # Plaatst de widget in het venster met de pack-layoutmanager.
                  foreground='#26384A', background='#FFFFFF').pack(anchor=tk.W, pady=(0, 20))  # type: ignore

        # Invoervelden met strakke styling
        # Maakt een label aan; dit toont tekst in de interface.
        ttk.Label(login_frame, text="Gebruikersnaam", font=('Source Sans Pro', 11, 'bold'),
                  # Plaatst de widget in het venster met de pack-layoutmanager.
                  foreground='#26384A', background='#FFFFFF').pack(anchor=tk.W, pady=(5, 2))  # type: ignore
        # Maakt een Tkinter-variabele voor tekst die automatisch gekoppeld kan worden aan een invoerveld.
        self.username_var = tk.StringVar()
        # Maakt een invoerveld aan waarin de gebruiker tekst kan typen.
        self.username_entry = ttk.Entry(login_frame, textvariable=self.username_var, font=('Source Sans Pro', 12),
                                        # Maakt of wijzigt een variabele die later in de code gebruikt wordt.
                                        width=30)
        # Plaatst de widget in het venster met de pack-layoutmanager.
        self.username_entry.pack(fill=tk.X, pady=(0, 10))  # type: ignore
        # Deze regel voert een onderdeel van de applicatielogica of interface-opbouw uit.
        self.username_entry.focus_set()

        # Maakt een label aan; dit toont tekst in de interface.
        ttk.Label(login_frame, text="Wachtwoord", font=('Source Sans Pro', 11, 'bold'),
                  # Plaatst de widget in het venster met de pack-layoutmanager.
                  foreground='#26384A', background='#FFFFFF').pack(anchor=tk.W, pady=(5, 2))  # type: ignore
        # Maakt een Tkinter-variabele voor tekst die automatisch gekoppeld kan worden aan een invoerveld.
        self.password_var = tk.StringVar()
        # Maakt een invoerveld aan waarin de gebruiker tekst kan typen.
        self.password_entry = ttk.Entry(login_frame, textvariable=self.password_var, show="*",
                                        # Maakt of wijzigt een variabele die later in de code gebruikt wordt.
                                        font=('Source Sans Pro', 12), width=30)
        # Plaatst de widget in het venster met de pack-layoutmanager.
        self.password_entry.pack(fill=tk.X, pady=(0, 20))  # type: ignore

        # De Haagse Hogeschool Grijze/Blauwe Button - relief="flat" lost de Literal warning op
        # Maakt een knop aan en koppelt deze via command aan een functie.
        self.login_btn = tk.Button(login_frame, text="INLOGGEN", command=self.check_login,
                                   # Maakt of wijzigt een variabele die later in de code gebruikt wordt.
                                   font=('Source Sans Pro', 12, 'bold'), bg='#5A7188', fg='#FFFFFF',
                                   # Maakt of wijzigt een variabele die later in de code gebruikt wordt.
                                   activebackground='#26384A', activeforeground='#FFFFFF',
                                   # Maakt of wijzigt een variabele die later in de code gebruikt wordt.
                                   relief="flat", bd=0, cursor='hand2', pady=8)
        # Plaatst de widget in het venster met de pack-layoutmanager.
        self.login_btn.pack(fill=tk.X)  # type: ignore

        # Koppelt een gebeurtenis, zoals Enter of datumselectie, aan een functie.
        self.root.bind('<Return>', lambda event: self.check_login())

    # Methode die controleert of de ingevoerde gebruikersnaam en het wachtwoord juist zijn.
    def check_login(self):
        """Controleert of de inloggegevens juist zijn."""
        # Haalt de huidige waarde uit een Tkinter-variabele of widget op.
        username = self.username_var.get().strip()
        # Haalt de huidige waarde uit een Tkinter-variabele of widget op.
        password = self.password_var.get().strip()

        # Controleert een voorwaarde; alleen als deze waar is wordt de onderliggende code uitgevoerd.
        if username == "admin" and password == "biker2026":
            # Sluit of vernietigt het betreffende venster.
            self.root.destroy()
            # Deze regel voert een onderdeel van de applicatielogica of interface-opbouw uit.
            self.start_main_app()
        else:
            # Toont een foutmelding aan de gebruiker.
            messagebox.showerror("Fout", "Onjuiste gebruikersnaam of wachtwoord!")
            # Deze regel voert een onderdeel van de applicatielogica of interface-opbouw uit.
            self.password_entry.delete(0, tk.END)

    # Geeft aan dat deze methode geen self nodig heeft en dus los van een object kan werken.
    @staticmethod
    # Methode die het hoofdvenster start nadat de gebruiker succesvol is ingelogd.
    def start_main_app():
        """Start de hoofdapplicatie na succesvol inloggen."""
        # Maakt een nieuw Tkinter-venster aan.
        main_root = tk.Tk()
        # Start een try-blok: code hierin kan een fout veroorzaken die later wordt opgevangen.
        try:
            # Deze regel voert een onderdeel van de applicatielogica of interface-opbouw uit.
            main_root.wm_iconbitmap('jouw_logo.ico')
        # Vangt een mogelijke fout af zodat het programma niet onverwacht crasht.
        except (tk.TclError, IOError):
            # Doet bewust niets; gebruikt wanneer een fout genegeerd mag worden.
            pass
        # Deze regel voert een onderdeel van de applicatielogica of interface-opbouw uit.
        BikerRentalApp(main_root)
        # Start de Tkinter event-loop waardoor het venster blijft reageren op acties.
        main_root.mainloop()


# Definieert de hoofdklasse waarin het fietsverhuursysteem wordt opgebouwd.
class BikerRentalApp:
    """De hoofdklasse voor het Fietsverhuur Systeem."""

    # Constructor: wordt automatisch uitgevoerd zodra een object van deze klasse wordt aangemaakt.
    def __init__(self, root):
        # Slaat het hoofdvenster op in self.root zodat andere methodes dit venster kunnen gebruiken.
        self.root = root
        # Stelt de titel van het venster in zoals die bovenaan het scherm zichtbaar is.
        self.root.title("Biker Haaglanden - Fietsverhuur Systeem")
        # Bepaalt de grootte van het venster in pixels.
        self.root.geometry("1200x850")
        # Past eigenschappen van een widget aan, zoals achtergrondkleur of scrollbar-koppeling.
        self.root.configure(bg="#F4F4F4")  # Lichtgrijze De Haagse Hogeschool Achtergrond

        # Initialiseer alle instance attributes vooraf om linter warnings te voorkomen
        # Maakt of wijzigt een variabele die later in de code gebruikt wordt.
        self.naam_var = None
        # Maakt of wijzigt een variabele die later in de code gebruikt wordt.
        self.naam_entry = None
        # Maakt of wijzigt een variabele die later in de code gebruikt wordt.
        self.email_var = None
        # Maakt of wijzigt een variabele die later in de code gebruikt wordt.
        self.email_entry = None
        # Maakt of wijzigt een variabele die later in de code gebruikt wordt.
        self.aantal_stad_dames = None
        # Maakt of wijzigt een variabele die later in de code gebruikt wordt.
        self.spin_stad_dames = None
        # Maakt of wijzigt een variabele die later in de code gebruikt wordt.
        self.aantal_stad_heren = None
        # Maakt of wijzigt een variabele die later in de code gebruikt wordt.
        self.spin_stad_heren = None
        # Maakt of wijzigt een variabele die later in de code gebruikt wordt.
        self.aantal_elek_dames = None
        # Maakt of wijzigt een variabele die later in de code gebruikt wordt.
        self.spin_elek_dames = None
        # Maakt of wijzigt een variabele die later in de code gebruikt wordt.
        self.aantal_elek_heren = None
        # Maakt of wijzigt een variabele die later in de code gebruikt wordt.
        self.spin_elek_heren = None
        # Maakt of wijzigt een variabele die later in de code gebruikt wordt.
        self.helm_var = None
        # Maakt of wijzigt een variabele die later in de code gebruikt wordt.
        self.kinderzitje_var = None
        # Maakt of wijzigt een variabele die later in de code gebruikt wordt.
        self.start_datum = None
        # Maakt of wijzigt een variabele die later in de code gebruikt wordt.
        self.eind_datum = None
        # Maakt of wijzigt een variabele die later in de code gebruikt wordt.
        self.terugkerend_var = None
        # Maakt of wijzigt een variabele die later in de code gebruikt wordt.
        self.betaalmethode_var = None
        # Maakt of wijzigt een variabele die later in de code gebruikt wordt.
        self.btn_res = None
        # Maakt of wijzigt een variabele die later in de code gebruikt wordt.
        self.btn_reset = None
        # Maakt of wijzigt een variabele die later in de code gebruikt wordt.
        self.btn_list = None
        # Maakt of wijzigt een variabele die later in de code gebruikt wordt.
        self.prijs_label = None
        # Maakt of wijzigt een variabele die later in de code gebruikt wordt.
        self.prijs_details_label = None
        # Slaat de borgbedragen per fietstype op in een dictionary.
        self.borg_label = None
        # Maakt of wijzigt een variabele die later in de code gebruikt wordt.
        self.dagen_label = None

        # Slaat de dagprijzen per fietstype/accessoire op in een dictionary.
        self.prijzen = {
            'stadfiets': Decimal('15.00'), 'elektrisch': Decimal('25.00'),
            'helm': Decimal('3.00'), 'kinderzitje': Decimal('4.00')
        }
        # Slaat de borgbedragen per fietstype op in een dictionary.
        self.borg = {'stadfiets': Decimal('50.00'), 'elektrisch': Decimal('100.00')}
        # Bepaalt de bestandsnaam waarin reserveringen worden opgeslagen.
        self.csv_bestand = 'verhuur_data.csv'
        # Roept de methode aan die controleert of het CSV-bestand bestaat.
        self.init_csv()

        # Configureer Tkinter TTK Styles voor Haagse Hogeschool uitstraling
        # Roept de methode aan die de vormgeving van de applicatie instelt.
        self.setup_styles()
        # Roept de methode aan die de interface daadwerkelijk opbouwt.
        self.create_widgets()

    # Geeft aan dat deze methode geen self nodig heeft en dus los van een object kan werken.
    @staticmethod
    # Methode die de visuele stijl van de ttk-widgets instelt.
    def setup_styles():
        """Configureer fonts en stijlen gebaseerd op de HHS-ontwerpfilosofie."""
        # Maakt een style-object aan waarmee ttk-widgets vormgegeven worden.
        style = ttk.Style()
        # Kiest het ttk-thema waarop de widgets gebaseerd worden.
        style.theme_use('clam')

        # Algemene fonts en achtergronden
        # Past eigenschappen van een widget aan, zoals achtergrondkleur of scrollbar-koppeling.
        style.configure('.', font=('Source Sans Pro', 11), background='#F4F4F4', foreground='#26384A')

        # Formulier styling (Wit contentblok)
        # Past eigenschappen van een widget aan, zoals achtergrondkleur of scrollbar-koppeling.
        style.configure('Content.TFrame', background='#FFFFFF')
        # Past eigenschappen van een widget aan, zoals achtergrondkleur of scrollbar-koppeling.
        style.configure('THHSR.TLabel', background='#FFFFFF', foreground='#26384A')
        # Past eigenschappen van een widget aan, zoals achtergrondkleur of scrollbar-koppeling.
        style.configure('THHSR_Sub.TLabel', background='#FFFFFF', foreground='#5A7188')
        # Past eigenschappen van een widget aan, zoals achtergrondkleur of scrollbar-koppeling.
        style.configure('THHSR_Check.TCheckbutton', background='#FFFFFF', foreground='#26384A')
        # Past eigenschappen van een widget aan, zoals achtergrondkleur of scrollbar-koppeling.
        style.configure('THHSR_Radio.TRadiobutton', background='#FFFFFF', foreground='#26384A')

        # Treeview (Reserveringen overzicht)
        # Past eigenschappen van een widget aan, zoals achtergrondkleur of scrollbar-koppeling.
        style.configure('Treeview', font=('Source Sans Pro', 10), background='#FFFFFF', foreground='#26384A',
                        # Maakt of wijzigt een variabele die later in de code gebruikt wordt.
                        rowheight=25)
        # Past eigenschappen van een widget aan, zoals achtergrondkleur of scrollbar-koppeling.
        style.configure('Treeview.Heading', font=('Source Sans Pro', 10, 'bold'), background='#26384A',
                        # Maakt of wijzigt een variabele die later in de code gebruikt wordt.
                        foreground='#FFFFFF')

    # Methode die het CSV-bestand aanmaakt als het nog niet bestaat.
    def init_csv(self):
        """Initialiseert het databasebestand als het nog niet bestaat."""
        # Controleert of het opgegeven bestand al bestaat.
        if not os.path.exists(self.csv_bestand):
            # Start een try-blok: code hierin kan een fout veroorzaken die later wordt opgevangen.
            try:
                # Opent een bestand veilig; na afloop wordt het bestand automatisch gesloten.
                with open(self.csv_bestand, 'w', newline='', encoding='utf-8') as f:
                    # Maakt een CSV-writer aan om rijen naar het CSV-bestand te schrijven.
                    writer = csv.writer(f)
                    # Schrijft één rij met gegevens naar het CSV-bestand.
                    writer.writerow(
                        # Deze regel voert een onderdeel van de applicatielogica of interface-opbouw uit.
                        ['ReserveringsID', 'Datum', 'Naam', 'Email', 'StadDames', 'StadHeren', 'ElekDames', 'ElekHeren',
                         'Helm', 'Kinderzitje', 'Startdatum', 'Einddatum', 'Dagen', 'Terugkerend', 'Betaalmethode',
                         'Borg', 'Totaalprijs', 'BetalingStatus', 'Status'])
            # Vangt een mogelijke fout af zodat het programma niet onverwacht crasht.
            except IOError as err:
                # Toont een foutmelding aan de gebruiker.
                messagebox.showerror("Fout", f"Kan CSV niet initialiseren: {err}")
                # Sluit of vernietigt het betreffende venster.
                self.root.destroy()

    # Methode die alle knoppen, invoervelden, labels en frames van de interface opbouwt.
    def create_widgets(self):
        """Bouwt de interface-elementen op."""
        # Asymmetrische Hoofdcontainer: Veel witruimte en padding als integer (30)
        # Maakt een frame aan; dit is een container waarin widgets netjes gegroepeerd worden.
        container = ttk.Frame(self.root, padding=30, style='TFrame')
        # Plaatst de widget in het venster met de pack-layoutmanager.
        container.pack(fill=tk.BOTH, expand=True)  # type: ignore
        # Maakt of wijzigt een variabele die later in de code gebruikt wordt.
        container.columnconfigure(0, weight=3)  # Linker kolom breder voor rustige layout
        # Maakt of wijzigt een variabele die later in de code gebruikt wordt.
        container.columnconfigure(1, weight=1)  # Rechter kolom smaller (Asymmetrisch)

        # ================= LINKER KOLOM: HET WITTE CONTENTBLOK =================
        # Maakt een frame aan; dit is een container waarin widgets netjes gegroepeerd worden.
        main_frame = ttk.Frame(container, style='Content.TFrame', padding=40)
        # Plaatst de widget in een rij en kolom met de grid-layoutmanager.
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 20))  # type: ignore

        # Grote Typografie (Titel conform De Haagse Hogeschool stijl: 28px krachtig)
        # Maakt een label aan; dit toont tekst in de interface.
        title_label = ttk.Label(main_frame, text="Biker Haaglanden", font=('Source Sans Pro', 28, 'bold'),
                                # Maakt of wijzigt een variabele die later in de code gebruikt wordt.
                                style='THHSR.TLabel')
        # Plaatst de widget in het venster met de pack-layoutmanager.
        title_label.pack(anchor=tk.W, pady=(0, 2))  # type: ignore

        # Maakt een label aan; dit toont tekst in de interface.
        subtitle_label = ttk.Label(main_frame, text="Fietsverhuur Den Haag — Connected met De Haagse Hogeschool",
                                   # Maakt of wijzigt een variabele die later in de code gebruikt wordt.
                                   font=('Source Sans Pro', 12), style='THHSR_Sub.TLabel')
        # Plaatst de widget in het venster met de pack-layoutmanager.
        subtitle_label.pack(anchor=tk.W, pady=(0, 30))  # type: ignore

        # --- Klantgegevens ---
        # Maakt een label aan; dit toont tekst in de interface.
        ttk.Label(main_frame, text="Klantgegevens", font=('Source Sans Pro', 16, 'bold'), style='THHSR.TLabel').pack(
            # Maakt of wijzigt een variabele die later in de code gebruikt wordt.
            anchor=tk.W, pady=(10, 10))  # type: ignore

        # Maakt een frame aan; dit is een container waarin widgets netjes gegroepeerd worden.
        row_klant = ttk.Frame(main_frame, style='Content.TFrame')
        # Plaatst de widget in het venster met de pack-layoutmanager.
        row_klant.pack(fill=tk.X, pady=(0, 20))  # type: ignore

        # Maakt een label aan; dit toont tekst in de interface.
        ttk.Label(row_klant, text="Naam:", style='THHSR.TLabel').pack(side=tk.LEFT, padx=(0, 10))  # type: ignore
        # Maakt een Tkinter-variabele voor tekst die automatisch gekoppeld kan worden aan een invoerveld.
        self.naam_var = tk.StringVar()
        # Maakt een invoerveld aan waarin de gebruiker tekst kan typen.
        self.naam_entry = ttk.Entry(row_klant, textvariable=self.naam_var, font=('Source Sans Pro', 11), width=25)
        # Plaatst de widget in het venster met de pack-layoutmanager.
        self.naam_entry.pack(side=tk.LEFT, padx=(0, 20))  # type: ignore

        # Maakt een label aan; dit toont tekst in de interface.
        ttk.Label(row_klant, text="Email:", style='THHSR.TLabel').pack(side=tk.LEFT, padx=(0, 10))  # type: ignore
        # Maakt een Tkinter-variabele voor tekst die automatisch gekoppeld kan worden aan een invoerveld.
        self.email_var = tk.StringVar()
        # Maakt een invoerveld aan waarin de gebruiker tekst kan typen.
        self.email_entry = ttk.Entry(row_klant, textvariable=self.email_var, font=('Source Sans Pro', 11), width=25)
        # Plaatst de widget in het venster met de pack-layoutmanager.
        self.email_entry.pack(side=tk.LEFT)  # type: ignore

        # --- Aantal Fietsen ---
        # Maakt een label aan; dit toont tekst in de interface.
        ttk.Label(main_frame, text="Aantal Fietsen", font=('Source Sans Pro', 16, 'bold'), style='THHSR.TLabel').pack(
            # Maakt of wijzigt een variabele die later in de code gebruikt wordt.
            anchor=tk.W, pady=(10, 10))  # type: ignore

        # Maakt een frame aan; dit is een container waarin widgets netjes gegroepeerd worden.
        grid_fietsen = ttk.Frame(main_frame, style='Content.TFrame')
        # Plaatst de widget in het venster met de pack-layoutmanager.
        grid_fietsen.pack(fill=tk.X, pady=(0, 20))  # type: ignore

        # Stadsfietsen rij
        # Maakt een label aan; dit toont tekst in de interface.
        ttk.Label(grid_fietsen, text="Stadsfiets Dames:", style='THHSR.TLabel').grid(row=0, column=0, sticky=tk.W,  # type: ignore
                                                                                     # Maakt of wijzigt een variabele die later in de code gebruikt wordt.
                                                                                     pady=5, padx=(0, 10))
        # Maakt een Tkinter-variabele voor gehele getallen, gebruikt voor aantallen fietsen.
        self.aantal_stad_dames = tk.IntVar(value=0)
        # Maakt een spinbox aan waarmee de gebruiker een aantal kan verhogen of verlagen.
        self.spin_stad_dames = ttk.Spinbox(grid_fietsen, from_=0, to=10, textvariable=self.aantal_stad_dames, width=5,
                                           # Maakt of wijzigt een variabele die later in de code gebruikt wordt.
                                           command=self.update_prijs)
        # Plaatst de widget in een rij en kolom met de grid-layoutmanager.
        self.spin_stad_dames.grid(row=0, column=1, pady=5, padx=(0, 40))

        # Maakt een label aan; dit toont tekst in de interface.
        ttk.Label(grid_fietsen, text="Stadsfiets Heren:", style='THHSR.TLabel').grid(row=0, column=2, sticky=tk.W,  # type: ignore
                                                                                     # Maakt of wijzigt een variabele die later in de code gebruikt wordt.
                                                                                     pady=5, padx=(0, 10))
        # Maakt een Tkinter-variabele voor gehele getallen, gebruikt voor aantallen fietsen.
        self.aantal_stad_heren = tk.IntVar(value=0)
        # Maakt een spinbox aan waarmee de gebruiker een aantal kan verhogen of verlagen.
        self.spin_stad_heren = ttk.Spinbox(grid_fietsen, from_=0, to=10, textvariable=self.aantal_stad_heren, width=5,
                                           # Maakt of wijzigt een variabele die later in de code gebruikt wordt.
                                           command=self.update_prijs)
        # Plaatst de widget in een rij en kolom met de grid-layoutmanager.
        self.spin_stad_heren.grid(row=0, column=3, pady=5)

        # E-bikes rij
        # Maakt een label aan; dit toont tekst in de interface.
        ttk.Label(grid_fietsen, text="Elektrische Dames:", style='THHSR.TLabel').grid(row=1, column=0, sticky=tk.W,  # type: ignore
                                                                                      # Maakt of wijzigt een variabele die later in de code gebruikt wordt.
                                                                                      pady=5, padx=(0, 10))
        # Maakt een Tkinter-variabele voor gehele getallen, gebruikt voor aantallen fietsen.
        self.aantal_elek_dames = tk.IntVar(value=0)
        # Maakt een spinbox aan waarmee de gebruiker een aantal kan verhogen of verlagen.
        self.spin_elek_dames = ttk.Spinbox(grid_fietsen, from_=0, to=10, textvariable=self.aantal_elek_dames, width=5,
                                           # Maakt of wijzigt een variabele die later in de code gebruikt wordt.
                                           command=self.update_prijs)
        # Plaatst de widget in een rij en kolom met de grid-layoutmanager.
        self.spin_elek_dames.grid(row=1, column=1, pady=5, padx=(0, 40))

        # Maakt een label aan; dit toont tekst in de interface.
        ttk.Label(grid_fietsen, text="Elektrische Heren:", style='THHSR.TLabel').grid(row=1, column=2, sticky=tk.W,  # type: ignore
                                                                                      # Maakt of wijzigt een variabele die later in de code gebruikt wordt.
                                                                                      pady=5, padx=(0, 10))
        # Maakt een Tkinter-variabele voor gehele getallen, gebruikt voor aantallen fietsen.
        self.aantal_elek_heren = tk.IntVar(value=0)
        # Maakt een spinbox aan waarmee de gebruiker een aantal kan verhogen of verlagen.
        self.spin_elek_heren = ttk.Spinbox(grid_fietsen, from_=0, to=10, textvariable=self.aantal_elek_heren, width=5,
                                           # Maakt of wijzigt een variabele die later in de code gebruikt wordt.
                                           command=self.update_prijs)
        # Plaatst de widget in een rij en kolom met de grid-layoutmanager.
        self.spin_elek_heren.grid(row=1, column=3, pady=5)

        # --- Accessoires & Datums ---
        # Maakt een frame aan; dit is een container waarin widgets netjes gegroepeerd worden.
        row_opties = ttk.Frame(main_frame, style='Content.TFrame')
        # Plaatst de widget in het venster met de pack-layoutmanager.
        row_opties.pack(fill=tk.X, pady=(10, 20))  # type: ignore

        # Accessoires links
        # Maakt een frame aan; dit is een container waarin widgets netjes gegroepeerd worden.
        acc_frame = ttk.Frame(row_opties, style='Content.TFrame')
        # Plaatst de widget in het venster met de pack-layoutmanager.
        acc_frame.pack(side=tk.LEFT, anchor=tk.N, padx=(0, 50))  # type: ignore
        # Maakt een label aan; dit toont tekst in de interface.
        ttk.Label(acc_frame, text="Accessoires", font=('Source Sans Pro', 14, 'bold'), style='THHSR.TLabel').pack(
            # Maakt of wijzigt een variabele die later in de code gebruikt wordt.
            anchor=tk.W, pady=(0, 5))  # type: ignore
        # Maakt een Tkinter-variabele voor True/False-keuzes, gebruikt bij checkboxes.
        self.helm_var = tk.BooleanVar()
        # Maakt een checkbox aan voor ja/nee-keuzes zoals accessoires of korting.
        ttk.Checkbutton(acc_frame, text="Helm (€3.00/dg)", variable=self.helm_var, command=self.update_prijs,
                        # Plaatst de widget in het venster met de pack-layoutmanager.
                        style='THHSR_Check.TCheckbutton').pack(anchor=tk.W, pady=2)  # type: ignore
        # Maakt een Tkinter-variabele voor True/False-keuzes, gebruikt bij checkboxes.
        self.kinderzitje_var = tk.BooleanVar()
        # Maakt een checkbox aan voor ja/nee-keuzes zoals accessoires of korting.
        ttk.Checkbutton(acc_frame, text="Kinderzitje (€4.00/dg)", variable=self.kinderzitje_var,
                        # Plaatst de widget in het venster met de pack-layoutmanager.
                        command=self.update_prijs, style='THHSR_Check.TCheckbutton').pack(anchor=tk.W, pady=2)  # type: ignore

        # Datums rechts
        # Maakt een frame aan; dit is een container waarin widgets netjes gegroepeerd worden.
        date_frame = ttk.Frame(row_opties, style='Content.TFrame')
        # Plaatst de widget in het venster met de pack-layoutmanager.
        date_frame.pack(side=tk.LEFT, anchor=tk.N)  # type: ignore
        # Maakt een label aan; dit toont tekst in de interface.
        ttk.Label(date_frame, text="Huurperiode", font=('Source Sans Pro', 14, 'bold'), style='THHSR.TLabel').pack(
            # Maakt of wijzigt een variabele die later in de code gebruikt wordt.
            anchor=tk.W, pady=(0, 5))  # type: ignore

        # Maakt een datumveld met kalenderselectie aan.
        self.start_datum = DateEntry(date_frame, width=15, background='#26384A', foreground='white', borderwidth=2,
                                     # Haalt de huidige datum en/of tijd op.
                                     date_pattern='dd-mm-yyyy', mindate=datetime.now())
        # Plaatst de widget in het venster met de pack-layoutmanager.
        self.start_datum.pack(side=tk.LEFT, padx=(0, 10))  # type: ignore
        # Maakt een datumveld met kalenderselectie aan.
        self.start_datum.bind("<<DateEntrySelected>>", lambda event: self.update_prijs())

        # Maakt een datumveld met kalenderselectie aan.
        self.eind_datum = DateEntry(date_frame, width=15, background='#26384A', foreground='white', borderwidth=2,
                                    # Gebruikt timedelta om dagen bij een datum op te tellen of huurduur te berekenen.
                                    date_pattern='dd-mm-yyyy', mindate=datetime.now() + timedelta(days=1))
        # Plaatst de widget in het venster met de pack-layoutmanager.
        self.eind_datum.pack(side=tk.LEFT)  # type: ignore
        # Maakt een datumveld met kalenderselectie aan.
        self.eind_datum.bind("<<DateEntrySelected>>", lambda event: self.update_prijs())

        # --- Korting & Betaling ---
        # Maakt een Tkinter-variabele voor True/False-keuzes, gebruikt bij checkboxes.
        self.terugkerend_var = tk.BooleanVar()
        # Maakt een checkbox aan voor ja/nee-keuzes zoals accessoires of korting.
        ttk.Checkbutton(main_frame, text="Terugkerende klant / THHSR Student (10% korting)",
                        # Maakt of wijzigt een variabele die later in de code gebruikt wordt.
                        variable=self.terugkerend_var, command=self.update_prijs,
                        # Plaatst de widget in het venster met de pack-layoutmanager.
                        style='THHSR_Check.TCheckbutton').pack(anchor=tk.W, pady=(10, 15))  # type: ignore

        # Maakt een label aan; dit toont tekst in de interface.
        ttk.Label(main_frame, text="Betaalmethode:", font=('Source Sans Pro', 12, 'bold'), style='THHSR.TLabel').pack(
            # Maakt of wijzigt een variabele die later in de code gebruikt wordt.
            anchor=tk.W, pady=(5, 2))  # type: ignore
        # Maakt een frame aan; dit is een container waarin widgets netjes gegroepeerd worden.
        pay_frame = ttk.Frame(main_frame, style='Content.TFrame')
        # Plaatst de widget in het venster met de pack-layoutmanager.
        pay_frame.pack(anchor=tk.W, pady=(0, 30))  # type: ignore
        # Maakt een Tkinter-variabele voor tekst die automatisch gekoppeld kan worden aan een invoerveld.
        self.betaalmethode_var = tk.StringVar(value='ideal')
        # Maakt een radiobutton aan; hiermee kiest de gebruiker één betaalmethode.
        ttk.Radiobutton(pay_frame, text="iDEAL (Online)", variable=self.betaalmethode_var, value='ideal',
                        # Plaatst de widget in het venster met de pack-layoutmanager.
                        style='THHSR_Radio.TRadiobutton').pack(side=tk.LEFT, padx=(0, 20))  # type: ignore
        # Maakt een radiobutton aan; hiermee kiest de gebruiker één betaalmethode.
        ttk.Radiobutton(pay_frame, text="PIN (Bij afhalen)", variable=self.betaalmethode_var, value='pin',
                        # Plaatst de widget in het venster met de pack-layoutmanager.
                        style='THHSR_Radio.TRadiobutton').pack(side=tk.LEFT)  # type: ignore

        # --- Actieknoppen ---
        # Maakt een frame aan; dit is een container waarin widgets netjes gegroepeerd worden.
        btn_frame = ttk.Frame(main_frame, style='Content.TFrame')
        # Plaatst de widget in het venster met de pack-layoutmanager.
        btn_frame.pack(anchor=tk.W)  # type: ignore

        # Maakt een knop aan en koppelt deze via command aan een functie.
        self.btn_res = tk.Button(btn_frame, text="RESERVEER", command=self.reserveer,
                                 # Maakt of wijzigt een variabele die later in de code gebruikt wordt.
                                 font=('Source Sans Pro', 11, 'bold'), bg='#5A7188', fg='#FFFFFF', relief="flat", bd=0,
                                 # Maakt of wijzigt een variabele die later in de code gebruikt wordt.
                                 cursor='hand2', padx=20, pady=8)
        # Plaatst de widget in een rij en kolom met de grid-layoutmanager.
        self.btn_res.grid(row=0, column=0, padx=(0, 10))

        # Maakt een knop aan en koppelt deze via command aan een functie.
        self.btn_reset = tk.Button(btn_frame, text="RESET", command=self.reset_form,
                                   # Maakt of wijzigt een variabele die later in de code gebruikt wordt.
                                   font=('Source Sans Pro', 11, 'bold'), bg='#F4F4F4', fg='#26384A', relief="flat",
                                   # Maakt of wijzigt een variabele die later in de code gebruikt wordt.
                                   bd=0, cursor='hand2', padx=20, pady=8)
        # Plaatst de widget in een rij en kolom met de grid-layoutmanager.
        self.btn_reset.grid(row=0, column=1, padx=(0, 10))

        # Maakt een knop aan en koppelt deze via command aan een functie.
        self.btn_list = tk.Button(btn_frame, text="BEKIJK RESERVERINGEN", command=self.toon_reserveringen,
                                  # Maakt of wijzigt een variabele die later in de code gebruikt wordt.
                                  font=('Source Sans Pro', 11, 'bold'), bg='#26384A', fg='#FFFFFF', relief="flat", bd=0,
                                  # Maakt of wijzigt een variabele die later in de code gebruikt wordt.
                                  cursor='hand2', padx=20, pady=8)
        # Plaatst de widget in een rij en kolom met de grid-layoutmanager.
        self.btn_list.grid(row=0, column=2)

        # ================= RECHTER KOLOM: DE LIMEGROENE SIDEBAR =================
        # Maakt een frame aan; dit is een container waarin widgets netjes gegroepeerd worden.
        sidebar_frame = tk.Frame(container, bg="#A3AD00", padx=25, pady=40)
        # Plaatst de widget in een rij en kolom met de grid-layoutmanager.
        sidebar_frame.grid(row=0, column=1, sticky=(tk.N, tk.E, tk.W, tk.S))  # type: ignore

        # Maakt een label aan; dit toont tekst in de interface.
        tk.Label(sidebar_frame, text="TOTAALPRIJS", font=('Source Sans Pro', 14, 'bold'), fg='#26384A',
                 # Plaatst de widget in het venster met de pack-layoutmanager.
                 bg='#A3AD00').pack(anchor=tk.W, pady=(0, 10))  # type: ignore

        # Enorm prijzen label conform de grote typografie wens van De Haagse Hogeschool
        # Maakt een label aan; dit toont tekst in de interface.
        self.prijs_label = tk.Label(sidebar_frame, text="€0.00", font=('Source Sans Pro', 36, 'bold'), fg='#26384A',
                                    # Maakt of wijzigt een variabele die later in de code gebruikt wordt.
                                    bg='#A3AD00')
        # Plaatst de widget in het venster met de pack-layoutmanager.
        self.prijs_label.pack(anchor=tk.W, pady=(0, 20))  # type: ignore

        # Wit informatievlak binnen de sidebar voor ademruimte - relief="flat" toegevoegd
        # Maakt een frame aan; dit is een container waarin widgets netjes gegroepeerd worden.
        details_box = tk.Frame(sidebar_frame, bg='#FFFFFF', padx=15, pady=15, relief="flat")
        # Plaatst de widget in het venster met de pack-layoutmanager.
        details_box.pack(fill=tk.X, pady=(0, 20))  # type: ignore

        # Maakt een label aan; dit toont tekst in de interface.
        self.prijs_details_label = tk.Label(details_box, text="", font=('Source Sans Pro', 10), fg='#26384A',
                                            # Maakt of wijzigt een variabele die later in de code gebruikt wordt.
                                            bg='#FFFFFF', justify=tk.LEFT, anchor=tk.W)  # type: ignore
        # Plaatst de widget in het venster met de pack-layoutmanager.
        self.prijs_details_label.pack(fill=tk.BOTH)  # type: ignore

        # Maakt een label aan; dit toont tekst in de interface.
        self.borg_label = tk.Label(sidebar_frame, text="", font=('Source Sans Pro', 11, 'bold'), fg='#26384A',
                                   # Maakt of wijzigt een variabele die later in de code gebruikt wordt.
                                   bg='#A3AD00', justify=tk.LEFT)  # type: ignore
        # Plaatst de widget in het venster met de pack-layoutmanager.
        self.borg_label.pack(anchor=tk.W)  # type: ignore

        # Maakt een label aan; dit toont tekst in de interface.
        self.dagen_label = tk.Label(sidebar_frame, text="Aantal dagen: 1", font=('Source Sans Pro', 12), fg='#26384A',
                                    # Maakt of wijzigt een variabele die later in de code gebruikt wordt.
                                    bg='#A3AD00')
        # Plaatst de widget in het venster met de pack-layoutmanager.
        self.dagen_label.pack(anchor=tk.W, pady=(20, 0))  # type: ignore

        # Deze regel voert een onderdeel van de applicatielogica of interface-opbouw uit.
        self.update_prijs()

    # Methode die alle prijzen, korting, borg en het aantal dagen berekent.
    def bereken_prijs_values(self):
        """Interne berekening zonder type checker issues."""
        # Start een try-blok: code hierin kan een fout veroorzaken die later wordt opgevangen.
        try:
            # Haalt de geselecteerde datum uit het DateEntry-veld op.
            start = self.start_datum.get_date()
            # Haalt de geselecteerde datum uit het DateEntry-veld op.
            eind = self.eind_datum.get_date()
            # Maakt of wijzigt een variabele die later in de code gebruikt wordt.
            dagen = (eind - start).days
            # Controleert een voorwaarde; alleen als deze waar is wordt de onderliggende code uitgevoerd.
            if dagen < 1:
                # Maakt of wijzigt een variabele die later in de code gebruikt wordt.
                dagen = 1
                # Zet de datum van het DateEntry-veld naar een nieuwe waarde.
                self.eind_datum.set_date(start + timedelta(days=1))
        # Vangt een mogelijke fout af zodat het programma niet onverwacht crasht.
        except (ValueError, TypeError):
            # Maakt of wijzigt een variabele die later in de code gebruikt wordt.
            dagen = 1

        # Maakt of wijzigt een variabele die later in de code gebruikt wordt.
        self.dagen_label.config(text=f"Aantal huurdagen: {dagen}")

        # Haalt de huidige waarde uit een Tkinter-variabele of widget op.
        s_dames = max(0, self.aantal_stad_dames.get())
        # Haalt de huidige waarde uit een Tkinter-variabele of widget op.
        s_heren = max(0, self.aantal_stad_heren.get())
        # Haalt de huidige waarde uit een Tkinter-variabele of widget op.
        e_dames = max(0, self.aantal_elek_dames.get())
        # Haalt de huidige waarde uit een Tkinter-variabele of widget op.
        e_heren = max(0, self.aantal_elek_heren.get())

        # Gebruikt Decimal voor betrouwbare berekeningen met eurobedragen.
        totaal_stadsfietsen = Decimal(s_dames + s_heren)
        # Gebruikt Decimal voor betrouwbare berekeningen met eurobedragen.
        totaal_elektrisch = Decimal(e_dames + e_heren)
        # Berekent een onderdeel van de totaalprijs, borg of korting.
        totaal_fietsen = totaal_stadsfietsen + totaal_elektrisch

        # Gebruikt Decimal voor betrouwbare berekeningen met eurobedragen.
        prijs_stads = totaal_stadsfietsen * self.prijzen['stadfiets'] * Decimal(dagen)
        # Gebruikt Decimal voor betrouwbare berekeningen met eurobedragen.
        prijs_elek = totaal_elektrisch * self.prijzen['elektrisch'] * Decimal(dagen)
        # Berekent een onderdeel van de totaalprijs, borg of korting.
        verhuur_totaal = prijs_stads + prijs_elek

        # Maakt een lege lijst waarin de prijsregels voor de sidebar worden opgeslagen.
        details = []
        # Controleert een voorwaarde; alleen als deze waar is wordt de onderliggende code uitgevoerd.
        if totaal_stadsfietsen > 0:
            # Voegt een tekstregel toe aan de details-lijst.
            details.append(f"Stadsfietsen: {totaal_stadsfietsen}x\n  ↳ €{prijs_stads:.2f}")
        # Controleert een voorwaarde; alleen als deze waar is wordt de onderliggende code uitgevoerd.
        if totaal_elektrisch > 0:
            # Voegt een tekstregel toe aan de details-lijst.
            details.append(f"E-bikes: {totaal_elektrisch}x\n  ↳ €{prijs_elek:.2f}")
        # Controleert een voorwaarde; alleen als deze waar is wordt de onderliggende code uitgevoerd.
        if totaal_fietsen == 0:
            # Voegt een tekstregel toe aan de details-lijst.
            details.append("Geen fietsen geselecteerd.")

        # Controleert een voorwaarde; alleen als deze waar is wordt de onderliggende code uitgevoerd.
        if self.helm_var.get() and totaal_fietsen > 0:
            # Gebruikt Decimal voor betrouwbare berekeningen met eurobedragen.
            helm_totaal = self.prijzen['helm'] * Decimal(dagen)
            # Berekent een onderdeel van de totaalprijs, borg of korting.
            verhuur_totaal += helm_totaal
            # Voegt een tekstregel toe aan de details-lijst.
            details.append(f"Helm: €{helm_totaal:.2f}")

        # Controleert een voorwaarde; alleen als deze waar is wordt de onderliggende code uitgevoerd.
        if self.kinderzitje_var.get() and totaal_fietsen > 0:
            # Gebruikt Decimal voor betrouwbare berekeningen met eurobedragen.
            zitje_totaal = self.prijzen['kinderzitje'] * Decimal(dagen)
            # Berekent een onderdeel van de totaalprijs, borg of korting.
            verhuur_totaal += zitje_totaal
            # Voegt een tekstregel toe aan de details-lijst.
            details.append(f"Kinderzitje: €{zitje_totaal:.2f}")

        # Controleert een voorwaarde; alleen als deze waar is wordt de onderliggende code uitgevoerd.
        if self.terugkerend_var.get() and verhuur_totaal > 0:
            # Gebruikt Decimal voor betrouwbare berekeningen met eurobedragen.
            korting = verhuur_totaal * Decimal('0.10')
            # Berekent een onderdeel van de totaalprijs, borg of korting.
            verhuur_totaal -= korting
            # Voegt een tekstregel toe aan de details-lijst.
            details.append(f"Korting (10%): -€{korting:.2f}")

        # Berekent een onderdeel van de totaalprijs, borg of korting.
        borg_stads = totaal_stadsfietsen * self.borg['stadfiets']
        # Berekent een onderdeel van de totaalprijs, borg of korting.
        borg_elek = totaal_elektrisch * self.borg['elektrisch']
        # Berekent een onderdeel van de totaalprijs, borg of korting.
        borg_bedrag = borg_stads + borg_elek

        # Berekent een onderdeel van de totaalprijs, borg of korting.
        totaal_met_borg = verhuur_totaal + borg_bedrag
        # Geeft berekende waarden terug aan de plek waar de methode is aangeroepen.
        return totaal_met_borg, details, dagen, borg_bedrag, verhuur_totaal, totaal_fietsen

    # Methode die de actuele prijsberekening zichtbaar maakt in de interface.
    def update_prijs(self):
        """Updatet de interface-elementen met de actuele berekende prijzen."""
        # Berekent een onderdeel van de totaalprijs, borg of korting.
        totaal_met_borg, details, _, borg_bedrag, _, _ = self.bereken_prijs_values()
        # Maakt of wijzigt een variabele die later in de code gebruikt wordt.
        self.prijs_label.config(text=f"€{totaal_met_borg:.2f}")
        # Maakt of wijzigt een variabele die later in de code gebruikt wordt.
        self.prijs_details_label.config(text="\n".join(details))
        # Slaat de borgbedragen per fietstype op in een dictionary.
        self.borg_label.config(text=f"Borgsom (Inbegrepen):\n€{borg_bedrag:.2f}")

    # Methode die invoer valideert en daarna de reservering opslaat.
    def reserveer(self):
        """Valideert en slaat de reservering op in de database."""
        # Haalt de huidige waarde uit een Tkinter-variabele of widget op.
        naam = self.naam_var.get().strip()
        # Controleert een voorwaarde; alleen als deze waar is wordt de onderliggende code uitgevoerd.
        if not naam:
            # Toont een foutmelding aan de gebruiker.
            messagebox.showerror("Fout", "Voer een naam in")
            # Deze regel voert een onderdeel van de applicatielogica of interface-opbouw uit.
            self.naam_entry.focus_set()
            # Geeft berekende waarden terug aan de plek waar de methode is aangeroepen.
            return

        # Haalt de huidige waarde uit een Tkinter-variabele of widget op.
        email = self.email_var.get().strip()
        # Maakt of wijzigt een variabele die later in de code gebruikt wordt.
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,7}$'

        # Controleert een voorwaarde; alleen als deze waar is wordt de onderliggende code uitgevoerd.
        if not email or not re.fullmatch(email_pattern, email):
            # Toont een foutmelding aan de gebruiker.
            messagebox.showerror("Fout", "Voer een geldig emailadres in.")
            # Deze regel voert een onderdeel van de applicatielogica of interface-opbouw uit.
            self.email_entry.focus_set()
            # Geeft berekende waarden terug aan de plek waar de methode is aangeroepen.
            return

        # Berekent een onderdeel van de totaalprijs, borg of korting.
        totaal_met_borg, _, dagen, borg_bedrag, _, totaal_fietsen = self.bereken_prijs_values()
        # Controleert een voorwaarde; alleen als deze waar is wordt de onderliggende code uitgevoerd.
        if totaal_fietsen == 0:
            # Toont een foutmelding aan de gebruiker.
            messagebox.showerror("Fout", "Selecteer minimaal 1 fiets.")
            # Geeft berekende waarden terug aan de plek waar de methode is aangeroepen.
            return

        # Haalt de geselecteerde datum uit het DateEntry-veld op.
        start = self.start_datum.get_date()
        # Haalt de geselecteerde datum uit het DateEntry-veld op.
        eind = self.eind_datum.get_date()

        # Haalt de huidige datum en/of tijd op.
        reserverings_id = f"RES{datetime.now().strftime('%Y%m%d%H%M%S')}"
        # Haalt de huidige waarde uit een Tkinter-variabele of widget op.
        betaalmethode = self.betaalmethode_var.get()
        # Maakt of wijzigt een variabele die later in de code gebruikt wordt.
        betaalmethode_tekst = "iDEAL" if betaalmethode == 'ideal' else "PIN"
        # Maakt of wijzigt een variabele die later in de code gebruikt wordt.
        betaling_status = "Betaald" if betaalmethode == 'ideal' else "Bij afhalen"

        # Haalt de huidige datum en/of tijd op.
        datum = datetime.now().strftime("%Y-%m-%d %H:%M")
        # Zet een datum/tijd om naar een leesbare tekstnotatie.
        start_str = start.strftime("%d-%m-%Y")
        # Zet een datum/tijd om naar een leesbare tekstnotatie.
        eind_str = eind.strftime("%d-%m-%Y")

        # Start een try-blok: code hierin kan een fout veroorzaken die later wordt opgevangen.
        try:
            # Opent een bestand veilig; na afloop wordt het bestand automatisch gesloten.
            with open(self.csv_bestand, 'a', newline='', encoding='utf-8') as f:
                # Maakt een CSV-writer aan om rijen naar het CSV-bestand te schrijven.
                writer = csv.writer(f)
                # Schrijft één rij met gegevens naar het CSV-bestand.
                writer.writerow([
                    # Deze regel voert een onderdeel van de applicatielogica of interface-opbouw uit.
                    reserverings_id, datum, naam, email,
                    # Deze regel voert een onderdeel van de applicatielogica of interface-opbouw uit.
                    self.aantal_stad_dames.get(), self.aantal_stad_heren.get(),
                    # Deze regel voert een onderdeel van de applicatielogica of interface-opbouw uit.
                    self.aantal_elek_dames.get(), self.aantal_elek_heren.get(),
                    'Ja' if self.helm_var.get() else 'Nee', 'Ja' if self.kinderzitje_var.get() else 'Nee',
                    # Deze regel voert een onderdeel van de applicatielogica of interface-opbouw uit.
                    start_str, eind_str, str(dagen), 'Ja' if self.terugkerend_var.get() else 'Nee',
                    # Deze regel voert een onderdeel van de applicatielogica of interface-opbouw uit.
                    betaalmethode_tekst, f"{borg_bedrag:.2f}", f"{totaal_met_borg:.2f}", betaling_status, 'Actief'
                ])
        # Vangt een mogelijke fout af zodat het programma niet onverwacht crasht.
        except IOError as err:
            # Toont een foutmelding aan de gebruiker.
            messagebox.showerror("Fout", f"Kan reservering niet opslaan: {err}")
            # Geeft berekende waarden terug aan de plek waar de methode is aangeroepen.
            return

        # Maakt of wijzigt een variabele die later in de code gebruikt wordt.
        bevestiging_tekst = f"Succesvol Gereserveerd!\n\nID: {reserverings_id}\nNaam: {naam}\nAantal fietsen: " \
                            # Deze regel voert een onderdeel van de applicatielogica of interface-opbouw uit.
                            f"{int(totaal_fietsen)}\nPeriode: {start_str} tot {eind_str}\nTotaalbedrag (incl. borg): " \
                            # Deze regel voert een onderdeel van de applicatielogica of interface-opbouw uit.
                            f"€{totaal_met_borg:.2f}"
        # Toont een informatieve melding aan de gebruiker.
        messagebox.showinfo("Reservering Bevestigd", bevestiging_tekst)
        # Deze regel voert een onderdeel van de applicatielogica of interface-opbouw uit.
        self.reset_form()

    # Methode die het formulier terugzet naar de beginwaarden.
    def reset_form(self):
        """Zet alle velden in het formulier terug naar de standaardwaarde."""
        # Zet een Tkinter-variabele terug naar een nieuwe waarde.
        self.naam_var.set('')
        # Zet een Tkinter-variabele terug naar een nieuwe waarde.
        self.email_var.set('')
        # Zet een Tkinter-variabele terug naar een nieuwe waarde.
        self.aantal_stad_dames.set(0)
        # Zet een Tkinter-variabele terug naar een nieuwe waarde.
        self.aantal_stad_heren.set(0)
        # Zet een Tkinter-variabele terug naar een nieuwe waarde.
        self.aantal_elek_dames.set(0)
        # Zet een Tkinter-variabele terug naar een nieuwe waarde.
        self.aantal_elek_heren.set(0)
        # Zet een Tkinter-variabele terug naar een nieuwe waarde.
        self.helm_var.set(False)
        # Zet een Tkinter-variabele terug naar een nieuwe waarde.
        self.kinderzitje_var.set(False)
        # Zet de datum van het DateEntry-veld naar een nieuwe waarde.
        self.start_datum.set_date(datetime.now())
        # Zet de datum van het DateEntry-veld naar een nieuwe waarde.
        self.eind_datum.set_date(datetime.now() + timedelta(days=1))
        # Zet een Tkinter-variabele terug naar een nieuwe waarde.
        self.terugkerend_var.set(False)
        # Zet een Tkinter-variabele terug naar een nieuwe waarde.
        self.betaalmethode_var.set('ideal')
        # Deze regel voert een onderdeel van de applicatielogica of interface-opbouw uit.
        self.update_prijs()

    # Methode die een nieuw venster opent met alle opgeslagen reserveringen.
    def toon_reserveringen(self):
        """Toont een overzichtsvenster met alle opgeslagen reserveringen."""
        # Controleert of het opgegeven bestand al bestaat.
        if not os.path.exists(self.csv_bestand):
            # Toont een informatieve melding aan de gebruiker.
            messagebox.showinfo("Info", "Geen reserveringen gevonden")
            # Geeft berekende waarden terug aan de plek waar de methode is aangeroepen.
            return

        # Maakt een nieuw Tkinter-venster aan.
        window = tk.Toplevel(self.root)
        # Stelt de titel van het venster in zoals die bovenaan het scherm zichtbaar is.
        window.title("Reserveringen - Overzicht")
        # Bepaalt de grootte van het venster in pixels.
        window.geometry("1400x600")
        # Past eigenschappen van een widget aan, zoals achtergrondkleur of scrollbar-koppeling.
        window.configure(bg="#F4F4F4")

        # Maakt een frame aan; dit is een container waarin widgets netjes gegroepeerd worden.
        frame = ttk.Frame(window, padding=15)
        # Plaatst de widget in het venster met de pack-layoutmanager.
        frame.pack(fill=tk.BOTH, expand=True)  # type: ignore

        # Definieert de kolomnamen die in het reserveringenoverzicht worden getoond.
        columns = ('ReserveringsID', 'Datum', 'Naam', 'Email', 'StadDames', 'StadHeren', 'ElekDames', 'ElekHeren',
                   'Helm', 'Kinderzitje', 'Startdatum', 'Einddatum', 'Dagen', 'Terugkerend', 'Betaalmethode', 'Borg',
                   'Totaalprijs', 'BetalingStatus', 'Status')
        # Maakt een tabelweergave aan voor het reserveringenoverzicht.
        tree = ttk.Treeview(frame, columns=columns, show='headings', height=18)  # type: ignore

        # Herhaalt de code voor elk item in een reeks of lijst.
        for col in columns:
            # Stelt de kolomkop van de tabel in.
            tree.heading(col, text=col)
            # Controleert een voorwaarde; alleen als deze waar is wordt de onderliggende code uitgevoerd.
            if col == 'Email':
                # Stelt de breedte en uitlijning van een tabelkolom in.
                tree.column(col, width=140)
            # Controleert een tweede voorwaarde als de vorige if niet waar was.
            elif col in ['StadDames', 'StadHeren', 'ElekDames', 'ElekHeren', 'Dagen']:
                # Stelt de breedte en uitlijning van een tabelkolom in.
                tree.column(col, width=65, anchor=tk.CENTER)  # type: ignore
            else:
                # Stelt de breedte en uitlijning van een tabelkolom in.
                tree.column(col, width=85)

        # Maakt een verticale scrollbar voor de tabel.
        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=tree.yview)  # type: ignore
        # Past eigenschappen van een widget aan, zoals achtergrondkleur of scrollbar-koppeling.
        tree.configure(yscrollcommand=scrollbar.set)
        # Plaatst de widget in het venster met de pack-layoutmanager.
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)  # type: ignore
        # Plaatst de widget in het venster met de pack-layoutmanager.
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)  # type: ignore

        # Start een try-blok: code hierin kan een fout veroorzaken die later wordt opgevangen.
        try:
            # Opent een bestand veilig; na afloop wordt het bestand automatisch gesloten.
            with open(self.csv_bestand, 'r', encoding='utf-8') as f:
                # Maakt een CSV-reader aan om rijen uit het CSV-bestand te lezen.
                reader = csv.reader(f)
                # Deze regel voert een onderdeel van de applicatielogica of interface-opbouw uit.
                next(reader)
                # Herhaalt de code voor elk item in een reeks of lijst.
                for db_row in reader:
                    # Controleert een voorwaarde; alleen als deze waar is wordt de onderliggende code uitgevoerd.
                    if len(db_row) == len(columns):
                        # Voegt een reserveringsrij toe aan de tabel.
                        tree.insert('', tk.END, values=db_row)  # type: ignore
        # Vangt een mogelijke fout af zodat het programma niet onverwacht crasht.
        except IOError as err:
            # Toont een foutmelding aan de gebruiker.
            messagebox.showerror("Fout", f"Fout bij inlezen: {err}")
            # Sluit of vernietigt het betreffende venster.
            window.destroy()
            # Geeft berekende waarden terug aan de plek waar de methode is aangeroepen.
            return

        # Maakt een frame aan; dit is een container waarin widgets netjes gegroepeerd worden.
        btn_win_frame = ttk.Frame(window, padding=10)
        # Plaatst de widget in het venster met de pack-layoutmanager.
        btn_win_frame.pack()

        # Interne functie die een geselecteerde reservering annuleert volgens de 24-uursregel.
        def annuleer_reservering():
            # Haalt op welke rij de gebruiker in de tabel heeft geselecteerd.
            selection = tree.selection()
            # Controleert een voorwaarde; alleen als deze waar is wordt de onderliggende code uitgevoerd.
            if not selection:
                # Toont een waarschuwing aan de gebruiker.
                messagebox.showwarning("Waarschuwing", "Selecteer een reservering")
                # Geeft berekende waarden terug aan de plek waar de methode is aangeroepen.
                return

            # Haalt de gegevens op van de geselecteerde tabelrij.
            item = tree.item(selection[0])
            # Maakt of wijzigt een variabele die later in de code gebruikt wordt.
            values = item['values']

            # Controleert een voorwaarde; alleen als deze waar is wordt de onderliggende code uitgevoerd.
            if values[18] == 'Geannuleerd':
                # Toont een informatieve melding aan de gebruiker.
                messagebox.showinfo("Info", "Al geannuleerd")
                # Geeft berekende waarden terug aan de plek waar de methode is aangeroepen.
                return

            # Maakt of wijzigt een variabele die later in de code gebruikt wordt.
            target_id = values[0]
            # Maakt of wijzigt een variabele die later in de code gebruikt wordt.
            startdatum_str = values[10]

            # Start een try-blok: code hierin kan een fout veroorzaken die later wordt opgevangen.
            try:
                # Zet een tekstuele datum om naar een datetime-object.
                startdatum = datetime.strptime(startdatum_str, "%d-%m-%Y")
            # Vangt een mogelijke fout af zodat het programma niet onverwacht crasht.
            except ValueError:
                # Toont een foutmelding aan de gebruiker.
                messagebox.showerror("Fout", "Datumfout")
                # Geeft berekende waarden terug aan de plek waar de methode is aangeroepen.
                return

            # Controleert een voorwaarde; alleen als deze waar is wordt de onderliggende code uitgevoerd.
            if (startdatum - datetime.now()).total_seconds() / 3600 < 24:
                # Toont een foutmelding aan de gebruiker.
                messagebox.showerror("Fout", "Annuleren moet minimaal 24 uur van tevoren.")
                # Geeft berekende waarden terug aan de plek waar de methode is aangeroepen.
                return

            # Vraagt bevestiging aan de gebruiker en geeft True of False terug.
            if not messagebox.askyesno("Bevestig", f"Annuleer {target_id}?"):
                # Geeft berekende waarden terug aan de plek waar de methode is aangeroepen.
                return

            # Start een try-blok: code hierin kan een fout veroorzaken die later wordt opgevangen.
            try:
                # Opent een bestand veilig; na afloop wordt het bestand automatisch gesloten.
                with open(self.csv_bestand, 'r', encoding='utf-8') as file_in:
                    # Maakt een CSV-reader aan om rijen uit het CSV-bestand te lezen.
                    rows = list(csv.reader(file_in))
                # Herhaalt de code voor elk item in een reeks of lijst.
                for file_row in rows:
                    # Controleert een voorwaarde; alleen als deze waar is wordt de onderliggende code uitgevoerd.
                    if file_row[0] == target_id:
                        # Maakt of wijzigt een variabele die later in de code gebruikt wordt.
                        file_row[18] = 'Geannuleerd'
                        # Stopt de loop zodra de juiste reservering is gevonden.
                        break
                # Opent een bestand veilig; na afloop wordt het bestand automatisch gesloten.
                with open(self.csv_bestand, 'w', newline='', encoding='utf-8') as file_out:
                    # Maakt een CSV-writer aan om rijen naar het CSV-bestand te schrijven.
                    csv.writer(file_out).writerows(rows)
                # Sluit of vernietigt het betreffende venster.
                window.destroy()
                # Deze regel voert een onderdeel van de applicatielogica of interface-opbouw uit.
                self.toon_reserveringen()
            # Vangt een mogelijke fout af zodat het programma niet onverwacht crasht.
            except IOError as inner_err:
                # Toont een foutmelding aan de gebruiker.
                messagebox.showerror("Fout", f"Fout bij annuleren: {inner_err}")

        # Ook hier relief="flat" toegepast voor de overzichtsknoppen
        # Maakt een knop aan en koppelt deze via command aan een functie.
        tk.Button(btn_win_frame, text="ANNULEER RESERVERING", command=annuleer_reservering,
                  # Maakt of wijzigt een variabele die later in de code gebruikt wordt.
                  font=('Source Sans Pro', 10, 'bold'), bg='#5A7188', fg='#FFFFFF', relief="flat", pady=6,
                  # Plaatst de widget in een rij en kolom met de grid-layoutmanager.
                  padx=15).grid(row=0, column=0, padx=5)
        # Maakt een knop aan en koppelt deze via command aan een functie.
        tk.Button(btn_win_frame, text="SLUITEN", command=window.destroy, font=('Source Sans Pro', 10, 'bold'),
                  # Plaatst de widget in een rij en kolom met de grid-layoutmanager.
                  bg='#26384A', fg='#FFFFFF', relief="flat", pady=6, padx=15).grid(row=0, column=1, padx=5)


# Startfunctie van de applicatie; vanaf hier wordt het programma gestart.
def main():
    """Main startpunt van de applicatie."""
    # Maakt een nieuw Tkinter-venster aan.
    root = tk.Tk()
    # Start een try-blok: code hierin kan een fout veroorzaken die later wordt opgevangen.
    try:
        # Deze regel voert een onderdeel van de applicatielogica of interface-opbouw uit.
        root.wm_iconbitmap('jouw_logo.ico')
    # Vangt een mogelijke fout af zodat het programma niet onverwacht crasht.
    except (tk.TclError, IOError):
        # Doet bewust niets; gebruikt wanneer een fout genegeerd mag worden.
        pass
    # Deze regel voert een onderdeel van de applicatielogica of interface-opbouw uit.
    LoginWindow(root)
    # Start de Tkinter event-loop waardoor het venster blijft reageren op acties.
    root.mainloop()


# Controleert of dit bestand direct wordt uitgevoerd; dan wordt main() gestart.
if __name__ == "__main__":
    # Deze regel voert een onderdeel van de applicatielogica of interface-opbouw uit.
    main()
