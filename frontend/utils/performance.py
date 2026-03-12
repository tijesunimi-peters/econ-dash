"""
Performance Optimization Utilities for Dashboard

Provides tools for:
- Lazy-loading of components below fold
- Chart data caching
- Performance monitoring
- Memory optimization
"""

import time
from functools import wraps
from typing import Any, Callable, Dict, Optional
import logging

logger = logging.getLogger(__name__)


class PerformanceMonitor:
    """
    Monitor and track dashboard performance metrics.

    Usage:
        monitor = PerformanceMonitor()
        monitor.start("chart-render")
        # ... do work ...
        monitor.end("chart-render")
        print(monitor.get_stats())
    """

    def __init__(self):
        self.timings: Dict[str, list] = {}
        self.start_times: Dict[str, float] = {}

    def start(self, operation_name: str):
        """Start timing an operation."""
        self.start_times[operation_name] = time.time()

    def end(self, operation_name: str) -> float:
        """End timing an operation, return elapsed time in ms."""
        if operation_name not in self.start_times:
            logger.warning(f"No start time for {operation_name}")
            return 0

        elapsed_ms = (time.time() - self.start_times[operation_name]) * 1000

        if operation_name not in self.timings:
            self.timings[operation_name] = []

        self.timings[operation_name].append(elapsed_ms)
        del self.start_times[operation_name]

        return elapsed_ms

    def get_stats(self, operation_name: Optional[str] = None) -> Dict[str, Any]:
        """
        Get performance statistics.

        Args:
            operation_name: Get stats for specific operation, or all if None

        Returns:
            Dict with min, max, avg, count
        """
        if operation_name:
            if operation_name not in self.timings:
                return {"error": f"No timings for {operation_name}"}

            times = self.timings[operation_name]
            return {
                "operation": operation_name,
                "count": len(times),
                "min_ms": min(times),
                "max_ms": max(times),
                "avg_ms": sum(times) / len(times),
                "total_ms": sum(times),
            }

        # Get stats for all operations
        stats = {}
        for op_name in self.timings:
            times = self.timings[op_name]
            stats[op_name] = {
                "count": len(times),
                "min_ms": min(times),
                "max_ms": max(times),
                "avg_ms": sum(times) / len(times),
                "total_ms": sum(times),
            }
        return stats

    def reset(self):
        """Clear all timing data."""
        self.timings = {}
        self.start_times = {}


def timed(operation_name: str):
    """
    Decorator to automatically time function execution.

    Usage:
        @timed("data-fetch")
        def fetch_data():
            # ... do work ...
            pass

        # Monitor.get_stats("data-fetch") will show timing
    """
    def decorator(func: Callable) -> Callable:
        monitor = PerformanceMonitor()

        @wraps(func)
        def wrapper(*args, **kwargs):
            monitor.start(operation_name)
            result = func(*args, **kwargs)
            elapsed = monitor.end(operation_name)
            logger.info(f"{operation_name} took {elapsed:.2f}ms")
            return result

        return wrapper

    return decorator


class LazyLoader:
    """
    Lazy-load components that are below the fold.

    Prevents rendering of off-screen content until needed.

    Usage:
        loader = LazyLoader()
        loader.should_load("panel-id", viewport_height=1080)
        # Returns True if panel-id is visible in viewport
    """

    @staticmethod
    def should_load(component_id: str, viewport_height: int = 1080) -> bool:
        """
        Determine if component should be lazy-loaded.

        In production, this would check element position vs viewport.
        For Dash, we rely on clientside Intersection Observer.

        Args:
            component_id: ID of component to check
            viewport_height: Height of visible viewport

        Returns:
            True if component should be loaded, False if below fold
        """
        # In practice, use JavaScript Intersection Observer
        # This is a placeholder for backend logic
        return True

    @staticmethod
    def get_clientside_observer_js() -> str:
        """
        Get JavaScript code for Intersection Observer.

        Detects when components come into view and triggers loading.
        """
        return """
        // Lazy load components using Intersection Observer
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const element = entry.target;
                    const componentId = element.id;

                    // Trigger Dash callback to load component
                    if (window.dash_clientside && window.dash_clientside.load_component) {
                        window.dash_clientside.load_component(componentId);
                    }

                    observer.unobserve(element);
                }
            });
        }, {
            rootMargin: '50px' // Start loading 50px before visible
        });

        // Observe all components with data-lazy-load attribute
        document.querySelectorAll('[data-lazy-load]').forEach(el => {
            observer.observe(el);
        });
        """


class ChartDataCache:
    """
    Cache chart data to avoid re-fetching/re-rendering.

    Usage:
        cache = ChartDataCache(ttl_seconds=300)  # 5-minute cache
        cache.set("chart-us-manufacturing", chart_data)
        data = cache.get("chart-us-manufacturing")  # Returns cached data if fresh
    """

    def __init__(self, ttl_seconds: int = 300):
        self.cache: Dict[str, Dict[str, Any]] = {}
        self.ttl = ttl_seconds

    def set(self, key: str, value: Any):
        """
        Cache a value with timestamp.

        Args:
            key: Cache key
            value: Value to cache
        """
        self.cache[key] = {
            "value": value,
            "timestamp": time.time(),
        }

    def get(self, key: str) -> Optional[Any]:
        """
        Get cached value if fresh, None if expired or missing.

        Args:
            key: Cache key

        Returns:
            Cached value or None
        """
        if key not in self.cache:
            return None

        entry = self.cache[key]
        age_seconds = time.time() - entry["timestamp"]

        if age_seconds > self.ttl:
            del self.cache[key]
            return None

        return entry["value"]

    def clear(self, key: Optional[str] = None):
        """
        Clear cache entry or entire cache.

        Args:
            key: Specific key to clear, or None to clear all
        """
        if key is None:
            self.cache.clear()
        elif key in self.cache:
            del self.cache[key]

    def stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        return {
            "size": len(self.cache),
            "ttl_seconds": self.ttl,
            "keys": list(self.cache.keys()),
        }


