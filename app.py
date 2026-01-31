"""Streamlit web interface for Job Email Classifier"""

import streamlit as st
import time
import logging
from datetime import datetime
from gmail_client import GmailClient
from classifier import GroqClassifier

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

st.set_page_config(
    page_title="Job Email Classifier",
    page_icon="📧",
    layout="wide"
)


def init_session_state():
    """Initialize session state"""
    if 'gmail_client' not in st.session_state:
        st.session_state.gmail_client = GmailClient()
    if 'classifier' not in st.session_state:
        try:
            st.session_state.classifier = GroqClassifier()
        except ValueError as e:
            st.error(f"❌ {e}")
            st.info("Please create a .env file with your GROQ_API_KEY")
            st.stop()
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'emails' not in st.session_state:
        st.session_state.emails = []


def main():
    init_session_state()
    
    # Header
    st.markdown("""
    <div style="background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); 
                padding: 2rem; border-radius: 10px; color: white; 
                text-align: center; margin-bottom: 2rem;">
        <h1>📧 Job Email Classifier</h1>
        <p>Never miss an important job application email again!</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("🔧 Setup")
        
        # Authentication
        if not st.session_state.authenticated:
            if st.button("🔐 Connect to Gmail", type="primary"):
                with st.spinner("Authenticating..."):
                    if st.session_state.gmail_client.authenticate():
                        st.session_state.authenticated = True
                        st.success("✅ Connected!")
                        st.rerun()
                    else:
                        st.error("❌ Authentication failed")
        else:
            st.success("✅ Gmail Connected")
        
        st.divider()
        
        # Settings
        st.header("⚙️ Settings")
        days = st.slider("Days to check", 1, 30, 7)
        max_emails = st.slider("Max emails", 10, 100, 50)
        
        # Auto-process toggle
        auto_process = st.toggle("🔄 Auto-Process (continuous monitoring)", value=False)
        if auto_process:
            interval = st.slider("Check interval (minutes)", 5, 60, 15)
            st.info(f"🔄 Auto-processing enabled - will check every {interval} minutes")
        
        st.divider()
        
        # Classify button (only show if auto-process is disabled)
        if st.session_state.authenticated:
            if not auto_process and st.button("🤖 Classify Emails", type="primary"):
                with st.spinner("Fetching and classifying emails..."):
                    logging.info(f"🔍 Starting email classification - checking last {days} days")
                    
                    emails = st.session_state.gmail_client.get_unlabeled_emails(
                        days=days,
                        max_results=max_emails
                    )
                    
                    if not emails:
                        st.info("✅ No unlabeled emails found!")
                        logging.info("✅ No unlabeled emails found")
                    else:
                        st.info(f"📥 Found {len(emails)} emails to classify")
                        logging.info(f"📥 Found {len(emails)} emails to process")
                        
                        # Classify and label
                        results = []
                        progress_bar = st.progress(0)
                        
                        for i, email in enumerate(emails):
                            category, confidence, reason = st.session_state.classifier.classify_email(email)
                            
                            # Apply label
                            label_name = st.session_state.classifier.get_label_name(category)
                            label_id = st.session_state.gmail_client.get_or_create_label(label_name)
                            
                            if label_id:
                                st.session_state.gmail_client.apply_label(email['id'], label_id)
                            
                            # Log the classification
                            subject = email.get('subject', 'No Subject')[:50]
                            logging.info(f"✅ \"{subject}\": {email.get('sender', 'Unknown')} → {label_name} ({confidence:.0%})")
                            
                            results.append({
                                'email': email,
                                'category': category,
                                'confidence': confidence,
                                'reason': reason,
                                'label': label_name
                            })
                            
                            progress_bar.progress((i + 1) / len(emails))
                        
                        st.session_state.emails = results
                        logging.info(f"🎉 Completed processing {len(emails)} emails")
                        st.success(f"✅ Classified and labeled {len(results)} emails!")
                        st.rerun()
        
        # Auto-process functionality
        if st.session_state.authenticated and auto_process:
            if 'last_check' not in st.session_state:
                st.session_state.last_check = time.time()
            
            current_time = time.time()
            time_since_last = current_time - st.session_state.last_check
            next_check_in = (interval * 60) - time_since_last
            
            if next_check_in <= 0:
                # Time for auto-check
                with st.spinner("Auto-processing emails..."):
                    logging.info(f"🔄 Auto-check starting - checking last {days} days")
                    
                    emails = st.session_state.gmail_client.get_unlabeled_emails(
                        days=days,
                        max_results=max_emails
                    )
                    
                    if emails:
                        logging.info(f"📥 Auto-process found {len(emails)} emails")
                        
                        for email in emails:
                            category, confidence, reason = st.session_state.classifier.classify_email(email)
                            label_name = st.session_state.classifier.get_label_name(category)
                            label_id = st.session_state.gmail_client.get_or_create_label(label_name)
                            
                            if label_id:
                                st.session_state.gmail_client.apply_label(email['id'], label_id)
                            
                            subject = email.get('subject', 'No Subject')[:50]
                            logging.info(f"✅ \"{subject}\": {email.get('sender', 'Unknown')} → {label_name} ({confidence:.0%})")
                        
                        st.success(f"🔄 Auto-processed {len(emails)} emails!")
                        logging.info(f"🎉 Auto-process completed {len(emails)} emails")
                    else:
                        logging.info("✅ Auto-check: No unlabeled emails found")
                
                st.session_state.last_check = current_time
                st.rerun()
            else:
                st.info(f"⏰ Next auto-check in {int(next_check_in/60)}:{int(next_check_in%60):02d}")
                time.sleep(5)  # Refresh every 5 seconds
                st.rerun()
        
        else:
            st.warning("Connect to Gmail first")
        
        st.divider()
        
        # Info
        st.caption("🔒 Privacy: All processing happens locally")
        st.caption("🆓 Free: Uses Groq's free API tier")
    
    # Main content
    if st.session_state.emails:
        display_results(st.session_state.emails)
    else:
        display_welcome()


def display_results(results):
    """Display classification results"""
    st.header("📊 Classification Results")
    
    # Stats
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Emails", len(results))
    
    with col2:
        app_count = sum(1 for r in results if r['category'] == 'application_submitted')
        st.metric("🚀 Seeds Planted", app_count)
    
    with col3:
        action_count = sum(1 for r in results if r['category'] == 'followup_required')
        st.metric("⚡ Action Required", action_count)
    
    with col4:
        other_count = sum(1 for r in results if r['category'] == 'other')
        st.metric("📦 Inbox Clutter", other_count)
    
    st.divider()
    
    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "📧 All Emails",
        "🚀 Seeds Planted",
        "⚡ Action Required",
        "📦 Inbox Clutter"
    ])
    
    with tab1:
        display_email_list(results)
    
    with tab2:
        app_emails = [r for r in results if r['category'] == 'application_submitted']
        if app_emails:
            display_email_list(app_emails)
        else:
            st.info("No application confirmation emails found")
    
    with tab3:
        action_emails = [r for r in results if r['category'] == 'followup_required']
        if action_emails:
            display_email_list(action_emails)
        else:
            st.info("No action-required emails found")
    
    with tab4:
        other_emails = [r for r in results if r['category'] == 'other']
        if other_emails:
            display_email_list(other_emails)
        else:
            st.info("No other emails found")


def display_email_list(results):
    """Display list of emails"""
    for result in results:
        email = result['email']
        category = result['category']
        confidence = result['confidence']
        reason = result['reason']
        label = result['label']
        
        # Category emoji
        emoji = {
            'application_submitted': '🚀',
            'followup_required': '⚡',
            'other': '📦'
        }.get(category, '📧')
        
        with st.expander(f"{emoji} {email['subject'][:70]}..."):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.write(f"**From:** {email['sender']}")
                st.write(f"**Date:** {email['date']}")
                st.write(f"**Preview:** {email['snippet'][:200]}...")
            
            with col2:
                st.metric("Category", label)
                st.metric("Confidence", f"{confidence:.0%}")
                st.caption(f"💭 {reason}")


def display_welcome():
    """Display welcome screen"""
    st.info("👈 Connect to Gmail and click 'Classify Emails' to get started!")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 🚀 Quick Setup
        
        1. **Get Groq API Key**
           - Visit [console.groq.com](https://console.groq.com)
           - Sign up (free)
           - Create API key
           - Add to `.env` file
        
        2. **Setup Gmail API**
           - Go to [Google Cloud Console](https://console.cloud.google.com/)
           - Create project
           - Enable Gmail API
           - Create OAuth credentials
           - Download as `credentials.json`
        
        3. **Connect & Classify**
           - Click "Connect to Gmail"
           - Authorize the app
           - Click "Classify Emails"
        """)
    
    with col2:
        st.markdown("""
        ### ✨ Features
        
        - **🤖 AI-Powered** - Uses Groq's fast LLM
        - **🏷️ Auto-Labels** - Organizes Gmail automatically
        - **🔒 Private** - Runs on your machine
        - **⚡ Fast** - Processes emails in seconds
        - **🆓 Free** - No cost to use
        
        ### 📋 Categories
        
        - **🚀 Seeds Planted** - Application confirmations
        - **⚡ Action Required** - Interviews, offers
        - **📦 Inbox Clutter** - Alerts, marketing, rejections
        """)


if __name__ == "__main__":
    main()
