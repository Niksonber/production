class Part:
    def __init__(self, file, time, filament, material = 'PLA',quality='LOW', area=10, height=10):
        self.gcode = file
        self.filament = filament
        self.realTime = time
        self.time = time
        self.timeToPrint = time
        self.quality = quality
        self.material = material
        self.Ondoing = False
        self.priority = 1
        self.area = area
        self.height = height

    def __lt__(self, other):
        return self.time < other.time

    def __repr__(self):
        return str(self.time)


class Order():
    def __init__(self, id, parts, time, deadline, priority = 1, type_in = 'SERVICE'):
        self.id = id
        self.parts = parts
        self.time = time
        self.deadline = deadline
        self.priority = priority
        self.type = type_in
        self.code = 0
        self.parts.sort()
        self.parts.reverse()
#TODO search which part is printing
    def onGoing(self):
        return [True if part.Ondoing else False for part in self.parts]



class Printer:
    def __init__(self, name, material, stock, nozzle = 0.6, quality = 'LOW', type_in='Cartesiana', printableArea = 200, printableheight=180):
        self.name = name
        self.nozzle = nozzle
        self.queue = []
        self.idle = True
        self.occupationPercentage = 0.0
        self.relativeOcupation = 0.0
        self.material = material
        self.stock = stock
        self.permission = False
        self.idleBed = True
        self.totalTime = 0.0
        self.quality = quality
        self.type = type_in
        self.printableArea = printableArea
        self.printableheight = printableheight

    def newPrint(self):
        part = self.queue.pop()
        if self.stock < part.filament:
            self.stopPrint()
            print('Insufficient filament for print')
        self.idle = False
        return part
#TODO send serial, when finish, self.totalTime -= part.time, self.idle = True

    def stopPrint(self):
        pass

    def alloc(self, part, *urgent):
        self.queue.append(part)
        self.queue.sort()
        self.totalTime+= part.time

    def reset(self):
        self.queue = []
        self.totalTime = 0.0

    def __lt__(self, other):
        return self.totalTime < other.totalTime

    def __repr__(self):
        return self.name


class Manager:
    def __init__(self):
        self.printers = []
        self.orders = []
        self.parts = []
        self.incopatibleParts = []

    def add_printer(self, printer):
        self.printers.append(printer)

    def add_process(self, process):
        self.orders.append(process)
        self.parts.append(process.parts)
        for part in process.parts:
            printersCompatibles = self.printers#[printer for printer in self.printers if printer.quality>=process.quality]# and printer.material==process.material]
            if len(printersCompatibles)==0:
                #no exixts printer conpatible   
                print('sorry')
                self.incopatibleParts +=part
            else:    
                min(printersCompatibles).alloc(part)
        # choise the printer
    def add_process2(self, process):
        self.orders.append(process)
        self.parts+= process.parts
        self.parts.sort()
        self.parts.reverse()
        for printer in self.printers:
            printer.reset()
        for part in self.parts:
            printersCompatibles = [printer for printer in self.printers if  printer.quality>=part.quality and printer.material==part.material   and   \
                                                                            (printer.printableArea>= part.area and printer.printableheight>=part.height)]
            if len(printersCompatibles)==0:
                #no exixts printer conpatible   
                print('sorry, part isnt compatible')
            else:    
                min(printersCompatibles).alloc(part)
        # choise the printer
    

if __name__ == '__main__':
    g1 = Part('1', 10, 1)
    g2 = Part('2', 1, 1)
    g3 = Part('3', 25, 1)
    g4 = Part('4', 1, 1)
    g5 = Part('5', 100, 1)
    
    pr2 = Order(1,[g4, g5], 101,  60)
    pr = Order(2, [g1,g2,g3], 36,  60)
    p1 = Printer('p1', 'PLA', 30)
    p2 = Printer('p2', 'PLA', 30)

    m2 = Manager()
    m2.add_printer(p1)
    m2.add_printer(p2)
    m2.add_process2(pr)
    m2.add_process2(pr2)

    print("Fila da impressora 1: " + str(p1.queue))
    print("Fila da impressora 2: " + str(p2.queue))