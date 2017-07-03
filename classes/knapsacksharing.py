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

        # data;
        f.write('data;\n\n')

        # set G := 1 2;
        f.write('set G:=')
        for i in range(1, self.numGroups + 1):
            f.write(" ")
            f.write(str(i))
        f.write(';\n\n')

        # set I := 1 2 3 4 5;
        f.write('set I:=')
        for i in range(1, int(max(self.numItemsByGroups)) + 1):
            f.write(" ")
            f.write(str(i))
        f.write(';\n\n')

        # param p : 		1	2 :=
        #	            1	2	1
        #	            2	4	3
        #	            3	6	5
        #	            4	8	7
        #	            5	10	9;

        f.write('param p:		 ')
        for i in range(1, self.numGroups + 1):
            f.write(str(i))
            f.write(" ")
        f.write(":=\n")

        for i in range(0, int(max(self.numItemsByGroups))):
            f.write("			")
            f.write(str(i+1))
            for group in range(self.numGroups):
                f.write(" ")
                try:
                    f.write(str(self.items[group][i][1]))
                except IndexError:
                    f.write(str(0))
            f.write(";\n")


        # param w : 		1	2 :=
        #	            1	1	2
        #	            2	3	4
        #	            3	5	6
        #	            4	7	8
        #	            5	9	10;

        f.write('param w:		 ')
        for i in range(1, self.numGroups + 1):
            f.write(str(i))
            f.write(" ")
        f.write(":=\n")

        for i in range(0, int(max(self.numItemsByGroups))):
            f.write("			")
            f.write(str(i+1))
            for group in range(self.numGroups):
                f.write(" ")
                try:
                    f.write(str(self.items[group][i][0]))
                except IndexError:
                    f.write(str(0))
            f.write(";\n")

        # param n := 10;
        f.write('param n := ')
        f.write(str(self.numItems))
        f.write(';\n')

        # param c := 20;
        f.write('param c := ')
        f.write(str(self.capacity))
        f.write(';\n')

        # end;
        f.write('end;')

        f.close()
