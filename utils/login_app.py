import tkinter as tk
from tkinter import messagebox
import hashlib
import os
import re
from utils.saveJson import guardar_datos, cargar_datos

class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Login")
        self.root.geometry("400x350")
        self.root.configure(bg='#f0f0f0')
        
        self.db_file = "users-db.json"
        # Ahora self.users será una LISTA de diccionarios
        self.users = cargar_datos(self.db_file)
        
        self.create_widgets()
    
    def hash_password(self, password):
        #Hashea una contraseña con un salt y devuelve el salt + hash.
        salt = os.urandom(16)
        pwd_hash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
        return salt.hex() + ':' + pwd_hash.hex()

    def verify_password(self, stored_password, provided_password):
        #Verifica una contraseña ingresada contra una almacenada (salt+hash)
        try:
            salt_hex, hash_hex = stored_password.split(':')
            salt = bytes.fromhex(salt_hex)
            provided_hash = hashlib.pbkdf2_hmac('sha256', provided_password.encode('utf-8'), salt, 100000)
            return provided_hash.hex() == hash_hex
        except Exception as e:
            print(f"Error durante la verificación: {e}")
            return False

    def create_widgets(self):
        main_frame = tk.Frame(self.root, bg='#f0f0f0', padx=20, pady=20)
        main_frame.pack(expand=True, fill='both')
        title_label = tk.Label(main_frame, text="Inicio de Sesión", font=('Arial', 18, 'bold'), bg='#f0f0f0', fg='#333333')
        title_label.pack(pady=(0, 20))
        input_frame = tk.Frame(main_frame, bg='#f0f0f0')
        input_frame.pack(pady=5)
        user_label = tk.Label(input_frame, text="Usuario:", font=('Arial', 12), bg='#f0f0f0')
        user_label.grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.user_entry = tk.Entry(input_frame, font=('Arial', 12), width=20)
        self.user_entry.grid(row=0, column=1, padx=5, pady=5)
        self.user_entry.focus()
        pass_label = tk.Label(input_frame, text="Contraseña:", font=('Arial', 12), bg='#f0f0f0')
        pass_label.grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.pass_entry = tk.Entry(input_frame, font=('Arial', 12), width=20, show='*')
        self.pass_entry.grid(row=1, column=1, padx=5, pady=5)
        self.pass_entry.bind('<Return>', lambda event: self.login())
        button_frame = tk.Frame(main_frame, bg='#f0f0f0')
        button_frame.pack(pady=15)
        login_btn = tk.Button(button_frame, text="Iniciar Sesión", font=('Arial', 12, 'bold'), bg='#4CAF50', fg='white', width=15, command=self.login)
        login_btn.pack(pady=5)
        signin_btn = tk.Button(button_frame, text="Registrarse", font=('Arial', 12, 'bold'), bg="#4C65AF", fg='white', width=15, command=self.signin)
        signin_btn.pack(pady=5)
        clear_btn = tk.Button(main_frame, text="Limpiar", font=('Arial', 10), bg='#f44336', fg='white', width=10, command=self.clear_fields)
        clear_btn.pack(pady=10)


    def signin(self):
        """Registra un nuevo usuario en la lista de objetos."""
        username = self.user_entry.get().strip()
        password = self.pass_entry.get().strip()

        if not username or not password:
            messagebox.showerror("Error de Registro", "El usuario y la contraseña no pueden estar vacíos.")
            return

        # Parametros para la validación de una contraseña fuerte
        if len(password) < 8: messagebox.showerror("Contraseña Débil", "La contraseña debe tener al menos 8 caracteres."); return
        if not re.search(r"\d", password): messagebox.showerror("Contraseña Débil", "La contraseña debe contener al menos un número."); return
        if not re.search(r"[A-Z]", password): messagebox.showerror("Contraseña Débil", "La contraseña debe contener al menos una letra mayúscula."); return
        if not re.search(r"[!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>\/?]", password): messagebox.showerror("Contraseña Débil", "La contraseña debe contener al menos un carácter especial."); return
        
        # ### CAMBIO ESTRUCTURAL ###: Búsqueda de usuario en una lista
        # Ahora recorremos la lista para ver si el 'username' ya existe
        if any(user['username'] == username for user in self.users):
            messagebox.showerror("Error de Registro", "El nombre de usuario ya existe.")
            return
        
        hashed_password = self.hash_password(password)

        #Añadimos un nuevo objeto a la lista
        new_user = {
            "username": username,
            "password": hashed_password
        }
        self.users.append(new_user)
        
        # Guardamos la lista completa de vuelta en el JSON
        if guardar_datos(self.users, self.db_file):
            messagebox.showinfo("Registro Exitoso", f"Usuario '{username}' registrado de forma segura.")
            self.clear_fields()
        else:
            messagebox.showerror("Error de Registro", "No se pudo guardar el nuevo usuario.")

    def login(self):
        """Verifica las credenciales buscando al usuario en la lista."""
        username = self.user_entry.get().strip()
        password = self.pass_entry.get().strip()
        
        if not username or not password:
            messagebox.showerror("Error", "Por favor, complete todos los campos.")
            return
        #Aqui buscamos el usuario en la lista
        user_found = None
        for user in self.users:
            if user['username'] == username:
                user_found = user
                break
        
        if user_found:
            stored_password = user_found['password']
            if self.verify_password(stored_password, password):
                messagebox.showinfo("Éxito", f"¡Bienvenido, {username}!")
                self.open_dashboard(username)
            else:
                messagebox.showerror("Error", "Contraseña incorrecta.")
        else:
            messagebox.showerror("Error", "Usuario no encontrado.")
    
    def clear_fields(self):
        self.user_entry.delete(0, tk.END)
        self.pass_entry.delete(0, tk.END)
        self.user_entry.focus()
    
    def open_dashboard(self, username):
        self.root.destroy()
        dashboard = tk.Tk()
        dashboard.title("Dashboard Principal")
        dashboard.geometry("600x400")
        dashboard.configure(bg='#ffffff')
        welcome_label = tk.Label(dashboard, text=f"Bienvenido al Sistema, {username}!", font=('Arial', 16, 'bold'), bg='#ffffff', fg='#333333')
        welcome_label.pack(pady=50)
        logout_btn = tk.Button(dashboard, text="Cerrar Sesión", font=('Arial', 12), bg='#ff9800', fg='white', command=dashboard.quit)
        logout_btn.pack(pady=20)
        dashboard.mainloop()

def main():
    root = tk.Tk()
    window_width = 400
    window_height = 350
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    root.geometry(f'{window_width}x{window_height}+{x}+{y}')
    app = LoginApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()