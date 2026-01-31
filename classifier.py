"""Email classifier using Groq API"""

import os
from typing import Dict, Tuple
from groq import Groq
from dotenv import load_dotenv

load_dotenv()


class GroqClassifier:
    """Simple email classifier using Groq's LLM API"""
    
    # Label mapping - matches original project
    LABELS = {
        'application_submitted': '🚀 Seeds Planted',
        'followup_required': '⚡ Action Required',
        'other': '📦 Inbox Clutter'
    }
    
    def __init__(self, model: str = None):
        api_key = os.getenv('GROQ_API_KEY')
        if not api_key:
            raise ValueError("GROQ_API_KEY not found in .env file")
        
        self.client = Groq(api_key=api_key)
        self.model = model or os.getenv('GROQ_MODEL', 'openai/gpt-oss-20b')
    
    def classify_email(self, email: Dict) -> Tuple[str, float, str]:
        """
        Classify an email with exponential backoff retry
        
        Returns:
            (category, confidence, reasoning)
        """
        import time
        import random
        
        # Initial delay to prevent rate limiting
        time.sleep(3 + random.uniform(0, 2))
        
        prompt = self._create_prompt(email)
        max_retries = 10
        base_delay = 5
        
        for attempt in range(max_retries + 1):
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {
                            "role": "system",
                            "content": "You are an expert email classifier for job applications. Respond only with the exact format requested."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    temperature=0.1,
                    max_tokens=200
                )
                
                result = response.choices[0].message.content.strip()
                
                return self._parse_response(result)
                
            except Exception as e:
                if "429" in str(e):
                    # Exponential backoff: 5s, 10s, 20s, 40s, 80s... + jitter
                    delay = min(base_delay * (2 ** attempt), 300) + random.uniform(0, 5)
                    print(f"⚠️ Rate limited, retrying in {delay:.1f}s (attempt {attempt + 1}/{max_retries + 1})")
                    time.sleep(delay)
                    continue
                else:
                    print(f"⚠️ Classification error: {e}")
                    return 'other', 0.5, 'Classification failed'
        
        print("⚠️ Max retries exceeded, but continuing...")
        return 'other', 0.5, 'Rate limited - will retry later'
    
    def _create_prompt(self, email: Dict) -> str:
        """Create classification prompt - exact prompt from working project"""
        subject = email.get('subject', '')
        sender = email.get('sender', '')
        snippet = email.get('snippet', '')
        body = email.get('body', '')[:1000]  # Limit body length
        
        return f"""You are an expert email classifier specializing in job application emails. Your task is to classify emails into exactly one of these three categories:

1. **application_submitted** - Confirmation emails after submitting job applications
2. **followup_required** - Important emails requiring immediate action (interviews, document requests, offers)
3. **other** - All other emails (marketing, job alerts, newsletters, GitHub notifications, non-job related)

**IMPORTANT**: Job alert emails, marketing emails from job sites, and promotional content should ALWAYS be classified as "other" even if they mention jobs.

**Examples:**

Example 1:
Subject: "Just in: Comresource has new Senior Machine Learning Engineer jobs open"
Sender: lensa.com
CLASSIFICATION: other
REASON: Job alert/marketing email, not an application confirmation

Example 2:
Subject: "software engineer": Morningstar - Software Engineer and more
Sender: linkedin.com
CLASSIFICATION: other
REASON: LinkedIn job alert, promotional content

Example 3:
Subject: Re: [username/repo] Pull Request #7
Sender: github.com
CLASSIFICATION: other
REASON: GitHub notification, not job-related

Example 4:
Subject: Thank you for your application - Software Engineer Position
Sender: hr@techcompany.com
CLASSIFICATION: application_submitted
REASON: Direct application confirmation from company HR

Example 5:
Subject: Interview Invitation - Next Steps for Software Engineer Role
Sender: recruiter@company.com
CLASSIFICATION: followup_required
REASON: Interview invitation requiring immediate response

Example 6:
Subject: Thank you for your interest in our Software Engineer opening at Podium
Sender: no-reply@us.greenhouse-mail.io
Body: Unfortunately, the decision has been made to hold on filling the position for the time being
CLASSIFICATION: other
REASON: Job rejection email, no action needed

Example 7:
Subject: Sai, your application was sent to Theoris
Sender: jobs-noreply@linkedin.com
CLASSIFICATION: application_submitted
REASON: Application confirmation - application was sent/submitted

Example 8:
Subject: Your recent job application for Analyst - 244748
Sender: hdow.fa.sender@workflow.email.us-ashburn-1.ocs.oraclecloud.com
Body: Thank you for taking the time to apply for a position for Analyst at Newmark. We are now reviewing your application
CLASSIFICATION: application_submitted
REASON: Application confirmation - company acknowledging receipt and reviewing application

**Now classify this email:**
- Subject: {subject}
- Sender: {sender}
- Preview: {snippet}
- Body: {body}

**Key Classification Rules:**
- Job alerts from job sites (LinkedIn, Indeed, Lensa, etc.) = other
- Marketing emails with job listings = other
- GitHub/code repository notifications = other
- Newsletter/promotional content = other
- jobalerts-noreply@linkedin.com = other (job alerts/marketing)
- jobs-noreply@linkedin.com = application_submitted (application confirmation) 
- Only classify as "application_submitted" if it's a direct confirmation from a company you applied to
- Only classify as "followup_required" if it requires immediate action (interview, documents, offer)
- "is for" in subject typically means application_submitted (e.g., "Your application is for Software Engineer")

Respond exactly as:
CLASSIFICATION: [category]
CONFIDENCE: [0.0-1.0]
REASON: [brief explanation]
"""
    
    def _parse_response(self, response: str) -> Tuple[str, float, str]:
        """Parse LLM response"""
        category = 'other'
        confidence = 0.5
        reason = 'Parsed from AI response'
        
        lines = response.strip().split('\n')
        
        for line in lines:
            line = line.strip()
            if line.startswith('CLASSIFICATION:'):
                cat = line.split(':', 1)[1].strip().lower()
                if cat in self.LABELS:
                    category = cat
            elif line.startswith('CONFIDENCE:'):
                try:
                    confidence = float(line.split(':', 1)[1].strip())
                except:
                    confidence = 0.7
            elif line.startswith('REASON:'):
                reason = line.split(':', 1)[1].strip()
        
        # Validate classification
        valid_classifications = ['application_submitted', 'followup_required', 'other']
        if category not in valid_classifications:
            category = 'other'
            confidence = 0.3
        
        return category, confidence, reason
    
    def get_label_name(self, category: str) -> str:
        """Get Gmail label name for category"""
        return self.LABELS.get(category, self.LABELS['other'])
