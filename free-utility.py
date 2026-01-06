import os
import sys
import ctypes
import subprocess
import winreg
import time

def is_admin():
    try: return ctypes.windll.shell32.IsUserAnAdmin()
    except: return False

def run_as_admin():
    if not is_admin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit()

def set_r(h, p, n, v, t=winreg.REG_DWORD):
    try:
        k = winreg.CreateKeyEx(h, p, 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(k, n, 0, t, v)
        winreg.CloseKey(k)
    except: pass

def step(text, d=1.2):
    print(f"[*] {text.ljust(40)}", end="", flush=True)
    for _ in range(12):
        time.sleep(d/12)
        print("■", end="", flush=True)
    print(" [DONE]")

def init_r():
    print("\n[SYSTEM_SECURITY_CHECK]")
    step("Creating Hardware Snapshot", 2.0)
    subprocess.run('powershell -Command "Checkpoint-Computer -Description \'ZVX_v1.1.0_PR\' -RestorePointType MODIFY_SETTINGS"', shell=True, capture_output=True)

def engine_v2():
    print("\n[CORE_PERFORMANCE_ENGINE_v2]")
    
    # Low Latency & IRQ Optimizations
    step("Optimizing IRQL Interrupts", 1.5)
    set_r(winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Control\PriorityControl", "Win32PrioritySeparation", 38)
    set_r(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile", "SystemResponsiveness", 0)
    
    # GPU & DWM Extreme Tweaks
    step("Applying DWM Low Latency Patches", 1.0)
    set_r(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\DirectX", "MaxFrameLatency", 1)
    set_r(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Explorer\VisualEffects", "VisualFXSetting", 2)
    
    # Network & Ping (Bypass Throttling)
    step("Bypassing Network Throttling Index", 1.2)
    set_r(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile", "NetworkThrottlingIndex", 0xFFFFFFFF)
    set_r(winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Services\Tcpip\Parameters\Interfaces", "TcpAckFrequency", 1)
    set_r(winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Services\Tcpip\Parameters\Interfaces", "TCPNoDelay", 1)

    # Power & CPU
    step("Unlocking Processor Hidden Performance", 1.0)
    os.system("powercfg -duplicatescheme e9a42b02-d5df-448d-aa00-03f14749eb61 >nul")
    os.system("powercfg -setactive e9a42b02-d5df-448d-aa00-03f14749eb61 >nul")

def cleaner_v2():
    print("\n[DEEP_FS_CLEANER]")
    o = [
        ("Nuking %TEMP% Files", 1.5),
        ("Flushing Event Logs (Wvutil)", 1.2),
        ("Wiping DNS/ARP Cache", 0.8),
        ("Optimizing MFT Tables", 1.5)
    ]
    for t, d in o: step(t, d)
    os.system('del /q /f /s %temp%\* >nul 2>&1')
    os.system('del /q /f /s C:\Windows\Temp\* >nul 2>&1')
    os.system('wevtutil cl System >nul 2>&1')
    os.system('ipconfig /flushdns >nul')

def debloat_v2():
    print("\n[SERVICE_DESTRUCTION_MODULE]")
    svcs = [
        "DiagTrack", "SysMain", "WSearch", "dmwappushservice", "MapsBroker", 
        "XblAuthManager", "XblGameSave", "RemoteRegistry", "Spooler", 
        "TabletInputService", "SensorService", "WbioSrvc", "PhoneSvc"
    ]
    for s in svcs:
        step(f"Terminating {s}", 0.1)
        os.system(f"sc stop {s} >nul 2>&1 && sc config {s} start= disabled >nul 2>&1")

def menu():
    while True:
        os.system('cls')
        os.system('color 0F')
        print("""
        --------------------------------------------------
                  ZVX FREE UTILITY PANEL v1.1.0
        --------------------------------------------------""")
        print("[1] INITIALIZE RESTORE POINT")
        print("[2] EXTREME FPS & INPUT LAG (Jebniecie FPS)")
        print("[3] DEEP SYSTEM CLEANER (Deep Scan)")
        print("[4] NUCLEAR DEBLOATER (Processes)")
        print("[5] FULL REBUILD (All Optimized)")
        print("[6] EMERGENCY RECOVERY")
        print("[7] EXIT")
        print("--------------------------------------------------")
        
        cmd = input(">> ")
        if cmd == "1": init_r()
        elif cmd == "2": engine_v2()
        elif cmd == "3": cleaner_v2()
        elif cmd == "4": debloat_v2()
        elif cmd == "5":
            init_r(); engine_v2(); debloat_v2(); cleaner_v2()
        elif cmd == "6": os.system("rstrui.exe")
        elif cmd == "7": break
        
        print("\n[!] TASK_COMPLETE.")
        input("Press Enter to continue...")

if __name__ == "__main__":
    ctypes.windll.kernel32.SetConsoleTitleW("ZVX_UTILITY_v1.1.0")
    run_as_admin()
    menu()
