"""
Browser Storage Utilities for Dashboard Preferences

Handles localStorage persistence for:
- Collapsible card state (which panels are open/closed)
- Sidebar width preferences
- Active tab selections
- User layout preferences
- Custom view configurations

Note: Requires clientside JavaScript callbacks for actual localStorage access.
This module provides Python-side helpers for managing storage keys and data.
"""

import json
from typing import Dict, Any, Optional, List


class DashboardStorage:
    """
    Helper class for managing dashboard localStorage state.

    Usage:
        storage = DashboardStorage()
        storage.save_card_state("policy-card", True)  # Save collapsed state
        state = storage.get_card_state("policy-card")  # Retrieve state
    """

    # Storage keys
    CARD_STATE_PREFIX = "card-state-"
    SIDEBAR_WIDTH_KEY = "sidebar-width"
    ACTIVE_TAB_KEY = "active-tab"
    LAYOUT_PREFERENCE_KEY = "layout-preference"
    VIEW_PRESET_KEY = "view-preset"
    LAST_COUNTRY_KEY = "last-country"
    THEME_KEY = "theme"

    @staticmethod
    def get_card_state_key(card_id: str) -> str:
        """Get localStorage key for a card's collapsed/expanded state."""
        return f"{DashboardStorage.CARD_STATE_PREFIX}{card_id}"

    @staticmethod
    def save_card_state(card_id: str, is_open: bool) -> Dict[str, Any]:
        """
        Create data structure to save card state.

        Args:
            card_id: Unique card identifier
            is_open: True if card is expanded, False if collapsed

        Returns:
            Dict to pass to dcc.Store or return from callback
        """
        return {
            "type": "card_state",
            "card_id": card_id,
            "key": DashboardStorage.get_card_state_key(card_id),
            "value": is_open,
        }

    @staticmethod
    def save_sidebar_width(width_percent: float) -> Dict[str, Any]:
        """
        Create data structure to save sidebar width preference.

        Args:
            width_percent: Sidebar width as percentage (e.g., 25 for 25%)

        Returns:
            Dict to pass to dcc.Store
        """
        return {
            "type": "sidebar_width",
            "key": DashboardStorage.SIDEBAR_WIDTH_KEY,
            "value": width_percent,
        }

    @staticmethod
    def save_active_tab(tab_id: str) -> Dict[str, Any]:
        """Save which tab is currently active."""
        return {
            "type": "active_tab",
            "key": DashboardStorage.ACTIVE_TAB_KEY,
            "value": tab_id,
        }

    @staticmethod
    def save_layout_preference(preference: str) -> Dict[str, Any]:
        """
        Save layout preference (e.g., "2-col", "3-col", "adaptive").

        Args:
            preference: Layout type identifier

        Returns:
            Dict to pass to dcc.Store
        """
        return {
            "type": "layout_preference",
            "key": DashboardStorage.LAYOUT_PREFERENCE_KEY,
            "value": preference,
        }

    @staticmethod
    def save_view_preset(preset_name: str) -> Dict[str, Any]:
        """
        Save view preset (e.g., "analyst", "trader", "policy").

        Args:
            preset_name: Name of the preset configuration

        Returns:
            Dict to pass to dcc.Store
        """
        return {
            "type": "view_preset",
            "key": DashboardStorage.VIEW_PRESET_KEY,
            "value": preset_name,
        }

    @staticmethod
    def save_last_country(country_id: int) -> Dict[str, Any]:
        """Save last selected country for next session."""
        return {
            "type": "last_country",
            "key": DashboardStorage.LAST_COUNTRY_KEY,
            "value": country_id,
        }

    @staticmethod
    def get_card_states_bulk(card_ids: List[str]) -> Dict[str, str]:
        """
        Get localStorage keys for multiple cards.

        Args:
            card_ids: List of card identifiers

        Returns:
            Dict mapping card_id -> localStorage key
        """
        return {
            card_id: DashboardStorage.get_card_state_key(card_id)
            for card_id in card_ids
        }


# ═════════════════════════════════════════════════════════════════════════════
# Clientside JavaScript for localStorage Integration
# ═════════════════════════════════════════════════════════════════════════════

