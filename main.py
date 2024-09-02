import customtkinter as ctk
import tkinter.ttk as ttk
from ttkwidgets import CheckboxTreeview
import json

# Configura el tema de la aplicación
ctk.set_appearance_mode("dark")  # Cambia a "light" si prefieres un tema claro
ctk.set_default_color_theme("dark-blue")

# Crear la ventana principal
root = ctk.CTk()
root.title('Custom NOT')
root.geometry("700x300")
# Agregar un límite de tamaño mínimo para la ventana
root.minsize(650, 300)

# Función para cargar datos desde el archivo JSON
def load_programs():
    with open('config.json', 'r') as file:
        data = json.load(file)
        return data['programs'][0]  # Accedemos al primer elemento ya que JSON tiene una lista con un solo dict



def install_selected_programs():
    selected_programs = []

    print(f"--------------Total de programas: {install_button.cget("text")}------------------")
    for tab_name, tree in treeviews.items():
        for item in tree.get_children():
            if tree.item(item, 'tags') == ('checked',):
                program_name = tree.item(item, 'values')[0]
                selected_programs.append(program_name)
    
    if selected_programs:
        print(f"Installing: {', '.join(selected_programs)}")
    else:
        print("No programs selected.")

# Función para actualizar el texto del botón "Instalar"
def update_install_button(tree, install_button):
    selected_count = sum(1 for item in tree.get_children() if tree.item(item, 'tags') == ('checked',))
    
    # Actualiza el texto del botón
    install_button.configure(text=f"Install ({selected_count})")
    
    # Si no hay nada seleccionado, desactiva el botón y cámbialo a color gris
    if selected_count == 0:
        install_button.configure(state="disabled", fg_color="gray")
    else:
        # Si hay algo seleccionado, activa el botón y cámbialo a color verde
        install_button.configure(state="normal", fg_color="green")

# Funciones para seleccionar y limpiar la selección de checkboxes
def select_all(tree, install_button):
    for item in tree.get_children():
        tree.item(item, tags=('checked',))
    update_install_button(tree, install_button)

def clear_selection(tree, install_button):
    for item in tree.get_children():
        tree.item(item, tags=('unchecked',))  # Cambia 'checked' a 'unchecked'
    update_install_button(tree, install_button)

# Función para crear una lista de programas en un Tab
def create_program_list(tab_frame, program_list):
    list_frame = ctk.CTkFrame(tab_frame, fg_color="gray20")  # Cambia el color de fondo aquí
    list_frame.pack(side="left", fill="y", expand=False, padx=4, pady=10)

    tree = CheckboxTreeview(list_frame, columns=("name", "version", "date"))
    tree.pack(side="right", fill="both", expand=True)

    scrollbar = ctk.CTkScrollbar(list_frame, orientation="vertical")
    scrollbar.pack(side="right", fill="y")
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.configure(command=tree.yview)

    tree.column("#0", width=45, anchor="center", minwidth=45)
    tree.column("name", width=250, anchor="w", minwidth=200)
    tree.column("version", width=120, anchor="w", minwidth=100)
    tree.column("date", width=120, anchor="w", minwidth=80)

    tree.heading("#0", text="")
    tree.heading("name", text="Nombre")
    tree.heading("version", text="Versión")
    tree.heading("date", text="Fecha")

    # Insertar los programas en el CheckboxTreeview
    for program in program_list:
        tree.insert("", "end", text="", values=(program["display_name"], program["version"], program["update_date"]))

    return tree

# Crear el menú superior
menu_frame = ctk.CTkFrame(root, height=30)
menu_frame.pack(fill="x")

launcher_label = ctk.CTkLabel(menu_frame, text="Offline Launcher", text_color="white")
launcher_label.pack(side="left", padx=10)

# Crear el TabView
tabview = ctk.CTkTabview(root)
tabview.pack(side="left", expand=False, fill="y", padx=5, pady=5)

# Cargar los programas desde el archivo JSON
programs = load_programs()

# Diccionario para almacenar las referencias de los CheckboxTreeviews por pestaña
treeviews = {}

# Crear listas en las pestañas del TabView
for tab_name, program_list in programs.items():
    tab_frame = tabview.add(tab_name.capitalize())
    tree = create_program_list(tab_frame, program_list)
    treeviews[tab_name] = tree
    
    # Asociar la actualización del botón de instalación con el cambio de estado de los checkboxes
    tree.bind("<ButtonRelease-1>", lambda event, t=tree: update_install_button(t, install_button))

# Crear el frame para los botones al lado del TabView
button_frame = ctk.CTkFrame(root, width=180, height=150)
button_frame.pack(side="left", expand=False)
button_frame.pack_propagate(False)  # Evita que el Frame cambie de tamaño


# Botones
select_all_button = ctk.CTkButton(button_frame, text="Select ALL", text_color="white",
                                command=lambda: select_all_all_tabs(treeviews, install_button))
select_all_button.pack(side="top", pady=5)

clear_button = ctk.CTkButton(button_frame, text="Clear Selection", text_color="white",
                            command=lambda: clear_selection_all_tabs(treeviews, install_button))
clear_button.pack(side="top", pady=5)

install_button = ctk.CTkButton(button_frame, text="Install (0)", text_color="white", state="disabled", fg_color="gray")
install_button.pack(side="bottom", pady=(10, 10), fill="y")
install_button.configure(command=install_selected_programs)


# Funciones para seleccionar y limpiar la selección de todas las pestañas
def select_all_all_tabs(trees, install_button):
    for tree in trees.values():
        select_all(tree, install_button)

def clear_selection_all_tabs(trees, install_button):
    for tree in trees.values():
        clear_selection(tree, install_button)

# Actualizar la función del botón de instalación para manejar la selección total
def update_install_button(tree, install_button):
    selected_count = sum(
        sum(1 for item in t.get_children() if t.item(item, 'tags') == ('checked',))
        for t in treeviews.values()
    )
    
    # Actualiza el texto del botón
    install_button.configure(text=f"Install ({selected_count})")
    
    # Si no hay nada seleccionado, desactiva el botón y cámbialo a color gris
    if selected_count == 0:
        install_button.configure(state="disabled", fg_color="gray")
    else:
        # Si hay algo seleccionado, activa el botón y cámbialo a color verde
        install_button.configure(state="normal", fg_color="green")
        
        
# Iniciar la aplicación
root.mainloop()
