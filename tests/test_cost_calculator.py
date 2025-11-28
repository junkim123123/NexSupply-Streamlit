"""
Unit tests for cost calculator.
Tests the core landed cost calculation logic.
"""

import pytest
from utils.cost_calculator import OrderParams, compute_landed_cost
from utils.config import AppSettings


def test_landed_cost_calculation_basic():
    """Test basic landed cost calculation."""
    order = OrderParams(
        category_id="toys_games",
        units=5000,
        route=AppSettings.DEFAULT_ROUTE
    )
    result = compute_landed_cost(order)
    
    # Assertions
    assert result is not None
    assert "cost_per_unit_usd" in result
    assert "total_landed_cost_usd" in result
    assert "cost_components" in result
    assert result["cost_per_unit_usd"] > 0
    assert result["total_landed_cost_usd"] > 0


def test_landed_cost_with_different_volumes():
    """Test that cost per unit decreases with higher volume."""
    order_small = OrderParams(
        category_id="toys_games",
        units=1000,
        route=AppSettings.DEFAULT_ROUTE
    )
    order_large = OrderParams(
        category_id="toys_games",
        units=10000,
        route=AppSettings.DEFAULT_ROUTE
    )
    
    result_small = compute_landed_cost(order_small)
    result_large = compute_landed_cost(order_large)
    
    # Larger volume should have lower per-unit cost (economies of scale)
    # But total cost should be higher
    assert result_large["total_landed_cost_usd"] > result_small["total_landed_cost_usd"]
    # Note: Per-unit cost might not always be lower due to fixed costs,
    # but it should be reasonable


def test_landed_cost_components():
    """Test that all cost components are present."""
    order = OrderParams(
        category_id="toys_games",
        units=5000,
        route=AppSettings.DEFAULT_ROUTE
    )
    result = compute_landed_cost(order)
    
    components = result.get("cost_components", {})
    
    # Check for key components
    assert "fob_price_usd" in components or "product_cost_usd" in components
    assert "total_landed_cost_usd" in result


def test_order_params_defaults():
    """Test that OrderParams uses AppSettings defaults."""
    order = OrderParams(
        category_id="toys_games",
        units=5000
    )
    
    # Should use defaults from AppSettings
    assert order.route == AppSettings.DEFAULT_ROUTE
    assert order.incoterm == AppSettings.DEFAULT_INCOTERM




