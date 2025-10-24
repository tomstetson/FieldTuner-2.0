#!/usr/bin/env python3
"""
FieldTuner Windows Installer Creator
Creates a professional Windows installer using NSIS
"""

import os
import sys
import shutil
from pathlib import Path

def create_nsis_script():
    """Create NSIS installer script."""
    nsis_script = """
; FieldTuner Windows Installer Script
; Created by Tom with Love from Cursor

!define APPNAME "FieldTuner"
!define COMPANYNAME "Tom Stetson"
!define DESCRIPTION "Battlefield 6 Configuration Tool"
!define VERSIONMAJOR 1
!define VERSIONMINOR 0
!define VERSIONBUILD 0
!define HELPURL "https://github.com/tomstetson/FieldTuner"
!define UPDATEURL "https://github.com/tomstetson/FieldTuner/releases"
!define ABOUTURL "https://github.com/tomstetson/FieldTuner"
!define INSTALLSIZE 50000

RequestExecutionLevel admin
InstallDir "$PROGRAMFILES\\${APPNAME}"
Name "${APPNAME}"
outFile "FieldTuner_Setup.exe"
icon "..\\assets\\icon.ico"

!include LogicLib.nsh

page directory
page instfiles

!macro VerifyUserIsAdmin
UserInfo::GetAccountType
pop $0
${If} $0 != "admin"
    messageBox mb_iconstop "Administrator rights required!"
    setErrorLevel 740
    quit
${EndIf}
!macroend

function .onInit
    setShellVarContext all
    !insertmacro VerifyUserIsAdmin
functionEnd

section "install"
    setOutPath $INSTDIR
    file "FieldTuner.exe"
    file "Run_FieldTuner.bat"
    file "README.txt"
    file "LICENSE.txt"
    
    ; Create uninstaller
    writeUninstaller "$INSTDIR\\uninstall.exe"
    
    ; Create shortcuts
    createDirectory "$SMPROGRAMS\\${APPNAME}"
    createShortCut "$SMPROGRAMS\\${APPNAME}\\${APPNAME}.lnk" "$INSTDIR\\FieldTuner.exe" "" "$INSTDIR\\FieldTuner.exe"
    createShortCut "$SMPROGRAMS\\${APPNAME}\\Run as Administrator.lnk" "$INSTDIR\\Run_FieldTuner.bat" "" "$INSTDIR\\Run_FieldTuner.bat"
    createShortCut "$SMPROGRAMS\\${APPNAME}\\Uninstall.lnk" "$INSTDIR\\uninstall.exe"
    
    ; Desktop shortcut
    createShortCut "$DESKTOP\\${APPNAME}.lnk" "$INSTDIR\\FieldTuner.exe" "" "$INSTDIR\\FieldTuner.exe"
    
    ; Registry entries
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${APPNAME}" "DisplayName" "${APPNAME}"
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${APPNAME}" "UninstallString" "$INSTDIR\\uninstall.exe"
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${APPNAME}" "InstallLocation" "$INSTDIR"
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${APPNAME}" "DisplayIcon" "$INSTDIR\\FieldTuner.exe"
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${APPNAME}" "Publisher" "${COMPANYNAME}"
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${APPNAME}" "HelpLink" "${HELPURL}"
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${APPNAME}" "URLUpdateInfo" "${UPDATEURL}"
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${APPNAME}" "URLInfoAbout" "${ABOUTURL}"
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${APPNAME}" "DisplayVersion" "${VERSIONMAJOR}.${VERSIONMINOR}.${VERSIONBUILD}"
    WriteRegDWORD HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${APPNAME}" "VersionMajor" ${VERSIONMAJOR}
    WriteRegDWORD HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${APPNAME}" "VersionMinor" ${VERSIONMINOR}
    WriteRegDWORD HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${APPNAME}" "NoModify" 1
    WriteRegDWORD HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${APPNAME}" "NoRepair" 1
    WriteRegDWORD HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${APPNAME}" "EstimatedSize" ${INSTALLSIZE}
sectionEnd

section "uninstall"
    delete "$INSTDIR\\FieldTuner.exe"
    delete "$INSTDIR\\Run_FieldTuner.bat"
    delete "$INSTDIR\\README.txt"
    delete "$INSTDIR\\LICENSE.txt"
    delete "$INSTDIR\\uninstall.exe"
    
    ; Remove shortcuts
    delete "$SMPROGRAMS\\${APPNAME}\\${APPNAME}.lnk"
    delete "$SMPROGRAMS\\${APPNAME}\\Run as Administrator.lnk"
    delete "$SMPROGRAMS\\${APPNAME}\\Uninstall.lnk"
    rmdir "$SMPROGRAMS\\${APPNAME}"
    delete "$DESKTOP\\${APPNAME}.lnk"
    
    ; Remove registry entries
    DeleteRegKey HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${APPNAME}"
    
    rmdir $INSTDIR
sectionEnd
"""
    return nsis_script