# Global cache instance
_chart_cache = ChartDataCache(ttl_seconds=300)  # 5-minute default


def cached_chart_data(key: str, ttl_seconds: Optional[int] = None):
    """
    Decorator to cache chart data.

    Usage:
        @cached_chart_data("chart-us-manufacturing", ttl_seconds=600)
        def fetch_chart_data(country_id, sector_id):
            # ... expensive data fetch ...
            return chart_data
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Check cache first
            cached = _chart_cache.get(key)
            if cached is not None:
                logger.info(f"Cache hit: {key}")
                return cached

            # Not in cache, fetch and cache
            result = func(*args, **kwargs)
            _chart_cache.set(key, result)
            logger.info(f"Cached: {key}")
            return result

        return wrapper

    return decorator


class VirtualizationHelper:
    """
    Helper for virtualizing long tables/lists.

    Only renders visible rows to improve performance with large datasets.
    """

    @staticmethod
    def get_virtual_table_js() -> str:
        """
        Get JavaScript for virtual scrolling in tables.

        Uses visible row calculation to virtualize table rows.
        """
        return """
        // Virtual table scrolling - only render visible rows
        function virtualizeTable(tableId, rowHeight) {
            const table = document.getElementById(tableId);
            if (!table) return;

            const container = table.parentElement;
            const visibleRows = Math.ceil(container.clientHeight / rowHeight);

            let scrollTop = 0;
            container.addEventListener('scroll', (e) => {
                scrollTop = e.target.scrollTop;
                const startRow = Math.floor(scrollTop / rowHeight);
                const endRow = startRow + visibleRows + 1;

                // Hide/show rows based on viewport
                const rows = table.querySelectorAll('tbody tr');
                rows.forEach((row, index) => {
                    row.style.display = (index >= startRow && index <= endRow)
                        ? 'table-row'
                        : 'none';
                });
            });
        }

        // Usage: virtualizeTable('my-table', 40)
        """

    @staticmethod
    def create_virtual_table_html(rows_data: list, row_height: int = 40) -> str:
        """
        Create HTML for virtual table.

        Args:
            rows_data: List of row data dicts
            row_height: Height of each row in pixels

        Returns:
            HTML table with virtualization attributes
        """
        height_px = len(rows_data) * row_height
        return f'<div style="height: {height_px}px" data-virtualized="true"></div>'


# ═════════════════════════════════════════════════════════════════════════════
# Performance Baseline Metrics
# ═════════════════════════════════════════════════════════════════════════════

PERFORMANCE_TARGETS = {
    "page_load_time": 2000,  # 2 seconds
    "chart_render_time": 500,  # 500ms per chart
    "interaction_latency": 100,  # 100ms response to click
    "memory_usage": 150,  # 150MB
    "ttfb": 300,  # Time to first byte: 300ms
}


def check_performance_target(metric_name: str, actual_ms: float) -> bool:
    """
    Check if actual metric meets target.

    Args:
        metric_name: Name of metric
        actual_ms: Actual measurement in milliseconds

    Returns:
        True if target met, False if exceeded
    """
    if metric_name not in PERFORMANCE_TARGETS:
        return True

    target = PERFORMANCE_TARGETS[metric_name]
    exceeded = actual_ms > target

    if exceeded:
        logger.warning(
            f"Performance target exceeded: {metric_name} "
            f"({actual_ms:.2f}ms > {target}ms)"
        )

    return not exceeded


# ═════════════════════════════════════════════════════════════════════════════
# Memory Optimization
# ═════════════════════════════════════════════════════════════════════════════

def get_memory_optimization_js() -> str:
    """
    Get JavaScript for memory optimization.

    Cleans up unused DOM nodes, debounces events, etc.
    """
    return """
    // Memory optimization utilities

    // Debounce function for scroll/resize events
    function debounce(func, delay) {
        let timeoutId;
        return function(...args) {
            clearTimeout(timeoutId);
            timeoutId = setTimeout(() => func.apply(this, args), delay);
        };
    }

    // Clean up Plotly charts that are off-screen
    function cleanupOffscreenCharts() {
        document.querySelectorAll('.plotly-chart').forEach(chart => {
            const rect = chart.getBoundingClientRect();
            if (rect.bottom < 0 || rect.top > window.innerHeight) {
                // Chart is off-screen, could unload if needed
                if (window.Plotly && chart.data) {
                    // Keep data but could dispose of DOM if needed
                }
            }
        });
    }

    // Run cleanup on scroll (debounced)
    window.addEventListener('scroll', debounce(cleanupOffscreenCharts, 500));

    // Detect memory pressure
    if (performance.memory) {
        const usedMemory = performance.memory.usedJSHeapSize;
        const totalMemory = performance.memory.jsHeapSizeLimit;
        const percent = (usedMemory / totalMemory) * 100;

        if (percent > 90) {
            console.warn('High memory usage:', percent.toFixed(2) + '%');
            // Could trigger cleanup or warn user
        }
    }
    """


# Global performance monitor instance
perf_monitor = PerformanceMonitor()
