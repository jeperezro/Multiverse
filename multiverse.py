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
    
    def pop(self, index=None):
        """Removes and returns an item at a given index (or the last item by default)."""
        if self.size == 0:
            raise IndexError("Pop from empty list")

        if index is None:
            index = self.size - 1  # Default to last element
        elif not 0 <= index < self.size:
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

    
    def __repr__(self):
        """String representation of the list."""
        return f"([{', '.join(repr(self.array[i]) for i in range(self.size))}])"

class My_Dict:
    def __init__(self):
        self.keys = My_List()
        self.values = My_List()
    
    def __setitem__(self, key, value):
        for i in range(len(self.keys)):
            if self.keys[i] == key:
                self.values[i] = value
                return
        self.keys.append(key)
        self.values.append(value)
    
    def __getitem__(self, key):
        for i in range(len(self.keys)):
            if self.keys[i] == key:
                return self.values[i]
        raise KeyError("Key not found")
    
    def __delitem__(self, key):
        """Remove a key-value pair from the dictionary."""
        for i in range(len(self.keys)):
            if self.keys[i] == key:
                self.keys.pop(i)  # Remove key at index i
                self.values.pop(i)  # Remove corresponding value
                return
        raise KeyError("Key not found")  # Raise error if key does not exist

    
    def __contains__(self, key):
        for i in range(len(self.keys)):
            if self.keys[i] == key:
                return True
        return False
    
    def __iter__(self):
        """Iterate over keys in MyDict efficiently."""
        for i in range(len(self.keys)):
            yield self.keys[i]
    
    def items(self):
        return [(self.keys[i], self.values[i]) for i in range(len(self.keys))]

class My_Directed_Graph:
    def __init__(self):
        """Initialize an empty adjacency list using MyDict."""
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
            filtered_list = My_List()
            for item in self.graph[from_vertex]:
                if item != to_vertex:
                    filtered_list.append(item)
            self.graph[from_vertex] = filtered_list

    def remove_vertex(self, vertex):
        """Remove a vertex and all edges pointing to it."""
        if vertex in self.graph:
            del self.graph[vertex]  # Remove the vertex

        # Remove references to vertex from all adjacency lists
        for v in self.graph:
            for i in range(len(self.graph[v]) - 1, -1, -1):  # Iterate in reverse to avoid shifting issues
                if self.graph[v][i] == vertex:
                    self.graph[v].pop(i)

    def has_edge(self, from_vertex, to_vertex):
        """Check if an edge exists between two vertices."""
        return from_vertex in self.graph and to_vertex in self.graph[from_vertex]

    def get_vertices(self):
        """Return a list of all vertices in the graph."""
        return list(self.graph)

    def get_edges(self):
        """Return a list of all directed edges in the graph."""
        edges = []
        for vertex in self.graph:
            for neighbor in self.graph[vertex]:
                edges.append((vertex, neighbor))
        return edges

    def display(self):
        """Print the adjacency list of the graph."""
        for vertex in self.graph:
            print(f"{vertex} --> {self.graph[vertex]}")

    def display_vertex_connections(self, vertex):
        """Print the adjacency list of one vertex in the graph"""
        print(f"{vertex} --> {self.graph[vertex]}")

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
    
    def _create_connections(self, new_universe):
        """Create valid connections between universes based on modular relationships."""
        for existing_universe in self.graph.get_vertices():
            if existing_universe != new_universe:
                # Check if existing_universe can transition into new_universe
                if (new_universe.a % existing_universe.n == existing_universe.a % existing_universe.n and
                    new_universe.n % existing_universe.n == 0 and
                    len(self.graph.graph[existing_universe]) < 6):
                    self.graph.add_edge(existing_universe, new_universe)

                # Check if new_universe can transition into existing_universe
                if (existing_universe.a % new_universe.n == new_universe.a % new_universe.n and
                    existing_universe.n % new_universe.n == 0 and
                    len(self.graph.graph[new_universe]) < 6):
                    self.graph.add_edge(new_universe, existing_universe)

    
    def add_universe(self, a, n):
        universe = My_Zn_verse(a, n)
        if universe not in self.graph.get_vertices():
            self.graph.add_vertex(universe)
            self._create_connections(universe)
    
    def remove_universe(self, a, n):
        universe = My_Zn_verse(a, n)
        self.graph.remove_vertex(universe)
    
    def display_multiverse(self):
        self.graph.display()
  

# Example Usage:
multiverse = My_Multiverse()
multiverse.add_universe(2,6)
multiverse.add_universe(1,6)
multiverse.add_universe(4, 12)
multiverse.add_universe(8, 24)
multiverse.add_universe(0,2)
multiverse.add_universe(0,4)
multiverse.add_universe(0,6)
multiverse.add_universe(0,8)
multiverse.add_universe(0,12)
multiverse.remove_universe(8,24)

multiverse.display_multiverse()
