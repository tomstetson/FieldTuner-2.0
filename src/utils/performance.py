"""
FieldTuner V2.0 - Performance Optimization System
Comprehensive performance monitoring and optimization utilities.
"""

import time
import psutil
import threading
from typing import Dict, Any, Optional, Callable, List
from functools import wraps
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import datetime, timedelta

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from debug import log_info, log_error, log_warning


@dataclass
class PerformanceMetric:
    """Performance metric data structure."""
    name: str
    start_time: float
    end_time: Optional[float] = None
    duration: Optional[float] = None
    memory_usage: Optional[float] = None
    cpu_usage: Optional[float] = None
    context: Optional[Dict[str, Any]] = None
    
    def finish(self):
        """Finish timing and calculate metrics."""
        self.end_time = time.time()
        self.duration = self.end_time - self.start_time
        
        # Get memory usage
        try:
            process = psutil.Process()
            self.memory_usage = process.memory_info().rss / 1024 / 1024  # MB
            self.cpu_usage = process.cpu_percent()
        except Exception:
            self.memory_usage = 0
            self.cpu_usage = 0


class PerformanceMonitor:
    """Performance monitoring and optimization system."""
    
    def __init__(self):
        self.metrics: List[PerformanceMetric] = []
        self.active_metrics: Dict[str, PerformanceMetric] = {}
        self.max_metrics = 1000
        self.slow_threshold = 1.0  # seconds
        self.memory_threshold = 100  # MB
        
    def start_timing(self, name: str, context: Optional[Dict[str, Any]] = None) -> str:
        """Start timing a performance metric."""
        metric = PerformanceMetric(
            name=name,
            start_time=time.time(),
            context=context or {}
        )
        
        # Use thread-safe key
        key = f"{name}_{id(threading.current_thread())}_{int(time.time() * 1000)}"
        self.active_metrics[key] = metric
        
        return key
    
    def finish_timing(self, key: str) -> Optional[PerformanceMetric]:
        """Finish timing a performance metric."""
        if key not in self.active_metrics:
            log_warning(f"Performance metric key not found: {key}", "PERF")
            return None
        
        metric = self.active_metrics.pop(key)
        metric.finish()
        
        # Add to metrics list
        self.metrics.append(metric)
        
        # Maintain metrics list size
        if len(self.metrics) > self.max_metrics:
            self.metrics.pop(0)
        
        # Log slow operations
        if metric.duration and metric.duration > self.slow_threshold:
            log_warning(f"Slow operation detected: {metric.name} took {metric.duration:.2f}s", "PERF")
        
        # Log high memory usage
        if metric.memory_usage and metric.memory_usage > self.memory_threshold:
            log_warning(f"High memory usage: {metric.name} used {metric.memory_usage:.1f}MB", "PERF")
        
        return metric
    
    @contextmanager
    def time_operation(self, name: str, context: Optional[Dict[str, Any]] = None):
        """Context manager for timing operations."""
        key = self.start_timing(name, context)
        try:
            yield key
        finally:
            self.finish_timing(key)
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """Get a summary of performance metrics."""
        if not self.metrics:
            return {"total_operations": 0, "average_duration": 0, "slow_operations": 0}
        
        total_duration = sum(m.duration for m in self.metrics if m.duration)
        average_duration = total_duration / len(self.metrics)
        slow_operations = len([m for m in self.metrics if m.duration and m.duration > self.slow_threshold])
        
        # Group by operation name
        by_operation = {}
        for metric in self.metrics:
            if metric.name not in by_operation:
                by_operation[metric.name] = []
            by_operation[metric.name].append(metric)
        
        # Calculate stats per operation
        operation_stats = {}
        for name, metrics in by_operation.items():
            durations = [m.duration for m in metrics if m.duration]
            if durations:
                operation_stats[name] = {
                    "count": len(metrics),
                    "total_duration": sum(durations),
                    "average_duration": sum(durations) / len(durations),
                    "min_duration": min(durations),
                    "max_duration": max(durations),
                    "slow_count": len([d for d in durations if d > self.slow_threshold])
                }
        
        return {
            "total_operations": len(self.metrics),
            "average_duration": average_duration,
            "slow_operations": slow_operations,
            "by_operation": operation_stats,
            "recent_operations": [
                {
                    "name": m.name,
                    "duration": m.duration,
                    "memory_usage": m.memory_usage,
                    "timestamp": datetime.fromtimestamp(m.start_time)
                }
                for m in self.metrics[-10:]  # Last 10 operations
            ]
        }
    
    def clear_metrics(self):
        """Clear all performance metrics."""
        self.metrics.clear()
        self.active_metrics.clear()
        log_info("Performance metrics cleared", "PERF")


