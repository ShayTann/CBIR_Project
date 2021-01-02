import numpy as np
from scipy import ndimage as ndi
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

	