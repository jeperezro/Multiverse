import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as ttk
import math
import time

import ctypes

class My_List:
    def __init__(self):
        self.size = 0  # Number of elements in the list
        self.capacity = 1  # Default capacity
        self.array = self._make_array(self.capacity)
    
    def _make_array(self, capacity):
        """Creates a new array with the given capacity using ctypes."""
        return (capacity * ctypes.py_object)()
    
    def append(self, item):
        """Adds an element to the end of the list, resizing if necessary."""
        if self.size == self.capacity:
            self._resize(2 * self.capacity)  # Double capacity
        
        self.array[self.size] = item
        self.size += 1
    
    def insert(self, index, item):
        """Inserts an element at the specified index, shifting elements if needed."""
        if not 0 <= index <= self.size:
            raise IndexError("Index out of range")
        
        if self.size == self.capacity:
            self._resize(2 * self.capacity)
        
        for i in range(self.size, index, -1):  # Shift elements right
            self.array[i] = self.array[i - 1]
        
        self.array[index] = item
        self.size += 1

    def remove(self, value):
        """Removes the first occurrence of the specified value."""
        for i in range(self.size):
            if self.array[i] == value:
                self.pop(i)
                return
        raise ValueError("Value not found in list")
    
    def pop(self, index=None):
        """Removes and returns an item at a given index (or the last item by default)."""
        if self.size == 0:
            raise IndexError("Pop from empty list")

        if index is None:
            index = self.size - 1  # Default to last element
        
        if index < 0:  
            index += self.size  # Convert negative index to positive
        
        if not 0 <= index < self.size:
            raise IndexError("Index out of range")

        item = self.array[index]

        # Shift elements left to fill the gap
        for i in range(index, self.size - 1):
            self.array[i] = self.array[i + 1]

        self.array[self.size - 1] = None  # Avoid memory leak
        self.size -= 1

        # Shrink capacity if needed
        if self.size > 0 and self.size == self.capacity // 4:
            self._resize(self.capacity // 2)

        return item
    
    def clear(self):
        """Removes all elements from the list."""
        self.size = 0
        self.capacity = 1
        self.array = self._make_array(self.capacity)

    def _resize(self, new_capacity):
        """Resizes internal array to a new capacity."""
        new_array = self._make_array(new_capacity)
        
        for i in range(self.size):
            new_array[i] = self.array[i]
        
        self.array = new_array
        self.capacity = new_capacity
    
    def __len__(self):
        """Returns the number of elements in the list."""
        return self.size
    
    def __getitem__(self, index):
        """Retrieves an item at a given index."""
        if not 0 <= index < self.size:
            raise IndexError("Index out of range")
        return self.array[index]
    
    def __setitem__(self, index, value):
        """Sets an item at a given index."""
        if not 0 <= index < self.size:
            raise IndexError("Index out of range")
        self.array[index] = value
    
    def __repr__(self):
        """String representation of the list."""
        return f"([{', '.join(repr(self.array[i]) for i in range(self.size))}])"

class My_Dict:
    def __init__(self):
        self.keys = My_List()
        self.values = My_List()
    
    def __setitem__(self, key, value):
        """Sets or updates a key-value pair in the dictionary."""
        for i in range(len(self.keys)):
            if self.keys[i] == key:
                self.values[i] = value
                return
        self.keys.append(key)
        self.values.append(value)
    
    def __getitem__(self, key):
        """Retrieves the value associated with a given key."""
        for i in range(len(self.keys)):
            if self.keys[i] == key:
                return self.values[i]
        raise KeyError("Key not found")
    
    def __delitem__(self, key):
        """Removes a key-value pair from the dictionary."""
        for i in range(len(self.keys)):
            if self.keys[i] == key:
                self.keys.pop(i)  # Remove key at index i
                self.values.pop(i)  # Remove corresponding value
                return
        raise KeyError("Key not found")

    def __contains__(self, key):
        """Checks if a key exists in the dictionary."""
        for i in range(len(self.keys)):
            if self.keys[i] == key:
                return True
        return False
    
    def __iter__(self):
        """Iterates over keys in the dictionary."""
        for i in range(len(self.keys)):
            yield self.keys[i]

    def __len__(self):
        """Returns the number of key-value pairs."""
        return len(self.keys)

    def get(self, key, default=None):
        """Retrieves a value for a key, or returns default if the key does not exist."""
        for i in range(len(self.keys)):
            if self.keys[i] == key:
                return self.values[i]
        return default
    
    def keys(self):
        """Returns a My_List containing all keys."""
        keys_list = My_List()
        for key in self.keys:
            keys_list.append(key)
        return keys_list

    def values(self):
        """Returns a My_List containing all unique values."""
        values_list = My_List()
        for value in self.values:
            # Manually check if value already exists in values_list
            is_unique = True
            for existing_value in values_list:
                if existing_value == value:
                    is_unique = False
                    break
            if is_unique:
                values_list.append(value)
        return values_list

    def items(self):
        """Returns an iterator of (key, value) pairs."""
        for i in range(len(self.keys)):
            yield (self.keys[i], self.values[i])

    def pop(self, key, default=None):
        """Removes the specified key and returns its value. 
        If the key does not exist, return default (or raise KeyError if no default is provided)."""
        for i in range(len(self.keys)):
            if self.keys[i] == key:
                value = self.values.pop(i)  # Remove the value
                self.keys.pop(i)  # Remove the corresponding key
                return value
        if default is not None:
            return default
        raise KeyError(f"Key {key} not found")

    def __repr__(self):
        """String representation of the dictionary."""
        return f"{{{', '.join(f'{repr(self.keys[i])}: {repr(self.values[i])}' for i in range(len(self.keys)))}}}"

class My_Directed_Graph:
    def __init__(self):
        """Initialize an empty adjacency list using My_Dict."""
        self.graph = My_Dict()

    def add_vertex(self, vertex):
        """Add a vertex to the graph if it doesn't already exist."""
        if vertex not in self.graph:
            self.graph[vertex] = My_List()

    def add_edge(self, from_vertex, to_vertex):
        """Add a directed edge from one vertex to another."""
        if from_vertex not in self.graph:
            self.add_vertex(from_vertex)
        if to_vertex not in self.graph:
            self.add_vertex(to_vertex)
        self.graph[from_vertex].append(to_vertex)

    def remove_edge(self, from_vertex, to_vertex):
        """Remove a specific directed edge from the graph."""
        if from_vertex in self.graph:
            new_adj_list = My_List()
            for neighbor in self.graph[from_vertex]:
                if neighbor != to_vertex:
                    new_adj_list.append(neighbor)
            self.graph[from_vertex] = new_adj_list  # Replace with filtered list

    def remove_vertex(self, vertex):
        if vertex in self.graph:
            del self.graph[vertex]  # Remove the vertex itself

            for v in self.graph:
                new_list = My_List()  # Create an empty My_List instance
                for neighbor in self.graph[v]:
                    if neighbor != vertex:
                        new_list.append(neighbor)  # Add elements one by one

                self.graph[v] = new_list  # Assign the updated list back

    def has_edge(self, from_vertex, to_vertex):
        """Check if an edge exists between two vertices."""
        return from_vertex in self.graph and to_vertex in self.graph[from_vertex]

    def get_vertices(self):
        """Return a My_List of all vertices in the graph."""
        return self.graph.keys

    def get_edges(self):
        """Return a My_List of all directed edges in the graph."""
        edges = My_List()
        for vertex in self.graph:
            for neighbor in self.graph[vertex]:
                edges.append((vertex, neighbor))
        return edges  # Now returns a My_List
        
    def get_neighbors(self, vertex):
        """Returns a My_List of neighbors for a given vertex."""
        neighbors = My_List()
        if vertex in self.graph:
            for i in range(len(self.graph[vertex])):
                neighbors.append(self.graph[vertex][i])
        return neighbors

    def display(self):
        """Display the adjacency list of the graph."""
        print("Graph Representation (Adjacency List):")
        for vertex in self.graph:
            print(f"{vertex} --> {(self.graph[vertex])}")  # Convert to list for better readability

    def display_vertex_connections(self, vertex):
        """Return a string with the adjacency list of one vertex in the graph"""
        str = f"{vertex} --> {self.graph[vertex]}"
        return str


class My_Zn_verse:
    def __init__(self, a, n):
        if not (isinstance(a, int) and isinstance(n, int)):
            raise TypeError("Both a and n must be integers.")
        if n <= 1:
            raise ValueError("n must be greater than 1.")
        if not (0 <= a < n):
            raise ValueError("a must be in the range 0 <= a < n.")
        
        self.a = a
        self.n = n
    
    def contains(self, k):
        return isinstance(k, int) and (k - self.a) % self.n == 0
    
    def generate(self, lower, upper):
        if not (isinstance(lower, int) and isinstance(upper, int)):
            raise TypeError("Bounds must be integers.")
        if lower > upper:
            raise ValueError("Lower bound must be <= upper bound.")
        start = self.a if self.a >= lower else lower + (self.n - (lower - self.a) % self.n) % self.n
        return [k for k in range(start, upper + 1, self.n)]
    
    def __repr__(self):
        return f"[{self.a}]ℤ{self.n}"
    
    def __contains__(self, k):
        return self.contains(k)
    
    def __eq__(self, other):
        return isinstance(other, My_Zn_verse) and self.n == other.n and self.a % self.n == other.a % self.n
    
    def __hash__(self):
        return hash((self.a % self.n, self.n))

class My_Multiverse:
    def __init__(self):
        self.graph = My_Directed_Graph()
        self.initialize_multiverse()

    def initialize_multiverse(self):
        sets = My_List()  # Use My_List instead of a standard list
        for n in [2,3,4,6,8,9,12]:  
            sets.append(n)  # Add elements to My_List
        
        for i in range(len(sets)):  # Iterate through My_List using indexing
            n = sets[i]
            for a in range(n):  
                universe = My_Zn_verse(a, n)
                self.graph.add_vertex(universe)
                
                # 🔹 Fix: Establish connections immediately

        self._create_connections()

    
    def _create_connections(self):
        """Update all valid connections between universes, preventing duplicates."""
        vertices = self.graph.get_vertices()
        
        for universe1 in vertices:
            # Create a new list to track unique connections
            unique_connections = My_List()
            
            for universe2 in vertices:
                if universe1 != universe2:
                    # Check if universe1 can transition into universe2
                    connection_condition = (
                        universe2.a % universe1.n == universe1.a % universe1.n and
                        universe2.n % universe1.n == 0
                    )
                    
                    # Additional check to prevent excessive connections
                    is_duplicate = False
                    for existing_connection in unique_connections:
                        if existing_connection == universe2:
                            is_duplicate = True
                            break
                    
                    if connection_condition and not is_duplicate and len(unique_connections) < 6:
                        unique_connections.append(universe2)
            
            # Clear existing edges and add only unique connections
            self.graph.graph[universe1] = unique_connections


    
    def add_universe(self, a, n):
        universe = My_Zn_verse(a, n)
        if universe not in self.graph.get_vertices():
            self.graph.add_vertex(universe)
            
    
    def remove_universe(self, a, n):
        universe = My_Zn_verse(a, n)
        if universe in self.graph.get_vertices():
            self.graph.remove_vertex(universe)

    def get_related_universes(self, universe):
        """Returns all universes related to the given universe."""
        related = My_List()
        
        # Check for universes that have the current universe as a neighbor
        for vertex in self.graph.get_vertices():
            # Check if current universe is a neighbor of vertex
            neighbors = self.graph.get_neighbors(vertex)
            is_neighbor = False
            for i in range(len(neighbors)):
                if neighbors[i] == universe:
                    is_neighbor = True
                    break
            
            if is_neighbor:
                related.append(vertex)
        
        # Also check if the current universe has any neighbors
        current_neighbors = self.graph.get_neighbors(universe)
        for i in range(len(current_neighbors)):
            # Add any neighbors that aren't already in the list
            neighbor = current_neighbors[i]
            is_already_added = False
            for j in range(len(related)):
                if related[j] == neighbor:
                    is_already_added = True
                    break
            
            if not is_already_added:
                related.append(neighbor)
        
        return related
    
    def display_multiverse(self):
        self.graph.display()

class Multiverse_Model:
    def __init__(self):
        self.root = ttk.Window(themename="darkly")
        self.root.title("THE ZN-VERSE")
        
        self.canvas = ttk.Canvas(self.root, bg="black", width=800, height=600)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        window_width = 850
        window_height = 850

        _x = (screen_width - window_width) // 2
        _y = (screen_height - window_height - 70) // 2

        self.root.geometry(f"{window_width}x{window_height}+{_x}+{_y}")
        
        self.multiverse = My_Multiverse()
        self.universe_objects = My_Dict()
        self.orbits = My_Dict()
        self.labels = My_Dict()
        self.base_radii = My_Dict()
        self.base_periods = My_Dict()
        self.start_times = My_Dict()
        self.scale_factor = 1.0
        self.start_time = time.time()
        
        self.mod_uno = self.canvas.create_oval(390, 290, 410, 310, fill="white", outline="white")
        
        self.canvas.bind("<ButtonPress-1>", self.start_pan)
        self.canvas.bind("<B1-Motion>", self.pan)
        self.canvas.bind("<MouseWheel>", self.zoom)
        
        self.universe_traveler_frame = ttk.Frame(self.root)
        self.universe_traveler_frame.pack(side=tk.LEFT, fill=tk.Y)
        ttk.Label(self.universe_traveler_frame, text="Universe connections:").pack()
        ttk.Label(self.universe_traveler_frame, text="Insert universe to find connections:").pack()
        
        self.travel_entry_frame = ttk.Frame(self.universe_traveler_frame)
        self.travel_entry_frame.pack()

        ttk.Label(self.travel_entry_frame).pack(side="left", padx=10)
        ttk.Label(self.travel_entry_frame, text="[").pack(side="left")
        self.universe_a_entry = ttk.Entry(self.travel_entry_frame)
        self.universe_a_entry.pack(side="left", pady=4)
        ttk.Label(self.travel_entry_frame, text="]").pack(side="left")
        ttk.Label(self.travel_entry_frame, text="ℤ").pack(side="left")
        self.universe_zn_entry = ttk.Entry(self.travel_entry_frame)
        self.universe_zn_entry.pack(side="left", pady=4)
        ttk.Label(self.travel_entry_frame).pack(side="left", padx=10)

        self.find_connection_btn = ttk.Button(self.universe_traveler_frame, text="Find connections", command=self.get_universe_on_entry)
        self.find_connection_btn.pack(pady=6)

        self.reset_connection_btn = ttk.Button(self.universe_traveler_frame, text="Reset connections", command=self.reset_connections)
        self.reset_connection_btn.pack(pady=6)

        self.universe_manager_frame = ttk.Frame(self.root)
        self.universe_manager_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        ttk.Label(self.universe_manager_frame, text="Manage Universes:").pack()
        
        self.orbit_frame = ttk.Frame(self.universe_manager_frame)
        self.orbit_frame.pack()
        self.orbit_label = ttk.Label(self.orbit_frame, text="Insert value for universe's orbit (modulo) -->")
        self.orbit_label.pack(side="left")
        self.orbit_entry = ttk.Entry(self.orbit_frame)
        self.orbit_entry.pack(side="right")
        
        self.universe_frame = ttk.Frame(self.universe_manager_frame)
        self.universe_frame.pack()
        self.universe_label = ttk.Label(self.universe_frame, text="Insert value for universe's (equivalence class)")
        self.universe_label.pack(side="left")
        self.universe_entry = ttk.Entry(self.universe_frame)
        self.universe_entry.pack(side="right")
        
        self.add_universe_btn = ttk.Button(self.universe_manager_frame, text="Add Universe", command=self.add_universe)
        self.add_universe_btn.pack(pady=6)
        self.remove_planet_btn = ttk.Button(self.universe_manager_frame, text="Remove Universe", command=self.remove_universe)
        self.remove_planet_btn.pack(pady=3)

        self.remove_orbit_btn = ttk.Button(self.universe_manager_frame, text="Remove Orbit", command=self.remove_orbit)
        self.remove_orbit_btn.pack(pady=6)
        
        self.last_update_time = time.time()

        self.initialize_universes()
        self.update_universes()

        self.root.protocol('WM_DELETE_WINDOW', self.on_close)
        self.root.bind("<Escape>", lambda event: self.on_close())

        self.selected_universes = My_List()  # Track selected universes
        self.original_colors = {}  # Store original colors of universes


    def initialize_universes(self):
        """Draws all universes stored in My_Multiverse at startup."""
        self.multiverse.display_multiverse()
        for universe in self.multiverse.graph.get_vertices():  
            self.draw_universe(universe.a, universe.n)  # Just draw, don't re-add

    def find_universe_connections(self, universe):
        self.multiverse._create_connections()
        # Get all related universes
        related_universes = self.multiverse.get_related_universes(universe)
        print(related_universes)

        # 🔹 Ensure the universe exists in the canvas
        n, a = universe.n, universe.a
        if (n in self.universe_objects) and (a in self.universe_objects[n]):
            # Store the original color
            self.original_colors[(n, a)] = self.canvas.itemcget(self.universe_objects[n][a], "fill")
            # Highlight selected universe in white
            self.canvas.itemconfig(self.universe_objects[n][a], fill="white")
            self.selected_universes.append(My_Zn_verse(a, n))
        else:
            print(f"Warning: Universe {universe} not found in universe_objects.")

        # 🔹 Highlight related universes in cyan
        for related_universe in related_universes:
            rn, ra = related_universe.n, related_universe.a
            if (rn in self.universe_objects) and (ra in self.universe_objects[rn]):
                # Store the original color
                self.original_colors[(rn, ra)] = self.canvas.itemcget(self.universe_objects[rn][ra], "fill")
                # Change to cyan
                self.canvas.itemconfig(self.universe_objects[rn][ra], fill="red")
                self.selected_universes.append(My_Zn_verse(ra, rn))
            else:
                print(f"Warning: Related universe {related_universe} not found in universe_objects.")

        # 🔹 Get and display connections
        the_message = self.multiverse.graph.display_vertex_connections(universe)
        messagebox.showinfo(title=f"{repr(universe)} connections:", message=the_message)


    def reset_connections(self):
        # Reset previously selected universes to their original colors
        for universe in self.selected_universes:
            self.canvas.itemconfig(self.universe_objects[universe.n][universe.a], fill=self.original_colors[(universe.n, universe.a)])

        # Clear selection tracking
        self.selected_universes.clear()
        self.original_colors.clear()

    def get_universe_on_entry(self):
        try:
            a = int(self.universe_a_entry.get())
            n = int(self.universe_zn_entry.get())
            universe = My_Zn_verse(a, n)

            if universe not in self.multiverse.graph.get_vertices():
                messagebox.showerror(title="Error", message=f"Universe [{a}]ℤ{n} does not exist in Multiverse.")
                return

            # Get all related universes
            self.find_universe_connections(universe)

        except ValueError:
            messagebox.showerror(title="Value Error", message="Please enter valid integer values for a and n.")


    def add_universe(self):
        try:
            n = int(self.orbit_entry.get())
            a = int(self.universe_entry.get())

            if not (0 <= a < n and n > 1):
                messagebox.showerror(
                    title="Entry Error", 
                    message="Value for orbit should be greater than 1.\nValue for planet should range from 0 to n-1."
                )
                return

            universe = My_Zn_verse(a, n)

            # Explicit duplicate check using custom list iteration
            is_duplicate = False
            for existing_universe in self.multiverse.graph.get_vertices():
                if existing_universe == universe:
                    is_duplicate = True
                    break

            if is_duplicate:
                messagebox.showerror(
                    title="Entry Error", 
                    message=f"Universe {repr(universe)} already exists."
                )
                return  

            # Add the universe to My_Multiverse
            self.multiverse.add_universe(a, n)

            # Update connections for ALL universes
            self.multiverse._create_connections()
            
            # Draw the universe
            self.draw_universe(a, n)

            self.multiverse.display_multiverse()

        except ValueError:
            messagebox.showerror(title="Value Error", message="Inserted value type is not allowed.\nAn integer is expected.")

    def remove_universe(self):
        try:
            n = int(self.orbit_entry.get())
            a = int(self.universe_entry.get())
            universe = My_Zn_verse(a, n)

            # Ensure the universe exists
            if universe in self.multiverse.graph.get_vertices():
                if n in self.universe_objects and a in self.universe_objects[n]:
                    self.canvas.delete(self.universe_objects[n].pop(a))

                if n in self.labels and a in self.labels[n]:
                    self.canvas.delete(self.labels[n].pop(a))

                # Remove the universe from My_Multiverse
                self.multiverse.remove_universe(a, n)

                # Carefully remove edges, preventing duplicates
                vertices = list(self.multiverse.graph.get_vertices())
                for existing_universe in vertices:
                    # Create a new filtered list of neighbors
                    new_neighbors = My_List()
                    for neighbor in self.multiverse.graph.graph[existing_universe]:
                        if neighbor != universe:
                            new_neighbors.append(neighbor)
                    
                    # Update the graph's adjacency list
                    self.multiverse.graph.graph[existing_universe] = new_neighbors

                # Recreate connections to ensure clean state
                self.multiverse._create_connections()
                self.multiverse.display_multiverse()

            else:
                messagebox.showerror(title="Universe Not Found", message="The specified universe does not exist.")

        except ValueError:
            messagebox.showerror(title="Value Error", message="Inserted value is not allowed.\nAn integer is expected.")

    def draw_universe(self, a, n):
        """Draws a universe on the canvas without modifying My_Multiverse."""
        if n not in self.base_radii:
            self.base_radii[n] = 60 * n
            self.base_periods[n] = max(1.0, n*5)
            self.orbits[n] = self.canvas.create_oval(-self.base_radii[n],
                                                    -self.base_radii[n],
                                                    self.base_radii[n],
                                                    self.base_radii[n],
                                                    outline="gray", dash=(5, 2))
            self.universe_objects[n] = My_Dict()
            self.labels[n] = My_Dict()
            self.start_times[n] = My_Dict()

        color = ["gray", "yellow", "blue", "dark magenta"][n % 4]
        universe = {"size": 7, "color": color}

        if n % 2 == 1:
            initial_angle = (a * 2 * math.pi) / n  
            self.start_times[n][a] = self.start_time - (initial_angle * self.base_periods[n]) / (2 * math.pi)
        else:
            initial_angle = math.pi / n  
            self.start_times[n][a] = self.start_time - (initial_angle * self.base_periods[n])

        x = 400 + self.base_radii[n] * math.cos(initial_angle)
        y = 300 + self.base_radii[n] * math.sin(initial_angle)

        universe_obj = self.canvas.create_oval(x - 40, y - 40, x + 40, y + 40, fill=universe["color"], outline=universe["color"])
        self.universe_objects[n][a] = universe_obj

        label = self.canvas.create_text(x + 10, y - 10, text=f"[{a}]ℤ{n}", fill="white", font=("Arial", 9))
        self.labels[n][a] = label

    def remove_orbit(self):
        try:
            n = int(self.orbit_entry.get())
            vertices_to_remove = [v for v in self.multiverse.graph.get_vertices() if v.n == n]

            for v in vertices_to_remove:
                a = v.a
                self.canvas.delete(self.universe_objects[n].pop(a))
                self.canvas.delete(self.labels[n].pop(a))
                self.multiverse.remove_universe(a, n)

            self.canvas.delete(self.orbits.pop(n))
            self.base_radii.pop(n)
            self.base_periods.pop(n)
            self.universe_objects.pop(n)
            self.labels.pop(n)
        except ValueError:
            messagebox.showerror(title="Value Error", message="Inserted value is not allowed.\nAn integer is expected.")

    def update_universes(self):
        current_time = time.time()
        self.last_update_time = current_time

        for n in self.base_radii:
            scaled_radius = self.scale_factor * self.base_radii[n]

            for a in self.start_times.get(n, {}):
                elapsed_time = current_time - self.start_times[n][a]
                angle = (2 * math.pi * elapsed_time) / self.base_periods[n] + (a * 2 * math.pi / n)

                x = 400 + scaled_radius * math.cos(angle)
                y = 300 + scaled_radius * math.sin(angle)
                size = self.scale_factor * 7

                if n in self.universe_objects and a in self.universe_objects[n]:
                    self.canvas.coords(self.universe_objects[n][a], x - size, y - size, x + size, y + size)

                if n in self.labels and a in self.labels[n]:
                    self.canvas.coords(self.labels[n][a], x + 10, y - 10)

                if n in self.orbits:
                    self.canvas.coords(self.orbits[n], 400 - scaled_radius, 300 - scaled_radius, 
                                    400 + scaled_radius, 300 + scaled_radius)

        self.root.after(30, self.update_universes)
        
    def start_pan(self, event):
        self.canvas.scan_mark(event.x, event.y)
        
    def pan(self, event):
        self.canvas.scan_dragto(event.x, event.y, gain=1)
        
    def zoom(self, event):
        factor = 1.1 if event.delta > 0 else 0.9
        self.scale_factor *= factor

    def on_close(self):
        result = messagebox.askokcancel('Confirm', 'Ready to go?\nUnsaved changes will be deleted.')
        if result:
            self.root.destroy()

    def run(self):
        self.root.mainloop()
        
if __name__ == "__main__":
    try:
        main = Multiverse_Model()
        main.run()
        
    except KeyboardInterrupt:
        print("Application interrupted by user.")
