import streamlit as st
from pathlib import Path
import google.generativeai as genai

from api_key import api_key

genai.configure(api_key=api_key)

generation_config = {
    "temperature": 0.4,
    "top_p": 1,
    "top_k": 32,
    "max_output_tokens": 4096
}

safety_settings = [
{
"category": "HARM_CATEGORY_HARASSMENT",
"threshold": "BLOCK_MEDIUM_AND_ABOVE"
},
{
"category": "HARM_CATEGORY_HATE_SPEECH",
"threshold": "BLOCK_MEDIUM_AND_ABOVE"
},
{
"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
"threshold": "BLOCK_MEDIUM_AND_ABOVE"
},
{
"category": "HARM_CATEGORY_DANGEROUS_CONTENT",
"threshold": "BLOCK_MEDIUM_AND_ABOVE"
}
]

system_prompt = """

As a highly skilled medical practitioner specializing in image analysis, you are tasked with examining medical images for a renowned hospital. Your expertise is crucial in identifying any anomalies, diseases, or health issues that may be present in the image.

Your responsibilities include:

    1.Detailed Analysis : Throughly analuze each image, focusing on identifying the abnormal findings.
    2.Findings Report: Document all observed anomalies or signs of disease. Clearly articulate these findings in structured format.
    3.Recommendations and Next Steps: Based on your analysis, suggest potential next steps further tests and treantment as applicable.
    4.Treatment Suggestions: If appropraite , recommend possible treatment options or interventions.

Important Notes:
    1.Scope of response: Only respond if the image pertains to human health issues.
    2.Clarity of Image: In case where the image quality impedes clear analysis, note that certain ascpects are 'Unable to determined based on the provided image.'
    3.Disclaimer : Accompany your analysis with the decalimer: "Conult with a doctor before making any decisions".
    4.Your insights are invaluable in guiding clinical decisions. Please proceed with the analysis, adhering to the structured approach outlined above.
"""

model = genai.GenerativeModel(
  model_name="gemini-pro-vision",
  generation_config=generation_config,
  # safety_settings = Adjust safety settings
  
)


st.set_page_config(page_title="MedAI")

st.title("MedAI")

st.subheader("Get all the medical analysis with one click")

uploaded_file = st.file_uploader("Upload your medical image for analysis", type=["png", "jpeg", "jpg"])

if uploaded_file:
    st.image(uploaded_file, width=300, caption="Uploaded Image")
submit_button = st.button("Generate the Analysis")

if submit_button:
    #process the uploaded image
    image_data=uploaded_file.getvalue()
    image_parts = [
        {
            "mime_type": "image/jpeg",
            "data": image_data
        },
    ]

    prompt_parts = [
        image_parts[0],
        system_prompt
    ]

    # Generate a response based on prompt and image
    response = model.generate_content (prompt_parts)
    st.write (response.text)