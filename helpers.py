import imutils
import cv2

def resize_to_fit(image , width , height):
    """
    A helper function to resize an image to fit within a given size
    :param image: image to resize
    :param width: desired width in pixels
    :param height: desired height in pixels
    :return: the resized image
    """
      
    #grab the dimensions of the image , then initialize the padding values
    if w>h:
      image = imutils.resize(image,width=width)

    #otherwise , the height is greater than the width so the resize along the height 
    else : 
      image = imutils.resize(image , height= height)

  #determine the padding values for the width and height to obtain the target dimensions
    padW = int((width - image.shape[1])/2.0)
    padH = int((height - image.shape[0])/2.0)

    # pad the image then apply one more resizing to handle any rounding isues
    image = cv2.copyMakeBorder(image,padH,padH,padW,cv2.BORDER_REPLICATE)
    
    image = cv2.resize(image , (width , height))

    # return the pre_processed image 
    return image
