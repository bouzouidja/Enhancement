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
    
    choice  = input("Enter 'D' for denoising salt and pepper image...\n Enter 'H' for homogenize contrast image... \n Enter 'B' for bluring the image... \n" )
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
        print("Your input is")
        break    



# Applying filter according to option choosed
options = {"D"  : convfl.median_filter,
           "B"      : convfl.gaussian_filter,
           "H"      : convfl.homogeneous_contrast_image}
    

if choice =="B" :
        plt.figure(figsize=(15,10))
        plt.subplot(1,2,1)
        plt.title("Originale image")
        plt.imshow(img,cmap=plt.cm.gray)
        #result,amplitude = options["B"](img, 50)
        result = options["B"](img, level)
        plt.subplot(1,2,2)
        plt.title("Filtred image")
        plt.imshow(result, interpolation='none', cmap=plt.cm.gray)
        #plt.subplot(1,3,3)
        #plt.imshow(amplitude, interpolation='none', cmap='viridis')
        #plt.title('Fourier amplitude')
        #plt.axis('off')
elif choice == "D":
            plt.figure(figsize=(15,10))
            plt.subplot(1,2,1)
            plt.title("Originale image")
            plt.imshow(img, cmap=plt.cm.gray)
            plt.subplot(1,2,2)
            result = options["D"](img)
            plt.title("Denoised image")
            plt.imshow(result.astype('uint8'), cmap=plt.cm.gray)
            
            
elif choice == "H":
            plt.figure(figsize=(15,10))
            plt.subplot(1,2,1)
            plt.title("Originale image")
            plt.imshow(img)
            result, cumul_histo = options["H"](img)
            plt.subplot(1,2,2)
            plt.title("Homogeneous contrast image")
            plt.imshow(result)
            #plt.subplot(1,3,3)
            #plt.plot(cumul_histo)
            #plt.title("Cumulative histogram")

plt.show()
print("END....")