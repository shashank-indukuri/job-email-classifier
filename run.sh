#!/bin/bash
# Simple launcher script for Job Email Classifier

echo "📧 Job Email Classifier"
echo "======================="
echo ""
echo "Choose an option:"
echo "1) Run Web Interface (Streamlit)"
echo "2) Run Background Service"
echo "3) Exit"
echo ""
read -p "Enter choice [1-3]: " choice

case $choice in
    1)
        echo "🚀 Starting web interface..."
        if command -v uv &> /dev/null; then
            uv run streamlit run app.py
        else
            python -m streamlit run app.py
        fi
        ;;
    2)
        echo "🚀 Starting background service..."
        if command -v uv &> /dev/null; then
            uv run python background.py
        else
            python background.py
        fi
        ;;
    3)
        echo "👋 Goodbye!"
        exit 0
        ;;
    *)
        echo "❌ Invalid choice"
        exit 1
        ;;
esac
