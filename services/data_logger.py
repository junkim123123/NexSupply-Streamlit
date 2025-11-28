"""
NexSupply Data Logger - Business Intelligence & Trend Analysis
Tracks user searches and AI responses for market insight extraction.

Key Data Points:
- User search queries → Market demand signals
- Analysis mode selection → Customer pain point indicators
- AI results → Product/supplier trend data
"""

import sqlite3
import json
import os
import logging
from datetime import datetime
from typing import Dict, Optional, List, Tuple
from contextlib import contextmanager

import streamlit as st

# Configure logging (production-safe)
logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)  # Only log warnings and errors in production
if not logger.handlers:
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    logger.addHandler(handler)


# =============================================================================
# CONFIGURATION
# =============================================================================

# Database file path (in project root)
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "nexsupply_logs.db")


# =============================================================================
# DATABASE SETUP
# =============================================================================

def get_db_connection():
    """Get SQLite database connection."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Enable column access by name
    return conn


@contextmanager
def db_session():
    """Context manager for database sessions."""
    conn = get_db_connection()
    try:
        yield conn
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()


def init_database():
    """Initialize database with required tables."""
    with db_session() as conn:
        cursor = conn.cursor()
        
        # Main analysis logs table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS analysis_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                user_query TEXT NOT NULL,
                analysis_mode TEXT,
                confidence_score REAL,
                product_category TEXT,
                estimated_landed_cost REAL,
                supplier_count INTEGER,
                top_risk_factors TEXT,
                ai_result_json TEXT,
                user_email TEXT,
                session_id TEXT,
                request_source TEXT DEFAULT 'web',
                processing_time_ms INTEGER,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Quick start card usage tracking
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS mode_usage (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                mode_name TEXT NOT NULL,
                template_used TEXT,
                converted_to_analysis BOOLEAN DEFAULT 0,
                session_id TEXT
            )
        """)
        
        # Consultation requests tracking
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS consultation_requests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                user_email TEXT NOT NULL,
                user_name TEXT,
                product_query TEXT,
                message TEXT,
                analysis_id INTEGER,
                status TEXT DEFAULT 'pending',
                FOREIGN KEY (analysis_id) REFERENCES analysis_logs(id)
            )
        """)
        
        # Create indexes for common queries
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_logs_timestamp ON analysis_logs(timestamp)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_logs_mode ON analysis_logs(analysis_mode)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_logs_category ON analysis_logs(product_category)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_mode_usage_name ON mode_usage(mode_name)")


# =============================================================================
# LOGGING FUNCTIONS
# =============================================================================

def log_analysis(
    query: str,
    mode: str,
    json_data: Dict,
    user_email: Optional[str] = None,
    processing_time_ms: Optional[int] = None
) -> Optional[int]:
    """
    Log an analysis request and its AI response.
    
    Args:
        query: User's search query text
        mode: Analysis mode (e.g., 'market', 'verify', 'cost', 'leadtime')
        json_data: Full AI response JSON
        user_email: Optional user email (if report requested)
        processing_time_ms: Optional API processing time
    
    Returns:
        ID of the inserted log record, or None if failed
    """
    try:
        # Extract key metrics from JSON for quick analysis
        confidence = json_data.get("analysis_confidence", 0)
        product_info = json_data.get("product_info", {})
        product_category = product_info.get("category", "Unknown")
        
        landed_cost = json_data.get("landed_cost", {})
        estimated_cost = landed_cost.get("cost_per_unit_usd", 0)
        
        suppliers = json_data.get("suppliers", [])
        supplier_count = len(suppliers)
        
        # Extract top risk factors
        risk_analysis = json_data.get("risk_analysis", {})
        risk_items = risk_analysis.get("key_risks", [])
        top_risks = json.dumps(risk_items[:3] if risk_items else [], ensure_ascii=False)
        
        # Session tracking
        session_id = st.session_state.get("session_id", "unknown")
        
        with db_session() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO analysis_logs (
                    timestamp, user_query, analysis_mode, confidence_score,
                    product_category, estimated_landed_cost, supplier_count,
                    top_risk_factors, ai_result_json, user_email, session_id,
                    processing_time_ms
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                datetime.now().isoformat(),
                query,
                mode,
                confidence,
                product_category,
                estimated_cost,
                supplier_count,
                top_risks,
                json.dumps(json_data, ensure_ascii=False, default=str),
                user_email,
                session_id,
                processing_time_ms
            ))
            
            return cursor.lastrowid
            
    except Exception as e:
        # Log error but don't break the main flow
        logger.error(f"Error logging analysis: {e}", exc_info=True)
        return None


def log_mode_usage(
    mode_name: str,
    template_used: str,
    converted: bool = False
) -> Optional[int]:
    """
    Log when a user clicks a Quick Start card.
    
    Args:
        mode_name: Mode identifier (e.g., 'verify', 'market')
        template_used: The template prompt that was prefilled
        converted: Whether the user proceeded to analysis
    
    Returns:
        ID of the inserted record
    """
    try:
        session_id = st.session_state.get("session_id", "unknown")
        
        with db_session() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO mode_usage (timestamp, mode_name, template_used, converted_to_analysis, session_id)
                VALUES (?, ?, ?, ?, ?)
            """, (
                datetime.now().isoformat(),
                mode_name,
                template_used,
                converted,
                session_id
            ))
            
            return cursor.lastrowid
            
    except Exception as e:
        logger.error(f"Error logging mode usage: {e}", exc_info=True)
        return None


