import tkinter as tk
from environment import Environment
from algorithms import beam_search, dynamic_weighted_a_star,path_cost

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Hormiga busca el hongo 🐜🍄")

        #Configuración inicial
        self.size_var = tk.IntVar(value=10)
        self.beta_var = tk.IntVar(value=3)      # Parámetro beta para Beam Search
        self.epsilon_var = tk.DoubleVar(value=1.5)  # Parámetro epsilon para A*
        self.env = Environment(size=self.size_var.get())
        self.cell_size = 500 // self.env.size
        self.current_path = []  # Almacenar el camino encontrado
        self.current_step = 0   # Paso actual en la animación
        self.path_info_label = None  # Label para mostrar info

        #Canvas (área de dibujo) 
        self.canvas = tk.Canvas(root, width=500, height=500)
        self.canvas.pack(pady=10)

        #Label para información del camino
        self.path_info_label = tk.Label(root, text="", font=("Arial", 10), 
                                        justify=tk.LEFT, fg="blue")
        self.path_info_label.pack(pady=5)

        #Controles principales 
        controls = tk.Frame(root)
        controls.pack(pady=5)

        tk.Label(controls, text="Tamaño:").pack(side=tk.LEFT, padx=2)
        tk.Entry(controls, textvariable=self.size_var, width=4).pack(side=tk.LEFT, padx=2)
        tk.Button(controls, text="Aplicar", command=self.change_size).pack(side=tk.LEFT, padx=2)
        
        tk.Label(controls, text="| β:").pack(side=tk.LEFT, padx=2)
        tk.Entry(controls, textvariable=self.beta_var, width=4).pack(side=tk.LEFT, padx=2)
        
        tk.Label(controls, text="ε:").pack(side=tk.LEFT, padx=2)
        tk.Entry(controls, textvariable=self.epsilon_var, width=5).pack(side=tk.LEFT, padx=2)
        
        #Botones de algoritmos 
        algo_controls = tk.Frame(root)
        algo_controls.pack(pady=5)
        
        tk.Button(algo_controls, text="Beam Search", 
                 command=self.run_beam, bg="lightblue").pack(side=tk.LEFT, padx=5)
        tk.Button(algo_controls, text="Dynamic A*", 
                 command=self.run_dynamic, bg="lightgreen").pack(side=tk.LEFT, padx=5)
        tk.Button(algo_controls, text="Regenerar", 
                 command=self.reset).pack(side=tk.LEFT, padx=5)
        
        # Nuevos controles para la animación
        animation_controls = tk.Frame(root)
        animation_controls.pack(pady=5)
        
        tk.Button(animation_controls, text="Iniciar Animación", 
                 command=self.start_animation).pack(side=tk.LEFT, padx=5)
        tk.Button(animation_controls, text="Pausar", 
                 command=self.pause_animation).pack(side=tk.LEFT, padx=5)
        tk.Button(animation_controls, text="Siguiente", 
                 command=self.next_step).pack(side=tk.LEFT, padx=5)

        self.draw_grid()

    def draw_grid(self):
        """Dibuja el tablero mostrando el estado actual"""
        self.canvas.delete("all")
        self.cell_size = 500 // self.env.size
        
        for i in range(self.env.size):
            for j in range(self.env.size):
                x0, y0 = j * self.cell_size, i * self.cell_size
                x1, y1 = x0 + self.cell_size, y0 + self.cell_size
                color = "white"
                
                # Obstáculos
                if self.env.grid[i][j] == 'X':
                    color = "red"
                # Posición inicial
                elif (i, j) == self.env.start:
                    color = "blue"
                # Posición final
                elif (i, j) == self.env.goal:
                    color = "green"
                # Camino recorrido (pasos anteriores)
                elif (i, j) in self.current_path[:self.current_step]:
                    color = "yellow"
                # Posición actual de la hormiga
                elif (self.current_step > 0 and 
                      (i, j) == self.current_path[self.current_step - 1]):
                    color = "orange"
                
                self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="black")
                
                # Mostrar números de paso en las celdas del camino
                if (i, j) in self.current_path:
                    step_index = self.current_path.index((i, j))
                    if step_index < self.current_step:
                        self.canvas.create_text(x0 + self.cell_size//2, 
                                              y0 + self.cell_size//2,
                                              text=str(step_index + 1))

    def run_beam(self):
        """Ejecuta Beam Search y prepara la animación"""
        beta = self.beta_var.get()
        print(f"Ejecutando Beam Search (β={beta})...")

        path = beam_search(self.env, beta=beta)

        if path:
            # ✅ Calculamos el costo total del camino
            total_cost = path_cost(path, self.env)

            # Guardamos la ruta y reiniciamos pasos
            self.current_path = path
            self.current_step = 0

            print(f"Camino encontrado: {len(path)} pasos | Costo total: {total_cost}")

            # Redibuja el tablero
            self.draw_grid()

            # ✅ Muestra la información del algoritmo y del costo
            total_cost = path_cost(path, self.env)
            self.show_path_info(path, f"Beam Search (β={beta})", total_cost)

            
        else:
            print("No se encontró camino")
            self.current_path = []
            self.current_step = 0
            self.path_info_label.config(text=f"Beam Search (β={beta}): Sin camino")


    def run_dynamic(self):
        """Ejecuta Dynamic A* y prepara la animación"""
        epsilon = self.epsilon_var.get()
        print(f"🔍 Ejecutando Dynamic Weighted A* (ε={epsilon})...")
        path = dynamic_weighted_a_star(self.env, epsilon=epsilon)
        if path:
            self.current_path = path
            self.current_step = 0
            total_cost = path_cost(path, self.env)   # 🔹 calcula costo total
            print(f"✅ Camino encontrado: {len(path)} pasos | Costo total: {total_cost}")
            self.draw_grid()
            self.show_path_info(path, f"Dynamic A* (ε={epsilon})", total_cost)  # 🔹 pasa el costo al label
        else:
            print("No se encontró camino")
            self.current_path = []
            self.current_step = 0
            self.path_info_label.config(text=f"Dynamic A* (ε={epsilon}): Sin camino")

    def show_path_info(self, path, algorithm_name="Algoritmo", total_cost=None):
        """Muestra información sobre el camino encontrado"""
        print("\nINFORMACIÓN DEL CAMINO:")
        print(f"Algoritmo: {algorithm_name}")
        print(f"Inicio: {path[0]}")
        print(f"Meta: {path[-1]}")
        print(f"Longitud del camino: {len(path)} pasos")
        if total_cost is not None:
            print(f"Costo total: {total_cost}")
        print(f"Camino completo: {path}")
        
        info_text = f"{algorithm_name}: {len(path)} pasos"
        if total_cost is not None:
            info_text += f" | Costo total: {total_cost}"
        info_text += f" | Inicio: {path[0]} → Meta: {path[-1]}"
        self.path_info_label.config(text=info_text)


    def start_animation(self):
        """Inicia la animación automática del camino"""
        if not self.current_path:
            print(" Primero ejecuta un algoritmo")
            return
        
        self.animate_step()

    def animate_step(self):
        """Anima un paso del camino"""
        if self.current_step < len(self.current_path):
            self.draw_grid()
            self.current_step += 1
            # Programar siguiente paso después de 500ms
            self.root.after(500, self.animate_step)
        else:
            print("Animación completada!")

    def pause_animation(self):
        """Pausa la animación"""
        # Cancelar cualquier animación programada
        self.root.after_cancel(self.animate_step)

    def next_step(self):
        """Avanza un paso manualmente"""
        if self.current_path and self.current_step < len(self.current_path):
            self.current_step += 1
            self.draw_grid()
            
            # Mostrar información del paso actual
            current_pos = self.current_path[self.current_step - 1]
            print(f"Paso {self.current_step}: {current_pos}")
            
            if current_pos == self.env.goal:
                print("¡La hormiga llegó al hongo!")
        else:
            print("No hay más pasos o camino no definido")

    def reset(self):
        """Reinicia el entorno"""
        self.env.generate()
        self.current_path = []
        self.current_step = 0
        self.draw_grid()
        print("Entorno regenerado")

    def change_size(self):
        """Cambia el tamaño de la matriz"""
        try:
            new_size = int(self.size_var.get())
            if new_size < 3 or new_size > 30:
                raise ValueError
            self.env = Environment(size=new_size)
            self.current_path = []
            self.current_step = 0
            self.draw_grid()
            print(f" Tamaño cambiado a: {new_size}x{new_size}")
        except ValueError:
            print("Ingresa un número válido entre 3 y 30")


# Ejecutar la app
if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()