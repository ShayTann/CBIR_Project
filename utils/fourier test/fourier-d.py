import cv2
import numpy

MIN_DESCRIPTOR = 2 # just copied this
TRAINING_SIZE = 100


def findDescriptor(img):
    """ had function katrja3 countour d fourier"""
    contour = []
    contour, hierarchy = cv2.findContours(
        img,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_NONE,
        contour)
    contour_array = contour[0][:, 0, :]
    contour_complex = numpy.empty(contour_array.shape[:-1], dtype=complex)
    contour_complex.real = contour_array[:, 0]
    contour_complex.imag = contour_array[:, 1]
    fourier_result = numpy.fft.fft(contour_complex)
    return fourier_result


def truncate_descriptor(descriptors, degree):
    """had function kat9sm wtshift and then kat insheft (don't why but found that u should in a tuto) """
    descriptors = numpy.fft.fftshift(descriptors)
    center_index = (len(descriptors) / 2)
    descriptors = descriptors[int(center_index - degree / 2):int(center_index + degree / 2)]#wadik int tma hit kib9a y3tini dik error slice indices must be integers
    descriptors = numpy.fft.ifftshift(descriptors)
    return descriptors


def reconstruct(descriptors, degree):
    """ attempts to reconstruct the image
    using the first [degree] descriptors of descriptors"""
    # calling truncate
    descriptor_in_use = truncate_descriptor(descriptors, degree)
    contour_reconstruct = numpy.fft.ifft(descriptor_in_use)
    contour_reconstruct = numpy.array([contour_reconstruct.real, contour_reconstruct.imag])
    contour_reconstruct = numpy.transpose(contour_reconstruct)
    contour_reconstruct = numpy.expand_dims(contour_reconstruct, axis=1)
    # make positive
    if contour_reconstruct.min() < 0:
        contour_reconstruct -= contour_reconstruct.min()
    # normalization
    contour_reconstruct *= 800 / contour_reconstruct.max()
    # type cast to int32
    contour_reconstruct = contour_reconstruct.astype(numpy.int32, copy=False)
    black = numpy.zeros((800, 800), numpy.uint8)
    # draw and visualize
    cv2.drawContours(black, contour_reconstruct, -1, 255, thickness=-1)
    cv2.imshow("black", black)
    return descriptor_in_use


def addNoise(descriptors):
    """this function adds gaussian noise to descriptors
    descriptors should be a [N,2] numpy array"""
    scale = descriptors.max() / 10
    noise = numpy.random.normal(0, scale, descriptors.shape[0])
    noise = noise + 1j * noise
    descriptors += noise



sample1 = cv2.imread("imgtest.jpg", 0)
cv2.imshow("none",sample1)

           
retval, sample1 = cv2.threshold(sample1, 130, 255, cv2.THRESH_BINARY_INV)#
del retval 

cv2.imshow("threshold",sample1)

fourier_result =findDescriptor (sample1)
print(fourier_result)

contour_reconstruct = reconstruct(fourier_result, MIN_DESCRIPTOR)
print("\n \n countour reconstruct")
print(contour_reconstruct)


cv2.waitKey(0)       
cv2.destroyAllWindows()