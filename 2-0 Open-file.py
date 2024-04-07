from filefifo import Filefifo
data = Filefifo(10, name = 'capture_250Hz_01.txt')
for i in range(100):
 print(data.get())