# Informe del Proyecto: Hormiga busca el hongo 🐜🍄

## Índice
1. [Descripción General](#descripción-general)
2. [Estructura del Proyecto](#estructura-del-proyecto)
3. [Módulo Environment](#módulo-environment)
4. [Módulo Algorithms](#módulo-algorithms)
5. [Módulo Main (Interfaz Gráfica)](#módulo-main-interfaz-gráfica)
6. [Funcionamiento de los Algoritmos](#funcionamiento-de-los-algoritmos)
7. [Guía de Uso](#guía-de-uso)

---

## Descripción General

Este proyecto implementa un simulador de búsqueda de caminos donde una hormiga debe encontrar el camino más corto hacia un hongo en un entorno con obstáculos (venenos). El proyecto utiliza dos algoritmos de búsqueda informada:

- **Beam Search**: Búsqueda por haz con ancho de beam configurable
- **Dynamic Weighted A***: A* con peso dinámico que se ajusta según la profundidad

La interfaz gráfica está desarrollada con **Tkinter** y permite visualizar el entorno, ejecutar los algoritmos y animar el recorrido paso a paso.

---

## Estructura del Proyecto

```
Inteligencia_Artificial/
├── environment.py      # Define el entorno (grid, obstáculos, posiciones)
├── algorithms.py       # Implementa Beam Search y Dynamic Weighted A*
├── main.py            # Interfaz gráfica con Tkinter
└── __pycache__/       # Archivos compilados de Python
```

---

## Módulo Environment

**Archivo**: `environment.py`

### Clase `Environment`

Esta clase representa el entorno donde la hormiga se mueve.

#### Constructor `__init__(self, size=10)`

```python
def __init__(self, size=10):
    self.size = size
    self.grid = [['.' for _ in range(size)] for _ in range(size)]
    self.start = (0, 0)
    self.goal = (size-1, size-1)
    self.generate()
```

**Parámetros:**
- `size`: Tamaño de la matriz cuadrada (por defecto 10x10)

**Atributos:**
- `self.size`: Dimensión del tablero
- `self.grid`: Matriz que representa el entorno (`.` = espacio libre, `X` = obstáculo)
- `self.start`: Posición inicial de la hormiga (esquina superior izquierda)
- `self.goal`: Posición del hongo (esquina inferior derecha)

#### Método `generate(self)`

Genera un nuevo entorno aleatorio:

1. **Limpia el tablero**: Inicializa todas las celdas con `.`
2. **Coloca obstáculos**: Añade aproximadamente `size × 1.5` obstáculos aleatorios marcados con `X`
3. **Coloca elementos clave**:
   - `A`: Hormiga en la posición inicial
   - `H`: Hongo en la posición objetivo

**Nota**: Los obstáculos nunca se colocan en las posiciones de inicio o meta.

#### Método `get_neighbors(self, node)`

Devuelve los vecinos válidos de un nodo (celda) dado.

```python
def get_neighbors(self, node):
    x, y = node
    moves = [(1,0), (-1,0), (0,1), (0,-1)]
    neighbors = []
    for dx, dy in moves:
        nx, ny = x+dx, y+dy
        if 0 <= nx < self.size and 0 <= ny < self.size:
            if self.grid[nx][ny] != 'X':
                neighbors.append((nx, ny))
    return neighbors
```

**Funcionamiento:**
- Considera movimientos en 4 direcciones: arriba, abajo, izquierda, derecha
- Valida que el vecino esté dentro de los límites del tablero
- Excluye celdas con obstáculos (`X`)

---

## Módulo Algorithms

**Archivo**: `algorithms.py`

Este módulo implementa los algoritmos de búsqueda.

### Función `heuristic(a, b)`

Calcula la **distancia de Manhattan** entre dos puntos:

```python
def heuristic(a, b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])
```

**Fórmula**: `h(a, b) = |ax - bx| + |ay - by|`

Esta heurística es **admisible** (nunca sobreestima el costo real) y **consistente**, lo que la hace ideal para A*.

---

### Algoritmo 1: Beam Search

```python
def beam_search(env, beta):
```

**Parámetros:**
- `env`: Instancia del entorno
- `beta`: Ancho del beam (número de nodos a mantener en cada nivel)

**Características:**
- Búsqueda por niveles (como BFS)
- En cada nivel, mantiene solo los `β` nodos más prometedores según la heurística
- Reduce el uso de memoria pero **no garantiza encontrar el camino óptimo**

**Algoritmo:**

1. **Inicialización**:
   - Frontera con el nodo inicial: `[(h, nodo, camino)]`
   - Conjunto de visitados para evitar ciclos

2. **Bucle principal**:
   ```python
   while frontier:
       # Ordenar por heurística y mantener solo β mejores
       frontier.sort(key=lambda x: x[0])
       frontier = frontier[:beta]
       
       new_frontier = []
       for h_val, node, path in frontier:
           if node == goal:
               return path
           
           # Expandir vecinos
           for neighbor in env.get_neighbors(node):
               if neighbor not in visited:
                   visited.add(neighbor)
                   h_neighbor = heuristic(neighbor, goal)
                   new_frontier.append((h_neighbor, neighbor, path + [neighbor]))
       
       frontier = new_frontier
   ```

3. **Retorno**: Camino encontrado o `None` si no hay solución

**Ventajas:**
- Eficiente en memoria (limitado por β)
- Más rápido que búsqueda exhaustiva

**Desventajas:**
- No garantiza optimalidad
- Puede fallar si β es muy pequeño

---

### Algoritmo 2: Dynamic Weighted A*

```python
def dynamic_weighted_a_star(env, epsilon=1.5):
```

**Parámetros:**
- `env`: Instancia del entorno
- `epsilon`: Factor de peso para la heurística (ε ≥ 1)

**Características:**
- Variante de A* con peso dinámico que disminuye con la profundidad
- Usa **heap** para mantener la frontera ordenada eficientemente
- Más exploratorio al inicio, más preciso cerca de la meta

**Algoritmo:**

1. **Inicialización**:
   ```python
   counter = 0  # Para desempatar nodos con mismo f
   frontier = [(0, counter, start, [start], 0, 0)]
   # Formato: (f_score, contador, nodo, camino, g_score, profundidad)
   visited = set()
   N = env.size * env.size
   ```

2. **Función de evaluación**:
   ```python
   weight = 1 + epsilon * (1 - (depth / N))
   f = g + weight * h
   ```
   
   Donde:
   - `g`: Costo real desde el inicio (número de pasos)
   - `h`: Heurística (distancia de Manhattan)
   - `weight`: Peso dinámico que decrece con la profundidad
   - `depth`: Profundidad actual
   - `N`: Número total de celdas

3. **Bucle principal**:
   ```python
   while frontier:
       f, _, node, path, g, d = heapq.heappop(frontier)
       
       if node in visited:
           continue
       visited.add(node)
       
       if node == goal:
           return path

       for neighbor in env.get_neighbors(node):
           if neighbor not in visited:
               g_new = g + 1
               h = heuristic(neighbor, goal)
               depth_new = d + 1
               
               weight = 1 + epsilon * (1 - (depth_new / N))
               f_new = g_new + weight * h
               
               counter += 1
               heapq.heappush(frontier, 
                             (f_new, counter, neighbor, path + [neighbor], g_new, depth_new))
   ```

**Ventajas:**
- Más flexible que A* estándar
- El peso dinámico permite balancear exploración y explotación
- Con ε = 1.0, se comporta como A* clásico

**Desventajas:**
- No garantiza optimalidad si ε > 1
- Mayor uso de memoria que Beam Search

---

## Módulo Main (Interfaz Gráfica)

**Archivo**: `main.py`

### Clase `App`

Implementa la interfaz gráfica usando **Tkinter**.

#### Constructor `__init__(self, root)`

Inicializa la aplicación con:

**Variables de configuración:**
```python
self.size_var = tk.IntVar(value=10)           # Tamaño del grid
self.beta_var = tk.IntVar(value=3)            # Parámetro β para Beam Search
self.epsilon_var = tk.DoubleVar(value=1.5)    # Parámetro ε para A*
```

**Estado de la aplicación:**
```python
self.env = Environment(size=self.size_var.get())
self.cell_size = 500 // self.env.size
self.current_path = []  # Camino encontrado
self.current_step = 0   # Paso actual en animación
```

**Componentes de la interfaz:**

1. **Canvas** (500x500 px): Área de dibujo del grid
2. **Label informativo**: Muestra información del camino
3. **Controles principales**: Tamaño, β, ε
4. **Botones de algoritmos**: Beam Search, Dynamic A*, Regenerar
5. **Controles de animación**: Iniciar, Pausar, Siguiente

---

#### Método `draw_grid(self)`

Dibuja el tablero con colores según el estado:

```python
def draw_grid(self):
    self.canvas.delete("all")
    self.cell_size = 500 // self.env.size
    
    for i in range(self.env.size):
        for j in range(self.env.size):
            x0, y0 = j * self.cell_size, i * self.cell_size
            x1, y1 = x0 + self.cell_size, y0 + self.cell_size
            color = "white"
            
            # Determinar color según tipo de celda
            if self.env.grid[i][j] == 'X':
                color = "red"  # Obstáculo
            elif (i, j) == self.env.start:
                color = "blue"  # Inicio
            elif (i, j) == self.env.goal:
                color = "green"  # Meta
            elif (i, j) in self.current_path[:self.current_step]:
                color = "yellow"  # Camino recorrido
            elif (self.current_step > 0 and 
                  (i, j) == self.current_path[self.current_step - 1]):
                color = "orange"  # Posición actual
            
            self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="black")
            
            # Números de paso
            if (i, j) in self.current_path:
                step_index = self.current_path.index((i, j))
                if step_index < self.current_step:
                    self.canvas.create_text(x0 + self.cell_size//2, 
                                          y0 + self.cell_size//2,
                                          text=str(step_index + 1))
```

**Código de colores:**
- 🔴 Rojo: Obstáculos (venenos)
- 🔵 Azul: Posición inicial (hormiga)
- 🟢 Verde: Posición objetivo (hongo)
- 🟡 Amarillo: Camino recorrido
- 🟠 Naranja: Posición actual de la hormiga
- ⚪ Blanco: Celdas libres

---

#### Método `run_beam(self)`

Ejecuta el algoritmo Beam Search:

```python
def run_beam(self):
    beta = self.beta_var.get()
    print(f"Ejecutando Beam Search (β={beta})...")
    path = beam_search(self.env, beta=beta)
    if path:
        self.current_path = path
        self.current_step = 0
        print(f"✅ Camino encontrado: {len(path)} pasos")
        self.draw_grid()
        self.show_path_info(path, f"Beam Search (β={beta})")
    else:
        print("❌ No se encontró camino")
        self.current_path = []
        self.current_step = 0
        self.path_info_label.config(text=f"Beam Search (β={beta}): Sin camino")
```

---

#### Método `run_dynamic(self)`

Ejecuta el algoritmo Dynamic Weighted A*:

```python
def run_dynamic(self):
    epsilon = self.epsilon_var.get()
    print(f"🔍 Ejecutando Dynamic Weighted A* (ε={epsilon})...")
    path = dynamic_weighted_a_star(self.env, epsilon=epsilon)
    if path:
        self.current_path = path
        self.current_step = 0
        print(f"✅ Camino encontrado: {len(path)} pasos")
        self.draw_grid()
        self.show_path_info(path, f"Dynamic A* (ε={epsilon})")
    else:
        print("❌ No se encontró camino")
        self.current_path = []
        self.current_step = 0
        self.path_info_label.config(text=f"Dynamic A* (ε={epsilon}): Sin camino")
```

---

#### Método `show_path_info(self, path, algorithm_name)`

Muestra información detallada del camino:

```python
def show_path_info(self, path, algorithm_name="Algoritmo"):
    print("\nINFORMACIÓN DEL CAMINO:")
    print(f"Algoritmo: {algorithm_name}")
    print(f"🐜 Inicio: {path[0]}")
    print(f"🍄 Meta: {path[-1]}")
    print(f"📏 Longitud del camino: {len(path)} pasos")
    print(f"Camino completo: {path}")
    
    # Actualizar label en la interfaz
    info_text = f"{algorithm_name}: {len(path)} pasos | Inicio: {path[0]} → Meta: {path[-1]}"
    self.path_info_label.config(text=info_text)
```

---

#### Métodos de Animación

**`start_animation(self)`**: Inicia la animación automática
```python
def start_animation(self):
    if not self.current_path:
        print("⚠️ Primero ejecuta un algoritmo")
        return
    self.animate_step()
```

**`animate_step(self)`**: Anima un paso cada 500ms
```python
def animate_step(self):
    if self.current_step < len(self.current_path):
        self.draw_grid()
        self.current_step += 1
        self.root.after(500, self.animate_step)
    else:
        print("✅ Animación completada!")
```

**`pause_animation(self)`**: Pausa la animación
```python
def pause_animation(self):
    self.root.after_cancel(self.animate_step)
```

**`next_step(self)`**: Avanza manualmente un paso
```python
def next_step(self):
    if self.current_path and self.current_step < len(self.current_path):
        self.current_step += 1
        self.draw_grid()
        current_pos = self.current_path[self.current_step - 1]
        print(f"Paso {self.current_step}: {current_pos}")
        if current_pos == self.env.goal:
            print("🎉 ¡La hormiga llegó al hongo!")
    else:
        print("⚠️ No hay más pasos o camino no definido")
```

---

#### Otros Métodos

**`reset(self)`**: Regenera el entorno
```python
def reset(self):
    self.env.generate()
    self.current_path = []
    self.current_step = 0
    self.draw_grid()
    print("🔄 Entorno regenerado")
```

**`change_size(self)`**: Cambia el tamaño del tablero
```python
def change_size(self):
    try:
        new_size = int(self.size_var.get())
        if new_size < 3 or new_size > 30:
            raise ValueError
        self.env = Environment(size=new_size)
        self.current_path = []
        self.current_step = 0
        self.draw_grid()
        print(f"✅ Tamaño cambiado a: {new_size}x{new_size}")
    except ValueError:
        print("❌ Ingresa un número válido entre 3 y 30")
```

---

## Funcionamiento de los Algoritmos

### Comparación: Beam Search vs Dynamic Weighted A*

| Característica | Beam Search | Dynamic Weighted A* |
|---------------|-------------|---------------------|
| **Tipo** | Búsqueda local por haz | Búsqueda informada |
| **Parámetro** | β (ancho del beam) | ε (factor de peso) |
| **Optimalidad** | No garantizada | No garantizada (si ε > 1) |
| **Memoria** | O(β × niveles) | O(nodos expandidos) |
| **Velocidad** | Rápida | Media |
| **Completitud** | No garantizada | Garantizada* |

*Si existe un camino y ε es razonable

### Efecto de los Parámetros

**β (Beam Search):**
- β pequeño (1-3): Más rápido pero puede no encontrar camino
- β medio (4-8): Balance entre velocidad y éxito
- β grande (>10): Se acerca a BFS, más lento pero más confiable

**ε (Dynamic A*):**
- ε = 1.0: A* clásico (óptimo)
- ε = 1.5-2.0: Más rápido, soluciones subóptimas aceptables
- ε > 2.0: Muy exploratorio, menos preciso

---

## Guía de Uso

### 1. Ejecutar la aplicación

```bash
python main.py
```

### 2. Configurar parámetros

- **Tamaño**: Ajusta el tamaño de la matriz (3-30)
- **β**: Define el ancho del beam para Beam Search
- **ε**: Define el factor de peso para Dynamic A*

### 3. Ejecutar algoritmos

- Click en **"Beam Search"**: Ejecuta búsqueda por haz
- Click en **"Dynamic A*"**: Ejecuta A* con peso dinámico
- Click en **"Regenerar"**: Crea un nuevo entorno aleatorio

### 4. Visualizar resultados

- El camino encontrado se muestra en la consola
- La interfaz muestra: inicio (azul), meta (verde), obstáculos (rojo)

### 5. Animar el camino

- **"Iniciar Animación"**: Reproduce el camino automáticamente (500ms por paso)
- **"Pausar"**: Detiene la animación
- **"Siguiente"**: Avanza un paso manualmente

### 6. Interpretar resultados

- Los números en las celdas indican el orden del recorrido
- La celda naranja muestra la posición actual de la hormiga
- Las celdas amarillas muestran el camino ya recorrido

---

## Conclusiones

Este proyecto demuestra:

1. **Implementación de algoritmos de IA**: Beam Search y Weighted A*
2. **Visualización interactiva**: Interfaz gráfica con Tkinter
3. **Comparación de algoritmos**: Diferentes enfoques para el mismo problema
4. **Aplicación práctica**: Búsqueda de caminos en entornos con obstáculos

El código es modular, bien estructurado y fácil de extender para agregar nuevos algoritmos o funcionalidades.

---

**Autor**: David  
**Fecha**: 2025  
**Lenguaje**: Python 3  
**Librerías**: tkinter, heapq, random, math
