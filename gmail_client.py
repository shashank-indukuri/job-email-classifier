"""Gmail API client for email operations"""

import os
import json
import base64
from datetime import datetime, timedelta
from typing import List, Dict, Optional

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from bs4 import BeautifulSoup

SCOPES = ['https://www.googleapis.com/auth/gmail.modify']


class GmailClient:
    """Simple Gmail API client"""
    
    def __init__(self, token_file: str = 'token.json'):
        self.service = None
        self.token_file = token_file
    
    def authenticate(self) -> bool:
        """Authenticate with Gmail API"""
        creds = None
        
        # Load existing token
        if os.path.exists(self.token_file):
            creds = Credentials.from_authorized_user_file(self.token_file, SCOPES)
        
        # Refresh or get new credentials
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not os.path.exists('credentials.json'):
                    print("❌ credentials.json not found!")
                    print("📋 Please download OAuth credentials from Google Cloud Console")
                    return False
                
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            
            # Save credentials
            with open(self.token_file, 'w') as token:
                token.write(creds.to_json())
        
        self.service = build('gmail', 'v1', credentials=creds)
        return True
    
    def get_unlabeled_emails(self, days: int = 7, max_results: int = 50) -> List[Dict]:
        """Fetch emails that haven't been labeled by our system"""
        try:
            after_date = (datetime.now() - timedelta(days=days)).strftime('%Y/%m/%d')
            
            # Query for emails without our labels
            query = f'after:{after_date} -label:"🚀 Seeds Planted" -label:"⚡ Action Required" -label:"📦 Inbox Clutter"'
            
            results = self.service.users().messages().list(
                userId='me',
                q=query,
                maxResults=max_results
            ).execute()
            
            messages = results.get('messages', [])
            emails = []
            
            for message in messages:
                email_data = self._get_email_details(message['id'])
                if email_data:
                    emails.append(email_data)
            
            return emails
            
        except HttpError as error:
            print(f'Gmail API error: {error}')
            return []
    
    def _get_email_details(self, message_id: str) -> Optional[Dict]:
        """Get email details"""
        try:
            message = self.service.users().messages().get(
                userId='me',
                id=message_id,
                format='full'
            ).execute()
            
            headers = message['payload'].get('headers', [])
            subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No Subject')
            sender = next((h['value'] for h in headers if h['name'] == 'From'), 'Unknown')
            date = next((h['value'] for h in headers if h['name'] == 'Date'), '')
            
            body = self._extract_body(message['payload'])
            
            return {
                'id': message_id,
                'subject': subject,
                'sender': sender,
                'date': date,
                'body': body,
                'snippet': message.get('snippet', '')
            }
            
        except HttpError:
            return None
    
    def _extract_body(self, payload: Dict) -> str:
        """Extract email body text"""
        body = ""
        
        if 'parts' in payload:
            for part in payload['parts']:
                if part['mimeType'] == 'text/plain' and 'data' in part['body']:
                    data = part['body']['data']
                    body = base64.urlsafe_b64decode(data).decode('utf-8', errors='ignore')
                    break
                elif part['mimeType'] == 'text/html' and 'data' in part['body']:
                    data = part['body']['data']
                    html = base64.urlsafe_b64decode(data).decode('utf-8', errors='ignore')
                    soup = BeautifulSoup(html, 'html.parser')
                    body = soup.get_text()
        else:
            if 'data' in payload['body']:
                data = payload['body']['data']
                text = base64.urlsafe_b64decode(data).decode('utf-8', errors='ignore')
                if payload['mimeType'] == 'text/html':
                    soup = BeautifulSoup(text, 'html.parser')
                    body = soup.get_text()
                else:
                    body = text
        
        return body.strip()
    
    def get_or_create_label(self, label_name: str) -> Optional[str]:
        """Get existing label ID or create new one"""
        try:
            # Check if label exists
            labels = self.service.users().labels().list(userId='me').execute()
            for label in labels['labels']:
                if label['name'] == label_name:
                    return label['id']
            
            # Create new label
            label_object = {
                'name': label_name,
                'labelListVisibility': 'labelShow',
                'messageListVisibility': 'show'
            }
            
            created = self.service.users().labels().create(
                userId='me',
                body=label_object
            ).execute()
            
            return created['id']
            
        except HttpError as error:
            print(f'Error managing label: {error}')
            return None
    
    def apply_label(self, message_id: str, label_id: str) -> bool:
        """Apply label to email"""
        try:
            self.service.users().messages().modify(
                userId='me',
                id=message_id,
                body={'addLabelIds': [label_id]}
            ).execute()
            return True
        except HttpError:
            return False
