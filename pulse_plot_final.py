import matplotlib.pyplot as plt
import numpy as np
import time
import time, random
import math
import serial
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from collections import deque
from scipy import signal



#Display loading 
class PlotData:
    def __init__(self, max_entries=30):
        self.axis_x = deque(maxlen=max_entries)
        self.axis_y = deque(maxlen=max_entries)
        self.f = deque(maxlen=max_entries)
    def add(self, x, y):
        self.axis_x.append(x)
        self.axis_y.append(y)


angle = np.linspace(-np.pi, np.pi, 50)
cirx = np.sin(angle)
ciry = np.cos(angle)
z = 1
r1 = np.roots([1,0])
r2 = np.roots([1,-np.exp((-np.pi))])
plt.figure(figsize=(8,8))
plt.plot(cirx, ciry,'k-')
for i in r1:
    plt.plot(np.real(i), np.imag(i), 'o', markersize=12)

for i in r2:
    plt.plot(np.real(i), np.imag(i), 'o', markersize=12)

plt.grid()

plt.xlim((-2, 2))
plt.xlabel('Real')
plt.ylim((-2, 2))
plt.ylabel('Imag')



#initial
fig, (ax,ax3,ax4) = plt.subplots(3,1)
line,  = ax.plot(np.random.randn(100))
#line2, = ax2.plot(np.random.randn(100))
line3, = ax3.plot(np.random.randn(100))
line4, = ax4.plot(np.random.randn(100))
plt.show(block = False)
#plt.setp(line2,color = 'r')
plt.setp(line3,color = 'g')
plt.setp(line4,color = 'r')

ax.set_xlabel('(t)')
ax.set_ylabel('y')
#ax2.set_xlabel('(t)')
ax3.set_xlabel('(Hz)')
ax4.set_xlabel('(t)')
ax4.set_ylabel('Origin Input')
ax3.set_ylabel('Amplitude')
ax.set_ylabel('Output')





PData= PlotData(500)
ax.set_ylim(-30,30)
#ax2.set_ylim(-8,8)
#ax3.set_ylim(0,500)


# plot parameters
print ('plotting data...')
# open serial port
strPort='com4'
ser = serial.Serial(strPort, 115200)
ser.flush()


root= tk.Tk() 



start = time.time()
i=0
j=0



count=[]

while True:
    
    for ii in range(10):

        try:
            data = float(ser.readline())
            #print(data)
            PData.add(time.time() - start, data)
            #ecg = np.fft.fft(PData.axis_y)
            #ecg[0] = 0
            #PData.axis_y= np.fft.ifft(ecg)

            
        except:
            pass
    #print(len(PData.axis_y))
    #data=signal.lfilter([1/4, -2/4, 1/4],1,PData.axis_y)

    data = PData.axis_y
    ecg = np.fft.fft(data)
    ecg3=np.fft.fft(data)
    ecg[0] = 0
    ecg3[0]=0
    #ecg3 = (signal.lfilter([1/3, 1/3, 1/3],1,ecg3))
    #for i in range(len(ecg)):
        #if i>90:
            #ecg[i]=0
        #elif i>90:
            #ecg[i]=0     
    data_y= np.fft.ifft(ecg)
    #a=signal.lfilter([1/3, 1/3, 1/3],1,data_y)
    #ecg = np.fft.fft(signal.lfilter([1/3, -1/3, -1/3],1,a))
    data_y= np.fft.ifft(ecg)
    b,c = signal.butter(1,0.2,'lowpass')
    #b, c = signal.butter(10, 0.05)
    data_y = signal.lfilter(b, c, data_y)
    #b, c = signal.butter(10, 0.05)
    #data_y = signal.lfilter(b, c, data_y)
    ecg3=np.fft.fft(data_y)
    for iii in range(50,len(ecg3),1):
        ecg3[iii]=0

    
    data_y = np.fft.ifft(ecg3)*10
    #data_y=signal.lfilter([1/3, 1/3, 1/3],1,data_y)
    for iii in range(len(data_y)-1):
        if abs(data_y[iii] - data_y[iii+1]) < 1:
            data_y[iii] = 0

    for iii in range(len(data_y)-1):
        if data_y[iii] != 0:
            data_y[iii] *= 2 
    maxy = np.max(data_y)
    
    c = 0
    for iii in range(len(data_y)):
        if data_y[iii] != 0:
            c = c + 1

    c = c * 4/5
    if c > 60 and c < 100:
        count.append(c)
    ax.title.set_text("BPM:" + str(np.average(count)))

    #b, c = signal.butter(10, 0.05)
    #data_y = signal.lfilter(b, c, data_y)




    w_hat = np.arange(0, 2*np.pi, np.pi*2/500)
    PData.f=100*w_hat/(2*np.pi)
    #data_y = PData.axis_y
    #for i in range(len(data_y)):
    #    data_y[i] *= 10 
    b, c = signal.butter(3, 0.025)
    y_data = data - np.mean(data)
    y_data = signal.lfilter(b, c, y_data)*2.5
        


    data4 =data - np.mean(data)    
    #print(len(data_y))
    #print(len(PData.axis_x))
    #print((y_data))
    #print(PData.axis_x)
    ax.set_xlim(PData.axis_x[0], PData.axis_x[0]+5)
    #ax2.set_xlim(PData.axis_x[0], PData.axis_x[0]+5)
    ax3.set_xlim(PData.f[0], PData.f[len(w_hat)-1])
    ax4.set_xlim(PData.axis_x[0], PData.axis_x[0]+5)
    
    #ax.set_ylim(data_y[5]-5,data_y[5]+5)
    #ax2.set_ylim(y_data[5]-5, y_data[5]+5)
    ax3.set_ylim(0,max(abs(ecg)))
    ax4.set_ylim(-5,5)



    line.set_xdata(PData.axis_x)
    line.set_ydata(data_y)
    
    
    #line2.set_xdata(PData.axis_x)
    #line2.set_ydata(y_data)

    if(len(data_y)>=500):
        line3.set_ydata(abs(ecg3))
        line3.set_xdata(PData.f)


    line4.set_xdata(PData.axis_x)
    line4.set_ydata(data4)
    

    


    #bar1 = FigureCanvasTkAgg(fig, root)

    #root.mainloop()
    fig.canvas.draw()
    fig.canvas.flush_events()
    #fig2.canvas.draw()
    #fig2.canvas.flush_events()


