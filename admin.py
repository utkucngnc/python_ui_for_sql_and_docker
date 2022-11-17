import ctypes
import sys
import platform

def admin() -> "Admin Bool":
    """Requests UAC Admin on Windows with a prompt"""
    if platform.system() == "Windows":
        ctypes.windll.shell32.ShellExecuteW(
            None,
            'runas',
            sys.executable,
            ' '.join(sys.argv),
            None,
            None
        )
        
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        
        except:
            return False
        
    else:
        raise OSError("admin() only works for windows.")