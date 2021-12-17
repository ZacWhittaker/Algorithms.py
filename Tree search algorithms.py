import math

class PriorityQueue:
    '''
    This class represents a priority que used within the tasks for the assignment
    '''
    def __init__(self):
        '''
        Constructor
        Complexity: O(1)
        '''
        self.queue = []

    def isEmpty(self):
        '''
        This function checks if the que is empty
        Complexity: O(1)
        @return: Boolean value representing the queue being empty or not
        '''
        return len(self.queue) == 0

    def insert(self, data):
        '''
        This function inserts a value into the priority queue
        Complexity: O(1)
        :param data: The data to be inserted
        :return: n/a
        '''
        self.queue.append(data)

    def update(self, vertex, val):
        '''
        This function is used to update a value in the priority queue
        Complexity: O(n) where n is the number of elements in the queue
        :param vertex: The vertex to be updated
        :param val: The value to replace
        :return: n/a
        '''
        for i in range(len(self.queue)):
            if self.queue[i][0] == vertex:
                self.queue[i][1] = val

    def pop(self):
        '''
        This function pops the smallest value from the priority queue
        Complexity: O(n) where n is the length of the priority queue
        :return:
        '''
        minVal = 0
        if len(self.queue) == 0:
            return -1
        for i in range(len(self.queue)):

            if self.queue[i][1] < self.queue[minVal][1]:
                minVal = i

        item = self.queue[minVal]
        del self.queue[minVal]
        return item

class UnionFind:
    '''
    This class impliments the unionfind data structure to reduce the cost of kruskals algorithm.
    '''
    def __init__(self, n):
        '''
        Constructor
        Complexity: O(n) where n is the number of vertecies
        :param n: the number of vertecies
        '''
        self.VertexID = [i for i in range(n)]
        self.Parent = [i for i in range(n)]

    def Union(self, u, v):
        '''
        This function joins two sets with the same id
        :param u: a vertex in one set
        :param v: a vertex in another
        :return: na
        '''
        u_val = self.find(u)
        v_val = self.find(v)
        self.Parent[v_val] = u_val

    def find(self, vert):
        '''
        This function finds and returns the set id of a vertex
        :param vert: The vertex in question
        :return: The set ID
        '''
        while self.Parent[vert] != vert:
           vert = self.Parent[vert]
        return vert

    def print(self):
        '''
        A print function for displaying the state
        :return:
        '''
        print('Vertex id: ')
        print(self.VertexID)
        print('parent: ')
        print(self.Parent)