def create_installer():
    """Create the Windows installer."""
    print("FieldTuner Windows Installer Creator")
    print("=" * 40)
    
    # Check if NSIS is available
    nsis_path = shutil.which("makensis")
    if not nsis_path:
        print("NSIS not found. Please install NSIS from https://nsis.sourceforge.io/")
        print("Or use the portable version without installer.")
        return False
    
    # Create installer directory
    installer_dir = Path("installer")
    installer_dir.mkdir(exist_ok=True)
    
    # Create NSIS script
    nsis_script = create_nsis_script()
    script_path = installer_dir / "FieldTuner.nsi"
    with open(script_path, "w", encoding="utf-8") as f:
        f.write(nsis_script)
    
    print(f"Created NSIS script: {script_path}")
    
    # Copy files to installer directory
    releases_dir = Path("releases/FieldTuner_Portable_v1.0")
    if not releases_dir.exists():
        print("Error: Portable release not found. Please run build_simple.py first.")
        return False
    
    # Copy executable and files
    files_to_copy = [
        "FieldTuner.exe",
        "Run_FieldTuner.bat", 
        "README.txt",
        "LICENSE.txt"
    ]
    
    for file_name in files_to_copy:
        src = releases_dir / file_name
        dst = installer_dir / file_name
        if src.exists():
            shutil.copy2(src, dst)
            print(f"Copied {file_name}")
        else:
            print(f"Warning: {file_name} not found in release")
    
    # Copy icon
    icon_src = Path("assets/icon.ico")
    icon_dst = installer_dir / "icon.ico"
    if icon_src.exists():
        shutil.copy2(icon_src, icon_dst)
        print("Copied icon.ico")
    
    # Run NSIS compiler
    print("Compiling installer...")
    import subprocess
    
    try:
        result = subprocess.run([
            "makensis", str(script_path)
        ], capture_output=True, text=True, cwd=installer_dir)
        
        if result.returncode == 0:
            print("Installer created successfully!")
            print(f"Installer: {installer_dir / 'FieldTuner_Setup.exe'}")
            return True
        else:
            print(f"NSIS compilation failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"Error running NSIS: {e}")
        return False

def create_simple_installer():
    """Create a simple installer using Python."""
    print("Creating simple Python installer...")
    
    installer_script = '''#!/usr/bin/env python3
"""
FieldTuner Simple Installer
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

def install_fieldtuner():
    """Install FieldTuner to Program Files."""
    print("FieldTuner Installer")
    print("=" * 20)
    
    # Check for admin privileges
    try:
        import ctypes
        if not ctypes.windll.shell32.IsUserAnAdmin():
            print("Error: Administrator privileges required!")
            print("Please run this installer as administrator.")
            input("Press Enter to exit...")
            return False
    except:
        print("Warning: Could not verify administrator privileges")
    
    # Installation directory
    install_dir = Path("C:/Program Files/FieldTuner")
    
    print(f"Installing to: {install_dir}")
    
    # Create installation directory
    install_dir.mkdir(parents=True, exist_ok=True)
    
    # Copy files
    source_dir = Path(".")
    files_to_install = [
        "FieldTuner.exe",
        "Run_FieldTuner.bat",
        "README.txt",
        "LICENSE.txt"
    ]
    
    for file_name in files_to_install:
        src = source_dir / file_name
        dst = install_dir / file_name
        if src.exists():
            shutil.copy2(src, dst)
            print(f"Installed {file_name}")
        else:
            print(f"Warning: {file_name} not found")
    
    # Create desktop shortcut
    desktop = Path.home() / "Desktop"
    shortcut_path = desktop / "FieldTuner.lnk"
    
    try:
        import winshell
        from win32com.client import Dispatch
        
        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(str(shortcut_path))
        shortcut.Targetpath = str(install_dir / "FieldTuner.exe")
        shortcut.WorkingDirectory = str(install_dir)
        shortcut.IconLocation = str(install_dir / "FieldTuner.exe")
        shortcut.save()
        print("Created desktop shortcut")
    except ImportError:
        print("Warning: Could not create desktop shortcut (winshell not available)")
    except Exception as e:
        print(f"Warning: Could not create desktop shortcut: {e}")
    
    # Create Start Menu shortcut
    start_menu = Path.home() / "AppData/Roaming/Microsoft/Windows/Start Menu/Programs"
    start_menu.mkdir(parents=True, exist_ok=True)
    
    try:
        shortcut_path = start_menu / "FieldTuner.lnk"
        shortcut = shell.CreateShortCut(str(shortcut_path))
        shortcut.Targetpath = str(install_dir / "FieldTuner.exe")
        shortcut.WorkingDirectory = str(install_dir)
        shortcut.IconLocation = str(install_dir / "FieldTuner.exe")
        shortcut.save()
        print("Created Start Menu shortcut")
    except Exception as e:
        print(f"Warning: Could not create Start Menu shortcut: {e}")
    
    print("\\nInstallation completed successfully!")
    print(f"FieldTuner installed to: {install_dir}")
    print("You can now run FieldTuner from the Start Menu or Desktop shortcut.")
    
    input("Press Enter to exit...")
    return True

if __name__ == "__main__":
    install_fieldtuner()
'''
    
    installer_path = Path("installer/install_fieldtuner.py")
    with open(installer_path, "w", encoding="utf-8") as f:
        f.write(installer_script)
    
    print(f"Created simple installer: {installer_path}")
    return True

def main():
    """Main installer creation function."""
    print("FieldTuner Installer Creator")
    print("=" * 30)
    
    # Try NSIS first
    if create_installer():
        print("NSIS installer created successfully!")
        return True
    
    # Fallback to simple installer
    print("Falling back to simple Python installer...")
    if create_simple_installer():
        print("Simple installer created successfully!")
        return True
    
    print("Failed to create installer")
    return False

if __name__ == "__main__":
    main()
