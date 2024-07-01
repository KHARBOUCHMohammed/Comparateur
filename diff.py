import os
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from PIL import Image, ImageTk
import pandas as pd

def compare_files():
    dir_path = entry_dir.get()

    if not dir_path:
        messagebox.showerror("Erreur", "Veuillez fournir le chemin du dossier contenant les fichiers à comparer.")
        return

    # Modification ici pour enlever l'extension '.txt' lors de la collecte des noms des fichiers
    txt_files = [os.path.splitext(file)[0] for file in os.listdir(dir_path) if file.endswith(".txt")]

    if len(txt_files) < 2:
        messagebox.showerror("Erreur", "Le dossier doit contenir au moins deux fichiers .txt pour la comparaison.")
        return

    all_packages = set()
    file_contents = {}
    empty_files = []
    file_vide = []

    # Trouver les éléments communs à tous les fichiers
    common_elements = set()
    is_first_file = True
    for file_name_with_extension in os.listdir(dir_path):
        if file_name_with_extension.endswith(".txt"):
            file_path = os.path.join(dir_path, file_name_with_extension)
            if os.path.getsize(file_path) == 0:  # Vérifier si le fichier est vide
                empty_files.append(os.path.splitext(file_name_with_extension)[0])  # Ajouter le nom du fichier vide à la liste
                continue  # Passer au fichier suivant sans traiter le fichier vide
            with open(file_path, 'r') as file:
                current_file_elements = {line.split()[0] for line in file if line.strip()}
                if is_first_file:
                    common_elements = current_file_elements
                    is_first_file = False
                else:
                    common_elements &= current_file_elements
                all_packages.update(current_file_elements)
                file_contents[os.path.splitext(file_name_with_extension)[0]] = current_file_elements

    file_vide = empty_files
    comparison_text = "Paquets communs dans tous les fichiers:\n" + "\n".join(sorted(common_elements)) + "\n\n"

    # Exclure les éléments communs du tableau de résultats
    unique_packages = all_packages - common_elements

    # Après avoir identifié les fichiers vides et avant de commencer la comparaison
    txt_files = [file_name for file_name in txt_files if os.path.splitext(file_name + '.txt')[0] not in empty_files]

    # Préparation des données pour Excel avec les noms des fichiers sans l'extension '.txt'
    common_data = pd.DataFrame(sorted(common_elements), columns=["Paquets communs"])
    unique_data_rows = [[package] + ["Oui" if package in file_contents[file_name] else "Non" for file_name in txt_files] for package in sorted(unique_packages)]
    unique_data = pd.DataFrame(unique_data_rows, columns=["Paquet"] + txt_files)

    # Écriture dans un fichier Excel
    with pd.ExcelWriter('resultats_paquets.xlsx', engine='xlsxwriter') as writer:
        common_data.to_excel(writer, sheet_name='Paquets Communs', index=False)
        unique_data.to_excel(writer, sheet_name='Tableau Paquets', index=False)

    result_table = "Paquet\t" + "\t".join(txt_files) + "\n"
    for package in sorted(unique_packages):
        row = [package] + ["Oui" if package in file_contents[file_name] else "Non" for file_name in txt_files]
        result_table += "\t".join(row) + "\n"

    # Affichage dans la zone de texte (facultatif)
    text_output.config(state=tk.NORMAL)
    text_output.delete('1.0', tk.END)
    text_output.insert(tk.END, "les fichier ignorée \n\n")
    text_output.insert(tk.END,file_vide )
    text_output.insert(tk.END, "\n\n")
    text_output.insert(tk.END, comparison_text)
    text_output.insert(tk.END, result_table)
    text_output.insert(tk.END, "Paquets communs et tableau des paquets écrits dans 'resultats_paquets.xlsx'")
    text_output.config(state=tk.DISABLED)




def browse_dir():
    # Fonction pour sélectionner le dossier
    dir_path = filedialog.askdirectory()
    entry_dir.delete(0, tk.END)
    entry_dir.insert(0, dir_path)

def copy_to_clipboard():
    # Fonction pour copier le texte de la zone de texte dans le presse-papiers
    text_output.clipboard_clear()
    text_output.clipboard_append(text_output.get('1.0', tk.END))

# Création de la fenêtre principale
root = tk.Tk()
root.title("Comparateur de fichiers texte dans un dossier")


# Chargement de l'image du logo
logo_img = Image.open("int.jpg")  
logo_img = logo_img.resize((200, 100))  
logo_img = ImageTk.PhotoImage(logo_img)

# Cadre pour le logo
frame_logo = tk.Frame(root, bg="lightgray")
frame_logo.pack()

# Affichage du logo
logo_label = tk.Label(frame_logo, image=logo_img, bg="lightgray")
logo_label.pack()

# Cadre pour les entrées de dossier
frame_dir = tk.Frame(root, padx=10, pady=10, relief=tk.SUNKEN, borderwidth=2, bg="lightblue")
frame_dir.pack(fill=tk.BOTH, padx=10, pady=(10, 5))

# Champ de texte pour le dossier
label_dir = tk.Label(frame_dir, text="Dossier :", padx=5, pady=5, bg="lightblue")
label_dir.grid(row=0, column=0, sticky=tk.E)
entry_dir = tk.Entry(frame_dir, width=50)
entry_dir.grid(row=0, column=1, padx=50)
button_browse = tk.Button(frame_dir, text="Parcourir", command=browse_dir, bg="lightgreen")
button_browse.grid(row=0, column=2, padx=5)

# Bouton pour comparer les fichiers
button_compare = tk.Button(root, text="Comparer", command=compare_files, padx=10, pady=5, bg="orange", fg="white")
button_compare.pack(pady=5)

# Zone de texte pour afficher les résultats (scrolledtext pour défilement)
text_output = scrolledtext.ScrolledText(root, height=20, width=80, wrap=tk.WORD)
text_output.pack(padx=20, pady=(0, 5), fill=tk.BOTH, expand=True)
text_output.config(state=tk.NORMAL)
# Bouton pour copier le texte
button_copy = tk.Button(root, text="Copier le texte", command=copy_to_clipboard, padx=10, pady=5, bg="lightgreen")
button_copy.pack(pady=(5, 10))

# Lancement de la boucle principale
root.mainloop()