# Global performance monitor
performance_monitor = PerformanceMonitor()


def time_function(name: Optional[str] = None, context: Optional[Dict[str, Any]] = None):
    """Decorator to time function execution."""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            function_name = name or f"{func.__module__}.{func.__name__}"
            with performance_monitor.time_operation(function_name, context):
                return func(*args, **kwargs)
        return wrapper
    return decorator


def time_method(name: Optional[str] = None, context: Optional[Dict[str, Any]] = None):
    """Decorator to time method execution."""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            method_name = name or f"{self.__class__.__name__}.{func.__name__}"
            with performance_monitor.time_operation(method_name, context):
                return func(self, *args, **kwargs)
        return wrapper
    return decorator


class ResourceMonitor:
    """System resource monitoring."""
    
    def __init__(self):
        self.monitoring = False
        self.monitor_thread: Optional[threading.Thread] = None
        self.resource_data: List[Dict[str, Any]] = []
        self.max_data_points = 1000
        
    def start_monitoring(self, interval: float = 1.0):
        """Start resource monitoring."""
        if self.monitoring:
            return
        
        self.monitoring = True
        self.monitor_thread = threading.Thread(
            target=self._monitor_resources,
            args=(interval,),
            daemon=True
        )
        self.monitor_thread.start()
        log_info("Resource monitoring started", "PERF")
    
    def stop_monitoring(self):
        """Stop resource monitoring."""
        self.monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=2.0)
        log_info("Resource monitoring stopped", "PERF")
    
    def _monitor_resources(self, interval: float):
        """Monitor system resources."""
        while self.monitoring:
            try:
                # Get system resources
                cpu_percent = psutil.cpu_percent(interval=0.1)
                memory = psutil.virtual_memory()
                disk = psutil.disk_usage('/')
                
                # Get process resources
                process = psutil.Process()
                process_memory = process.memory_info().rss / 1024 / 1024  # MB
                process_cpu = process.cpu_percent()
                
                resource_data = {
                    "timestamp": datetime.now(),
                    "system_cpu": cpu_percent,
                    "system_memory_percent": memory.percent,
                    "system_memory_available": memory.available / 1024 / 1024 / 1024,  # GB
                    "system_disk_percent": disk.percent,
                    "system_disk_free": disk.free / 1024 / 1024 / 1024,  # GB
                    "process_memory": process_memory,
                    "process_cpu": process_cpu
                }
                
                self.resource_data.append(resource_data)
                
                # Maintain data size
                if len(self.resource_data) > self.max_data_points:
                    self.resource_data.pop(0)
                
                # Log warnings for high resource usage
                if cpu_percent > 80:
                    log_warning(f"High CPU usage: {cpu_percent:.1f}%", "PERF")
                
                if memory.percent > 85:
                    log_warning(f"High memory usage: {memory.percent:.1f}%", "PERF")
                
                if process_memory > 200:  # MB
                    log_warning(f"High process memory usage: {process_memory:.1f}MB", "PERF")
                
            except Exception as e:
                log_error(f"Error monitoring resources: {str(e)}", "PERF", e)
            
            time.sleep(interval)
    
    def get_resource_summary(self) -> Dict[str, Any]:
        """Get a summary of resource usage."""
        if not self.resource_data:
            return {"monitoring": False, "data_points": 0}
        
        latest = self.resource_data[-1]
        
        # Calculate averages
        avg_cpu = sum(d["system_cpu"] for d in self.resource_data) / len(self.resource_data)
        avg_memory = sum(d["system_memory_percent"] for d in self.resource_data) / len(self.resource_data)
        avg_process_memory = sum(d["process_memory"] for d in self.resource_data) / len(self.resource_data)
        
        return {
            "monitoring": self.monitoring,
            "data_points": len(self.resource_data),
            "current": latest,
            "averages": {
                "cpu_percent": avg_cpu,
                "memory_percent": avg_memory,
                "process_memory_mb": avg_process_memory
            },
            "peak": {
                "cpu_percent": max(d["system_cpu"] for d in self.resource_data),
                "memory_percent": max(d["system_memory_percent"] for d in self.resource_data),
                "process_memory_mb": max(d["process_memory"] for d in self.resource_data)
            }
        }


