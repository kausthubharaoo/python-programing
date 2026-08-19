import os
import streamlit as st
from google import genai
from google.genai import types
from pydantic import BaseModel, Field

# Define structured JSON output schema using Pydantic
class GrievanceAnalysis(BaseModel):
    category: str = Field(description="Department responsible: Water Supply, Road Maintenance, Sanitation, Electricity, or General")
    urgency: str = Field(description="Urgency level: Low, Medium, High, or Emergency")
    summary: str = Field(description="1-2 sentence executive summary of the complaint")
    recommended_action: str = Field(description="Immediate action for dispatch")

st.set_page_config(page_title="AI Governance Assistant", page_icon="🏛️", layout="centered")

st.title("🏛️ AI Citizen Grievance Router")
st.caption("Track 1 Prototype: AI for Digital Public Infrastructure & Governance")

# Check for API Key
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    api_key = st.text_input("Enter Gemini API Key:", type="password")

complaint_text = st.text_area(
    "Describe your complaint or civic issue:",
    placeholder="e.g., There is a huge water leak from a broken pipeline on 5th Main Street near the hospital. Water has been wasting for 3 hours.",
    height=120
)

if st.button("Submit Grievance", type="primary"):
    if not complaint_text:
        st.warning("Please enter a complaint before submitting.")
    elif not api_key:
        st.error("Please provide a Gemini API Key.")
    else:
        with st.spinner("Analyzing and routing grievance..."):
            try:
                client = genai.Client(api_key=api_key)
                
                response = client.models.generate_content(
                    model='gemini-3.6-flash',
                    contents=complaint_text,
                    config=types.GenerateContentConfig(
                        response_mime_type="application/json",
                        response_schema=GrievanceAnalysis,
                        system_instruction="You are an official AI Governance Assistant. Analyze the incoming citizen grievance and accurately route and categorize it.",
                    ),
                )
                
                # Parse JSON output
                result = GrievanceAnalysis.model_validate_json(response.text)
                
                st.success("Grievance Successfully Processed & Routed!")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Assigned Department", result.category)
                with col2:
                    st.metric("Urgency Level", result.urgency)
                    
                st.markdown("**Summary:**")
                st.info(result.summary)
                
                st.markdown("**Recommended Action:**")
                st.write(f"📌 {result.recommended_action}")
                
            except Exception as e:
                st.error(f"Error processing request: {e}")