def log_consultation_request(
    user_email: str,
    user_name: str = "",
    product_query: str = "",
    message: str = "",
    analysis_id: Optional[int] = None
) -> Optional[int]:
    """Log a consultation request."""
    try:
        with db_session() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO consultation_requests (
                    timestamp, user_email, user_name, product_query, message, analysis_id
                ) VALUES (?, ?, ?, ?, ?, ?)
            """, (
                datetime.now().isoformat(),
                user_email,
                user_name,
                product_query,
                message,
                analysis_id
            ))
            
            return cursor.lastrowid
            
    except Exception as e:
        logger.error(f"Error logging consultation: {e}", exc_info=True)
        return None


# =============================================================================
# ANALYTICS FUNCTIONS
# =============================================================================

def get_consultation_requests(days: int = 30, limit: int = 100) -> List[Dict]:
    """Get recent consultation requests from database."""
    try:
        with db_session() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT 
                    id, timestamp, user_email, user_name, 
                    product_query, message, status
                FROM consultation_requests
                WHERE timestamp >= datetime('now', ?)
                ORDER BY timestamp DESC
                LIMIT ?
            """, (f'-{days} days', limit))
            
            return [dict(row) for row in cursor.fetchall()]
            
    except Exception as e:
        logger.error(f"Error getting consultation requests: {e}", exc_info=True)
        return []


def get_top_queries(limit: int = 20, days: int = 30) -> List[Dict]:
    """Get most frequent search queries."""
    try:
        with db_session() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT user_query, COUNT(*) as count, analysis_mode
                FROM analysis_logs
                WHERE timestamp >= datetime('now', ?)
                GROUP BY user_query
                ORDER BY count DESC
                LIMIT ?
            """, (f'-{days} days', limit))
            
            return [dict(row) for row in cursor.fetchall()]
            
    except Exception as e:
        logger.error(f"Error getting top queries: {e}", exc_info=True)
        return []


def get_mode_distribution(days: int = 30) -> Dict[str, int]:
    """Get distribution of analysis modes used."""
    try:
        with db_session() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT analysis_mode, COUNT(*) as count
                FROM analysis_logs
                WHERE timestamp >= datetime('now', ?)
                GROUP BY analysis_mode
                ORDER BY count DESC
            """, (f'-{days} days',))
            
            return {row['analysis_mode']: row['count'] for row in cursor.fetchall()}
            
    except Exception as e:
        logger.error(f"Error getting mode distribution: {e}", exc_info=True)
        return {}


