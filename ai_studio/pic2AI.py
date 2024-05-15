from openai import OpenAI
from config import *
import base64
import requests
set_gpt4o()
client = OpenAI()

# Function to encode the image
def convert_image_to_base64(image_path):
  with open(image_path, "rb") as image_file:
    base64_image = base64.b64encode(image_file.read()).decode("utf-8")
  return base64_image

image_path = "photos/1.jpg"
base64_image = convert_image_to_base64(image_path)


response = client.chat.completions.create(
  model="gpt-4o",
  messages=[
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "What’s in this image,response in chinese?"
        },
        {
          "type": "image_url",
          "image_url": {
            "url": f"data:image/jpeg;base64,{base64_image}"
          },
        },
      ],
    }
  ],
  max_tokens=300,
)

print(response.choices[0])