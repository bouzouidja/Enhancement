from skimage.io import imread,imsave,imshow
from scipy.signal import convolve2d
from skimage.filters import gaussian
from skimage.filters.rank import median, mean
from matplotlib import pyplot as plt
import numpy as np
from skimage.color import rgb2hsv , hsv2rgb,rgb2gray
from skimage.morphology import square, disk
from skimage.feature import canny
import convolve_filter as convfl


print(" \n \n\t \t \tWelcome to enhancement tools.\n In this program you can enhance your images.\n" )
print("First you need to enter the name of your image. The images and this program should be in the same repository.\n")




while True :
    try :
        image = input("Enter your image name here, like YourImage.jpg \n")
        img = imread(image)

    except :
            print("Could not read" ,image)
    else : 
        break
 
print(" \n \n\t \t \tEnhancement options \n")
while True:    
    
    choice  = input("If you have an image with salt and pepper noise enter 'D' Denoising...\nEnter 'B' for bluring the image... \n Enter 'H' for homogenize contrast image... \n" )    
    

    if choice != "D" and choice != "B" and choice != "H" : 
        print ("Your input is not the correct value:")
    elif  choice == "B":
        
            level  = input("Enter your Blur level from 1 to 10 ...")
            if int(level) > 10 or int(level) < 0 :
                print ("\n ERROR:Assure that the value of level  between 1 and 10 "  )
           
            else : 
                print("Level checked")
                break


    
    else :
        print("Your input is right" ,choice)
        break    


plt.figure()
plt.subplot(1,2,1)
plt.title("Originale image")





if len(img.shape)>2:


    plt.imshow(img )
    options = {"D"  : convfl.median_filter ,
           "B"      : convfl.Gaussian_filter,
           "H"      : convfl.homogeneous_contrast_image}
    

    plt.subplot(1,2,2)
    if choice =="B" :
        result = options["B"](img , level)
        plt.imshow(result)
        plt.title("Blur image ")
    else : 
        result = options[choice](img )
    
        if choice == "D":

            plt.imshow(result.astype('uint8'))
            plt.title("Denoised RGB image ")
        elif choice == "H" :
            plt.imshow(result)
            plt.title("Homogeneous contrast image ")

    

else : 

    plt.imshow(img, cmap=plt.cm.gray )
    options = {"D"  : convfl.median_filter ,
           "B"      : convfl.Gaussian_filter,
           "H"      : convfl.homogeneous_contrast_image}
    plt.subplot(1,2,2)
    if choice =="B" : 
        result = options["B"](img , level)
        plt.imshow(result ,cmap=plt.cm.gray)
        plt.title("Blur image ")
    else :

        result = options[choice](img )
    
        if choice == "D":
            plt.imshow(result ,cmap=plt.cm.gray)
            plt.title("Denoised grayscale image ")
            
        elif choice == "H" :
            plt.imshow(result , cmap =plt.cm.gray)
            plt.title("Homogeneous contrast image ")



plt.show()







print("END....")