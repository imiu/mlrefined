# This file pairs with chapter 3 of the textbook "Machine Learning Refined" published by Cambridge University Press, 
# free for download at www.mlrefined.com
import math
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D
from IPython import display
import time

class Regression_Demo2:
    def __init__(self):
        self.x = 0
        self.y = 0
        
        fig = plt.figure(num=None, figsize=(12, 5), dpi=80, facecolor='w', edgecolor='k')
        self.ax1 = fig.add_subplot(121)
        self.ax2 = fig.add_subplot(122,projection='3d')
        
    # load in a two-dimensional dataset from csv - input should be in first column, oiutput in second column, no headers 
    def load_data(self,csvname):
        # load data
        data = np.asarray(pd.read_csv(csvname,header = None))
        self.x = data[:,0]
        self.y = data[:,1]
        
        # center data
        self.x = self.x - np.mean(self.x)
        self.y = self.y - np.mean(self.y)
       
    ##### plotting functions ####
    # plot data
    def plot_pts(self):
        self.ax1.scatter(self.x,self.y)
        xgap = float(max(self.x) - min(self.x))/float(10)
        self.ax1.set_xlim([min(self.x)-xgap,max(self.x)+xgap])
        ygap = float(max(self.y) - min(self.y))/float(10)
        self.ax1.set_ylim([min(self.y)-ygap,max(self.y)+ygap])
        self.ax1.set_xticks([])
        self.ax1.set_yticks([])
        
    # create cost surface
    def make_cost_surface(self):
        # make grid over which surface will be plotted
        r = np.linspace(-4.5,4.5,100)    
        s,t = np.meshgrid(r,r)
        s = np.reshape(s,(np.size(s),1))
        t = np.reshape(t,(np.size(t),1))

        # generate surface based on given data - done very lazily - recomputed each time
        g = 0
        P = len(self.y)
        for p in range(0,P):
            g+= (s + t*math.sin(2*math.pi*self.x[p]) - self.y[p])**2

        # reshape and plot the surface, as well as where the zero-plane is
        s.shape = (np.size(r),np.size(r))
        t.shape = (np.size(r),np.size(r))
        g.shape = (np.size(r),np.size(r))
        self.ax2.plot_surface(s,t,g,alpha = 0.15)
        self.ax2.plot_surface(s,t,g*0,alpha = 0.1)

        # make plot look nice
        self.ax2.view_init(40,20)        
        self.ax2.set_xticks([])
        self.ax2.set_yticks([])
        self.ax2.set_zticks([])

        self.ax2.set_xlabel('intercept ',fontsize = 14,labelpad = -5)
        self.ax2.set_ylabel('slope  ',fontsize = 14,labelpad = -5)
        
        self.ax2.zaxis.set_rotate_label(False)  # disable automatic rotation
        self.ax2.set_zlabel('cost  ',fontsize = 14, rotation = 0,labelpad = 1)
        
   
    #### computation functions ####    
    def compute_cost(self,b,w):
        cost = 0
        for p in range(0,len(self.y)):
            cost +=(b + w*math.sin(2*math.pi*self.x[p]) - self.y[p])**2
        return cost
                
    # gradient descent function
    def run_grad_descent(self,max_its,inits,alpha):    
        # plot points and cost function 
        fig = plt.figure(num=None, figsize=(12, 5), dpi=80, facecolor='w', edgecolor='k')
        self.ax1 = fig.add_subplot(121)
        self.ax2 = fig.add_subplot(122,projection='3d')
        self.plot_pts()
        self.make_cost_surface()
        
        # initialize parameters - we choose this special to illustrate whats going on
        b = inits[0]    # initial intercept
        w = inits[1]      # initial slope
        P = len(self.y)
        
        # plot first parameters on cost surface
        cost = self.compute_cost(b,w)
        self.ax2.scatter(b,w,cost,color = 'r',marker = 'x',linewidth = 3, alpha = 0.8)

        # gradient descent loop
        for k in range(1,max_its+1):   

            # compute each partial derivative - gprime_b is partial with respect to b, gprime_w the partial with respect to w            
            gprime_b = 0
            gprime_w = 0
            for p in range(0,P):
                temp = 2*(b + w*math.sin(2*math.pi*self.x[p]) - self.y[p])
                gprime_b += temp
                gprime_w += temp*self.x[p]
            
            # take descent step in each partial derivative
            b = b - alpha*gprime_b
            w = w - alpha*gprime_w

            ### visualize descent step ###

            # compute cost function value 
            cost = self.compute_cost(b,w)
            
            # plot the line generated by most recent params
            s = np.linspace(np.min(self.x)-1, np.max(self.x)+10, 300)
            t = b + np.sin(2*math.pi*s)*w
            ln = self.ax1.plot(s,t,'-r',linewidth = 3) 

            # plot point on cost surface g(b,w)
            self.ax2.scatter(b,w,cost,color = 'r',marker = 'x',linewidth = 3, alpha = 0.8)
           
            # pause very briefly for visualization
            time.sleep(0.05)

            # clear panels
            display.clear_output(wait=True)
            display.display(plt.gcf()) 
            
            # remove current fit line from plot
            for pt in ln:
                pt.remove()
        
        # prevent two plots from being created (for some reason this happens)
        display.clear_output(wait=True)
        
        # redraw final fit
        s = np.linspace(np.min(self.x)-1, np.max(self.x)+10, 300)
        t = b + np.sin(2*math.pi*s)*w
        ln = self.ax1.plot(s,t,'-r',linewidth = 3)