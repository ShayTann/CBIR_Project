import numpy as np
from scipy import ndimage as ndi
from skimage.filters import gabor_kernel
import skimage




class TextureDescriptor:

	def lbp(self, im, n_points=24, rad=8):
		""" Calculate Local Binary Pattern for a grayscale image
            :param im: grayscale image
            :param n_points: number of points considered in a circular neighborhood
            :param rad: radius of neighborhood
            :return: histogram of local binary pattern
        """
		desc = skimage.feature.local_binary_pattern(im, n_points, rad, method='uniform')
		(hist, _) = np.histogram(desc.ravel(), bins=np.arange(0, n_points + 3),
								 range=(0, n_points + 2))

		# normalization
		hist = hist / np.sum(hist)
		# flatten
		hist = hist.flatten()

		return hist

	# We can also use Gabor descriptor, its will give us almost the same result as the Local
	# Binany descriptor
	def gaborDescriptor(self,img):
		""" Apply Gabor filter
		        :param img: grayscale image
		    """

		kernels = []
		#theta: desired orientation for feature extraction
		for theta in range(4):
			theta = theta / 4. * np.pi
			#sigma: standard deviation of gaussian
			for sigma in (1, 3):
				for frequency in (0.05, 0.25):
					kernel = np.real(gabor_kernel(frequency, theta=theta,
												  sigma_x=sigma,
												  sigma_y=sigma))
					kernels.append(kernel)

		feats = np.zeros((len(kernels), 2), dtype=np.double)
		for k, kernel in enumerate(kernels):
			filtered = ndi.convolve(img, kernel, mode='wrap')
			feats[k, 0] = filtered.mean()
			feats[k, 1] = filtered.var()

		return np.hstack((feats[:, 0].ravel(), feats[:, 1].ravel())).ravel()
