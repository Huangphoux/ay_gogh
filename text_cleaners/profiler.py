import time
from functools import wraps

# Global timing dict: {step_name: {"total": float, "count": int}}
_step_times = {}


def profile_step(func):
    """Decorator to profile individual processing steps."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        step_name = func.__name__
        start = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start

        if step_name not in _step_times:
            _step_times[step_name] = {"total": 0, "count": 0}
        _step_times[step_name]["total"] += elapsed
        _step_times[step_name]["count"] += 1

        return result

    return wrapper


def profile_remake(func):
    """Decorator to profile remakeTestFile and print timing results."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        global _step_times
        _step_times = {}

        result = func(*args, **kwargs)

        # Print results
        print("\n" + "=" * 50)
        print("TIMING RESULTS")
        print("=" * 50)

        # Calculate totals
        total_time = sum(item["total"] for item in _step_times.values())
        results = []
        for step_name, data in _step_times.items():
            total = data["total"]
            percentage = (total / total_time * 100) if total_time > 0 else 0
            results.append((step_name, total, percentage))

        # Sort by total time descending
        results.sort(key=lambda x: x[1], reverse=True)

        # Print header
        print(f"{'Step':20s} | {'Time (s)':>10} | {'%':>6}")
        print("-" * 40)

        # Print results
        for step_name, total, percentage in results:
            print(f"{step_name:20s} | {total:>10.2f} | {percentage:>5.1f}%")

        print("-" * 40)
        print(f"{'TOTAL':20s} | {total_time:>10.2f} |")

        return result

    return wrapper
