import sys
sys.path.append('/home/devbox/.openclaw/workspace/tools')
from agent_introspection_framework import IntrospectionFramework, IntrospectionError

framework = IntrospectionFramework()

@framework.capture_errors
def trigger_file_not_found_error():
    """测试函数：故意触发 FileNotFoundError"""
    print("测试：触发 FileNotFoundError...")
    open("/tmp/non_existent_test_file_12345.txt")

@framework.capture_errors
def trigger_permission_error():
    """测试函数：故意触发 PermissionError"""
    print("测试：触发 PermissionError...")
    os.chmod("/tmp/non_existent_permission_test_12345.txt", 0o000)

@framework.capture_errors
def trigger_module_not_found_error():
    """测试函数：故意触发 ModuleNotFoundError"""
    print("测试：触发 ModuleNotFoundError...")
    import non_existent_module_12345

if __name__ == "__main__":
    print("🧪 开始内省框架测试\n")
    print("="*60)
    
    # 测试 1: FileNotFoundError
    print("🔴 测试 1: FileNotFoundError")
    try:
        trigger_file_not_found_error()
    except IntrospectionError as e:
        print(f"✅ 框架捕获到错误: {e}")
    except Exception as e:
        print(f"❌ 未捕获的错误: {e}")
    
    print("\n")
    
    # 测试 2: PermissionError
    print("🔴 测试 2: PermissionError")
    try:
        trigger_permission_error()
    except IntrospectionError as e:
        print(f"✅ 框架捕获到错误: {e}")
    except Exception as e:
        print(f"❌ 未捕获的错误: {e}")
    
    print("\n")
    
    # 测试 3: ModuleNotFoundError
    print("🔴 测试 3: ModuleNotFoundError")
    try:
        trigger_module_not_found_error()
    except IntrospectionError as e:
        print(f"✅ 框架捕获到错误: {e}")
    except Exception as e:
        print(f"❌ 未捕获的错误: {e}")
    
    print("\n")
    print("="*60)
    print("🧪 内省框架测试完成")
    print("📄 报告已生成：~/.openclaw/workspace/introspection_reports/")
