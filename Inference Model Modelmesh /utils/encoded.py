from PIL import Image
import base64

# Open the image file
with open('/home/hungnguyen/Capstone-Project-Model-Serving/high-density-model-serving/images/car_1.jpg', 'rb') as image_file:
    # Read the image data
    image_data = image_file.read()

# Encode the image data to base64
base64_encoded_image = base64.b64encode(image_data).decode('utf-8')

print("Base64 encoded image:", base64_encoded_image)











