import mysql.connector
import tkinter as tk
from tkinter import messagebox

conn = mysql.connector.connect(
  host="localhost",
  user="root", #votre user MySQL
  password="8520",  #votre MDP MySQL
  database="boutique"
)

window = tk.Tk()
window.title("Gestion des stocks")
width = 780
height = 500
window.geometry("780x500")
window.minsize(width,height)
window.maxsize(1000,height)


def ajouter_produit():
    nom = nom_entry.get()
    description = description_entry.get()
    prix = prix_entry.get()
    quantite = quantite_entry.get()
    categorie = categorie_var.get()

    if nom != "" and description != "" and prix != "" and quantite != "" and categorie != "":
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM categorie WHERE nom = %s", (categorie,))
        result = cursor.fetchone()
        if result:
            categorie_id = result[0]
        else:
            raise ValueError("Invalid category name: {}".format(categorie))

        cursor.execute("INSERT INTO produit (nom, description, prix, quantite, id_categorie) VALUES (%s, %s, %s, %s, %s)", (nom, description, prix, quantite, categorie_id))

        conn.commit()
        print("Produit ajouté avec succès !")
        cursor.close()
        messagebox.showinfo("Le produit a bien été ajouté.")

        nom_entry.delete(0, tk.END)
        description_entry.delete(0, tk.END)
        prix_entry.delete(0, tk.END)
        quantite_entry.delete(0, tk.END)
        categorie_menu.delete(0, tk.END)

    else:
        messagebox.showwarning("Champs manquants", "Veuillez remplir tous les champs !")

cursor = conn.cursor()
cursor.execute("SELECT nom FROM categorie")
categories = cursor.fetchall()
cursor.close()


def supprimer_produit():
    id_produit = id_entry.get()

    if id_produit == "":
        messagebox.showwarning("ID manquant", "Veuillez saisir l'ID du produit à supprimer.")
        return

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM produit WHERE id = %s", (id_produit,))
    produit = cursor.fetchone()
    cursor.close()

    if produit is None:
        messagebox.showwarning("ID invalide", f"L'ID {id_produit} ne correspond à aucun produit.")
        return

    confirmation = messagebox.askyesno("Confirmer la suppression", f"Voulez-vous vraiment supprimer le produit {produit[1]} ({produit[3]}€) ?")

    if confirmation:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM produit WHERE id = %s", (id_produit,))
        conn.commit()
        cursor.close()

        id_entry.delete(0, tk.END)
        quantite_modif_entry.delete(0, tk.END)
        afficher_produits()

def afficher_produits():
    cursor = conn.cursor()
    cursor.execute("SELECT id, nom, description, prix, quantite, id_categorie FROM produit")
    produits = cursor.fetchall()
    output_text.delete("1.0", tk.END)
    for produit in produits:
        output_text.insert(tk.END, f"{produit[0]} - {produit[1]} ({produit[3]}€) - quantité : {produit[4]} - {produit[2]}\n")
    cursor.close()

def modifier_quantite():
    id_produit = id_entry.get()
    quantite = quantite_modif_entry.get()

    if id_produit != "" and quantite != "":
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM produit WHERE id=%s", (id_produit,))
        produit = cursor.fetchone()
        if produit:
            cursor.execute("UPDATE produit SET quantite=%s WHERE id=%s", (quantite, id_produit))
            conn.commit()
            print("Quantité mise à jour.")
            id_entry.delete(0, tk.END)
            quantite_modif_entry.delete(0, tk.END)
            status_label.config(text="Quantité mise à jour.", fg="green")
        else:
            messagebox.showwarning("Produit introuvable", "Le produit avec cet ID n'existe pas.")
        cursor.close()
    else:
        messagebox.showwarning("Champs manquants", "Veuillez remplir tous les champs !")


# widgets
nom_label = tk.Label(window, text="Nom du produit :")
nom_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
nom_var = tk.StringVar()
nom_entry = tk.Entry(window, textvariable=nom_var)
nom_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)

status_label = tk.Label(window, text="", fg="red")
status_label.grid(row=9, column=0, columnspan=2, padx=5, pady=5)


description_label = tk.Label(window, text="Description du produit :")
description_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
description_var = tk.StringVar()
description_entry = tk.Entry(window, textvariable=description_var)
description_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)


prix_label = tk.Label(window, text="Prix du produit :")
prix_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
prix_var = tk.StringVar()
prix_entry = tk.Entry(window, textvariable=prix_var)
prix_entry.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)


quantite_label = tk.Label(window, text="Quantité en stock :")
quantite_label.grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
quantite_entry = tk.Entry(window)
quantite_entry.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)


categorie_var = tk.StringVar(window)
categorie_var.set(categories[0][0])
categorie_label = tk.Label(window, text="Catégorie :")
categorie_label.grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)
categorie_menu = tk.OptionMenu(window, categorie_var, *[cat[0] for cat in categories])
categorie_menu.grid(row=4, column=1, padx=5, pady=5, sticky=tk.W)


ajouter_button = tk.Button(window, text="Ajouter un produit", command=ajouter_produit)
ajouter_button.grid(row=5, column=1, padx=5, pady=5, sticky=tk.W)


id_label = tk.Label(window, text="ID du produit :")
id_label.grid(row=8, column=0, padx=5, pady=5, sticky=tk.W)
id_var = tk.StringVar()
id_entry = tk.Entry(window, textvariable=id_var)
id_entry.grid(row=8, column=1, padx=5, pady=5, sticky=tk.W)


quantite_modif_label = tk.Label(window, text="Nouvelle quantité :")
quantite_modif_label.grid(row=9, column=0, padx=5, pady=5, sticky=tk.W)
quantite_modif_var = tk.StringVar()
quantite_modif_entry = tk.Entry(window, textvariable=quantite_modif_var)
quantite_modif_entry.grid(row=9, column=1, padx=5, pady=5, sticky=tk.W)


modifier_button = tk.Button(window, text="Modifier la quantité", command=modifier_quantite)
modifier_button.grid(row=6, column=1, padx=5, pady=5, sticky=tk.W)


supprimer_button = tk.Button(window, text="Supprimer un produit", command=supprimer_produit)
supprimer_button.grid(row=7, column=1, padx=5, pady=5, sticky=tk.W)


afficher_button = tk.Button(window, text="Afficher les produits", command=afficher_produits)
afficher_button.grid(row=10, column=0, padx=5, pady=5, sticky=tk.W)
output_text = tk.Text(window, width=75, height=7)
output_text.grid(row=10, column=1, padx=5, pady=5)


status_label = tk.Label(window, text="")
status_label.grid(row=9, column=0, columnspan=2, padx=5, pady=5)

window.mainloop()