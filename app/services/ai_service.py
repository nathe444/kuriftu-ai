import google.generativeai as genai
from typing import List
from app.core.config import settings
from app.db.models import KuriftuService

class AIService:
    def __init__(self):
        genai.configure(api_key=settings.GOOGLE_API_KEY)
        try:
            # Use the newer model version
            self.model = genai.GenerativeModel('gemini-1.5-pro')
        except Exception as e:
            print(f"Error initializing model: {e}")
            self.model = None
        
    def _format_services(self, services: List[KuriftuService]) -> str:
        formatted_services = []
        for service in services:
            formatted_services.append(
                f"- {service.name}\n"
                f"  Description: {service.description}\n"
                f"  Category: {service.category}\n"
                f"  Location: {service.location}\n"
            )
        return "\n".join(formatted_services)
        
    def generate_itinerary(self, user_interests: str, matched_services: List[KuriftuService], days: int = 3) -> str:
        try:
            prompt = f"""
            Create a {days}-day itinerary based on these interests:
            {user_interests}
            
            Available Services:
            {self._format_services(matched_services)}
            
            Format the response EXACTLY as follows:
            **{days}-Day Personalized Itinerary**

            **Day 1: [Day Title]**
            * **Morning:** [Activity] (Location) - [Description]
            * **Afternoon:** [Activity] (Location) - [Description]
            * **Evening:** [Activity] (Location) - [Description]

            [Repeat for each day]
            """
            
            response = self.model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            print(f"Error generating itinerary: {e}")
            return ""

# Create a singleton instance
ai_service = AIService()