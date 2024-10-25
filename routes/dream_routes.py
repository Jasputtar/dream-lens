from flask import Blueprint, render_template, request
import os
import vertexai
from vertexai.generative_models import GenerativeModel

# Create a blueprint for dream routes
dream_bp = Blueprint('dream', __name__)

# Set up Google Vertex AI credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "key/dreamapp_key.json"

project_id = "dreamapp-439417"  # Replace with your project ID
location = "us-central1"          # Replace with the location of your model
model_id = "gemini-1.5-flash-001"  # Replace with your model ID

vertexai.init(project=project_id, location=location)

prompt = """You are a dream interpreter specializing in various schools of dream analysis, including Jungian, Western, Mayan, and Indian interpretations. 

**User Input:** {dream_description}

**Interpretation Style:** {requested_style} 

1. Provide a detailed interpretation of the dream based on the chosen style.
2. Identify and extract the key symbols from the dream.
3. For each symbol, provide its meaning according to the specified interpretation style.
4. Present your response in a clear and organized format, separating the interpretation and the symbols with their meanings.

**Response Format:**
- **Dream Interpretation:**
  - [Your detailed interpretation here]
  
- **Extracted Symbols and Meanings:**
  - **Symbol 1:** [Symbol Name]
    - Meaning: [Meaning of Symbol 1]
  - **Symbol 2:** [Symbol Name]
    - Meaning: [Meaning of Symbol 2]
  - [Continue for additional symbols...]
"""

model = GenerativeModel(
    model_name=model_id,
    system_instruction=prompt,
)

@dream_bp.route("/", methods=["GET", "POST"])
def index():
    interpretation = None
    if request.method == "POST":
        dream_description = request.form.get("dream_description")
        requested_style = request.form.get("requested_style")
        
        # Generate the response from the model
        response = model.generate_content([prompt.format(dream_description=dream_description, requested_style=requested_style)])
        interpretation = response.text
        
    return render_template("index.html", interpretation=interpretation)