# Global resource monitor
resource_monitor = ResourceMonitor()


class CacheManager:
    """Simple in-memory cache manager for performance optimization."""
    
    def __init__(self, max_size: int = 100, default_ttl: int = 300):
        self.cache: Dict[str, Dict[str, Any]] = {}
        self.max_size = max_size
        self.default_ttl = default_ttl  # seconds
        
    def get(self, key: str) -> Optional[Any]:
        """Get a value from the cache."""
        if key not in self.cache:
            return None
        
        entry = self.cache[key]
        
        # Check if expired
        if time.time() > entry["expires_at"]:
            del self.cache[key]
            return None
        
        # Update access time
        entry["last_accessed"] = time.time()
        return entry["value"]
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Set a value in the cache."""
        if ttl is None:
            ttl = self.default_ttl
        
        # Remove oldest entries if cache is full
        if len(self.cache) >= self.max_size:
            self._evict_oldest()
        
        self.cache[key] = {
            "value": value,
            "created_at": time.time(),
            "last_accessed": time.time(),
            "expires_at": time.time() + ttl
        }
    
    def _evict_oldest(self):
        """Evict the oldest entry from the cache."""
        if not self.cache:
            return
        
        oldest_key = min(self.cache.keys(), key=lambda k: self.cache[k]["last_accessed"])
        del self.cache[oldest_key]
    
    def clear(self):
        """Clear the cache."""
        self.cache.clear()
        log_info("Cache cleared", "PERF")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        if not self.cache:
            return {"size": 0, "hit_rate": 0}
        
        total_entries = len(self.cache)
        expired_entries = len([k for k, v in self.cache.items() if time.time() > v["expires_at"]])
        
        return {
            "size": total_entries,
            "max_size": self.max_size,
            "expired_entries": expired_entries,
            "active_entries": total_entries - expired_entries
        }


# Global cache manager
cache_manager = CacheManager()


class LazyLoader:
    """Lazy loading utility for expensive operations."""
    
    def __init__(self, loader_func: Callable, *args, **kwargs):
        self.loader_func = loader_func
        self.args = args
        self.kwargs = kwargs
        self._value = None
        self._loaded = False
    
    def get(self) -> Any:
        """Get the value, loading it if necessary."""
        if not self._loaded:
            self._value = self.loader_func(*self.args, **self.kwargs)
            self._loaded = True
        return self._value
    
    def is_loaded(self) -> bool:
        """Check if the value has been loaded."""
        return self._loaded
    
    def reload(self) -> Any:
        """Force reload the value."""
        self._loaded = False
        return self.get()


def optimize_ui_updates(func: Callable) -> Callable:
    """Decorator to optimize UI updates by batching them."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        # This would implement UI update batching
        # For now, just time the operation
        with performance_monitor.time_operation(f"ui_update_{func.__name__}"):
            return func(*args, **kwargs)
    return wrapper


def memory_efficient(func: Callable) -> Callable:
    """Decorator to monitor memory usage of functions."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        process = psutil.Process()
        memory_before = process.memory_info().rss / 1024 / 1024  # MB
        
        result = func(*args, **kwargs)
        
        memory_after = process.memory_info().rss / 1024 / 1024  # MB
        memory_delta = memory_after - memory_before
        
        if memory_delta > 10:  # More than 10MB increase
            log_warning(f"High memory usage in {func.__name__}: {memory_delta:.1f}MB", "PERF")
        
        return result
    return wrapper


def get_performance_report() -> Dict[str, Any]:
    """Get a comprehensive performance report."""
    return {
        "performance_metrics": performance_monitor.get_performance_summary(),
        "resource_usage": resource_monitor.get_resource_summary(),
        "cache_stats": cache_manager.get_stats(),
        "timestamp": datetime.now().isoformat()
    }
