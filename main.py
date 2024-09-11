import tkinter as tk
from PIL import Image, ImageTk
from pubchempy import get_compounds, Compound
from bs4 import BeautifulSoup
import requests
import io
from rdkit import Chem
from rdkit.Chem import Draw

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack(fill="both", expand=True)
        self.create_widgets()

    def create_widgets(self):
        self.search_frame = tk.Frame(self)
        self.search_frame.pack(side="top", fill="x")

        self.compound_name_label = tk.Label(self.search_frame, text="Compound Name:")
        self.compound_name_label.pack(side="left")

        self.compound_name_entry = tk.Entry(self.search_frame)
        self.compound_name_entry.pack(side="left", expand=True, fill="x")

        self.search_button = tk.Button(self.search_frame)
        self.search_button["text"] = "Search"
        self.search_button["command"] = self.search_compound
        self.search_button.pack(side="left")

        self.result_frame = tk.Frame(self)
        self.result_frame.pack(side="top", fill="both", expand=True)

        self.image_label = tk.Label(self.result_frame)
        self.image_label.pack(side="top")

        self.info_label = tk.Label(self.result_frame, text="", wraplength=400)
        self.info_label.pack(side="top", fill="both", expand=True)

        self.exit_button = tk.Button(self)
        self.exit_button["text"] = "Exit"
        self.exit_button["command"] = self.master.destroy
        self.exit_button["bg"] = "red"
        self.exit_button["fg"] = "white"
        self.exit_button.pack(side="bottom", fill="x")

    def search_compound(self):
        compound_name = self.compound_name_entry.get()
        self.display_compound_info(compound_name)

    def get_compound_image(self, compound):
        smiles = compound.canonical_smiles
        mol = Chem.MolFromSmiles(smiles)
        img = Draw.MolToImage(mol)
        img_data = io.BytesIO()
        img.save(img_data, format='PNG')
        img_data.seek(0)
        return img_data

    def display_compound_info(self, compound_name):
        compounds = get_compounds(compound_name, 'name')
        if compounds:
            compound = compounds[0]
            img_data = self.get_compound_image(compound)
            img = Image.open(img_data)
            img = ImageTk.PhotoImage(img)
            self.image_label.image = img
            self.image_label.config(image=img)

            info_text = ""
            if compound.iupac_name:
                info_text += f"Compound Name: {compound.iupac_name}\n"
            if compound.molecular_formula:
                info_text += f"Molecular Formula: {compound.molecular_formula}\n"
            if compound.molecular_weight:
                if isinstance(compound.molecular_weight, (int, float)):
                    info_text += f"Molecular Weight: {compound.molecular_weight:.2f}\n"
                else:
                    info_text += f"Molecular Weight: {compound.molecular_weight}\n"
            if compound.synonyms:
                synonyms = compound.synonyms[:5]
                info_text += f"Synonyms: {', '.join(synonyms)}\n"
            if hasattr(compound, 'classification') and compound.classification:
                info_text += f"Class: {compound.classification[0].label}\n"
            self.info_label.config(text=info_text)
        else:
            self.image_label.config(image="")
            self.info_label.config(text="Compound not found in PubChem")

root = tk.Tk()
root.title("Compound Search")
root.geometry("400x600")  
app = Application(master=root)
app.mainloop()