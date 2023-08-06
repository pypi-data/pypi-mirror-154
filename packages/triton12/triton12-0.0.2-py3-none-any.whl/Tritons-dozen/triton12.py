
import os
import numpy as np
from pandas import DataFrame
from scipy.signal import savgol_filter




def get_datafolders(directory):
    paths = _get_filepaths(directory)
    names = []
    for i in range(0,len(paths)):
        names.append(os.path.split(os.path.split(paths[i])[0].strip("/"))[1]) #This monster gets the folder name that contains a .dat file and I love it
        
    names = DataFrame(names)
 

    return names




def get_data(folder,num):
    
    
     # Read and fix the data format
        
    rawdata = _read_data(folder,num)
    
    #Get the labels from names
    labels = rawdata.iloc[0,:]
    labels.drop(0, inplace = True) #By default everything is ofset by one
    labels.dropna(inplace = True)
    labels.reset_index(drop=True, inplace = True)
    
    #Gets rid of empty columns and rows, as well as the rows contaning names of columns
    rawdata.drop([0,1,2], inplace = True)
    rawdata.dropna("columns", "all", inplace = True)
    rawdata.rename(index = str, columns = labels, inplace = True)
    rawdata.dropna("rows","all",inplace = True)
    rawdata.reset_index(drop = True, inplace = True)
    
    return rawdata




# class MidpointNormalize(colors.Normalize):
#     def __init__(self, vmin=None, vmax=None, midpoint=None, clip=False):
#         self.midpoint = midpoint
#         colors.Normalize.__init__(self, vmin, vmax, clip)

#     def __call__(self, value, clip=None):
#         x, y = [self.vmin, self.midpoint, self.vmax], [0, 0.5, 1]
#         return np.ma.masked_array(np.interp(value, x, y))


### THE STUFF ABOVE USES THESE. NOT YOU ###


def _get_filepaths(directory):
    file_paths = []
    for root, directories, files in os.walk(directory):
        for filename in files:
            if filename.endswith(".dat"):
                filepath = os.path.join(root, filename)
                file_paths.append(filepath)
                file_paths
    file_paths = sorted(file_paths)
    return file_paths 




def _read_data(folder,num):
#     print(_get_filepaths(folder)[num])
    with open(_get_filepaths(folder)[num]) as f:
        data = DataFrame(l.rstrip().split() for l in f)
    
    return data


def get_data_batch(batch,num):
     # Read and fix the data format       
    rawdata = _read_data_batch(batch,num)
    
    #Get the labels from names
    labels = rawdata.iloc[0,:]
    labels.drop(0, inplace = True) #By default everything is ofset by one
    labels.dropna(inplace = True)
    labels.reset_index(drop=True, inplace = True)
    
    #Gets rid of empty columns and rows, as well as the rows contaning names of columns
    rawdata.drop([0,1,2], inplace = True)
    rawdata.dropna("columns", "all", inplace = True)
    rawdata.rename(index = str, columns = labels, inplace = True)
    rawdata.dropna("rows","all",inplace = True)
    rawdata.reset_index(drop = True, inplace = True)
    
    return rawdata


def _read_data_batch(batch,num):
#     print(_get_filepaths(folder)[num])
    with open(batch[num]) as f:
        data = DataFrame(l.rstrip().split() for l in f)
    
    return data


def dirMake(directory):                       ## Makes a directory
    if not os.path.exists(directory):
        os.makedirs(directory)
    return(directory)


def find_nearest_index(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return idx

def autorangey(datax,datay,xlims):
    idx_min = find_nearest_index(datax,xlims[0])
    idx_max = find_nearest_index(datax,xlims[1])
    
    if idx_min < idx_max:
        lim_data = datay[idx_min:idx_max]
    else:
        lim_data = datay[idx_max:idx_min]
    ymax = np.max(lim_data)+np.abs(np.max(lim_data)-np.average(lim_data))
    ymin = np.min(lim_data) - np.abs(np.average(lim_data)-np.min(lim_data))
    return ymin,ymax


def findThreshold(Vg, G, threshold = 0.1, polyorder = 3):
    window = int(len(Vg)/20)
    if window %2 == 0: window +=1
    G_fltr = savgol_filter(G, window, polyorder)
    
    Vg_10 = Vg[G_fltr > threshold * np.max(G_fltr)]
    G_10 = G_fltr[G_fltr > threshold * np.max(G_fltr)]
    
    Vth = Vg_10[np.argmin(G_10)]
    
    return Vth


def bootstrap(pop, reps, size):
    samples = []
    for n in range(reps):
        x = np.random.choice(pop, size=size, replace=True)
        samples.append(x.mean())
    return(samples)