class Graph:
    '''
    This class is used to represent a graph and perform the operations required
    '''
    def __init__(self, gfile):
        '''
        Constructor for the graph class, The graph is represented as an adjacency matrix
        Complexity: O(n^2) Where n is the number of nodes in the graph
        :param gfile: a file name to import the graph data from
        '''
        # Read the data in from the file
        f = open(gfile, "r")
        lines = f.readlines()
        f.close()
        weights = []
        # read the lines
        for i in range(len(lines)):
            lines[i] = lines[i].replace('\n', '')

        num_nodes = int(lines[0])
        graph = [[0]*num_nodes for _ in range(num_nodes)]
        # add the data to the adjacency matrix
        for i in range(1, len(lines)):
            line_details = lines[i].split()
            x = int(line_details[0])
            y = int(line_details[1])
            weight = int(line_details[2])
            graph[x][y] = weight
            graph[y][x] = weight
            weights.append([x, y, weight])
        # store a sorted list of edge weights
        self.sortedEdges = sorted(weights, key=lambda x: x[2])
        # store the graph
        self.graph = graph
        # init an adjacency list for storing data in later functions
        self.adjacencyList = [[] for _ in range(len(self.graph))]

    def prims(self, r):
        '''
        This is an implimentation of prims algorithm for finding a spanning tree beginning
        at node r
        Complexity: O(n^2) Where n is the number of nodes in the graph
        :param r: The node to start the algorithm from
        :return: The maximum depth of the spanning tree rooted at r
        '''
        MST = []
        dist = [math.inf for _ in range(len(self.graph))]
        parent = [None for _ in range(len(self.graph))]
        dist[r] = 0
        Q = PriorityQueue()
        # insert all edges into a priority queue
        for x in range(len(self.graph)):
            Q.insert([x, dist[x]])
        # while the queue is not empty
        while not Q.isEmpty():
            # pop the smallest edge
            u = Q.pop()
            MST.append(u[0])
            # iterate over the neighbours of that edge
            for e in range(len(self.graph[u[0]])):
                # if it does not produce a cycle
                if self.graph[u[0]][e] != 0 and e not in MST and dist[e] > 1:
                    Q.update(e, 1)
                    dist[e] = 1 + dist[u[0]]
                    parent[e] = u[0]
        # returns the maximum depth of the spanning tree rooted at r
        return max(dist)

    def shallowest_spanning_tree(self):
        '''
        This function finds and returns the root and depth of the spanning tree with
        the minimum height from a node.
        Complexity: O(n^3) Where n is the number of nodes in the tree
        :return: A tuple containing the root vertex and the height of the tree
        '''
        # init the nodes
        Vert = [v for v in range(len(self.graph))]
        depth = []
        # for each vertex
        for v in Vert:
            # do prims
            depth.append(self.prims(v))
            # find the min
        minVal = min(depth)
        # find the index
        minIndex = depth.index(minVal)
        # return
        return (Vert[minIndex], minVal)

    def kruskal(self):
        '''
        This function is an implementation of kruskals algorithm for finding minimum
        spanning trees. It utilizes the UnionFind class defined above
        Complexity: O(Elog(V)) Where E is the number of edges and V is the number of nodes
        :return: Returns an adjacency list representing the minimum spanning tree
        '''

        Union = UnionFind(len(self.graph))
        # for each edge in the sorted edges
        for item in self.sortedEdges:
            # if it does cause a cycle
            if Union.find(item[0]) != Union.find(item[1]):
                # add to the list
                Union.Union(item[0], item[1])
                self.adjacencyList[item[0]].append(item[1])
                self.adjacencyList[item[1]].append(item[0])
        # return
        return self.adjacencyList


    def dijkstra(self, start):
        '''
        This is an implementation of a modified dijkstra's algorithm that uses an
        adjacency list to represent the graph. It returns all paths taken and distances to
        each node from start
        Complexity: O(Elog(V)) Where E is the number of edges and V is the number of vertices
        :param start: The node to start as
        :return: the distances and paths to each node
        '''
        # init containers for storing values
        dist = [math.inf for _ in range(len(self.graph))]
        dist[start] = 0
        paths = [[] for _ in range(len(self.graph))]
        paths[start] = [start]
        pq = PriorityQueue()
        pq.insert([start, 0, paths[start]])
        # while the queue is not empty
        while not pq.isEmpty():
            currentVal =  pq.pop()
            currentDist = currentVal[1]
            currentNode = currentVal[0]
            currentPath = currentVal[2]

            # for each neighbour of the current node
            for neighbour in self.adjacencyList[currentNode]:
                distance = currentDist + self.graph[currentNode][neighbour]
                path = currentPath + [neighbour]
                # if the distance is less than the stored distance
                if distance < dist[neighbour]:
                    dist[neighbour] = distance
                    paths[neighbour] = path
                    pq.insert([neighbour, distance, path])
        return dist, paths

    def shortest_errand(self, home, destination, ice_locs, ice_cream_locs):
        '''
        This function finds the shortest path between home and destination that passes through at least one ice_loc then
        at least one ice_cream_loc.
        Complexity: O(Elog(V)) Where E is the number of edges and V is the number of vertices
        :param home: The home vertex
        :param destination: The destination vertex
        :param ice_locs: The locations of ice
        :param ice_cream_locs: The locations of ice cream
        :return: A tuple containing the path taken and distance of the route
        '''

        # run kruskals algorithm on the graph. The result is stored within the class
        self.kruskal()
        # run dijkstras algorithm from home
        distances, paths = self.dijkstra(home)

        # find the most efficient path from home to the ice
        ice_distance = []
        for node in ice_locs:
            ice_distance.append(distances[node])
        distance_to_ice = min(ice_distance)
        index_distance_to_ice = ice_distance.index(distance_to_ice)
        path_to_ice = paths[ice_locs[index_distance_to_ice]]

        # run dijkstras algorithm from the ice location
        distances, paths = self.dijkstra(path_to_ice[-1])
        icecream_distance = []
        # find the most efficient path from ice to the ice cream
        for node in ice_cream_locs:
            icecream_distance.append(distances[node])

        distance_to_icecream = min(icecream_distance)
        index_distance_to_icecream = icecream_distance.index(distance_to_icecream)
        path_to_icecream = paths[ice_cream_locs[index_distance_to_icecream]]
        # run dijkstras algorithm from the ice cream location
        # find the most efficient path from icecream to destination
        distances, paths = self.dijkstra(path_to_icecream[-1])

        # create the result
        final_path = path_to_ice + path_to_icecream[1:] + paths[destination][1:]
        final_distance = distance_to_ice + distance_to_icecream + distances[destination]
        # return
        return (final_distance, final_path)

