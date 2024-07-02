import numpy as np
import cv2
from PIL import Image
import matplotlib.pyplot as plt

def colorize_image(image_path):
    # Load the image
    image = Image.open(image_path)
    open_cv_image = np.array(image)
    open_cv_image = open_cv_image[:, :, ::-1].copy()

    # Convert image to grayscale
    gray_image = cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2GRAY)
    gray_image = cv2.cvtColor(gray_image, cv2.COLOR_GRAY2BGR)

    # Load pre-trained colorization model files
    proto_file = "colorization_deploy_v2.prototxt"
    model_file = "colorization_release_v2.caffemodel"
    hull_pts = "pts_in_hull.npy"

    # Load the model
    net = cv2.dnn.readNetFromCaffe(proto_file, model_file)

    # Load the cluster centers
    pts_in_hull = np.load(hull_pts)
    pts_in_hull = pts_in_hull.transpose().reshape(2, 313, 1, 1)

    # Add the cluster centers as 1x1 convolutions to the model
    net.getLayer(net.getLayerId('class8_ab')).blobs = [pts_in_hull.astype(np.float32)]
    net.getLayer(net.getLayerId('conv8_313_rh')).blobs = [np.full([1, 313], 2.606, np.float32)]

    # Convert the image to a format compatible with the model
    normalized = gray_image.astype("float32") / 255.0
    lab = cv2.cvtColor(normalized, cv2.COLOR_BGR2LAB)
    l = lab[:, :, 0]

    # Resize the L channel to 224x224 (the size the model was trained on)
    resized_l = cv2.resize(l, (224, 224))
    resized_l -= 50  # Subtract 50 for mean-centering

    # Predict the a and b channels
    net.setInput(cv2.dnn.blobFromImage(resized_l))
    ab = net.forward()[0, :, :, :].transpose((1, 2, 0))

    # Resize the predicted a and b channels to the original size
    ab = cv2.resize(ab, (open_cv_image.shape[1], open_cv_image.shape[0]))

    # Combine the original L channel with the predicted a and b channels
    lab = np.concatenate((l[:, :, np.newaxis], ab), axis=2)

    # Convert the LAB image back to BGR
    colorized = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
    colorized = (colorized * 255).astype("uint8")

    return Image.fromarray(colorized)

# Path to your black and white image
image_path = "SCAN0002.JPG"
colorized_image = colorize_image(image_path)

# Display the colorized image
plt.imshow(colorized_image)
plt.axis('off')
plt.show()
