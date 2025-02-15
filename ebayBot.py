"""
Install an additional SDK for JSON schema support Google AI Python SDK

$ pip install google.ai.generativelanguage
"""

import os
import google.generativeai as genai
from google.ai.generativelanguage_v1beta.types import content

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

def upload_to_gemini(path, mime_type=None):
  """Uploads the given file to Gemini.

  See https://ai.google.dev/gemini-api/docs/prompting_with_media
  """
  file = genai.upload_file(path, mime_type=mime_type)
  print(f"Uploaded file '{file.display_name}' as: {file.uri}")
  return file

# Create the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-2.0-flash",
  generation_config=generation_config,
  # Google Search as a tool is not available in this version of the SDK.
  # Please try the new genAI SDK (https://ai.google.dev/gemini-api/docs/sdks)
  # and see the docs here (https://ai.google.dev/gemini-api/docs/grounding?lang=python#search-tool)
)

# TODO Make these files available on the local file system
# You may need to update the file paths
files = [
  upload_to_gemini("Image February 15, 2025 - 12:23PM.jpeg", mime_type="image/jpeg"),
]

chat_session = model.start_chat(
  history=[
    {
      "role": "user",
      "parts": [
        files[0],
        "Tell me what product is in this image please",
      ],
    },
    {
      "role": "model",
      "parts": [
        "```json\n{\n  \"product_name\": \"New Balance 515\"\n}\n```",
      ],
    },
    {
      "role": "user",
      "parts": [
        "Can you tell me how much a second hand New Balance 515 costs\n",
      ],
    },
    {
      "role": "model",
      "parts": [
        "The cost of second-hand New Balance 515 sneakers can vary quite a bit depending on factors like condition, size, and specific style. Based on listings on eBay, you can find them for as low as $16.00 or as high as $64.95. Many pairs are listed in the $25 to $55 range.\n",
      ],
    },
  ]
)

response = chat_session.send_message("INSERT_INPUT_HERE")

print(response.text)