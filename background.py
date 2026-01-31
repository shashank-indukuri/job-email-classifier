#!/usr/bin/env python3
"""Background service for continuous email monitoring"""

import os
import time
import logging
import argparse
from datetime import datetime
from gmail_client import GmailClient
from classifier import GroqClassifier

def parse_args():
    parser = argparse.ArgumentParser(description='Job Email Classifier Background Service')
    parser.add_argument('--days', type=int, help='Number of days to check for emails (overrides env var)')
    parser.add_argument('--interval', type=int, help='Check interval in minutes (overrides env var)')
    return parser.parse_args()

# Parse command line arguments
args = parse_args()

# Configuration
CHECK_INTERVAL_MINUTES = args.interval or int(os.getenv('CHECK_INTERVAL_MINUTES', '15'))
DAYS_TO_CHECK = args.days or int(os.getenv('DAYS_TO_CHECK', '1'))
MAX_EMAILS = int(os.getenv('MAX_EMAILS', '50'))

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('classifier.log'),
        logging.StreamHandler()
    ]
)


def process_emails(gmail_client: GmailClient, classifier: GroqClassifier) -> int:
    """Process unlabeled emails"""
    try:
        # Fetch unlabeled emails
        emails = gmail_client.get_unlabeled_emails(
            days=DAYS_TO_CHECK,
            max_results=MAX_EMAILS
        )
        
        if not emails:
            logging.info("✅ No unlabeled emails found")
            return 0
        
        logging.info(f"📥 Found {len(emails)} emails to process")
        
        # Process each email
        processed = 0
        for email in emails:
            try:
                # Classify
                category, confidence, reason = classifier.classify_email(email)
                
                # Get label
                label_name = classifier.get_label_name(category)
                label_id = gmail_client.get_or_create_label(label_name)
                
                # Apply label
                if label_id:
                    gmail_client.apply_label(email['id'], label_id)
                    processed += 1
                    logging.info(
                        f"✅ {email['subject'][:50]}... → {label_name} ({confidence:.0%})"
                    )
                
            except Exception as e:
                logging.error(f"❌ Error processing email: {e}")
        
        return processed
        
    except Exception as e:
        logging.error(f"❌ Error in process_emails: {e}")
        return 0


def main():
    """Main background service loop"""
    print("🚀 Job Email Classifier - Background Service")
    print("=" * 50)
    print(f"📅 Checking emails from last {DAYS_TO_CHECK} days")
    print(f"⏰ Check interval: {CHECK_INTERVAL_MINUTES} minutes")
    print("=" * 50)
    
    # Check credentials
    if not os.path.exists('credentials.json'):
        print("❌ credentials.json not found!")
        print("📋 Please download OAuth credentials from Google Cloud Console")
        return
    
    if not os.path.exists('.env'):
        print("❌ .env file not found!")
        print("📋 Please create .env with your GROQ_API_KEY")
        return
    
    # Initialize clients
    print("🔐 Authenticating with Gmail...")
    gmail_client = GmailClient()
    
    if not gmail_client.authenticate():
        print("❌ Gmail authentication failed")
        return
    
    print("✅ Gmail authenticated")
    
    print("🤖 Initializing Groq classifier...")
    try:
        classifier = GroqClassifier()
        print(f"✅ Classifier ready (model: {classifier.model})")
    except ValueError as e:
        print(f"❌ {e}")
        return
    
    # Start monitoring
    print(f"⏰ Checking every {CHECK_INTERVAL_MINUTES} minutes")
    print(f"📧 Processing last {DAYS_TO_CHECK} day(s) of emails")
    print("Press Ctrl+C to stop\n")
    
    total_processed = 0
    
    try:
        while True:
            start_time = datetime.now()
            logging.info(f"🔍 Starting check at {start_time.strftime('%H:%M:%S')}")
            
            # Process emails
            processed = process_emails(gmail_client, classifier)
            total_processed += processed
            
            # Log stats
            elapsed = (datetime.now() - start_time).total_seconds()
            logging.info(
                f"📊 Processed {processed} emails in {elapsed:.1f}s "
                f"(Total: {total_processed})"
            )
            
            # Sleep until next check
            logging.info(f"😴 Sleeping for {CHECK_INTERVAL_MINUTES} minutes...\n")
            time.sleep(CHECK_INTERVAL_MINUTES * 60)
            
    except KeyboardInterrupt:
        print("\n🛑 Stopping background service...")
        print(f"✅ Total emails processed: {total_processed}")
        print("👋 Goodbye!")


if __name__ == "__main__":
    main()
