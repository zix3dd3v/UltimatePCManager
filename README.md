# UltimatePCManager

**UltimatePCManager** is an all-in-one windows maintenance and optimization utility designed to help keep your pc clean, fast, and stable. built with python and packaged into a standalone exe, UltimatePCManager combines multiple system tools into a single easy-to-use application. this was 100% vibecoded but works like magic dawg

## Features

### 🧹 PC Cleanup

* Removes temporary files and unnecessary system clutter
* Scans deeper than standard temp folders
* Displays the total amount of storage space recovered

### 🛡️ System Security

* Runs Windows System File Checker (SFC)
* Performs system integrity checks
* Helps identify corrupted or damaged Windows files

### ⚙️ Process Overlord

* Displays running processes and memory usage
* Highlights applications consuming the most RAM
* One-click process termination

### 🌐 Network Command Center

* View active network connections and ports
* Flush DNS cache
* Reset network configurations
* Open and edit the Windows hosts file

### 🚀 System Optimization

* One-click optimization routine
* Remove unnecessary background processes
* Restart Windows Explorer instantly
* GPU reset utility
* Emergency recovery tools

### 🔄 System Restore

* Create and manage restore points
* Roll back system changes when needed

### 📊 Performance Benchmark

* Benchmark CPU performance
* Benchmark GPU performance
* Benchmark disk performance

### 💥 Browser Cache Nuke

* Clear browser cache data
* Supports multiple browsers
* Additional browser support planned

### 🔍 Duplicate Finder

* Scan folders for duplicate files
* Select custom search locations
* Helps recover disk space

### ⚡ Power Profiles

* Switch between:

  * Ultimate Performance
  * Balanced
  * Power Saver

## Building From Source

### Requirements

* Python 3.11 or newer
* PyInstaller

Install PyInstaller:

```bash
pip install pyinstaller
```

Build the executable:

```bash
python -m PyInstaller --onefile --icon=broom.ico ultimatepcmanager.py
```

After compilation, the executable will be located in the `dist` folder.

## Disclaimer

UltimatePCManager performs system-level operations that may modify Windows settings, processes, and files. Use the application responsibly and create restore points before making significant system changes.

## License

Add your preferred license here (MIT, GPL, Apache 2.0, etc.).