STORAGE_CLIENTSIDE_JS = """
// Dashboard localStorage integration

window.dashboardStorage = {
    // Get item from localStorage
    getItem: function(key) {
        try {
            return localStorage.getItem(key);
        } catch (e) {
            console.warn('localStorage access denied:', e);
            return null;
        }
    },

    // Set item in localStorage
    setItem: function(key, value) {
        try {
            localStorage.setItem(key, JSON.stringify(value));
            return true;
        } catch (e) {
            console.warn('localStorage write failed:', e);
            return false;
        }
    },

    // Remove item from localStorage
    removeItem: function(key) {
        try {
            localStorage.removeItem(key);
            return true;
        } catch (e) {
            console.warn('localStorage delete failed:', e);
            return false;
        }
    },

    // Clear all dashboard data from localStorage
    clearAll: function() {
        try {
            const keys = Object.keys(localStorage);
            keys.forEach(key => {
                if (key.startsWith('card-state-') ||
                    key.startsWith('sidebar-') ||
                    key === 'layout-preference' ||
                    key === 'view-preset' ||
                    key === 'active-tab' ||
                    key === 'last-country') {
                    localStorage.removeItem(key);
                }
            });
            return true;
        } catch (e) {
            console.warn('localStorage clear failed:', e);
            return false;
        }
    },

    // Get all dashboard preferences
    getAll: function() {
        const prefs = {};
        const keys = Object.keys(localStorage);

        keys.forEach(key => {
            if (key.startsWith('card-state-') ||
                key.startsWith('sidebar-') ||
                key === 'layout-preference' ||
                key === 'view-preset' ||
                key === 'active-tab' ||
                key === 'last-country') {
                try {
                    prefs[key] = JSON.parse(localStorage.getItem(key));
                } catch (e) {
                    prefs[key] = localStorage.getItem(key);
                }
            }
        });

        return prefs;
    },

    // Watch for changes and sync to Dash store
    syncToStore: function(storeId) {
        const store = document.querySelector(`[id='${storeId}']`);
        if (!store) return;

        const data = this.getAll();

        // Simulate Dash store update
        if (window.dash_clientside && window.dash_clientside.update_store) {
            window.dash_clientside.update_store(data);
        }
    }
};

// Auto-sync on page load
document.addEventListener('DOMContentLoaded', function() {
    // Restore collapsible card states
    const cardStates = window.dashboardStorage.getAll();
    Object.entries(cardStates).forEach(([key, value]) => {
        if (key.startsWith('card-state-')) {
            const cardId = key.replace('card-state-', '');
            const content = document.querySelector(
                `[id='{"type":"collapsible-content","index":"${cardId}"}']`
            );
            if (content && value === false) {
                // Card should be closed
                content.style.display = 'none';
                content.style.maxHeight = '0';
                content.style.opacity = '0';
            }
        }
    });

    // Restore sidebar width
    const sidebarWidth = window.dashboardStorage.getItem('sidebar-width');
    if (sidebarWidth) {
        const sidebar = document.querySelector('.sidebar-layout');
        if (sidebar) {
            const width = JSON.parse(sidebarWidth);
            sidebar.style.gridTemplateColumns = `${width}fr ${100-width}fr`;
        }
    }
});

// Listen for storage events from other tabs
window.addEventListener('storage', function(event) {
    if (event.key && event.key.startsWith('card-state-')) {
        // Another tab updated a card state, could sync if needed
        console.log('Storage updated from another tab:', event.key);
    }
});
"""


# ═════════════════════════════════════════════════════════════════════════════
# Dash Callbacks Helper
# ═════════════════════════════════════════════════════════════════════════════

def create_storage_callback(app, store_id: str):
    """
    Create a callback that persists data to localStorage via dcc.Store.

    Usage in app.py:
        storage_store = dcc.Store(id='storage-store', storage_type='session')
        create_storage_callback(app, 'storage-store')

    Args:
        app: Dash application instance
        store_id: ID of dcc.Store component
    """
    from dash import callback, Input, Output, State, ctx

    @callback(
        Output(store_id, "data"),
        Input({"type": "collapsible-toggle", "index": "ALL"}, "n_clicks"),
        State({"type": "collapsible-content", "index": "ALL"}, "style"),
        prevent_initial_call=True,
    )
    def save_card_states(n_clicks_list, styles):
        """Save collapsible card states to storage."""
        if not ctx.triggered:
            return {}

        state_data = {}
        if isinstance(styles, list):
            for i, style in enumerate(styles):
                is_open = style.get("display", "block") == "block" if style else True
                state_data[f"card-state-{i}"] = is_open

        return state_data


# ═════════════════════════════════════════════════════════════════════════════
# Preset Configurations
# ═════════════════════════════════════════════════════════════════════════════

PRESET_CONFIGS = {
    "analyst": {
        "layout": "2-col",
        "collapsed_panels": [],  # All open
        "visible_panels": ["intelligence", "sentiment", "structural", "policy", "trade"],
        "sidebar_width": 25,
        "description": "All panels visible for comprehensive analysis",
    },
    "trader": {
        "layout": "2-col",
        "collapsed_panels": ["policy", "structural"],
        "visible_panels": ["intelligence", "sentiment", "trade"],
        "sidebar_width": 25,
        "description": "Focus on market sentiment and trade flows",
    },
    "policy": {
        "layout": "1-col",
        "collapsed_panels": [],
        "visible_panels": ["intelligence", "policy", "structural", "sentiment"],
        "sidebar_width": 30,
        "description": "Policy-focused view with structural metrics",
    },
    "supply_chain": {
        "layout": "2-col",
        "collapsed_panels": ["policy", "sentiment"],
        "visible_panels": ["intelligence", "trade", "structural"],
        "sidebar_width": 25,
        "description": "Trade flows and supply chain risk focus",
    },
}


def get_preset_config(preset_name: str) -> Optional[Dict[str, Any]]:
    """
    Get configuration for a preset view.

    Args:
        preset_name: Name of preset ("analyst", "trader", "policy", "supply_chain")

    Returns:
        Configuration dict or None if preset not found
    """
    return PRESET_CONFIGS.get(preset_name)


def list_presets() -> List[str]:
    """Get list of available preset names."""
    return list(PRESET_CONFIGS.keys())