def get_category_trends(days: int = 30) -> List[Dict]:
    """Get trending product categories."""
    try:
        with db_session() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT 
                    product_category,
                    COUNT(*) as search_count,
                    AVG(estimated_landed_cost) as avg_cost,
                    AVG(confidence_score) as avg_confidence
                FROM analysis_logs
                WHERE timestamp >= datetime('now', ?)
                    AND product_category IS NOT NULL
                    AND product_category != 'Unknown'
                GROUP BY product_category
                ORDER BY search_count DESC
                LIMIT 15
            """, (f'-{days} days',))
            
            return [dict(row) for row in cursor.fetchall()]
            
    except Exception as e:
        logger.error(f"Error getting category trends: {e}", exc_info=True)
        return []


def get_risk_trends(days: int = 30) -> Dict[str, int]:
    """Get frequency of different risk factors mentioned."""
    try:
        risk_counts = {}
        
        with db_session() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT top_risk_factors
                FROM analysis_logs
                WHERE timestamp >= datetime('now', ?)
                    AND top_risk_factors IS NOT NULL
            """, (f'-{days} days',))
            
            for row in cursor.fetchall():
                try:
                    risks = json.loads(row['top_risk_factors'])
                    for risk in risks:
                        risk_name = risk.get('type', str(risk)) if isinstance(risk, dict) else str(risk)
                        risk_counts[risk_name] = risk_counts.get(risk_name, 0) + 1
                except:
                    continue
        
        return dict(sorted(risk_counts.items(), key=lambda x: x[1], reverse=True))
        
    except Exception as e:
        logger.error(f"Error getting risk trends: {e}", exc_info=True)
        return {}


