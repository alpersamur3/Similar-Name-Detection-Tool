import os
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from datetime import datetime
import jellyfish
import subprocess
import platform

root = tk.Tk()
root.title("Similar Name Detection Tool")
root.state('zoomed')

context_menu = None
current_path = None

def init_context_menu():
    global context_menu
    if context_menu is None:
        context_menu = tk.Menu(root, tearoff=0)
        context_menu.add_command(label="Open Containing Folder", command=open_folder_from_label)
        context_menu.add_command(label="Open Item", command=open_item_from_label)
        context_menu.add_separator()
        context_menu.add_command(label="Copy Path", command=copy_path_from_label)

def open_item_from_label():
    global current_path
    if current_path and os.path.exists(current_path):
        open_item(current_path)

def open_folder_from_label():
    global current_path
    if current_path and os.path.exists(current_path):
        folder = os.path.dirname(current_path) if os.path.isfile(current_path) else current_path
        open_item(folder)

def copy_path_from_label():
    global current_path
    if current_path and os.path.exists(current_path):
        root.clipboard_clear()
        root.clipboard_append(current_path)

def open_item(path):
    try:
        if platform.system() == "Windows":
            os.startfile(path)
        elif platform.system() == "Darwin":
            subprocess.call(["open", path])
        else:
            subprocess.call(["xdg-open", path])
    except Exception:
        messagebox.showerror("Error", f"Could not open: {path}")

def get_extension(name):
    return os.path.splitext(name)[1].lower()

def format_time(timestamp):
    return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M")

def get_mtime(path):
    try:
        return format_time(os.path.getmtime(path))
    except:
        return "Unknown"

