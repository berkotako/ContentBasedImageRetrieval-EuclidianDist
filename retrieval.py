from operator import ne
import cv2
import math
import numpy as np
import glob
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.colors as colors
#def HSVConv

#Normalize X - min / max - min
def Normalization(Maxx,Minn,arr):
    new_arr = np.zeros((256),dtype = np.float32)
    for px in range(256):
        new_arr[px] = (arr[px] - Minn)/(Maxx-Minn)
    return new_arr
    
def Euclidian_X(arr1,arr2):
    
    arr_euc_x = 0.0
    for px in range(256):
        arr_euc_x = arr_euc_x + pow((arr1[px]-arr2[px]),2)
    arr_euc_x = math.sqrt(arr_euc_x)
    return arr_euc_x

def Euclidian_Y(arr1,arr2):
    arr_euc_y = 0
    for px in range(256):
        arr_euc_y = arr_euc_y + pow((arr1[px]-arr2[px]),2)
    arr_euc_y = math.sqrt(arr_euc_y)
    return arr_euc_y

def Euclidian_XY(eucX,eucY):
    return math.sqrt(pow((eucX+eucY),2))

def Read_Img(path):
    return cv2.imread(path)

def Create_Hist(arr):
    Hist = np.zeros((256),dtype = np.float32)
    for x in arr:
        Hist[x] = Hist[x]+1
    return Hist



def CreateHue_Hist(img1):
   img_hsv = cv2.cvtColor(img1, cv2.COLOR_BGR2HSV )
   Hue_Hist = np.zeros((256),dtype = np.float32)
   for px in img_hsv[:,:,0]:
        Hue_Hist[px] = Hue_Hist[px]+1   
   Hue_Hist_Norm = np.zeros((256),dtype = np.float32)
   H_Max = max(Hue_Hist)
   H_Min = min(Hue_Hist)
   Hue_Hist_Norm = Normalization(H_Max,H_Min,Hue_Hist)
   return Hue_Hist_Norm
   
   # Euclidian Distance hesapla ve döndür
def Euclidian_Imgs(Hist_Norm,Hist2_Norm):
    EucX = Euclidian_X(Hist_Norm,Hist2_Norm)
    EucY = Euclidian_Y(Hist_Norm,Hist2_Norm)
    EuxXY = Euclidian_XY(EucX,EucY)
    return EuxXY

#def General_RGB_Euc():

def Create_RGB_Hists(img):
    Hist_List=[]
    #Red 
    CH_Red = img[:,:,0]
    Hist_Red=np.zeros((256),dtype = np.float32)
    Hist_Red_N=np.zeros((256),dtype = np.float32)
    Hist_Red=Create_Hist(CH_Red)
    #Red Normalization
    Red_Max = max(Hist_Red)
    Red_Min = min(Hist_Red)
    Hist_Red_N=Normalization(Red_Max,Red_Min,Hist_Red)
    #Green
    CH_Green = img[:,:,1]
    Hist_Green=np.zeros((256),dtype = np.float32)
    Hist_Green_N=np.zeros((256),dtype = np.float32)
    Hist_Green=Create_Hist(CH_Green)
     #Green Normalization
    Green_Max = max(Hist_Green)
    Green_Min = min(Hist_Green)
    Hist_Green_N=Normalization(Green_Max,Green_Min,Hist_Green)
    #Blue
    CH_Blue = img[:,:,2]
    Hist_Blue=np.zeros((256),dtype = np.float32)
    Hist_Blue_N=np.zeros((256),dtype = np.float32)
    Hist_Blue=Create_Hist(CH_Blue)
     #Blue Normalization
    Blue_Max = max(Hist_Blue)
    Blue_Min = min(Hist_Blue)
    Hist_Blue_N=Normalization(Blue_Max,Blue_Min,Hist_Blue)
    #Adding to list
    Hist_List.append(Hist_Red_N)
    Hist_List.append(Hist_Green_N)
    Hist_List.append(Hist_Blue_N)
    return Hist_List
    
    

