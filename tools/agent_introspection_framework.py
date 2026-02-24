import functools
import os
import subprocess
import json
import traceback
import sys
from datetime import datetime, timezone
from typing import Dict, Any, Optional, Callable

# 确保标准库可访问
import io

class IntrospectionFramework:
    """
    主动探索者：Agent 内省调试框架
    基于 EvoMap Hub 推荐资产 (GDI: 66) 实现
    
    核心功能：
    1. 全局错误捕获 (Global Error Capture)
    2. 根因分析 (Root Cause Analysis)
    3. 自动修复 (Automatic Repair)
    4. 自动生成内省报告 (Auto-Generate Introspection Reports)
    
    修复版本：v1.1 (2026-02-24)
    - 修复了 `os` 导入问题（冗余防御）
    - 修复了 `pip` 命令未找到问题（尝试 pip3）
    """
    def __init__(self):
        self.error_log = []
        self.repair_log = []
        self.repair_rules = {
            "FileNotFoundError": {
                "cause": "Missing file or directory",
                "repair": self._repair_missing_file
            },
            "PermissionError": {
                "cause": "Insufficient file permissions",
                "repair": self._repair_permissions
            },
            "ModuleNotFoundError": {
                "cause": "Missing Python module",
                "repair": self._repair_missing_module
            },
            "ConnectionError": {
                "cause": "Network connection failed (often rate limit)",
                "repair": self._repair_rate_limit
            },
            "TimeoutError": {
                "cause": "Request timeout (often rate limit or slow network)",
                "repair": self._repair_rate_limit
            },
            "NameError": {
                "cause": "Python name undefined (e.g., missing import)",
                "repair": self._repair_name_error
            }
        }
    
    def capture_errors(self, func: Callable) -> Callable:
        """
        装饰器：捕获函数执行中的错误
        
        从混沌理论视角：
        - 正常状态是系统稳定吸引子（稳定运行）
        - 错误是系统偏离稳定吸引子（分岔或吸引子逃逸）
        - 错误捕获是反馈机制，试图将系统拉回稳定吸引子
        
        从信息论视角：
        - 错误信息是负熵（减少不确定性的信息）
        - 记录错误是信息熵减过程（将无序的错误信息转化为有序的日志）
        """
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                error_type = type(e).__name__
                
                # 确保 os 模块可用（冗余防御）
                if error_type == "NameError" and "os" in str(e):
                    # 尝试动态导入 os（作为备用）
                    try:
                        import os as os_module
                        # 将 sys.modules 中的 os 模块替换到全局命名空间
                        globals()["os"] = os_module
                    except ImportError:
                        # 如果导入失败，记录严重错误
                        error_type = "ImportError"
                
                error_trace = traceback.format_exc()
                
                # 根因分析
                rule = self.repair_rules.get(error_type, {})
                cause = rule.get("cause", "Unknown cause")
                repair_func = rule.get("repair", None)
                
                # 尝试自动修复
                repair_result = None
                if repair_func:
                    try:
                        repair_result = repair_func(e, func, args, kwargs)
                    except Exception as repair_exception:
                        repair_result = {
                            "status": "failed",
                            "error": str(repair_exception)
                        }
                
                # 记录内省信息
                introspection_data = {
                    "timestamp": datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z',
                    "function_name": func.__name__,
                    "error_type": error_type,
                    "error_message": str(e),
                    "error_trace": error_trace,
                    "cause": cause,
                    "repair_attempted": repair_func is not None,
                    "repair_result": repair_result
                }
                
                self.error_log.append(introspection_data)
                if repair_result:
                    self.repair_log.append(repair_result)
                
                # 生成报告
                self.generate_introspection_report(introspection_data)
                
                # 重新抛出异常（或根据策略处理）
                # 在主动探索者模式中，我们重新抛出以保持透明度
                raise IntrospectionError(f"IntrospectionFramework caught: {introspection_data['error_type']}") from e
                
        return wrapper
    
    def _repair_missing_file(self, e: Exception, func: Callable, args: tuple, kwargs: dict) -> Dict[str, Any]:
        """自动修复：创建缺失文件"""
        error_str = str(e)
        file_path = None
        
        if "'" in error_str:
            file_path = error_str.split("'")[1]
        elif '"' in error_str:
            file_path = error_str.split('"')[1]
        
        if file_path:
            try:
                dir_path = os.path.dirname(file_path)
                if dir_path and not os.path.exists(dir_path):
                    os.makedirs(dir_path)
                    return {"status": "success", "action": "created_directory", "path": dir_path}
                with open(file_path, 'w') as f:
                    f.write('')
                return {"status": "success", "action": "created_file", "path": file_path}
            except Exception as repair_error:
                return {"status": "failed", "action": "create_file", "error": str(repair_error)}
        
        return {"status": "skipped", "reason": "could not parse file path"}
    
    def _repair_permissions(self, e: Exception, func: Callable, args: tuple, kwargs: dict) -> Dict[str, Any]:
        """自动修复：修复文件权限"""
        try:
            # 修复当前目录（通常包含问题文件）
            os.chmod('.', 0o755)
            return {"status": "success", "action": "chmod_directory", "path": "."}
        except Exception as repair_error:
            return {"status": "failed", "action": "chmod", "error": str(repair_error)}
    
    def _repair_missing_module(self, e: Exception, func: Callable, args: tuple, kwargs: dict) -> Dict[str, Any]:
        """
        自动修复：安装缺失的模块
        
        从信息论视角：
        - 这是负熵减：通过安装模块减少系统不确定性（"模块存在"的熵减）
        - 优化依赖：安装缺失的模块优化信息流（模块之间的信息传递）
        """
        error_str = str(e)
        module_name = None
        
        if "No module named" in error_str:
            module_name = error_str.split("'")[1].strip("'")
        elif "cannot import" in error_str.lower():
            # 提取模块名（从 "cannot import module XXX"）
            parts = error_str.split()
            for part in parts:
                if "'" in part or '"' in part:
                    module_name = part.strip("'").strip('"')
                    break
        
        if module_name:
            # 尝试 pip3 和 pip
            pip_commands = [
                ["pip3", "install", module_name],
                ["pip", "install", module_name]
            ]
            
            for pip_cmd in pip_commands:
                try:
                    result = subprocess.run(
                        pip_cmd,
                        capture_output=True,
                        text=True,
                        timeout=30
                    )
                    if result.returncode == 0:
                        return {"status": "success", "action": "pip_install", "module": module_name, "cmd": pip_cmd[0]}
                    else:
                        # 如果 pip3/pip 失败，尝试 pipx（用户级安装）
                        if "No such file or directory" in result.stderr and "pip" in result.stderr:
                            # 尝试 python -m pip
                            try:
                                result = subprocess.run(
                                    ["python3", "-m", "pip", "install", module_name],
                                    capture_output=True,
                                    text=True,
                                    timeout=30
                                )
                                if result.returncode == 0:
                                    return {"status": "success", "action": "pip_install", "module": module_name, "cmd": "python3 -m pip"}
                            except Exception:
                                continue
                        continue
                except Exception as repair_error:
                    return {"status": "failed", "action": "pip_install", "module": module_name, "error": str(repair_error)}
        
        return {"status": "skipped", "reason": "could not parse module name"}
    
    def _repair_name_error(self, e: Exception, func: Callable, args: tuple, kwargs: dict) -> Dict[str, Any]:
        """自动修复：尝试重新导入 os 模块"""
        try:
            # 尝试动态导入 os
            import os as os_module
            globals()["os"] = os_module
            return {"status": "success", "action": "reload_os_module", "module": "os"}
        except Exception as repair_error:
            return {"status": "failed", "action": "reload_os_module", "error": str(repair_error)}
    
    def _repair_rate_limit(self, e: Exception, func: Callable, args: tuple, kwargs: dict) -> Dict[str, Any]:
        """
        自动修复：等待速率限制冷却（指数退避）
        
        从混沌理论视角：
        - 速率限制是系统进入"不稳定区域"（混沌区域）
        - 指数退避是"吸引子导航"：在相空间中导航回稳定区域
        - 等待是"暂态"：系统暂时不在稳定状态，需要等待稳定
        """
        import time
        wait_time = 5  # 5 秒冷却
        try:
            time.sleep(wait_time)
            return {"status": "success", "action": "rate_limit_cooldown", "wait_seconds": wait_time}
        except Exception as repair_error:
            return {"status": "failed", "action": "sleep", "error": str(repair_error)}
    
    def generate_introspection_report(self, introspection_data: Dict[str, Any]):
        """
        自动生成内省报告
        
        从信息论视角：
        - 报告是信息熵减的核心：将混乱的错误信息转化为有序的结构化数据
        - 结构化数据（JSON/Markdown）降低了信息熵（确定性增加）
        - 报告的"信息密度"优化：包含关键信息（错误类型、原因、修复结果）
        """
        report = f"""
---
# 🤖 Agent Introspection Report
**Generated at**: {introspection_data['timestamp']}
**Function**: {introspection_data['function_name']}

## 🚨 Error Analysis

**Error Type**: {introspection_data['error_type']}
**Error Message**: {introspection_data['error_message']}

### 💻 Root Cause Analysis

**Cause**: {introspection_data['cause']}
**Analysis**: 
From a chaos theory perspective, this error represents a divergence from the stable attractor (normal operation). The error is a bifurcation point where the system's behavior changed unexpectedly.

From an information theory perspective, this error increases system uncertainty (entropy). The repair attempt aims to perform entropy reduction by fixing the issue.

### 🔧 Repair Attempt

**Repair Attempted**: {introspection_data['repair_attempted']}
**Repair Result**:
```json
{json.dumps(introspection_data['repair_result'], indent=2) if introspection_data['repair_result'] else "null"}
```

## 💡 Theoretical Analysis

### 🧠 Chaos Theory Perspective
- **Attractor Divergence**: The error caused the system to diverge from its stable attractor.
- **Bifurcation Point**: The error is a bifurcation point where system behavior changed.
- **Chaos Management**: The repair attempt attempts to manage chaos by restoring stability.

### 💻 Information Theory Perspective
- **Entropy Reduction**: The error increased system entropy. The repair attempt aims to perform entropy reduction.
- **Information Density Optimization**: The error log provides high-density information (type, cause, repair).
- **Information Flow**: The repair action adjusts information flow to restore normal operation.

### 🎮 Cybernetics Perspective
- **Feedback Control**: The error is feedback (negative feedback) indicating system deviation.
- **Adaptive Control**: The repair action is adaptive (based on error type and rules).
- **Stability Control**: The repair attempt aims to restore system stability.

---

*Report generated by Active Explorer Agent*
"""
        print(report)
        
        # 保存报告到文件
        report_dir = os.path.expanduser("~/.openclaw/workspace/introspection_reports/")
        os.makedirs(report_dir, exist_ok=True)
        report_file = os.path.join(report_dir, f"report_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}.md")
        with open(report_file, 'w') as f:
            f.write(report)
        
        print(f"📄 Report saved to: {report_file}")

class IntrospectionError(Exception):
    """自定义异常：表示框架捕获的错误"""
    pass

# 示例用法
if __name__ == "__main__":
    framework = IntrospectionFramework()
    
    @framework.capture_errors
    def example_function():
        """示例函数：故意触发错误以演示框架"""
        print("Before error")
        # 故意触发 FileNotFound 错误
        open("/non/existent/file.txt")
        print("After error")
    
    # 测试框架
    try:
        example_function()
    except Exception as e:
        print(f"Caught by framework: {e}")
