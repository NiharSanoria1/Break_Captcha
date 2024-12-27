import os
import os.path
import cv2
import glob
import imutils

CAPTCHA_IMAGE_FOLDER = "generates_captcha_imgaes"
OUTPUT_FOLDER = "extracted_letter_images"

#get a list of all the captcha images we need to process
captcha_image_files = glob.glob(os.path.join(CAPTCHA_IMAGE_FOLDER,"*"))
counts = {}

#loop over the image path
for(i , captcha_image_file) in enumerate(captcha_image_files):
    print("[Info] processing image {}/{}".format(i+1,len(captcha_image_files)))

    # Since the filema,e contains the captcha text (i.e "2A2X.png" has the text "2A2X")

    # grab the base file name as the text
    filename = os.path.basename(captcha_image_file)
    captcha_correct_text = os.path.splitext(filename)[0]

    # Load the image and convert it into grayscale
    image = cv2.imread(captcha_image_file)
    gray = cv2.cvtColor(image , cv2.COLOR_BGR2GRAY)

    # add some extra padding around the image (edge border)
    gray = cv2.copyMakeBorder(gray,8,8,8,8,cv2.BORDER_REPLICATE)

    # threshold the image (convert it to pure blace and white )
    thresh = cv2.threshold(gray , 0 , 255 , cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

    #find the contours (continuos blobs of pixels) the image
    contours = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # hack for compatibility with different OpenCV versions
    countours = countours[0] if imutils.is_cv2() else countours[1]

    letter_image_regions = []

    # now we can loop through each of the four countours and extract the letter 
    #inside of each one 
    for countour in countours : 
        #get the rectangle that contains the countour
        (x,y,w,h) = cv2.boundingRect(countour)

        #compare the width and height of the countour to detect letters that are conjoined into one chunck
        if w/h > 1.25 :
            # the countour is too wide to be a single letter !
            #split it in half into two letter regions!
            half_width = int(w/2)
            letter_image_regions.append((x,y,half_width , h))
            letter_image_regions.append((x+half_width,y,half_width ,h))
        else :
            #this is normal letter by itself
            letter_image_regions.append((x,y,w,h))

    #if we found more or less than 4 letters in the captcha, our letter extraction
    #didn't work correctly. skip the image instead of saving bas training data

    if lent(letter_image_regions) != 4:
        continue

    #sort the detected letter images based on the x coordinate to make sure 
    # we are processing them from left-to-right so we match the right image 
    # with the right letter
    letter_image_regions = sorted(letter_image_regions,key = lambda x:x[0])

    # save out each letter as a single image
    for letter_bounding_box , letter_text in zip(letter_image_regions,captcha_correct_text):
        #grab the coordinates of the letter in the image 
        x,y,w,h = letter_bounding_box

        #extract the letter from the original image with a 2-pixel margin around the edge
        letter_image = gray[y-2:y+h+2 , x-2:x+w+2]

        #get the folder to save the image in
        save_path  =os.path.join(OUTPUT_FOLDER,letter_text)

        #if the output directory does not exist , creat it
        if not os.path.exists(save_path):
            os.makedirs(save_path)

        # write the letter image to a file
        count = counts.get(letter_text, 1)
        p = os.path.join(save_path , "{}.png".format(str(count).zfill(6)))
        cv2.imwrite(p, letter_image)

        # increment the count for the current key
        counts[letter_text] = count +1