def General_RGB_Euc(img,img2):
    #R G B Histogramları
    RGB_Hist_List1 = Create_RGB_Hists(img)
    RGB_Hist_List2 = Create_RGB_Hists(img2)
    RGB_Euc_list = []
    #Hepsi için Dist hesapla
    R = Euclidian_Imgs(RGB_Hist_List1[0],RGB_Hist_List2[0])
    G = Euclidian_Imgs(RGB_Hist_List1[1],RGB_Hist_List2[1])
    B = Euclidian_Imgs(RGB_Hist_List1[2],RGB_Hist_List2[2])
    RGB_Euc_list.append(R)
    RGB_Euc_list.append(G)
    RGB_Euc_list.append(B)
    return RGB_Euc_list





# Image Image2 R_Dist G_Dist B_Dist H_Dist
def Main():
    #PNG Dosyalarını al
    pngfiles = []
    for file in glob.glob("*.jpg"):
        pngfiles.append(file)
            
    Image_Dict_List=[]
    Image_Dist_Dict ={
        "Image1":"img1",
        "Image2":"img2",
        "R_Dist":0,
        "G_Dist":0,
        "B_Dist":0,
        "H_Dist":0
    }
    
    #Resimleri klasörden oku
    for i in range(len(pngfiles)-1):
        img1 = Read_Img(pngfiles[i])
        img1_hue_hist=CreateHue_Hist(img1)
        for a in range(i+1,len(pngfiles),1):
            img2 = Read_Img(pngfiles[a])
            img2_hue_hist=CreateHue_Hist(img2)
            Img_Hue_Euc_Dist=Euclidian_Imgs(img1_hue_hist,img2_hue_hist)
            RGB_List = General_RGB_Euc(img1,img2)
            Image_Dist_Dict["Image1"]=pngfiles[i]
            Image_Dist_Dict["Image2"]=pngfiles[2]
            Image_Dist_Dict["R_Dist"]=RGB_List[0]
            Image_Dist_Dict["G_Dist"]=RGB_List[1]
            Image_Dist_Dict["B_Dist"]=RGB_List[2]
            Image_Dist_Dict["H_Dist"]=Img_Hue_Euc_Dist
            Image_Dict_List.append(Image_Dist_Dict.copy())
        
    R_list=[]
    R_list_Name=[]
    G_list=[]
    B_list=[]
    H_list=[]
    
    for vars in Image_Dict_List:
        R_list.append(vars["R_Dist"])
        R_list_Name.append(vars["Image1"])
        G_list.append(vars["G_Dist"])
        B_list.append(vars["B_Dist"])
        H_list.append(vars["H_Dist"])
    
    listLength=len(Image_Dict_List)
    listLength=listLength-5
    
    for a in range(listLength):
        R_list.remove(max(R_list)) 
        G_list.remove(max(G_list)) 
        B_list.remove(max(B_list)) 
        H_list.remove(max(H_list))
        
    #r icin liste olusturma
    tmp=Image_Dict_List.copy()
    enk=10000
    List3=[]
    flag=[]
    for vars in range(5):
        for vars2 in tmp:
            if(vars2["R_Dist"] < enk ):
                enk = vars2["R_Dist"]
                flag=vars2.copy()
                tmp.remove(vars2)
        List3.append(flag) 
        enk=10000




    #g icin liste olusturma
    tmp=Image_Dict_List.copy()
    enk=10000
    List4=[]
    for vars in range(5):
        for vars2 in tmp:
            if(vars2["G_Dist"] < enk ):
                enk = vars2["G_Dist"]
                flag=vars2.copy()
                tmp.remove(vars2)
        List4.append(flag)
        enk=10000
         

    #b icin liste olusturma
    tmp=Image_Dict_List.copy()
    enk=10000
    List5=[]
    for vars in range(5):
        for vars2 in tmp:
            if(vars2["B_Dist"] < enk ):
                enk = vars2["B_Dist"]
                flag=vars2.copy()
                tmp.remove(vars2)
        List5.append(flag) 
        enk=10000
        
    
    

    #H icin liste olusturma
    tmp=Image_Dict_List.copy()
    enk=10000
    List6=[]
    for vars in range(5):
        for vars2 in tmp:
            if(vars2["H_Dist"] < enk ):
                enk = vars2["H_Dist"]
                flag=vars2.copy()
                tmp.remove(vars2)
        List6.append(flag)
        enk=10000
    
    print(List3)
    print('\n')
    
    print(List4)
    print('\n')
    
    print(List5)
    print('\n')
    
    print(List6)
    print('\n')
Main()

