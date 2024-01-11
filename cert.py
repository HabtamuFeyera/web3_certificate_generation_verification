import openai
import cv2
import requests
import numpy as np
from PIL import Image
from io import BytesIO

# OpenAI API key
api_key = open("API_KEY.txt", "r").read().strip()

# Initialize OpenAI client
openai.api_key = api_key

try:
    # Generate an image using OpenAI API
    response = openai.Image.create(
        prompt="a white certificate background with space for text and logo",
        n=1
    )

    
    if response.get('status') == 'success':
        # Extract the image URL from the API response
        if 'data' in response and response['data'] and 'url' in response['data'][0]:
            image_url = response['data'][0]['url']

            # Download the generated image
            image_content = requests.get(image_url).content

            # Load the image using PIL
            image_pil = Image.open(BytesIO(image_content))
            image_np = np.array(image_pil)

            # Check if the image has an alpha channel
            if image_np.shape[2] == 4:
                # Convert RGBA to RGB
                image_np = cv2.cvtColor(image_np, cv2.COLOR_RGBA2RGB)
            else:
                # Convert BGR to RGB
                image_np = cv2.cvtColor(image_np, cv2.COLOR_BGR2RGB)

            # x, y, x_logo, y_logo, x_date, y_date with your actual values
            x, y = 10, 15  # Coordinates for Full Name
            x_logo, y_logo = 40, 5  # Coordinates for Logo
            x_date, y_date = 20, 30  # Coordinates for Date

            # Add Full Name, Logo, and Date to the image
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 1
            font_thickness = 2
            font_color = (0, 0, 0)  # Black color

            cv2.putText(image_np, "Full Name", (x, y), font, font_scale, font_color, font_thickness)
            cv2.putText(image_np, "logo", (x_logo, y_logo), font, font_scale, font_color, font_thickness)
            cv2.putText(image_np, "Date: January 10, 2024", (x_date, y_date), font, font_scale, font_color, font_thickness)

            # Display the final image
            cv2.imshow("Personalized Certificate", image_np)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        else:
            print(f"Invalid or missing image URL in the OpenAI API response.")

    else:
        print(f"OpenAI API request was not successful. Error: {response.get('error')}")

except Exception as e:
    print(f"An error occurred: {e}")
    

print("OpenAI API Response:", response)

