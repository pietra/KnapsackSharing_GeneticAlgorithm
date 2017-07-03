class KnapsackSharing:
    def __init__(self):
        self.numItems = None  # 1st line
        self.numGroups = None  # 2nd line
        self.capacity = None  # 3rd line
        self.numItemsByGroups = None  # 4th line
        self.items = None  # Other lines
        self.seed = None  # Random seed

    def readingfile(self, file):
        f = open(file, 'r')
        self.numItems = int(f.readline())
        self.numGroups = int(f.readline())
        self.capacity = int(f.readline())
        self.numItemsByGroups = (f.readline()).split()

        # ITEMS DATA STRUCT: List (groups) of lists (items) of tuples (weight|value)
        self.items = []

        # Inicializing items struct
        for i in range(self.numGroups):
            self.items.append([])

        groupIndex = 0

        for numItems in self.numItemsByGroups:
            for i in range(int(numItems)):
                item = (f.readline()).split()
                self.items[groupIndex].append((int(item[0]), int(item[1])))
            groupIndex += 1

        f.close()

    def generatingGlpkData(self):
        f = open('dat', 'w')
        f.write('data;\n\n')
        f.write('set G:= ')

        for i in range(1, self.numGroups + 1):
            f.write(i)
        f.write('\n\n')

        f.write('param w:		 1 2 :=')
        #for i in range ()



        f.close()






