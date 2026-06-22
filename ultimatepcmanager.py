import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

import platform
import time
import sys
import os
import shutil
import ctypes
import threading
import subprocess
import tkinter as tk
import customtkinter as ctk
import psutil

# Fast, native C-types interface for NVIDIA tracking
try:
    import pynvml
    pynvml.nvmlInit()
    NVML_READY = True
except Exception:
    NVML_READY = False

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class AdvancedTelemetrySuite(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Ultimate PC Manager")
        self.geometry("1400x950")  # Optimized for 11 tabs with ultimate features
        self.resizable(True, True)  # Now fully resizable!
        
        # Set custom icon if it exists
        try:
            icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "broom.ico")
            if os.path.exists(icon_path):
                self.iconbitmap(icon_path)
        except:
            pass  # If icon doesn't exist, use default
        
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        self.spec_labels = {}
        self.last_net_io = psutil.net_io_counters()
        self.last_net_time = time.time()

        # --- MAIN TABVIEW ---
        self.tabview = ctk.CTkTabview(self, fg_color="#141418", 
                                       segmented_button_selected_color="#00D2FF", 
                                       segmented_button_selected_hover_color="#0099CC")
        self.tabview.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Original Tabs
        self.tab_telemetry = self.tabview.add("SYSTEM TELEMETRY")
        self.tab_cleaner = self.tabview.add("PC CLEANUP")
        self.tab_virus = self.tabview.add("SYSTEM SECURITY")
        
        # New God-Mode Tabs
        self.tab_process = self.tabview.add("PROCESS OVERLORD")
        self.tab_network = self.tabview.add("NETWORK COMMAND")
        self.tab_coresystem = self.tabview.add("SYSTEM OPTIMIZATION")
        
        # Ultimate Power Tabs
        self.tab_restore = self.tabview.add("SYSTEM RESTORE")
        self.tab_benchmark = self.tabview.add("PERFORMANCE BENCHMARK")
        self.tab_browser = self.tabview.add("BROWSER CACHE NUKE")
        self.tab_duplicates = self.tabview.add("DUPLICATE FINDER")
        self.tab_power = self.tabview.add("POWER PROFILES")
        
        # Build All Tabs
        self.build_telemetry_tab()
        self.build_cleaner_tab()
        self.build_security_tab()
        self.build_process_tab()
        self.build_network_tab()
        self.build_coresystem_tab()
        self.build_restore_tab()
        self.build_benchmark_tab()
        self.build_browser_tab()
        self.build_duplicates_tab()
        self.build_power_tab()

        self.after(150, self.deferred_system_init)
        
    # ==========================================
    # TAB 1: SYSTEM TELEMETRY
    # ==========================================
    def build_telemetry_tab(self):
        header_frame = ctk.CTkFrame(self.tab_telemetry, fg_color="transparent")
        header_frame.pack(fill="x", padx=10, pady=(10, 2))
        ctk.CTkLabel(header_frame, text="SYSTEM TELEMETRY", font=ctk.CTkFont(family="Segoe UI", size=20, weight="bold"), text_color="#00D2FF").pack(anchor="w")
        ctk.CTkLabel(header_frame, text="REAL-TIME HARDWARE ARCHITECTURE AND POWER MONITOR", font=ctk.CTkFont(family="Segoe UI", size=10), text_color="#606065").pack(anchor="w")
        
        specs_frame = ctk.CTkFrame(self.tab_telemetry, corner_radius=8, fg_color="#1A1A20", border_width=1, border_color="#222228")
        specs_frame.pack(fill="x", padx=10, pady=5)
        ctk.CTkLabel(specs_frame, text="■ SYSTEM ARCHITECTURE", font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"), text_color="#A0A0A5").pack(anchor="w", padx=15, pady=(6, 2))
        
        self.create_spec_node(specs_frame, "HOST OS", "Querying...", "os")
        self.create_spec_node(specs_frame, "PROCESSOR", "Querying...", "cpu")
        self.create_spec_node(specs_frame, "GRAPHICS", "Querying...", "gpu")
        self.create_spec_node(specs_frame, "MEMORY", "Querying...", "ram")
        self.create_spec_node(specs_frame, "STORAGE", "Querying...", "storage")
        
        perf_frame = ctk.CTkFrame(self.tab_telemetry, corner_radius=8, fg_color="#1A1A20", border_width=1, border_color="#222228")
        perf_frame.pack(fill="x", padx=10, pady=5)
        ctk.CTkLabel(perf_frame, text="■ LIVE UTILITY METRICS", font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"), text_color="#A0A0A5").pack(anchor="w", padx=15, pady=(6, 2))
        
        self.cpu_label = ctk.CTkLabel(perf_frame, text="CPU COMPUTE UTILITY: 0%", font=ctk.CTkFont(size=11, weight="bold"))
        self.cpu_label.pack(anchor="w", padx=20)
        self.cpu_bar = ctk.CTkProgressBar(perf_frame, progress_color="#00D2FF", fg_color="#222228", height=5)
        self.cpu_bar.pack(fill="x", padx=20, pady=(1, 5))
        
        self.ram_label = ctk.CTkLabel(perf_frame, text="DYNAMIC MEMORY ALLOCATION: 0%", font=ctk.CTkFont(size=11, weight="bold"))
        self.ram_label.pack(anchor="w", padx=20)
        self.ram_bar = ctk.CTkProgressBar(perf_frame, progress_color="#B162FF", fg_color="#222228", height=5)
        self.ram_bar.pack(fill="x", padx=20, pady=(1, 5))

        self.gpu_label = ctk.CTkLabel(perf_frame, text="GPU CORE UTILIZATION: 0%", font=ctk.CTkFont(size=11, weight="bold"))
        self.gpu_label.pack(anchor="w", padx=20)
        self.gpu_bar = ctk.CTkProgressBar(perf_frame, progress_color="#00FF87", fg_color="#222228", height=5)
        self.gpu_bar.pack(fill="x", padx=20, pady=(1, 5))

        self.disk_label = ctk.CTkLabel(perf_frame, text="PRIMARY DRIVE CAPACITY USED: 0%", font=ctk.CTkFont(size=11, weight="bold"))
        self.disk_label.pack(anchor="w", padx=20)
        self.disk_bar = ctk.CTkProgressBar(perf_frame, progress_color="#FF9F00", fg_color="#222228", height=5)
        self.disk_bar.pack(fill="x", padx=20, pady=(1, 6))
        
        intel_frame = ctk.CTkFrame(self.tab_telemetry, corner_radius=8, fg_color="#1A1A20", border_width=1, border_color="#222228")
        intel_frame.pack(fill="x", padx=10, pady=5)
        ctk.CTkLabel(intel_frame, text="■ NETWORK & ACTIVE PROCESS INTEL", font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"), text_color="#00FFD2").pack(anchor="w", padx=15, pady=(6, 2))
        self.net_down_lbl = ctk.CTkLabel(intel_frame, text="NETWORK DOWNLINK : 0.00 MB/s", font=ctk.CTkFont(family="Consolas", size=11), text_color="#E5E5EA")
        self.net_down_lbl.pack(anchor="w", padx=20, pady=1)
        self.net_up_lbl = ctk.CTkLabel(intel_frame, text="NETWORK UPLINK   : 0.01 MB/s", font=ctk.CTkFont(family="Consolas", size=11), text_color="#E5E5EA")
        self.net_up_lbl.pack(anchor="w", padx=20, pady=1)
        self.proc_hog_lbl = ctk.CTkLabel(intel_frame, text="RESOURCE LEADER  : Scanning...", font=ctk.CTkFont(family="Consolas", size=11), text_color="#FF6262")
        self.proc_hog_lbl.pack(anchor="w", padx=20, pady=1)
        self.uptime_lbl = ctk.CTkLabel(intel_frame, text="SYSTEM UP-TIME   : 0h 0m 0s", font=ctk.CTkFont(family="Consolas", size=11), text_color="#A0A0A5")
        self.uptime_lbl.pack(anchor="w", padx=20, pady=(1, 6))

        self.power_frame = ctk.CTkFrame(self.tab_telemetry, corner_radius=8, fg_color="#1A1A20", border_width=1, border_color="#222228")
        self.power_frame.pack(fill="x", padx=10, pady=5)
        ctk.CTkLabel(self.power_frame, text="⚡ ENERGY & WATTAGE TELEMETRY", font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"), text_color="#FFE600").pack(anchor="w", padx=15, pady=(6, 2))
        
        self.gpu_watt_lbl = ctk.CTkLabel(self.power_frame, text="GPU POWER DRAW: 0.0 W", font=ctk.CTkFont(family="Consolas", size=12), text_color="#E5E5EA")
        self.gpu_watt_lbl.pack(anchor="w", padx=20, pady=1)
        self.cpu_watt_lbl = ctk.CTkLabel(self.power_frame, text="EST. CPU POWER DRAW: 0.0 W", font=ctk.CTkFont(family="Consolas", size=12), text_color="#E5E5EA")
        self.cpu_watt_lbl.pack(anchor="w", padx=20, pady=1)
        self.total_watt_lbl = ctk.CTkLabel(self.power_frame, text="TOTAL ESTIMATED PC LOAD: 0.0 W", font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"), text_color="#FFE600")
        self.total_watt_lbl.pack(anchor="w", padx=20, pady=(3, 10))
        
    def create_spec_node(self, parent, category, placeholder, key):
        node = ctk.CTkFrame(parent, fg_color="transparent")
        node.pack(fill="x", padx=15, pady=1)
        cat_lbl = ctk.CTkLabel(node, text=f"{category:<12}", font=ctk.CTkFont(family="Consolas", size=11, weight="bold"), text_color="#00D2FF", width=90, anchor="w")
        cat_lbl.pack(side="left")
        val_lbl = ctk.CTkLabel(node, text=placeholder, font=ctk.CTkFont(family="Segoe UI", size=12), text_color="#E5E5EA", anchor="w")
        val_lbl.pack(side="left", fill="x", expand=True)
        self.spec_labels[key] = val_lbl

    # ==========================================
    # TAB 2: PC CLEANER
    # ==========================================
    def build_cleaner_tab(self):
        self.cleaner_console = ctk.CTkTextbox(self.tab_cleaner, height=450, fg_color="#0A0A0C", text_color="#00FF87", font=ctk.CTkFont(family="Consolas", size=12))
        self.cleaner_console.pack(fill="x", padx=20, pady=(20, 10))
        self.cleaner_console.insert("0.0", "================================================\n  GOD-TIER PC CLEANUP & HEALTH PROTOCOL\n================================================\n\n[IDLE] Awaiting command...\n")
        self.cleaner_console.configure(state="disabled")

        stats_frame = ctk.CTkFrame(self.tab_cleaner, fg_color="transparent")
        stats_frame.pack(fill="x", padx=20, pady=10)
        
        self.clean_mem_lbl = ctk.CTkLabel(stats_frame, text="0%\nMemory Usage", justify="left", font=ctk.CTkFont(size=14, weight="bold"))
        self.clean_mem_lbl.pack(side="left", padx=20)
        
        self.temp_size_lbl = ctk.CTkLabel(stats_frame, text="Calculating...\nTemporary Files", justify="left", font=ctk.CTkFont(size=14, weight="bold"))
        self.temp_size_lbl.pack(side="left", padx=40)

        self.btn_clean = ctk.CTkButton(self.tab_cleaner, text="EXECUTE CLEANUP PROTOCOL", fg_color="#0055FF", hover_color="#0033CC", height=50, font=ctk.CTkFont(size=14, weight="bold"), command=self.start_cleanup_thread)
        self.btn_clean.pack(fill="x", padx=20, pady=20)

    def log_cleaner(self, text):
        self.cleaner_console.configure(state="normal")
        self.cleaner_console.insert("end", text + "\n")
        self.cleaner_console.see("end")
        self.cleaner_console.configure(state="disabled")

    def get_dir_size(self, path):
        total = 0
        try:
            for dirpath, _, filenames in os.walk(path):
                for f in filenames:
                    fp = os.path.join(dirpath, f)
                    if not os.path.islink(fp): total += os.path.getsize(fp)
        except: pass
        return total

    def start_cleanup_thread(self):
        self.btn_clean.configure(state="disabled", text="CLEANING IN PROGRESS...")
        threading.Thread(target=self.run_cleanup_logic, daemon=True).start()

    def run_cleanup_logic(self):
        targets = [
            os.environ.get('TEMP'),
            r"C:\Windows\Temp",
            r"C:\Windows\Prefetch",
            r"C:\Windows\SoftwareDistribution\Download"
        ]
        freed_bytes = 0
        self.log_cleaner("\n>>> PHASE 1: Initiating Junk Eradication <<<")

        for i, path in enumerate(targets):
            if not path or not os.path.exists(path): continue
            self.log_cleaner(f"[{i+1}/{len(targets)}] Scrubbing {path}...")
            time.sleep(0.5) 
            try:
                items = os.listdir(path)
            except PermissionError:
                self.log_cleaner(f"    [!] Access Denied. Skipping folder.")
                continue 
            
            for item in items:
                item_path = os.path.join(path, item)
                try:
                    size = os.path.getsize(item_path) if os.path.isfile(item_path) else self.get_dir_size(item_path)
                    if os.path.isfile(item_path): os.remove(item_path)
                    elif os.path.isdir(item_path): shutil.rmtree(item_path)
                    freed_bytes += size
                except Exception: pass

        self.log_cleaner("\n[*] Incinerating Recycle Bin contents...")
        try:
            ctypes.windll.shell32.SHEmptyRecycleBinW(None, None, 7)
        except Exception as e:
            self.log_cleaner(f"[!] Recycle bin skip: {e}")

        mb_freed = freed_bytes / (1024 * 1024)
        self.log_cleaner(f"\n[SUCCESS] Protocol Complete. Incinerated {mb_freed:.2f} MB of junk.")
        self.btn_clean.configure(state="normal", text="EXECUTE CLEANUP PROTOCOL")
        self.temp_size_lbl.configure(text=f"0 KB\nTemporary Files")

    # ==========================================
    # TAB 3: SYSTEM SECURITY
    # ==========================================
    def build_security_tab(self):
        self.sec_console = ctk.CTkTextbox(self.tab_virus, height=450, fg_color="#0A0A0C", text_color="#FFCC00", font=ctk.CTkFont(family="Consolas", size=12))
        self.sec_console.pack(fill="x", padx=20, pady=(20, 10))
        self.sec_console.insert("0.0", "================================================\n  SYSTEM INTEGRITY & THREAT DETECTION\n================================================\n\nReady for scan sequence...\n")
        self.sec_console.configure(state="disabled")

        self.btn_scan = ctk.CTkButton(self.tab_virus, text="INITIATE DEEP SCAN (SFC + DEFENDER)", fg_color="#990000", hover_color="#660000", height=50, font=ctk.CTkFont(size=14, weight="bold"), command=self.start_security_thread)
        self.btn_scan.pack(fill="x", padx=20, pady=20)

    def log_security(self, text):
        self.sec_console.configure(state="normal")
        self.sec_console.insert("end", text + "\n")
        self.sec_console.see("end")
        self.sec_console.configure(state="disabled")

    def start_security_thread(self):
        self.btn_scan.configure(state="disabled", text="SCANNING SYSTEM...")
        threading.Thread(target=self.run_security_logic, daemon=True).start()

    def run_security_logic(self):
        self.log_security("\n>>> PHASE 1: Executing SFC /SCANNOW <<<")
        try:
            process = subprocess.Popen(["sfc", "/scannow"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
            for line in iter(process.stdout.readline, ''):
                if line.strip(): self.log_security(f"[SFC] {line.strip()}")
            process.wait()
        except Exception as e: self.log_security(f"[!] SFC Error: {e}")

        self.log_security("\n>>> PHASE 2: Windows Defender Quick Scan <<<")
        try:
            process = subprocess.Popen(["powershell", "-Command", "Start-MpScan -ScanType QuickScan"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
            for line in iter(process.stdout.readline, ''):
                if line.strip(): self.log_security(f"[DEFENDER] {line.strip()}")
            process.wait()
        except Exception as e: self.log_security(f"[!] Defender Error: {e}")

        self.log_security("\n[SUCCESS] All security protocols finished.")
        self.btn_scan.configure(state="normal", text="INITIATE DEEP SCAN (SFC + DEFENDER)")

    # ==========================================
    # TAB 4: #1 PROCESS OVERLORD
    # ==========================================
    def build_process_tab(self):
        header_frame = ctk.CTkFrame(self.tab_process, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=(10, 5))
        ctk.CTkLabel(header_frame, text="PROCESS OVERLORD", font=ctk.CTkFont(size=20, weight="bold"), text_color="#FF3366").pack(anchor="w")
        
        # The dropdown selector
        self.proc_selector = ctk.CTkOptionMenu(self.tab_process, values=["Refresh to load processes..."], width=400)
        self.proc_selector.pack(fill="x", padx=20, pady=10)
        
        btn_frame = ctk.CTkFrame(self.tab_process, fg_color="transparent")
        btn_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkButton(btn_frame, text="REFRESH LIST", fg_color="#222228", command=self.update_process_overlord).pack(side="left", fill="x", expand=True, padx=(0, 5))
        ctk.CTkButton(btn_frame, text="TERMINATE SELECTED", fg_color="#990000", hover_color="#BB0000", command=self.nuke_selected_process).pack(side="left", fill="x", expand=True, padx=(5, 0))

        # NEW: Process Memory Display with Kill Buttons
        memory_label_frame = ctk.CTkFrame(self.tab_process, fg_color="transparent")
        memory_label_frame.pack(fill="x", padx=20, pady=(15, 5))
        ctk.CTkLabel(memory_label_frame, text="TOP MEMORY CONSUMERS", font=ctk.CTkFont(size=12, weight="bold"), text_color="#FF3366").pack(anchor="w")
        
        self.proc_memory_frame = ctk.CTkScrollableFrame(self.tab_process, fg_color="#1A1A20", corner_radius=8)
        self.proc_memory_frame.pack(fill="both", expand=True, padx=20, pady=(5, 20))

    def update_process_overlord(self):
        procs = []
        for p in psutil.process_iter(['pid', 'name']):
            try:
                if p.info['name']:
                    procs.append(f"{p.info['pid']} - {p.info['name']}")
            except: continue
        
        # Sort alphabetically by process name
        procs.sort()
        self.proc_selector.configure(values=procs)
        self.proc_selector.set(procs[0]) # Default to first
        
        # Update memory display
        self.update_memory_display()

    def update_memory_display(self):
        # Clear existing widgets
        for widget in self.proc_memory_frame.winfo_children():
            widget.destroy()
        
        # Get process memory info
        proc_mem_list = []
        try:
            for p in psutil.process_iter(['pid', 'name', 'memory_percent']):
                try:
                    mem_percent = p.info['memory_percent'] or 0
                    if mem_percent > 0.1:  # Only show processes using > 0.1% memory
                        proc_mem_list.append({
                            'pid': p.info['pid'],
                            'name': p.info['name'],
                            'memory_percent': mem_percent
                        })
                except: continue
        except: pass
        
        # Sort by memory usage
        proc_mem_list.sort(key=lambda x: x['memory_percent'], reverse=True)
        
        # Display top 8 memory hogs
        for proc in proc_mem_list[:8]:
            proc_row = ctk.CTkFrame(self.proc_memory_frame, fg_color="#0A0A0C", corner_radius=6)
            proc_row.pack(fill="x", padx=10, pady=5)
            
            # Process info
            info_text = f"{proc['name']:<30} {proc['memory_percent']:>6.2f}% RAM"
            info_label = ctk.CTkLabel(proc_row, text=info_text, font=ctk.CTkFont(family="Consolas", size=10), text_color="#E5E5EA", anchor="w")
            info_label.pack(side="left", fill="both", expand=True, padx=10, pady=8)
            
            # Kill button
            kill_btn = ctk.CTkButton(proc_row, text="KILL", width=60, height=30, fg_color="#990000", hover_color="#BB0000", 
                                    font=ctk.CTkFont(size=10, weight="bold"), 
                                    command=lambda pid=proc['pid'], name=proc['name']: self.kill_process_by_id(pid, name))
            kill_btn.pack(side="right", padx=10, pady=8)

    def kill_process_by_id(self, pid, name):
        try:
            p = psutil.Process(pid)
            p.kill()
            ctypes.windll.user32.MessageBoxW(0, f"Terminated {name} (PID: {pid})", "PROCESS ELIMINATED", 0x40)
            self.update_memory_display()
        except Exception as e:
            ctypes.windll.user32.MessageBoxW(0, f"Cannot terminate: {e}", "ACCESS DENIED", 0x10)

    def nuke_top_hog(self):
        # Always re-check the top process list to ensure accuracy
        if hasattr(self, 'current_proc_list') and self.current_proc_list:
            target = self.current_proc_list[0] # The one at the top is the biggest hog
            try:
                proc = psutil.Process(target['pid'])
                proc_name = proc.name()
                
                # Perform the termination
                proc.kill()
                
                # Log success
                self.proc_textbox.configure(state="normal")
                self.proc_textbox.insert("end", f"\n>>> [!] TERMINATED: {proc_name} (PID: {target['pid']})\n")
                self.proc_textbox.configure(state="disabled")
                
                # Refresh UI
                self.update_process_overlord()
            except Exception as e:
                ctypes.windll.user32.MessageBoxW(0, f"Cannot terminate system process: {e}", "ACCESS DENIED", 0x10)
        else:
            ctypes.windll.user32.MessageBoxW(0, "No process found to terminate.", "SYSTEM OVERLORD", 0x30)

    def purge_working_sets(self):
        purged = 0
        for p in psutil.process_iter(['pid', 'name']):
            try:
                # Open system handle and flush memory working sets natively
                handle = ctypes.windll.kernel32.OpenProcess(0x1F0FFF, False, p.info['pid'])
                if handle:
                    ctypes.windll.psapi.EmptyWorkingSet(handle)
                    ctypes.windll.kernel32.CloseHandle(handle)
                    purged += 1
            except: pass
        ctypes.windll.user32.MessageBoxW(0, f"Flushed working sets across {purged} active system processes.", "RAM OVERHAUL COMPLETE", 0x40)

    # ==========================================
    # TAB 5: #2 NETWORK COMMAND
    # ==========================================
    def build_network_tab(self):
        header_frame = ctk.CTkFrame(self.tab_network, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=(10, 5))
        ctk.CTkLabel(header_frame, text="NETWORK COMMAND CENTER", font=ctk.CTkFont(size=20, weight="bold"), text_color="#00FFD2").pack(anchor="w")
        ctk.CTkLabel(header_frame, text="PORT SOCKET INTERCEPTIONS AND KERNEL ADAPTER CONTROLS", font=ctk.CTkFont(size=10), text_color="#606065").pack(anchor="w")

        self.net_textbox = ctk.CTkTextbox(self.tab_network, height=350, fg_color="#0A0A0C", text_color="#00FFD2", font=ctk.CTkFont(family="Consolas", size=12))
        self.net_textbox.pack(fill="x", padx=20, pady=10)

        btn_frame = ctk.CTkFrame(self.tab_network, fg_color="transparent")
        btn_frame.pack(fill="x", padx=20, pady=10)

        ctk.CTkButton(btn_frame, text="MAP ACTIVE PORTS & TUNNELS", fg_color="#222228", hover_color="#33333B", command=self.map_network_sockets).pack(side="left", fill="x", expand=True, padx=(0, 5))
        ctk.CTkButton(btn_frame, text="FLUSH DNS & IP CORESYSTEM", fg_color="#0055FF", hover_color="#0033CC", command=self.flush_network_stack).pack(side="left", fill="x", expand=True, padx=(5, 0))

        host_frame = ctk.CTkFrame(self.tab_network, corner_radius=8, fg_color="#1A1A20", border_width=1, border_color="#222228")
        host_frame.pack(fill="x", padx=20, pady=15)
        ctk.CTkLabel(host_frame, text="■ DIRECT HOST ROUTING INTERFACE", font=ctk.CTkFont(size=12, weight="bold"), text_color="#A0A0A5").pack(anchor="w", padx=15, pady=(10, 2))
        
        self.btn_hosts = ctk.CTkButton(host_frame, text="OPEN SYSTEM HOSTS MATRIX FOR EDITING", fg_color="#00FFD2", text_color="#0A0A0C", hover_color="#00CCAA", height=40, font=ctk.CTkFont(weight="bold"), command=self.open_hosts_file)
        self.btn_hosts.pack(fill="x", padx=15, pady=15)

    def map_network_sockets(self):
        self.net_textbox.configure(state="normal")
        self.net_textbox.delete("1.0", "end")
        self.net_textbox.insert("end", f"{'PROTO':<6}{'LOCAL ADDRESS':<24}{'STATUS':<15}{'PROCESS (PID)':<20}\n")
        self.net_textbox.insert("end", "-"*65 + "\n")
        
        for conn in psutil.net_connections(kind='inet'):
            try:
                laddr = f"{conn.laddr.ip}:{conn.laddr.port}"
                status = conn.status
                pid_str = f"{psutil.Process(conn.pid).name()} ({conn.pid})" if conn.pid else "SYSTEM"
                self.net_textbox.insert("end", f"{conn.type.name:<6}{laddr:<24}{status:<15}{pid_str:<20}\n")
            except: pass
        self.net_textbox.configure(state="disabled")

    def flush_network_stack(self):
        subprocess.run(["ipconfig", "/flushdns"], creationflags=subprocess.CREATE_NO_WINDOW)
        subprocess.run(["ipconfig", "/release"], creationflags=subprocess.CREATE_NO_WINDOW)
        subprocess.run(["ipconfig", "/renew"], creationflags=subprocess.CREATE_NO_WINDOW)
        ctypes.windll.user32.MessageBoxW(0, "DNS cache flushed. Network configurations re-indexed successfully.", "NETWORK COMMAND", 0x40)

    def open_hosts_file(self):
        subprocess.Popen(["notepad.exe", r"C:\Windows\System32\drivers\etc\hosts"])

    # ==========================================
    # TAB 6: #3 & #4 SYSTEM OPTIMIZATION (MERGED)
    # ==========================================
    def build_coresystem_tab(self):
        header_frame = ctk.CTkFrame(self.tab_coresystem, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=(10, 5))
        ctk.CTkLabel(header_frame, text="SYSTEM OPTIMIZATION MATRIX", font=ctk.CTkFont(size=20, weight="bold"), text_color="#FFE600").pack(anchor="w")
        ctk.CTkLabel(header_frame, text="WINDOWS TELEMETRY ERADICATION AND SYSTEM GLITCH RECOVERY", font=ctk.CTkFont(size=10), text_color="#606065").pack(anchor="w")

        # Section PREMIUM: Fresh Start
        fresh_start_frame = ctk.CTkFrame(self.tab_coresystem, corner_radius=8, fg_color="#0D1F40", border_width=2, border_color="#0055FF")
        fresh_start_frame.pack(fill="x", padx=20, pady=15)
        ctk.CTkLabel(fresh_start_frame, text="⚡ FRESH START - COMPLETE SYSTEM OVERHAUL", font=ctk.CTkFont(size=12, weight="bold"), text_color="#00D2FF").pack(anchor="w", padx=15, pady=(10, 2))
        ctk.CTkLabel(fresh_start_frame, text="Execute full cleanup, security scan, memory optimization, DNS flush, and bloatware removal in one comprehensive operation.", font=ctk.CTkFont(size=11), text_color="#A0D2FF").pack(anchor="w", padx=15, pady=2)
        
        self.btn_fresh_start = ctk.CTkButton(fresh_start_frame, text="INITIATE FRESH START PROTOCOL", fg_color="#0055FF", text_color="#FFFFFF", hover_color="#0033CC", height=50, font=ctk.CTkFont(size=14, weight="bold"), command=self.start_fresh_start_thread)
        self.btn_fresh_start.pack(fill="x", padx=15, pady=15)

        # Section A: Debloat & Telemetry
        debloat_frame = ctk.CTkFrame(self.tab_coresystem, corner_radius=8, fg_color="#1A1A20", border_width=1, border_color="#222228")
        debloat_frame.pack(fill="x", padx=20, pady=15)
        ctk.CTkLabel(debloat_frame, text="■ DEBLOAT & MICROSOFT TELEMETRY KILLSWITCH", font=ctk.CTkFont(size=12, weight="bold"), text_color="#FFE600").pack(anchor="w", padx=15, pady=(10, 2))
        ctk.CTkLabel(debloat_frame, text="Nukes background OS analytics engines and unloads provisioning bloatware tasks.", font=ctk.CTkFont(size=11), text_color="#606065").pack(anchor="w", padx=15, pady=2)
        
        self.btn_kill_telemetry = ctk.CTkButton(debloat_frame, text="EXECUTE TELEMETRY & BLOAT ERADICATION", fg_color="#FFE600", text_color="#0A0A0C", hover_color="#CCB200", height=40, font=ctk.CTkFont(weight="bold"), command=self.nuke_telemetry)
        self.btn_kill_telemetry.pack(fill="x", padx=15, pady=15)

        # Section B: Recovery Panels
        recovery_frame = ctk.CTkFrame(self.tab_coresystem, corner_radius=8, fg_color="#1A1A20", border_width=1, border_color="#222228")
        recovery_frame.pack(fill="x", padx=20, pady=15)
        ctk.CTkLabel(recovery_frame, text="■ EMERGENCY RECOVERY ENGINE", font=ctk.CTkFont(size=12, weight="bold"), text_color="#FF3333").pack(anchor="w", padx=15, pady=(10, 2))
        ctk.CTkLabel(recovery_frame, text="Instantly bypasses system locks or display driver corruption hard-freezes.", font=ctk.CTkFont(size=11), text_color="#606065").pack(anchor="w", padx=15, pady=2)

        self.btn_reset_explorer = ctk.CTkButton(recovery_frame, text="FORCE RESET WINDOWS EXPLORER SHELL", fg_color="#222228", hover_color="#33333B", height=40, command=self.restart_explorer)
        self.btn_reset_explorer.pack(fill="x", padx=15, pady=(15, 10))

        self.btn_reset_gpu = ctk.CTkButton(recovery_frame, text="REBOOT SUBSYSTEM DESKTOP WINDOW MANAGER (GPU RESET)", fg_color="#990000", hover_color="#BB0000", height=40, command=self.restart_dwm)
        self.btn_reset_gpu.pack(fill="x", padx=15, pady=(0, 15))

    def start_fresh_start_thread(self):
        self.btn_fresh_start.configure(state="disabled", text="FRESH START IN PROGRESS...")
        threading.Thread(target=self.run_fresh_start_logic, daemon=True).start()

    def run_fresh_start_logic(self):
        """Execute complete system overhaul: cleanup, security scan, memory optimization, DNS flush, and bloatware removal"""
        ctypes.windll.user32.MessageBoxW(0, "Fresh Start Protocol Initiated.\n\nPlease ensure no important applications are running.\nThis may take 5-15 minutes.", "FRESH START PROTOCOL", 0x40)
        
        # PHASE 1: Cleanup
        self.log_cleaner("\n=== FRESH START PHASE 1: SYSTEM CLEANUP ===\n")
        self.run_cleanup_logic()
        
        # PHASE 2: Security Scan
        self.log_security("\n=== FRESH START PHASE 2: SECURITY SCAN ===\n")
        self.run_security_logic()
        
        # PHASE 3: Memory Optimization - Kill Memory Hogs
        self.log_cleaner("\n=== FRESH START PHASE 3: MEMORY OPTIMIZATION ===\n")
        self.log_cleaner("[*] Scanning for memory-intensive processes...")
        time.sleep(1)
        proc_mem_list = []
        try:
            for p in psutil.process_iter(['pid', 'name', 'memory_percent']):
                try:
                    mem_percent = p.info['memory_percent'] or 0
                    if mem_percent > 2.0:  # Kill processes using > 2% RAM
                        proc_mem_list.append({'pid': p.info['pid'], 'name': p.info['name'], 'mem': mem_percent})
                except: continue
        except: pass
        
        proc_mem_list.sort(key=lambda x: x['mem'], reverse=True)
        
        killed_count = 0
        for proc in proc_mem_list[:10]:  # Kill top 10 memory hogs
            try:
                psutil.Process(proc['pid']).kill()
                self.log_cleaner(f"[✓] Terminated {proc['name']} ({proc['mem']:.2f}% RAM)")
                killed_count += 1
            except: pass
            time.sleep(0.3)
        
        self.log_cleaner(f"[SUCCESS] Closed {killed_count} memory hog processes.\n")
        
        # PHASE 4: DNS & Network Flush
        self.log_cleaner("\n=== FRESH START PHASE 4: NETWORK OPTIMIZATION ===\n")
        self.log_cleaner("[*] Flushing DNS cache...")
        try:
            subprocess.run(["ipconfig", "/flushdns"], creationflags=subprocess.CREATE_NO_WINDOW)
            self.log_cleaner("[✓] DNS cache flushed successfully")
        except: pass
        
        self.log_cleaner("[*] Releasing and renewing IP configuration...")
        try:
            subprocess.run(["ipconfig", "/release"], creationflags=subprocess.CREATE_NO_WINDOW)
            subprocess.run(["ipconfig", "/renew"], creationflags=subprocess.CREATE_NO_WINDOW)
            self.log_cleaner("[✓] IP configuration renewed")
        except: pass
        
        # PHASE 5: Bloatware & Telemetry Removal
        self.log_cleaner("\n=== FRESH START PHASE 5: TELEMETRY & BLOATWARE ERADICATION ===\n")
        self.log_cleaner("[*] Disabling Windows telemetry services...")
        reg_cmds = [
            r'reg add "HKLM\SOFTWARE\Policies\Microsoft\Windows\DataCollection" /v AllowTelemetry /t REG_DWORD /d 0 /f',
            r'reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\DataCollection" /v AllowTelemetry /t REG_DWORD /d 0 /f',
            r'sc config DiagTrack start= disabled',
            r'sc stop DiagTrack'
        ]
        for cmd in reg_cmds:
            try:
                subprocess.run(cmd, shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
            except: pass
        self.log_cleaner("[✓] Telemetry services disabled\n")
        
        self.log_cleaner("="*50)
        self.log_cleaner("[SUCCESS] FRESH START PROTOCOL COMPLETE!")
        self.log_cleaner("="*50)
        self.log_cleaner("\nYour system has been thoroughly optimized.")
        self.log_cleaner("Consider restarting your computer for optimal results.\n")
        
        self.btn_fresh_start.configure(state="normal", text="INITIATE FRESH START PROTOCOL")
        ctypes.windll.user32.MessageBoxW(0, "Fresh Start Complete!\n\nSystem has been cleaned, optimized, and secured.\n\nA restart is recommended.", "FRESH START COMPLETE", 0x40)

    def nuke_telemetry(self):
        # Force low level registry killswitches
        reg_cmds = [
            r'reg add "HKLM\SOFTWARE\Policies\Microsoft\Windows\DataCollection" /v AllowTelemetry /t REG_DWORD /d 0 /f',
            r'reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\DataCollection" /v AllowTelemetry /t REG_DWORD /d 0 /f',
            r'sc config DiagTrack start= disabled',
            r'sc stop DiagTrack'
        ]
        for cmd in reg_cmds:
            subprocess.run(cmd, shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
        ctypes.windll.user32.MessageBoxW(0, "Telemetry hooks decoupled. Background transmission modules halted.", "GOD MODE PROTCOLS", 0x40)

    def nuke_selected_process(self):
        selection = self.proc_selector.get()
        if not selection: return
        
        # Extract PID from string "PID - Name"
        pid = int(selection.split(" - ")[0])
        name = selection.split(" - ")[1]
        
        try:
            p = psutil.Process(pid)
            p.kill()
            ctypes.windll.user32.MessageBoxW(0, f"Terminated {name} (PID: {pid})", "GOD MODE", 0x40)
            self.update_process_overlord()
        except Exception as e:
            ctypes.windll.user32.MessageBoxW(0, f"Access Denied: {e}", "CRITICAL ERROR", 0x10)

    def restart_explorer(self):
        subprocess.run(["taskkill", "/f", "/im", "explorer.exe"], creationflags=subprocess.CREATE_NO_WINDOW)
        subprocess.Popen(["explorer.exe"])

    def restart_dwm(self):
        # Killing DWM forcefully flushes the graphics context/composition stack immediately (similar to Win+Ctrl+Shift+B)
        subprocess.run(["taskkill", "/f", "/im", "dwm.exe"], creationflags=subprocess.CREATE_NO_WINDOW)

    # ==========================================
    # TAB 7: SYSTEM RESTORE POINT CREATOR
    # ==========================================
    def build_restore_tab(self):
        header_frame = ctk.CTkFrame(self.tab_restore, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=(10, 5))
        ctk.CTkLabel(header_frame, text="SYSTEM RESTORE POINT MANAGER", font=ctk.CTkFont(size=20, weight="bold"), text_color="#00FF87").pack(anchor="w")
        ctk.CTkLabel(header_frame, text="CREATE AND MANAGE SYSTEM SNAPSHOTS FOR RECOVERY", font=ctk.CTkFont(size=10), text_color="#606065").pack(anchor="w")
        
        create_frame = ctk.CTkFrame(self.tab_restore, corner_radius=8, fg_color="#1A1A20", border_width=1, border_color="#222228")
        create_frame.pack(fill="x", padx=20, pady=15)
        ctk.CTkLabel(create_frame, text="■ CREATE NEW RESTORE POINT", font=ctk.CTkFont(size=12, weight="bold"), text_color="#00FF87").pack(anchor="w", padx=15, pady=(10, 2))
        ctk.CTkLabel(create_frame, text="Snapshot your system state for emergency rollback if something breaks.", font=ctk.CTkFont(size=11), text_color="#606065").pack(anchor="w", padx=15, pady=2)
        
        self.restore_name_entry = ctk.CTkEntry(create_frame, placeholder_text="Custom restore point name (optional)", fg_color="#0A0A0C", border_color="#222228")
        self.restore_name_entry.pack(fill="x", padx=15, pady=10)
        
        self.btn_create_restore = ctk.CTkButton(create_frame, text="CREATE RESTORE POINT NOW", fg_color="#00FF87", text_color="#0A0A0C", hover_color="#00CC66", height=40, font=ctk.CTkFont(weight="bold"), command=self.create_restore_point)
        self.btn_create_restore.pack(fill="x", padx=15, pady=15)
        
        list_frame = ctk.CTkFrame(self.tab_restore, corner_radius=8, fg_color="#1A1A20", border_width=1, border_color="#222228")
        list_frame.pack(fill="both", expand=True, padx=20, pady=15)
        ctk.CTkLabel(list_frame, text="■ EXISTING RESTORE POINTS", font=ctk.CTkFont(size=12, weight="bold"), text_color="#00FFD2").pack(anchor="w", padx=15, pady=(10, 2))
        
        self.restore_textbox = ctk.CTkTextbox(list_frame, fg_color="#0A0A0C", text_color="#00FFD2", font=ctk.CTkFont(family="Consolas", size=10))
        self.restore_textbox.pack(fill="both", expand=True, padx=15, pady=15)
        self.restore_textbox.insert("0.0", "Loading restore points...\n")
        self.restore_textbox.configure(state="disabled")
        
        btn_frame = ctk.CTkFrame(self.tab_restore, fg_color="transparent")
        btn_frame.pack(fill="x", padx=20, pady=10)
        ctk.CTkButton(btn_frame, text="REFRESH LIST", fg_color="#222228", command=self.refresh_restore_list).pack(side="left", fill="x", expand=True, padx=(0, 5))

    def create_restore_point(self):
        self.btn_create_restore.configure(state="disabled", text="CREATING RESTORE POINT...")
        threading.Thread(target=self.run_create_restore, daemon=True).start()

    def run_create_restore(self):
        custom_name = self.restore_name_entry.get() or "Manual Checkpoint"
        try:
            cmd = f'powershell -Command "Checkpoint-Computer -Description \'{custom_name}\' -RestorePointType \'MODIFY_SETTINGS\'"'
            subprocess.run(cmd, shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
            ctypes.windll.user32.MessageBoxW(0, f"Restore point '{custom_name}' created successfully!", "SYSTEM SNAPSHOT CREATED", 0x40)
            self.refresh_restore_list()
        except Exception as e:
            ctypes.windll.user32.MessageBoxW(0, f"Error: {e}", "RESTORE POINT FAILED", 0x10)
        self.btn_create_restore.configure(state="normal", text="CREATE RESTORE POINT NOW")

    def refresh_restore_list(self):
        threading.Thread(target=self.load_restore_points, daemon=True).start()

    def load_restore_points(self):
        self.restore_textbox.configure(state="normal")
        self.restore_textbox.delete("1.0", "end")
        self.restore_textbox.insert("end", "Scanning restore points...\n\n")
        
        try:
            cmd = 'powershell -Command "Get-ComputerRestorePoint | Select-Object -First 10 | Format-Table -AutoSize CreationTime,Description,RestorePointType"'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
            output = result.stdout if result.stdout else "No restore points found."
            self.restore_textbox.delete("1.0", "end")
            self.restore_textbox.insert("end", output)
        except Exception as e:
            self.restore_textbox.insert("end", f"Error loading restore points: {e}")
        
        self.restore_textbox.configure(state="disabled")

    # ==========================================
    # TAB 8: PERFORMANCE BENCHMARK
    # ==========================================
    def build_benchmark_tab(self):
        header_frame = ctk.CTkFrame(self.tab_benchmark, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=(10, 5))
        ctk.CTkLabel(header_frame, text="PERFORMANCE BENCHMARK SUITE", font=ctk.CTkFont(size=20, weight="bold"), text_color="#FFD700").pack(anchor="w")
        ctk.CTkLabel(header_frame, text="MEASURE CPU, GPU, AND DISK PERFORMANCE", font=ctk.CTkFont(size=10), text_color="#606065").pack(anchor="w")
        
        btn_frame = ctk.CTkFrame(self.tab_benchmark, fg_color="transparent")
        btn_frame.pack(fill="x", padx=20, pady=15)
        ctk.CTkButton(btn_frame, text="RUN FULL BENCHMARK", fg_color="#FFD700", text_color="#0A0A0C", hover_color="#CCAA00", height=45, font=ctk.CTkFont(size=12, weight="bold"), command=self.start_benchmark_thread).pack(fill="x")
        
        self.benchmark_textbox = ctk.CTkTextbox(self.tab_benchmark, fg_color="#0A0A0C", text_color="#FFD700", font=ctk.CTkFont(family="Consolas", size=11))
        self.benchmark_textbox.pack(fill="both", expand=True, padx=20, pady=20)
        self.benchmark_textbox.insert("0.0", "═" * 50 + "\n  PERFORMANCE BENCHMARK SUITE\n" + "═" * 50 + "\n\nReady to measure your system...\n")
        self.benchmark_textbox.configure(state="disabled")

    def start_benchmark_thread(self):
        threading.Thread(target=self.run_benchmark, daemon=True).start()

    def run_benchmark(self):
        self.benchmark_textbox.configure(state="normal")
        self.benchmark_textbox.delete("1.0", "end")
        self.benchmark_textbox.insert("end", "═" * 50 + "\n  STARTING BENCHMARK SEQUENCE\n" + "═" * 50 + "\n\n")
        
        # CPU Benchmark
        self.benchmark_textbox.insert("end", "[1/3] CPU COMPUTATION TEST...\n")
        self.benchmark_textbox.see("end")
        self.benchmark_textbox.update()
        
        start_time = time.time()
        result = 0
        for i in range(50000000):
            result += i ** 2
        cpu_time = time.time() - start_time
        self.benchmark_textbox.insert("end", f"✓ CPU computed 50M operations in {cpu_time:.2f}s\n")
        self.benchmark_textbox.insert("end", f"  Score: {50000000/cpu_time:.0f} ops/sec\n\n")
        self.benchmark_textbox.see("end")
        self.benchmark_textbox.update()
        
        # Disk Benchmark
        self.benchmark_textbox.insert("end", "[2/3] DISK I/O TEST...\n")
        self.benchmark_textbox.see("end")
        self.benchmark_textbox.update()
        
        try:
            test_file = os.path.expanduser("~\\benchmark_test.tmp")
            test_data = b"X" * 1024 * 1024  # 1MB
            
            # Write speed
            start_time = time.time()
            with open(test_file, 'wb') as f:
                for _ in range(10):
                    f.write(test_data)
            write_time = time.time() - start_time
            write_speed = (10 * 1024) / write_time  # MB/s
            
            # Read speed
            start_time = time.time()
            with open(test_file, 'rb') as f:
                while f.read(1024 * 1024):
                    pass
            read_time = time.time() - start_time
            read_speed = (10 * 1024) / read_time  # MB/s
            
            os.remove(test_file)
            
            self.benchmark_textbox.insert("end", f"✓ Disk Write: {write_speed:.1f} MB/s\n")
            self.benchmark_textbox.insert("end", f"✓ Disk Read: {read_speed:.1f} MB/s\n\n")
        except Exception as e:
            self.benchmark_textbox.insert("end", f"✗ Disk test failed: {e}\n\n")
        
        # RAM Info
        self.benchmark_textbox.insert("end", "[3/3] MEMORY ANALYSIS...\n")
        ram_total = psutil.virtual_memory().total / (1024**3)
        ram_used = psutil.virtual_memory().used / (1024**3)
        ram_available = psutil.virtual_memory().available / (1024**3)
        self.benchmark_textbox.insert("end", f"✓ Total RAM: {ram_total:.1f} GB\n")
        self.benchmark_textbox.insert("end", f"✓ Used RAM: {ram_used:.1f} GB\n")
        self.benchmark_textbox.insert("end", f"✓ Available: {ram_available:.1f} GB\n\n")
        
        self.benchmark_textbox.insert("end", "═" * 50 + "\n")
        self.benchmark_textbox.insert("end", "BENCHMARK COMPLETE ✓\n")
        self.benchmark_textbox.insert("end", "═" * 50 + "\n")
        self.benchmark_textbox.see("end")
        self.benchmark_textbox.configure(state="disabled")

    # ==========================================
    # TAB 9: BROWSER CACHE NUKE
    # ==========================================
    def build_browser_tab(self):
        header_frame = ctk.CTkFrame(self.tab_browser, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=(10, 5))
        ctk.CTkLabel(header_frame, text="BROWSER CACHE & DATA ANNIHILATOR", font=ctk.CTkFont(size=20, weight="bold"), text_color="#FF6B9D").pack(anchor="w")
        ctk.CTkLabel(header_frame, text="OBLITERATE BROWSER CACHE, COOKIES, AND HISTORY", font=ctk.CTkFont(size=10), text_color="#606065").pack(anchor="w")
        
        # Browser selection
        self.browser_var = ctk.CTkOptionMenu(self.tab_browser, values=["All Browsers", "Google Chrome", "Microsoft Edge", "Mozilla Firefox"], fg_color="#1A1A20")
        self.browser_var.pack(fill="x", padx=20, pady=10)
        self.browser_var.set("All Browsers")
        
        # Cache info frame
        info_frame = ctk.CTkFrame(self.tab_browser, corner_radius=8, fg_color="#1A1A20", border_width=1, border_color="#222228")
        info_frame.pack(fill="x", padx=20, pady=10)
        
        self.cache_info_label = ctk.CTkLabel(info_frame, text="Analyzing browser cache sizes...", font=ctk.CTkFont(size=11), text_color="#A0A0A5", wraplength=500, justify="left")
        self.cache_info_label.pack(anchor="w", padx=15, pady=15)
        
        # Action buttons
        btn_frame = ctk.CTkFrame(self.tab_browser, fg_color="transparent")
        btn_frame.pack(fill="x", padx=20, pady=15)
        ctk.CTkButton(btn_frame, text="ANALYZE CACHE", fg_color="#222228", command=self.analyze_browser_cache).pack(side="left", fill="x", expand=True, padx=(0, 5))
        ctk.CTkButton(btn_frame, text="NUKE BROWSER DATA", fg_color="#FF6B9D", hover_color="#DD4477", height=40, font=ctk.CTkFont(weight="bold"), command=self.nuke_browser_cache).pack(side="left", fill="x", expand=True, padx=(5, 0))
        
        self.browser_console = ctk.CTkTextbox(self.tab_browser, fg_color="#0A0A0C", text_color="#FF6B9D", font=ctk.CTkFont(family="Consolas", size=10))
        self.browser_console.pack(fill="both", expand=True, padx=20, pady=10)
        self.browser_console.insert("0.0", "Browser cache analysis ready...\n")
        self.browser_console.configure(state="disabled")

    def analyze_browser_cache(self):
        threading.Thread(target=self.get_browser_cache_size, daemon=True).start()

    def get_browser_cache_size(self):
        browser_selected = self.browser_var.get()
        cache_sizes = {}
        
        # Chrome
        chrome_path = os.path.expanduser(r"~\AppData\Local\Google\Chrome\User Data\Default\Cache")
        if os.path.exists(chrome_path):
            cache_sizes["Chrome"] = self.get_dir_size(chrome_path) / (1024*1024)
        
        # Edge
        edge_path = os.path.expanduser(r"~\AppData\Local\Microsoft\Edge\User Data\Default\Cache")
        if os.path.exists(edge_path):
            cache_sizes["Edge"] = self.get_dir_size(edge_path) / (1024*1024)
        
        # Firefox
        firefox_path = os.path.expanduser(r"~\AppData\Local\Mozilla\Firefox")
        if os.path.exists(firefox_path):
            for item in os.listdir(firefox_path):
                profile_cache = os.path.join(firefox_path, item, "cache2")
                if os.path.exists(profile_cache):
                    cache_sizes["Firefox"] = self.get_dir_size(profile_cache) / (1024*1024)
                    break
        
        info_text = "Cache Sizes Found:\n\n"
        total_size = 0
        for browser, size in cache_sizes.items():
            info_text += f"• {browser}: {size:.1f} MB\n"
            total_size += size
        info_text += f"\nTotal: {total_size:.1f} MB"
        
        self.cache_info_label.configure(text=info_text)

    def nuke_browser_cache(self):
        threading.Thread(target=self.run_browser_nuke, daemon=True).start()

    def run_browser_nuke(self):
        browser_selected = self.browser_var.get()
        self.browser_console.configure(state="normal")
        self.browser_console.delete("1.0", "end")
        self.browser_console.insert("end", ">>> INITIATING BROWSER DATA ANNIHILATION <<<\n\n")
        
        paths_to_nuke = []
        
        if browser_selected in ["All Browsers", "Google Chrome"]:
            paths_to_nuke.append((os.path.expanduser(r"~\AppData\Local\Google\Chrome\User Data\Default\Cache"), "Chrome"))
            paths_to_nuke.append((os.path.expanduser(r"~\AppData\Local\Google\Chrome\User Data\Default\Cache2"), "Chrome"))
        
        if browser_selected in ["All Browsers", "Microsoft Edge"]:
            paths_to_nuke.append((os.path.expanduser(r"~\AppData\Local\Microsoft\Edge\User Data\Default\Cache"), "Edge"))
        
        if browser_selected in ["All Browsers", "Mozilla Firefox"]:
            firefox_path = os.path.expanduser(r"~\AppData\Local\Mozilla\Firefox")
            if os.path.exists(firefox_path):
                for item in os.listdir(firefox_path):
                    cache2 = os.path.join(firefox_path, item, "cache2")
                    if os.path.exists(cache2):
                        paths_to_nuke.append((cache2, "Firefox"))
        
        for path, browser_name in paths_to_nuke:
            if os.path.exists(path):
                try:
                    shutil.rmtree(path)
                    self.browser_console.insert("end", f"✓ {browser_name} cache eliminated\n")
                except Exception as e:
                    self.browser_console.insert("end", f"✗ {browser_name} error: {e}\n")
            self.browser_console.see("end")
            self.browser_console.update()
            time.sleep(0.5)
        
        self.browser_console.insert("end", "\n[SUCCESS] Browser data purged!\n")
        self.browser_console.see("end")
        self.browser_console.configure(state="disabled")

    # ==========================================
    # TAB 10: DUPLICATE FILE FINDER
    # ==========================================
    def build_duplicates_tab(self):
        header_frame = ctk.CTkFrame(self.tab_duplicates, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=(10, 5))
        ctk.CTkLabel(header_frame, text="DUPLICATE FILE TERMINATOR", font=ctk.CTkFont(size=20, weight="bold"), text_color="#00FF87").pack(anchor="w")
        ctk.CTkLabel(header_frame, text="FIND AND ELIMINATE DUPLICATE FILES TO RECLAIM STORAGE", font=ctk.CTkFont(size=10), text_color="#606065").pack(anchor="w")
        
        # Scan options
        option_frame = ctk.CTkFrame(self.tab_duplicates, fg_color="transparent")
        option_frame.pack(fill="x", padx=20, pady=10)
        ctk.CTkLabel(option_frame, text="Scan Location:", font=ctk.CTkFont(size=11, weight="bold"), text_color="#00FF87").pack(side="left", padx=(0, 10))
        self.dup_location_var = ctk.CTkOptionMenu(self.tab_duplicates, values=["User Folder", "Downloads", "Documents", "Desktop", "Custom"], fg_color="#1A1A20")
        self.dup_location_var.pack(fill="x", padx=20, pady=(0, 10))
        self.dup_location_var.set("Downloads")
        
        btn_frame = ctk.CTkFrame(self.tab_duplicates, fg_color="transparent")
        btn_frame.pack(fill="x", padx=20, pady=10)
        ctk.CTkButton(btn_frame, text="SCAN FOR DUPLICATES", fg_color="#00FF87", text_color="#0A0A0C", hover_color="#00CC66", height=40, font=ctk.CTkFont(weight="bold"), command=self.start_duplicate_scan).pack(fill="x")
        
        self.duplicate_console = ctk.CTkTextbox(self.tab_duplicates, fg_color="#0A0A0C", text_color="#00FF87", font=ctk.CTkFont(family="Consolas", size=10))
        self.duplicate_console.pack(fill="both", expand=True, padx=20, pady=20)
        self.duplicate_console.insert("0.0", "Ready to scan for duplicate files...\n")
        self.duplicate_console.configure(state="disabled")

    def start_duplicate_scan(self):
        threading.Thread(target=self.scan_duplicates, daemon=True).start()

    def scan_duplicates(self):
        location = self.dup_location_var.get()
        if location == "User Folder":
            scan_path = os.path.expanduser("~")
        elif location == "Downloads":
            scan_path = os.path.expanduser("~/Downloads")
        elif location == "Documents":
            scan_path = os.path.expanduser("~/Documents")
        elif location == "Desktop":
            scan_path = os.path.expanduser("~/Desktop")
        else:
            scan_path = os.path.expanduser("~")
        
        self.duplicate_console.configure(state="normal")
        self.duplicate_console.delete("1.0", "end")
        self.duplicate_console.insert("end", f">>> SCANNING {scan_path.upper()} <<<\n\n")
        self.duplicate_console.insert("end", "Building file index...\n")
        self.duplicate_console.see("end")
        self.duplicate_console.update()
        
        import hashlib
        file_hashes = {}
        duplicates = []
        scanned_count = 0
        
        try:
            for root, dirs, files in os.walk(scan_path):
                # Skip system folders
                dirs[:] = [d for d in dirs if d not in ['.git', '$Recycle.Bin', 'AppData']]
                
                for file in files:
                    scanned_count += 1
                    if scanned_count % 100 == 0:
                        self.duplicate_console.insert("end", f"Scanned {scanned_count} files...\n")
                        self.duplicate_console.see("end")
                        self.duplicate_console.update()
                    
                    filepath = os.path.join(root, file)
                    try:
                        with open(filepath, 'rb') as f:
                            file_hash = hashlib.md5(f.read()).hexdigest()
                        
                        if file_hash in file_hashes:
                            duplicates.append((filepath, file_hashes[file_hash], os.path.getsize(filepath)))
                        else:
                            file_hashes[file_hash] = filepath
                    except: pass
        except Exception as e:
            self.duplicate_console.insert("end", f"\n[!] Scan error: {e}\n")
        
        self.duplicate_console.insert("end", f"\n[*] Scan complete. Found {len(duplicates)} duplicates.\n\n")
        
        if duplicates:
            total_space = sum(d[2] for d in duplicates) / (1024*1024)
            self.duplicate_console.insert("end", f"TOTAL WASTED SPACE: {total_space:.1f} MB\n\n")
            
            for dup_file, original, size in duplicates[:50]:  # Show first 50
                size_mb = size / (1024*1024)
                self.duplicate_console.insert("end", f"[DUP] {dup_file}\n     Size: {size_mb:.2f} MB\n")
            
            if len(duplicates) > 50:
                self.duplicate_console.insert("end", f"\n... and {len(duplicates)-50} more duplicates\n")
            
            self.duplicate_console.insert("end", "\n[!] Manual deletion recommended for safety.\n")
        else:
            self.duplicate_console.insert("end", "No duplicates found!\n")
        
        self.duplicate_console.see("end")
        self.duplicate_console.configure(state="disabled")

    # ==========================================
    # TAB 11: POWER PROFILES
    # ==========================================
    def build_power_tab(self):
        header_frame = ctk.CTkFrame(self.tab_power, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=(10, 5))
        ctk.CTkLabel(header_frame, text="POWER PROFILE SELECTOR", font=ctk.CTkFont(size=20, weight="bold"), text_color="#FFB6C1").pack(anchor="w")
        ctk.CTkLabel(header_frame, text="SWITCH BETWEEN POWER MODES FOR PERFORMANCE OR BATTERY LIFE", font=ctk.CTkFont(size=10), text_color="#606065").pack(anchor="w")
        
        # Quick action buttons
        quick_frame = ctk.CTkFrame(self.tab_power, fg_color="transparent")
        quick_frame.pack(fill="x", padx=20, pady=15)
        ctk.CTkButton(quick_frame, text="⚡ ULTIMATE PERFORMANCE", fg_color="#FFD700", text_color="#0A0A0C", hover_color="#CCAA00", height=50, font=ctk.CTkFont(size=12, weight="bold"), command=self.set_ultimate_performance).pack(fill="x", padx=(0, 5), side="left", expand=True)
        ctk.CTkButton(quick_frame, text="🔋 BALANCED", fg_color="#00D2FF", hover_color="#0099CC", height=50, font=ctk.CTkFont(size=12, weight="bold"), command=self.set_balanced_mode).pack(fill="x", padx=(5, 5), side="left", expand=True)
        ctk.CTkButton(quick_frame, text="💤 POWER SAVER", fg_color="#00FF87", text_color="#0A0A0C", hover_color="#00CC66", height=50, font=ctk.CTkFont(size=12, weight="bold"), command=self.set_power_saver).pack(fill="x", padx=(5, 0), side="left", expand=True)
        
        # Power plans list
        list_frame = ctk.CTkFrame(self.tab_power, corner_radius=8, fg_color="#1A1A20", border_width=1, border_color="#222228")
        list_frame.pack(fill="both", expand=True, padx=20, pady=15)
        ctk.CTkLabel(list_frame, text="■ AVAILABLE POWER PLANS", font=ctk.CTkFont(size=12, weight="bold"), text_color="#FFB6C1").pack(anchor="w", padx=15, pady=(10, 2))
        
        self.power_console = ctk.CTkTextbox(list_frame, fg_color="#0A0A0C", text_color="#FFB6C1", font=ctk.CTkFont(family="Consolas", size=10))
        self.power_console.pack(fill="both", expand=True, padx=15, pady=15)
        
        self.load_power_plans()

    def load_power_plans(self):
        self.power_console.configure(state="normal")
        self.power_console.delete("1.0", "end")
        
        try:
            result = subprocess.run('powercfg /list', shell=True, capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
            output = result.stdout
            self.power_console.insert("end", output)
        except Exception as e:
            self.power_console.insert("end", f"Error loading power plans: {e}\n")
        
        self.power_console.configure(state="disabled")

    def set_ultimate_performance(self):
        try:
            # Set High Performance plan
            subprocess.run('powercfg /setactive 8c5e7fda-e8bf-45a6-a6cc-4b3c6361d204', shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
            # Disable sleep timers
            subprocess.run('powercfg /change monitor-timeout-ac 0', shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
            subprocess.run('powercfg /change disk-timeout-ac 0', shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
            ctypes.windll.user32.MessageBoxW(0, "⚡ ULTIMATE PERFORMANCE MODE ACTIVATED\n\nMaximum CPU/GPU power, no sleep timers.", "POWER MODE CHANGED", 0x40)
            self.load_power_plans()
        except Exception as e:
            ctypes.windll.user32.MessageBoxW(0, f"Error: {e}", "POWER MODE FAILED", 0x10)

    def set_balanced_mode(self):
        try:
            # Set Balanced plan
            subprocess.run('powercfg /setactive 381b4222-f694-41f0-9685-ff5bb260df2e', shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
            # Normal sleep timers
            subprocess.run('powercfg /change monitor-timeout-ac 10', shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
            subprocess.run('powercfg /change disk-timeout-ac 20', shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
            ctypes.windll.user32.MessageBoxW(0, "🔋 BALANCED MODE ACTIVATED\n\nOptimal balance between performance and power.", "POWER MODE CHANGED", 0x40)
            self.load_power_plans()
        except Exception as e:
            ctypes.windll.user32.MessageBoxW(0, f"Error: {e}", "POWER MODE FAILED", 0x10)

    def set_power_saver(self):
        try:
            # Set Power Saver plan
            subprocess.run('powercfg /setactive a1841308-3541-4fab-bc81-f71556f20b4a', shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
            # Aggressive sleep timers
            subprocess.run('powercfg /change monitor-timeout-ac 5', shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
            subprocess.run('powercfg /change disk-timeout-ac 10', shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
            ctypes.windll.user32.MessageBoxW(0, "💤 POWER SAVER MODE ACTIVATED\n\nMaximum battery life, reduced performance.", "POWER MODE CHANGED", 0x40)
            self.load_power_plans()
        except Exception as e:
            ctypes.windll.user32.MessageBoxW(0, f"Error: {e}", "POWER MODE FAILED", 0x10)
    def deferred_system_init(self):
        try:
            data = {}
            data['os'] = f"{platform.system()} {platform.release()} ({platform.architecture()[0]})"
            data['cpu'] = platform.processor() or "Central Processor Core"
            
            if NVML_READY:
                try:
                    handle = pynvml.nvmlDeviceGetHandleByIndex(0)
                    gpu_name = pynvml.nvmlDeviceGetName(handle)
                    data['gpu'] = gpu_name.decode('utf-8') if isinstance(gpu_name, bytes) else gpu_name
                except: data['gpu'] = "NVIDIA Graphics Adapter"
            else:
                data['gpu'] = "Standard Display Adapter"
            
            data['ram'] = f"{round(psutil.virtual_memory().total / (1024 ** 3), 1)} GB Physical Memory"
            try: data['storage'] = f"{int(round(psutil.disk_usage('C:').total / (1024 ** 3), 0))} GB Storage Array"
            except: pass

            for key, value in data.items():
                if key in self.spec_labels: self.spec_labels[key].configure(text=value)
                    
            temp_path = os.environ.get('TEMP')
            if temp_path:
                mb = self.get_dir_size(temp_path) / (1024*1024)
                self.temp_size_lbl.configure(text=f"{mb:.1f} MB\nTemporary Files")
        except Exception: pass
        
        # Populate tables immediately on start
        self.update_process_overlord()
        self.map_network_sockets()
        self.refresh_telemetry()

    def refresh_telemetry(self):
        try:
            current_cpu = psutil.cpu_percent()
            current_ram = psutil.virtual_memory().percent
            current_disk = psutil.disk_usage('C:').percent if platform.system() == 'Windows' else 0
            
            current_gpu = 0
            gpu_watts = 0.0
            if NVML_READY:
                try:
                    handle = pynvml.nvmlDeviceGetHandleByIndex(0)
                    current_gpu = int(pynvml.nvmlDeviceGetUtilizationRates(handle).gpu)
                    gpu_watts = pynvml.nvmlDeviceGetPowerUsage(handle) / 1000.0  
                except: pass
            
            self.cpu_bar.set(current_cpu / 100)
            self.ram_bar.set(current_ram / 100)
            self.gpu_bar.set(current_gpu / 100)
            self.disk_bar.set(current_disk / 100)
            
            self.cpu_label.configure(text=f"CPU COMPUTE UTILITY: {current_cpu}%")
            self.ram_label.configure(text=f"DYNAMIC MEMORY ALLOCATION: {current_ram}%")
            self.gpu_label.configure(text=f"GPU CORE UTILIZATION: {current_gpu}%")
            self.disk_label.configure(text=f"PRIMARY DRIVE CAPACITY USED: {current_disk}%")
            
            self.clean_mem_lbl.configure(text=f"{current_ram}%\nMemory Usage")

            # Networking Speedometers
            now = time.time()
            current_net = psutil.net_io_counters()
            td = now - self.last_net_time
            if td > 0:
                self.net_down_lbl.configure(text=f"NETWORK DOWNLINK : {(current_net.bytes_recv - self.last_net_io.bytes_recv) / td / 1048576:.2f} MB/s")
                self.net_up_lbl.configure(text=f"NETWORK UPLINK   : {(current_net.bytes_sent - self.last_net_io.bytes_sent) / td / 1048576:.2f} MB/s")
            self.last_net_io = current_net
            self.last_net_time = now

            # Process Leader Tracking
            try:
                active_processes = []
                for p in psutil.process_iter(['name', 'cpu_percent']):
                    try:
                        name = p.info['name']
                        if name and name.lower() not in ['idle', 'system idle process', 'registry']:
                            active_processes.append(p.info)
                    except: pass
                if active_processes:
                    leader = max(active_processes, key=lambda x: x['cpu_percent'] or 0)
                    if leader and leader['cpu_percent'] > 1.0:
                        self.proc_hog_lbl.configure(text=f"RESOURCE LEADER  : {leader['name']} ({leader['cpu_percent']:.1f}% CPU)")
                    else:
                        self.proc_hog_lbl.configure(text="RESOURCE LEADER  : System Idle")
            except: pass

            try:
                uptime_seconds = time.time() - psutil.boot_time()
                h, m, s = int(uptime_seconds // 3600), int((uptime_seconds % 3600) // 60), int(uptime_seconds % 60)
                self.uptime_lbl.configure(text=f"SYSTEM UP-TIME   : {h}h {m}m {s}s")
            except: pass

            # Wattage Calculations
            cpu_watts = 25.0 + (current_cpu / 100.0) * 105.0
            system_overhead = 45.0
            total_watts = gpu_watts + cpu_watts + system_overhead
            
            self.gpu_watt_lbl.configure(text=f"GPU POWER DRAW: {gpu_watts:.1f} W")
            self.cpu_watt_lbl.configure(text=f"EST. CPU POWER DRAW: {cpu_watts:.1f} W")
            self.total_watt_lbl.configure(text=f"TOTAL ESTIMATED PC LOAD: {total_watts:.1f} W")

        except Exception: pass
        self.after(1000, self.refresh_telemetry)

    def on_closing(self):
        if NVML_READY:
            try: pynvml.nvmlShutdown()
            except: pass
        self.destroy()
        sys.exit(0)

def is_admin():
    try: return ctypes.windll.shell32.IsUserAnAdmin()
    except: return False

if __name__ == "__main__":
    import traceback 
    
    try:
        if not is_admin():
            print("[INFO] Elevating to System Admin...")
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join([f'"{sys.argv[0]}"'] + sys.argv[1:]), None, 1)
            sys.exit(0)
        
        app = AdvancedTelemetrySuite()
        app.mainloop()

    except Exception as e:
        print("\n" + "!"*60)
        print(" FATAL SYSTEM CRASH DETECTED ")
        print("!"*60)
        traceback.print_exc()
        print("!"*60)
        input("\nPress ENTER to close this window...")