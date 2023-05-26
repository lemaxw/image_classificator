import requests
import base64
import sys

def get_tags_google(image_path):
  # Your API key
  api_key = 'AIzaSyA-7Nif6WHWqJqoOqGDch9sQVfB4XPOZyY'

  # The URL of the Vision API
  url = f"https://vision.googleapis.com/v1/images:annotate?key={api_key}"

  # The image data
  image_data = base64.b64encode(open(image_path, 'rb').read()).decode()

  # The JSON payload
  payload = {
    "requests": [
      {
        "image": {
          "content": image_data
        },
        "features": [
          {
            "type": "LABEL_DETECTION"
          }
        ]
      }
    ]
  }

  # Make the request
  response = requests.post(url, json=payload)

  # Get the response data
  data = response.json()

  ret_res = {};
  # Extract and print labels
  labels = data['responses'][0]['labelAnnotations']
  for label in labels:
    ret_res[label['description'].lower()] = label['score'];
  #    print(f"{label['description'].lower()}, {label['score']}") 
  return ret_res