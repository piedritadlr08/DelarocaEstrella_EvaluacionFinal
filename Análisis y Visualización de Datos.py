import tkinter as tk
from tkinter import Toplevel, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class GraphApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Gráfica de Barras")
        self.geometry("800x600")

        self.column_names = ["Categoría"]
        self.data_values = []

        self.create_widgets()

    def create_widgets(self):
        self.category_label = tk.Label(self, text="Categoría")
        self.category_label.grid(row=0, column=0)

        self.value_label = tk.Label(self, text="Valor")
        self.value_label.grid(row=0, column=1)

        self.category_listbox = tk.Listbox(self, width=20)
        self.category_listbox.grid(row=1, column=0)

        self.value_listbox = tk.Listbox(self, width=20)
        self.value_listbox.grid(row=1, column=1)

        self.add_column_button = tk.Button(self, text="Agregar Columna", command=self.add_column)
        self.add_column_button.grid(row=2, column=0, columnspan=2)

        self.data_category_entry = tk.Entry(self)
        self.data_category_entry.grid(row=3, column=0)

        self.data_value_entry = tk.Entry(self)
        self.data_value_entry.grid(row=3, column=1)

        self.add_category_data_button = tk.Button(self, text="Datos Categoría", command=self.add_category_data)
        self.add_category_data_button.grid(row=4, column=0)

        self.add_value_data_button = tk.Button(self, text="Datos Valor", command=self.add_value_data)
        self.add_value_data_button.grid(row=4, column=1)

        self.edit_button = tk.Button(self, text="Editar", command=self.edit_data)
        self.edit_button.grid(row=5, column=0)

        self.delete_button = tk.Button(self, text="Eliminar Columna", command=self.delete_column)
        self.delete_button.grid(row=5, column=1)

        self.plot_button = tk.Button(self, text="Graficar", command=self.show_graph_popup)
        self.plot_button.grid(row=6, column=0, columnspan=2)

        self.fig = plt.Figure(figsize=(6, 6))
        self.bar_chart = None

    def add_column(self):
        self.column_names.append(f"Categoría {len(self.column_names)}")
        self.category_listbox.insert(tk.END, self.column_names[-1])
        self.value_listbox.insert(tk.END, "")

    def add_category_data(self):
        data_category = self.data_category_entry.get()
        if data_category:
            self.category_listbox.insert(tk.END, data_category)
            self.data_category_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Campo Vacío", "Llene el campo antes de subir los datos.")

    def add_value_data(self):
        data_value = self.data_value_entry.get()
        if data_value:
            self.value_listbox.insert(tk.END, data_value)
            self.data_value_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Campo Vacío", "Llene el campo antes de subir los datos.")

    def edit_data(self):
        selected_index = self.category_listbox.curselection()
        if selected_index:
            selected_index = selected_index[0]
            data_category = self.category_listbox.get(selected_index)
            data_value = self.value_listbox.get(selected_index)
            self.data_category_entry.delete(0, tk.END)
            self.data_category_entry.insert(tk.END, data_category)
            self.data_value_entry.delete(0, tk.END)
            self.data_value_entry.insert(tk.END, data_value)

    def delete_column(self):
        selected_index = self.category_listbox.curselection()
        if selected_index:
            selected_index = selected_index[0]
            self.category_listbox.delete(selected_index)
            self.value_listbox.delete(selected_index)

    def plot_graph(self):
        categories = self.category_listbox.get(0, tk.END)
        values = self.value_listbox.get(0, tk.END)

        if not categories or not values:
            messagebox.showwarning("Datos Faltantes", "Ingrese datos en ambas tablas antes de graficar.")
            return

        if self.bar_chart:
            self.bar_chart.get_tk_widget().destroy()

        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.bar(categories, values)
        ax.set_xlabel("Categoría")
        ax.set_ylabel("Valor")
        ax.set_title("Gráfica de Barras")
        ax.tick_params(axis='x', rotation=45)

        self.bar_chart = FigureCanvasTkAgg(self.fig, self)
        self.bar_chart.get_tk_widget().grid(row=7, column=0, columnspan=2)

    def show_graph_popup(self):
        categories = self.category_listbox.get(0, tk.END)
        values = self.value_listbox.get(0, tk.END)

        if not categories or not values:
            messagebox.showwarning("Datos Faltantes", "Ingrese datos en ambas tablas antes de graficar.")
            return

        popup_window = Toplevel(self)
        popup_window.title("Gráfica de Barras")
        popup_window.geometry("600x400")

        fig = plt.Figure(figsize=(6, 6))
        ax = fig.add_subplot(111)
        ax.bar(categories, values)
        ax.set_xlabel("Categoría")
        ax.set_ylabel("Valor")
        ax.set_title("Gráfica de Barras")
        ax.tick_params(axis='x', rotation=45)

        bar_chart = FigureCanvasTkAgg(fig, popup_window)
        bar_chart.get_tk_widget().pack(fill=tk.BOTH, expand=True)

if __name__ == "__main__":
    app = GraphApp()
    app.mainloop()