def get_daily_stats(days: int = 30) -> List[Dict]:
    """Get daily analysis counts."""
    try:
        with db_session() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT 
                    DATE(timestamp) as date,
                    COUNT(*) as count,
                    COUNT(DISTINCT session_id) as unique_sessions
                FROM analysis_logs
                WHERE timestamp >= datetime('now', ?)
                GROUP BY DATE(timestamp)
                ORDER BY date DESC
            """, (f'-{days} days',))
            
            return [dict(row) for row in cursor.fetchall()]
            
    except Exception as e:
        logger.error(f"Error getting daily stats: {e}", exc_info=True)
        return []


def get_conversion_funnel() -> Dict:
    """Get conversion funnel metrics."""
    try:
        with db_session() as conn:
            cursor = conn.cursor()
            
            # Mode card clicks
            cursor.execute("SELECT COUNT(*) FROM mode_usage")
            mode_clicks = cursor.fetchone()[0]
            
            # Converted to analysis
            cursor.execute("SELECT COUNT(*) FROM mode_usage WHERE converted_to_analysis = 1")
            mode_conversions = cursor.fetchone()[0]
            
            # Total analyses
            cursor.execute("SELECT COUNT(*) FROM analysis_logs")
            total_analyses = cursor.fetchone()[0]
            
            # Consultation requests
            cursor.execute("SELECT COUNT(*) FROM consultation_requests")
            consultations = cursor.fetchone()[0]
            
            return {
                "mode_card_clicks": mode_clicks,
                "mode_to_analysis": mode_conversions,
                "total_analyses": total_analyses,
                "consultation_requests": consultations,
                "conversion_rate": round(consultations / total_analyses * 100, 1) if total_analyses > 0 else 0
            }
            
    except Exception as e:
        logger.error(f"Error getting funnel: {e}", exc_info=True)
        return {}


# =============================================================================
# STREAMLIT ANALYTICS DASHBOARD
# =============================================================================

def render_analytics_dashboard():
    """Render internal analytics dashboard for NexSupply team."""
    
    st.title("📊 NexSupply Analytics Dashboard")
    st.markdown("*Internal business intelligence and trend analysis*")
    
    # Time range selector
    days = st.selectbox("Time Range", [7, 14, 30, 90], index=2, format_func=lambda x: f"Last {x} days")
    
    st.markdown("---")
    
    # Key Metrics Row
    col1, col2, col3, col4 = st.columns(4)
    
    funnel = get_conversion_funnel()
    
    with col1:
        st.metric("Total Analyses", funnel.get("total_analyses", 0))
    with col2:
        st.metric("Mode Card Clicks", funnel.get("mode_card_clicks", 0))
    with col3:
        st.metric("Consultation Requests", funnel.get("consultation_requests", 0))
    with col4:
        st.metric("Conversion Rate", f"{funnel.get('conversion_rate', 0)}%")
    
    st.markdown("---")
    
    # Consultation Requests Section (NEW - Primary Method)
    st.subheader("💬 Consultation Requests (Saved to Database)")
    consultation_requests = get_consultation_requests(days=days, limit=50)
    
    if consultation_requests:
        st.info(f"📊 **{len(consultation_requests)} requests** saved to database (primary method)")
        
        # Display requests in expandable sections
        for req in consultation_requests[:20]:  # Show latest 20
            with st.expander(f"📧 {req.get('user_email', 'No email')} - {req.get('timestamp', '')[:10]}"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Email:** {req.get('user_email', 'N/A')}")
                    st.write(f"**Name:** {req.get('user_name', 'N/A')}")
                    st.write(f"**Status:** {req.get('status', 'pending')}")
                with col2:
                    st.write(f"**Product/Query:** {req.get('product_query', 'N/A')[:100]}")
                    if req.get('message'):
                        st.write(f"**Message:** {req.get('message', '')[:200]}")
    else:
        st.info("No consultation requests yet")
    
    st.markdown("---")
    
    # Two column layout
    left_col, right_col = st.columns(2)
    
    with left_col:
        # Top Queries
        st.subheader("🔍 Top Search Queries")
        top_queries = get_top_queries(limit=10, days=days)
        if top_queries:
            for q in top_queries:
                st.markdown(f"**{q['count']}x** · {q['user_query'][:50]}...")
        else:
            st.info("No data yet")
        
        st.markdown("---")
        
        # Mode Distribution
        st.subheader("📊 Analysis Mode Distribution")
        mode_dist = get_mode_distribution(days=days)
        if mode_dist:
            import plotly.express as px
            fig = px.pie(
                values=list(mode_dist.values()),
                names=list(mode_dist.keys()),
                hole=0.4
            )
            fig.update_layout(height=300, margin=dict(t=20, b=20, l=20, r=20))
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No data yet")
    
    with right_col:
        # Category Trends
        st.subheader("📦 Trending Categories")
        categories = get_category_trends(days=days)
        if categories:
            for cat in categories[:8]:
                col_a, col_b = st.columns([3, 1])
                with col_a:
                    st.markdown(f"**{cat['product_category']}**")
                with col_b:
                    st.markdown(f"`{cat['search_count']} searches`")
        else:
            st.info("No data yet")
        
        st.markdown("---")
        
        # Risk Trends
        st.subheader("⚠️ Common Risk Factors")
        risks = get_risk_trends(days=days)
        if risks:
            for risk, count in list(risks.items())[:6]:
                st.markdown(f"• **{risk}**: {count} mentions")
        else:
            st.info("No data yet")
    
    # Daily Activity Chart
    st.markdown("---")
    st.subheader("📈 Daily Activity")
    
    daily = get_daily_stats(days=days)
    if daily:
        import plotly.express as px
        import pandas as pd
        df = pd.DataFrame(daily)
        fig = px.line(df, x='date', y='count', markers=True)
        fig.update_layout(height=250, margin=dict(t=20, b=20, l=20, r=20))
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No activity data yet")


# =============================================================================
# INITIALIZATION
# =============================================================================

# Initialize database on module import
try:
    init_database()
except Exception as e:
    logger.warning(f"Database initialization warning: {e}")

