from skimage.io import imread,imsave,imshow
from scipy.signal import convolve2d
from skimage.filters import gaussian
from skimage.filters.rank import median, mean
from matplotlib import pyplot as plt
import numpy as np
from skimage.morphology import square, disk
from numpy.fft import fft2,ifft2,fftshift,ifftshift

#Convolution in spatial space
def median_filter(image): 
	im_output = image.copy()

	if len(image.shape)>2	:
		# apply the median filter for each channel
		out_median_red = median(im_output[:,:,0], disk(4))
		out_median_green = median(im_output[:,:,1], disk(4))
		out_median_blue = median(im_output[:,:,2], disk(4))

		# after filtering with median, i notice that the output shape will be bigger then the image input, 
		# for avoiding shape error widh and heigh, i create a new image with the same shape from one of the mean channel output
		out_median = np.zeros((out_median_red.shape[0],out_median_red.shape[1],3))
		# median
		out_median[:, :, 0] = out_median_red
		out_median[:, :, 1] = out_median_green
		out_median[:, :, 2] = out_median_blue
		out = out_median
		imsave('RGB_denoised_image.jpg', out)
	else : 
		out = median(im_output , disk(4))
		imsave('Gray_denoised_image.jpg', out)
	
	return out

def mean_filter(image) : 
	im_output = image.copy()
	if len(image.shape)>2	:
	# apply the mean filter for each channel
		out_mean_red = mean(im_output[:,:,0], disk(3))
		out_mean_green = mean(im_output[:,:,1], disk(3))
		out_mean_blue = mean(im_output[:,:,2], disk(3))

	# after filtering with mean, i notice that the output shape will be bigger then the image input,
	# for avoiding shape error widh and heigh, i create a new image with the same shape from one of the mean channel output 
		out_mean = np.zeros((out_mean_red.shape[0],out_mean_red.shape[1],3))
		# median
		out_mean[:, :, 0] = out_mean_red
		out_mean[:, :, 1] = out_mean_green
		out_mean[:, :, 2] = out_mean_blue
		out = out_mean
		imsave('RGB_denoised_image.jpg', out)
	else : 
		out = mean(im_output , disk(5))
		imsave('Gray_denoised_image.jpg', out)
	return out

def gaussian_filter(image, level):
	im_output = image.copy()
	if len(image.shape)> 2:
		out =  gaussian(im_output.astype('uint8'), sigma=int(level) , multichannel=True)
	else :
		out =  gaussian(image, sigma=int(level))
	return  out

def cumul_hist(image):

	cumul_hist = np.zeros((256,))
	c = 0
	for v in range(256):
		c+= (v==image).sum()
		cumul_hist[v] = c 
	cumul_hist/= cumul_hist.max()
	
	return cumul_hist

def homogeneous_contrast_image(image):  
	"""This method is to perform equalization, it used to brightening the contrast of the image
		- This operation not reversible because we have changed the values of pixels (loosing information)
		 during the processing.
		- 
	"""
	histo = cumul_hist(image)
	lut = (histo*255).astype('uint8')
	im_out = lut[image]
	imsave('Homogeneous_image.jpg', im_out)

	return im_out, histo

## convolution in Fourier space
def fourier(im):
	return fftshift(fft2(im))

def ifourier(f):
	return ifft2(ifftshift(f)).real

def get_disk_mask(r, imshape):
	a, b = imshape[0]//2, imshape[1]//2   
	y,x = np.ogrid[-a:imshape[0]-a, -b:imshape[1]-b]
	mask = x*x + y*y <= r*r
	return mask

def prepare_mask(image,radius):
	mask = np.zeros(image.shape)
	d = disk(radius)
	mask[mask.shape[0]//2-d.shape[0]//2:mask.shape[0]//2+d.shape[0]//2+1,
	 mask.shape[1]//2-d.shape[1]//2:mask.shape[1]//2+d.shape[1]//2+1] = d
	return mask

def high_pass(image,r):
	f = fourier(image)
	mask = get_disk_mask(r,f.shape)
	f2 = f*(1-mask)
	return ifourier(f2)

def low_pass(image,r):
	f = fourier(image)
	mask = prepare_mask(image,r)
	f2 = f*mask
	amplitude = np.sqrt(f2.real**2 + f2.imag**2)
	return ifourier(f2),amplitude