def calculate_folder_size(path):
    total = 0
    try:
        for dirpath, _, filenames in os.walk(path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                if os.path.exists(fp) and not os.path.islink(fp):
                    total += os.path.getsize(fp)
    except PermissionError:
        pass
    return total

def get_group_name(group):
    if not group:
        return "Unknown Group"
    if group[0]['is_file']:
        names = [item['name'] for item in group]
        base_name = min(names, key=len)
        ext = group[0]['ext']
        return f"{base_name} (*{ext})"
    else:
        names = [item['name'] for item in group]
        base_name = min(names, key=len)
        return f"{base_name} (folder)"

init_context_menu()

main_frame = ttk.Frame(root)
main_frame.pack(fill="both", expand=True, padx=15, pady=15)

control_panel = ttk.LabelFrame(main_frame, text="Settings", padding=10)
control_panel.pack(fill="x", pady=(0, 10))

ttk.Label(control_panel, text="Folder:").grid(row=0, column=0, sticky="w", pady=5)
folder_var = tk.StringVar()
ttk.Entry(control_panel, textvariable=folder_var, width=70).grid(row=0, column=1, padx=5, pady=5, sticky="w")
ttk.Button(control_panel, text="Browse",
           command=lambda: folder_var.set(filedialog.askdirectory(title="Select Folder") or "")).grid(row=0, column=2, pady=5)

ttk.Label(control_panel, text="Scan Mode:").grid(row=1, column=0, sticky="w", pady=5)
mode_var = tk.StringVar(value="Files only")
ttk.Combobox(control_panel, textvariable=mode_var, state="readonly", width=35,
             values=("All items (files + folders)", "Folders only", "Files only")).grid(row=1, column=1, sticky="w", padx=5, pady=5)

ttk.Label(control_panel, text="Grouping Criteria:").grid(row=2, column=0, sticky="w", pady=5)
grouping_var = tk.StringVar(value="Exact name + same extension")
ttk.Combobox(control_panel, textvariable=grouping_var, state="readonly", width=35,
             values=("Similar name only", "Similar name + same extension", "Exact name + same extension")).grid(row=2, column=1, sticky="w", padx=5, pady=5)

recursive_var = tk.BooleanVar(value=True)
ttk.Checkbutton(control_panel, text="Scan subfolders (recursive)", variable=recursive_var).grid(row=3, column=0, columnspan=3, sticky="w", pady=8)

ttk.Label(control_panel, text="Similarity threshold:").grid(row=4, column=0, sticky="w", pady=5)
name_entry = ttk.Entry(control_panel, width=10)
name_entry.insert(0, "4")
name_entry.grid(row=4, column=1, sticky="w", padx=5)

ttk.Label(control_panel, text="Minimum file size (MB):").grid(row=5, column=0, sticky="w", pady=5)
min_size_var = tk.DoubleVar(value=1.0)
ttk.Entry(control_panel, textvariable=min_size_var, width=10).grid(row=5, column=1, sticky="w", padx=5)

ext_frame = ttk.LabelFrame(control_panel, text="Popular Extension Selection", padding=5)
ext_frame.grid(row=6, column=0, columnspan=3, sticky="ew", pady=10)

image_var = tk.BooleanVar()
ttk.Checkbutton(ext_frame, text="Image (.jpg .png .gif .bmp .webp)", variable=image_var).grid(row=0, column=0, sticky="w")

video_var = tk.BooleanVar()
ttk.Checkbutton(ext_frame, text="Video (.mp4 .avi .mkv .mov .wmv)", variable=video_var).grid(row=0, column=1, sticky="w")

doc_var = tk.BooleanVar()
ttk.Checkbutton(ext_frame, text="Document (.pdf .doc .docx .txt)", variable=doc_var).grid(row=1, column=0, sticky="w")

archive_var = tk.BooleanVar()
ttk.Checkbutton(ext_frame, text="Archive (.zip .rar .7z .tar)", variable=archive_var).grid(row=1, column=1, sticky="w")

audio_var = tk.BooleanVar()
ttk.Checkbutton(ext_frame, text="Audio (.mp3 .wav .flac .ogg)", variable=audio_var).grid(row=2, column=0, sticky="w")

other_var = tk.BooleanVar()
ttk.Checkbutton(ext_frame, text="Other (.exe .dll .iso)", variable=other_var).grid(row=2, column=1, sticky="w")

ttk.Label(control_panel, text="Additional extensions (e.g. .tmp .log):").grid(row=7, column=0, sticky="w", pady=5)
extension_filter_var = tk.StringVar()
ttk.Entry(control_panel, textvariable=extension_filter_var, width=50).grid(row=7, column=1, sticky="w", padx=5, pady=5)

filter_mode_var = tk.StringVar(value="Include")
ttk.Radiobutton(control_panel, text="Include only selected", variable=filter_mode_var, value="Include").grid(row=8, column=0, sticky="w", pady=5)
ttk.Radiobutton(control_panel, text="Exclude selected", variable=filter_mode_var, value="Exclude").grid(row=8, column=1, sticky="w", pady=5)

ttk.Button(control_panel, text="Start Scan", command=lambda: root.after(100, start_scan)).grid(row=9, column=0, columnspan=3, pady=20)

status_var = tk.StringVar(value="Ready.")
status_label = ttk.Label(main_frame, textvariable=status_var, foreground="blue")
status_label.pack(fill="x", pady=(0, 10))

tree_frame = ttk.Frame(main_frame)
tree_frame.pack(fill="both", expand=True)

columns = ("Type", "Name", "Size", "Last Modified", "Full Path")
tree = ttk.Treeview(tree_frame, columns=columns, show="tree headings")
tree.heading("#0", text="Groups")
tree.heading("Type", text="Type")
tree.heading("Name", text="Name")
tree.heading("Size", text="Size")
tree.heading("Last Modified", text="Last Modified")
tree.heading("Full Path", text="Full Path")

tree.column("#0", width=450)
tree.column("Type", width=80)
tree.column("Name", width=500)
tree.column("Size", width=110)
tree.column("Last Modified", width=150)
tree.column("Full Path", width=400)

vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
hsb = ttk.Scrollbar(tree_frame, orient="horizontal", command=tree.xview)
tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

tree.grid(row=0, column=0, sticky="nsew")
vsb.grid(row=0, column=1, sticky="ns")
hsb.grid(row=1, column=0, sticky="ew")
tree_frame.grid_rowconfigure(0, weight=1)
tree_frame.grid_columnconfigure(0, weight=1)

tree.bind("<Double-1>", lambda e: open_folder_from_selection())
tree.bind("<Button-3>", lambda e: show_context_menu(e))

def open_folder_from_selection():
    selection = tree.selection()
    if not selection:
        return
    item = tree.item(selection[0])
    values = item.get("values", ())
    if len(values) >= 5 and values[4] and os.path.exists(values[4]):
        path = values[4]
        folder = os.path.dirname(path) if os.path.isfile(path) else path
        open_item(folder)

def show_context_menu(event):
    global current_path
    current_path = None
    selection = tree.selection()
    if not selection:
        return
    item = tree.item(selection[0])
    values = item.get("values", ())
    if len(values) >= 5 and values[4] and os.path.exists(values[4]):
        current_path = values[4]
        context_menu.tk_popup(event.x_root, event.y_root)

def find_similar_items(items, name_threshold, grouping_mode):
    similar_groups = []
    visited = set()
    for i, item1 in enumerate(items):
        if i in visited:
            continue
        group = [item1]
        visited.add(i)
        for j in range(i + 1, len(items)):
            if j in visited:
                continue
            item2 = items[j]
            ext_match = True
            if item1['is_file'] and item2['is_file']:
                if grouping_mode in ["Similar name + same extension", "Exact name + same extension"]:
                    ext_match = item1['ext'] == item2['ext']
            if not ext_match:
                continue
            match = False
            if grouping_mode == "Exact name + same extension":
                if item1['name'] == item2['name']:
                    match = True
            elif "Similar" in grouping_mode:
                dist = jellyfish.levenshtein_distance(item1['name'], item2['name'])
                if 0 < dist <= name_threshold:
                    match = True
            if match:
                group.append(item2)
                visited.add(j)
        if len(group) > 1:
            similar_groups.append(group)
    return similar_groups

def start_scan():
    folder = folder_var.get()
    if not folder or not os.path.isdir(folder):
        messagebox.showerror("Error", "Please select a valid folder!")
        return

    for item in tree.get_children():
        tree.delete(item)

    status_var.set("Scan starting...")
    root.update_idletasks()

    selected_mode = mode_var.get()
    recursive = recursive_var.get()
    grouping = grouping_var.get()
    min_mb = min_size_var.get()
    min_bytes = min_mb * 1024 * 1024

    include_exts = set()
    if image_var.get():
        include_exts.update(['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'])
    if video_var.get():
        include_exts.update(['.mp4', '.avi', '.mkv', '.mov', '.wmv'])
    if doc_var.get():
        include_exts.update(['.pdf', '.doc', '.docx', '.txt'])
    if archive_var.get():
        include_exts.update(['.zip', '.rar', '.7z', '.tar', '.gz'])
    if audio_var.get():
        include_exts.update(['.mp3', '.wav', '.flac', '.ogg'])
    if other_var.get():
        include_exts.update(['.exe', '.dll', '.iso'])

    ext_text = extension_filter_var.get().strip().lower()
    if ext_text:
        for ext in ext_text.split():
            ext = ext.strip()
            if ext.startswith('-'):
                include_exts.discard(ext[1:] if ext[1:].startswith('.') else '.' + ext[1:])
            else:
                include_exts.add(ext if ext.startswith('.') else '.' + ext)

    filter_mode = filter_mode_var.get()

    try:
        thresh = int(name_entry.get()) if "Similar" in grouping else 0
    except ValueError:
        messagebox.showerror("Error", "Threshold value must be numeric!")
        return

    items = []

    def process_path(current_path):
        try:
            for entry in os.listdir(current_path):
                full_path = os.path.join(current_path, entry)
                if os.path.islink(full_path):
                    continue
                is_file = os.path.isfile(full_path)
                rel_path = os.path.relpath(full_path, folder).replace("\\", "/")

                if recursive and not is_file:
                    process_path(full_path)

                if selected_mode == "Folders only" and is_file:
                    continue
                if selected_mode == "Files only" and not is_file:
                    continue

                size = os.path.getsize(full_path) if is_file else calculate_folder_size(full_path)
                mtime = get_mtime(full_path)

                if is_file:
                    ext = get_extension(entry)
                    include_match = not include_exts or ext in include_exts
                    if filter_mode == "Include" and not include_match:
                        continue
                    if filter_mode == "Exclude" and ext in include_exts:
                        continue
                    if size < min_bytes:
                        continue

                if is_file:
                    name_no_ext = os.path.splitext(entry)[0].lower()
                    items.append({
                        'name': name_no_ext,
                        'full_name': entry,
                        'display': rel_path,
                        'path': full_path,
                        'size': size,
                        'mtime': mtime,
                        'is_file': True,
                        'ext': ext
                    })
                else:
                    items.append({
                        'name': entry.lower(),
                        'display': rel_path,
                        'path': full_path,
                        'size': size,
                        'mtime': mtime,
                        'is_file': False,
                        'ext': ''
                    })

                status_var.set(f"Processing: {rel_path} | Found: {len(items)} items")
                root.update_idletasks()
        except PermissionError:
            pass

    process_path(folder)

    similar_groups = find_similar_items(items, thresh, grouping)
    similar_groups.sort(key=lambda g: sum(item['size'] for item in g), reverse=True)

    for group in similar_groups:
        group.sort(key=lambda x: x['size'], reverse=True)

    for group in similar_groups:
        group_name = get_group_name(group)
        total_size_mb = sum(item['size'] for item in group) / (1024 * 1024)
        group_id = tree.insert("", "end",
                               text=f"{group_name} ({len(group)} items – {total_size_mb:.2f} MB)",
                               open=True)
        for item in group:
            display_name = item.get('full_name', item['display']) if item['is_file'] else item['display']
            size_mb = item['size'] / (1024 * 1024)
            tree.insert(group_id, "end", values=(
                "File" if item['is_file'] else "Folder",
                display_name,
                f"{size_mb:.2f} MB",
                item['mtime'],
                item['path']
            ))

    status_var.set(f"Scan completed! {len(similar_groups)} groups found. Total {len(items)} items.")
    if not similar_groups:
        tree.insert("", "end", text="No groups found matching the criteria.", values=("", "", "", "", ""))

root.mainloop()
