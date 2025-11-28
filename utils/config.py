"""
Configuration module for secure API key handling.
Uses environment variables and Streamlit secrets.
"""

import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file (override=True to refresh)
load_dotenv(override=True)


class Config:
    """
    Secure configuration management for NexSupply.
    Handles API keys and application settings.
    """
    
    # Gemini API Configuration
    GEMINI_TIMEOUT = 60
    
    @staticmethod
    def get_gemini_api_key() -> Optional[str]:
        """
        Get Gemini API key from environment or Streamlit secrets.
        Priority: Environment variable > Streamlit secrets
        """
        # Try environment variable first
        api_key = os.getenv("GEMINI_API_KEY")
        
        if api_key:
            return api_key
        
        # Try Streamlit secrets
        try:
            import streamlit as st
            if hasattr(st, 'secrets') and 'GEMINI_API_KEY' in st.secrets:
                return st.secrets['GEMINI_API_KEY']
        except Exception:
            pass
        
        return None
    
    @staticmethod
    def get_database_url() -> Optional[str]:
        """Get database URL from environment or Streamlit secrets."""
        db_url = os.getenv("DATABASE_URL")
        
        if db_url:
            return db_url
        
        try:
            import streamlit as st
            if hasattr(st, 'secrets') and 'DATABASE_URL' in st.secrets:
                return st.secrets['DATABASE_URL']
        except Exception:
            pass
        
        return None
    
    @staticmethod
    def get_consultation_email() -> str:
        """
        Get consultation team email from environment or Streamlit secrets.
        Defaults to public email if not configured.
        """
        # Try environment variable first
        email = os.getenv("CONSULTATION_EMAIL") or os.getenv("OUTREACH_EMAIL")
        
        if email:
            return email
        
        # Try Streamlit secrets
        try:
            import streamlit as st
            if hasattr(st, 'secrets'):
                if 'CONSULTATION_EMAIL' in st.secrets:
                    return st.secrets['CONSULTATION_EMAIL']
                if 'OUTREACH_EMAIL' in st.secrets:
                    return st.secrets['OUTREACH_EMAIL']
        except Exception:
            pass
        
        # Default public email (safe to expose)
        return "outreach@nexsupply.net"
    
    @classmethod
    def validate_config(cls) -> dict:
        """
        Validate that required configuration is present.
        Returns a dict with validation status.
        """
        return {
            "gemini_api_key": cls.get_gemini_api_key() is not None,
            "database_url": cls.get_database_url() is not None,
        }


# Application Settings
class AppSettings:
    """Application-wide settings."""
    
    APP_NAME = "NexSupply"
    APP_DESCRIPTION = "B2B Sourcing Platform"
    VERSION = "0.1.0"
    
    # Design System Colors
    PRIMARY_COLOR = "#0EA5E9"  # Sky Blue
    BACKGROUND_COLOR = "#FFFFFF"  # Clean White
    
    # UI Settings
    PAGE_ICON = "🏭"
    LAYOUT = "wide"

