"""Resource Monitor — Vol II Ch20.

If GPU or CPU exceeds threshold: save checkpoint -> pause -> cool down -> resume.
Uses pynvml (nvidia-ml-py) for GPU temp on your RTX 3050.
"""
from __future__ import annotations
import time
import psutil
from ..logging_setup import get_logger

log = get_logger("planner.resource_monitor")

try:
    import pynvml
    pynvml.nvmlInit()
    _NVML_OK = True
except Exception:
    _NVML_OK = False
    log.warning("pynvml unavailable — GPU temperature guard disabled")


class ResourceMonitor:
    def __init__(self, gpu_temp_warn_c: int, gpu_temp_pause_c: int,
                 vram_warn_pct: int, ram_warn_pct: int, cooldown_seconds: int,
                 cpu_warn_pct: int = 85, cpu_pause_pct: int = 95,
                 cpu_sustained_checks: int = 3):
        self.gpu_temp_warn_c = gpu_temp_warn_c
        self.gpu_temp_pause_c = gpu_temp_pause_c
        self.vram_warn_pct = vram_warn_pct
        self.ram_warn_pct = ram_warn_pct
        self.cooldown_seconds = cooldown_seconds
        self.cpu_warn_pct = cpu_warn_pct
        self.cpu_pause_pct = cpu_pause_pct
        self.cpu_sustained_checks = cpu_sustained_checks
        self._cpu_overload_streak = 0
        self._handle = pynvml.nvmlDeviceGetHandleByIndex(0) if _NVML_OK else None

    def snapshot(self) -> dict:
        status = {
            "ram_percent": psutil.virtual_memory().percent,
            "cpu_percent": psutil.cpu_percent(interval=0.2),
            "gpu_temp_c": None,
            "vram_percent": None,
        }
        if _NVML_OK:
            status["gpu_temp_c"] = pynvml.nvmlDeviceGetTemperature(self._handle, pynvml.NVML_TEMPERATURE_GPU)
            mem = pynvml.nvmlDeviceGetMemoryInfo(self._handle)
            status["vram_percent"] = round(100 * mem.used / mem.total, 1)
        return status

    def should_pause(self, status: dict) -> bool:
        gpu_temp = status.get("gpu_temp_c")
        if gpu_temp is not None and gpu_temp >= self.gpu_temp_pause_c:
            log.warning(f"GPU temp {gpu_temp}C >= pause threshold {self.gpu_temp_pause_c}C")
            self._cpu_overload_streak = 0
            return True

        if status.get("ram_percent", 0) >= self.ram_warn_pct:
            log.warning(f"RAM usage {status['ram_percent']}% >= warn threshold")
            self._cpu_overload_streak = 0
            return True

        cpu_percent = status.get("cpu_percent", 0)
        if cpu_percent >= self.cpu_pause_pct:
            self._cpu_overload_streak += 1
            log.warning(
                f"CPU usage {cpu_percent}% >= pause threshold {self.cpu_pause_pct}% "
                f"(streak {self._cpu_overload_streak}/{self.cpu_sustained_checks})"
            )
            if self._cpu_overload_streak >= self.cpu_sustained_checks:
                self._cpu_overload_streak = 0
                return True
            return False
        else:
            if cpu_percent >= self.cpu_warn_pct:
                log.info(f"CPU usage {cpu_percent}% >= warn threshold {self.cpu_warn_pct}%")
            self._cpu_overload_streak = 0

        return False

    def cooldown(self):
        log.info(f"Cooling down for {self.cooldown_seconds}s")
        time.sleep(self.cooldown_seconds)