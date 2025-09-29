#!/usr/bin/env python3
# crc_gui_filecheck.py
# Calcul CRC (formules vérifiées) + test batch fichier

import tkinter as tk
from tkinter import filedialog, messagebox

def parse_hex_input(s):
    """Accepte 'AA BB CC ...' ou 'AABBCC...' et renvoie une liste d'octets ints, ou None si invalide."""
    s = s.strip().replace(',', ' ').replace('\t', ' ')
    parts = [p for p in s.split() if p]
    if len(parts) == 1 and len(parts[0]) % 2 == 0 and all(c in "0123456789abcdefABCDEF" for c in parts[0]):
        hexstr = parts[0]
        parts = [hexstr[i:i+2] for i in range(0, len(hexstr), 2)]
    try:
        return [int(x, 16) for x in parts]
    except ValueError:
        return None

# --- compute function (formules vérifiées) ---
def bit(byte, n):
    """n: 7 = MSB .. 0 = LSB"""
    return (byte >> n) & 1

def compute_crc_from_6bytes(B):
    # B = [B0, B1, B2, B3, B4, B5] (les 6 octets utiles)
    crc = [0]*16
    crc[0]  = bit(B[0],0) ^ bit(B[3],2) ^ bit(B[4],4) ^ bit(B[4],0) ^ bit(B[5],6) ^ bit(B[5],3)
    crc[1]  = bit(B[0],4) ^ bit(B[4],5) ^ bit(B[4],1) ^ bit(B[5],7) ^ bit(B[5],4)
    crc[2]  = bit(B[0],7) ^ bit(B[0],4) ^ bit(B[3],4) ^ bit(B[4],6) ^ bit(B[4],2) ^ bit(B[4],0) ^ bit(B[5],5)
    crc[3]  = bit(B[0],7) ^ bit(B[0],4) ^ bit(B[3],5) ^ bit(B[4],7) ^ bit(B[4],3) ^ bit(B[4],1) ^ bit(B[5],6)
    crc[4]  = bit(B[0],0) ^ bit(B[3],4) ^ bit(B[3],2) ^ bit(B[4],5) ^ bit(B[4],3) ^ bit(B[4],2) ^ bit(B[4],0) ^ bit(B[5],7) ^ bit(B[5],6) ^ bit(B[5],2) ^ bit(B[5],0)
    crc[5]  = bit(B[3],5) ^ bit(B[3],4) ^ bit(B[3],2) ^ bit(B[4],6) ^ bit(B[4],4) ^ bit(B[4],3) ^ bit(B[4],1) ^ bit(B[4],0) ^ bit(B[5],7) ^ bit(B[5],3) ^ bit(B[5],1)
    crc[6]  = bit(B[0],7) ^ bit(B[0],4) ^ bit(B[0],0) ^ bit(B[3],5) ^ bit(B[3],4) ^ bit(B[3],2) ^ bit(B[4],7) ^ bit(B[4],3) ^ bit(B[4],2) ^ bit(B[4],1) ^ bit(B[5],6) ^ bit(B[5],4) ^ bit(B[5],0)
    crc[7]  = bit(B[0],4) ^ bit(B[0],0) ^ bit(B[3],6) ^ bit(B[3],5) ^ bit(B[4],4) ^ bit(B[4],3) ^ bit(B[4],2) ^ bit(B[5],7) ^ bit(B[5],5) ^ bit(B[5],1)
    crc[8]  = bit(B[0],7) ^ bit(B[0],4) ^ bit(B[3],6) ^ bit(B[3],2) ^ bit(B[4],7) ^ bit(B[4],6) ^ bit(B[4],5) ^ bit(B[4],3) ^ bit(B[5],7) ^ bit(B[5],6) ^ bit(B[5],1) ^ bit(B[5],0)
    crc[9]  = bit(B[0],4) ^ bit(B[3],6) ^ bit(B[3],4) ^ bit(B[4],5) ^ bit(B[4],4) ^ bit(B[4],3) ^ bit(B[4],0) ^ bit(B[5],6) ^ bit(B[5],2) ^ bit(B[5],0)
    crc[10] = bit(B[0],7) ^ bit(B[3],6) ^ bit(B[3],5) ^ bit(B[3],2) ^ bit(B[4],6) ^ bit(B[4],3) ^ bit(B[4],1) ^ bit(B[4],0) ^ bit(B[5],7) ^ bit(B[5],6) ^ bit(B[5],3) ^ bit(B[5],2) ^ bit(B[5],1) ^ bit(B[5],0)
    crc[11] = bit(B[0],4) ^ bit(B[0],0) ^ bit(B[3],2) ^ bit(B[4],7) ^ bit(B[4],5) ^ bit(B[4],3) ^ bit(B[4],2) ^ bit(B[4],1) ^ bit(B[5],7) ^ bit(B[5],6) ^ bit(B[5],4) ^ bit(B[5],3) ^ bit(B[5],1) ^ bit(B[5],0)
    crc[12] = bit(B[0],7) ^ bit(B[0],4) ^ bit(B[4],6) ^ bit(B[4],4) ^ bit(B[4],3) ^ bit(B[4],2) ^ bit(B[4],0) ^ bit(B[5],7) ^ bit(B[5],5) ^ bit(B[5],4) ^ bit(B[5],2) ^ bit(B[5],1)
    crc[13] = bit(B[0],4) ^ bit(B[0],0) ^ bit(B[3],6) ^ bit(B[4],7) ^ bit(B[4],1) ^ bit(B[5],5) ^ bit(B[5],3) ^ bit(B[5],0)
    crc[14] = bit(B[0],4) ^ bit(B[0],0) ^ bit(B[3],2) ^ bit(B[4],2) ^ bit(B[5],6) ^ bit(B[5],4) ^ bit(B[5],1)
    crc[15] = bit(B[0],7) ^ bit(B[0],0) ^ bit(B[4],3) ^ bit(B[5],7) ^ bit(B[5],5) ^ bit(B[5],2)

    low = 0
    high = 0
    for i in range(8):
        low  |= (crc[i] & 1) << i
    for i in range(8,16):
        high |= (crc[i] & 1) << (i-8)

    return (low, high, (low << 8) | high)

# --- GUI ---
root = tk.Tk()
root.title("Calcul CRC — version corrigée + fichier")

tk.Label(root, text="Trame hex (ex: B4 33 EB 21 22 07 99 00 C8 82):").grid(row=0, column=0, sticky="w", padx=6, pady=(6,0))
entry = tk.Entry(root, width=64)
entry.grid(row=1, column=0, padx=6, pady=6, sticky="we")
entry.insert(0, "B4 33 EB 21 22 07 99 00 C8 82")
entry.focus()

def check_frame(parsed):
    """Retourne (ok, calc, ref)"""
    if parsed is None or len(parsed) < 10:
        return None, None, None
    B6 = parsed[2:8]
    crc_calc = compute_crc_from_6bytes(B6)
    crc_file = parsed[-2] | (parsed[-1] << 8)
    return (crc_calc == crc_file, crc_calc, crc_file)

def on_calculate(event=None):
    parsed = parse_hex_input(entry.get())
    if parsed is None:
        result_label.config(text="Format hex invalide", bg="orange"); return
    if len(parsed) < 10:
        result_label.config(text="Trame trop courte (≥10 octets)", bg="orange"); return

    B6 = parsed[2:8]
    low, high, _ = compute_crc_from_6bytes(B6)

    # CRC calculé = deux octets dans l'ordre trame
    calc_str = f"{low:02X} {high:02X}"

    # CRC extrait de la trame
    low_file, high_file = parsed[-2], parsed[-1]
    file_str = f"{low_file:02X} {high_file:02X}"

    if (low, high) == (low_file, high_file):
        result_label.config(text=f"CRC calculé: {calc_str}  (OK)", bg="lightgreen")
    else:
        result_label.config(text=f"CRC calculé: {calc_str}  (attendu {file_str})", bg="tomato")


def on_open_file():
    path = filedialog.askopenfilename(title="Choisir un fichier de trames",
                                      filetypes=[("Text files","*.txt"),("All files","*.*")])
    if not path: return
    total = okcount = 0
    bad_lines = []
    with open(path,"r",encoding="utf-8",errors="ignore") as f:
        for lineno,line in enumerate(f, start=1):
            parsed = parse_hex_input(line)
            if parsed is None or len(parsed) < 10:
                bad_lines.append(f"Ligne {lineno}: format invalide")
                continue
            total += 1
            ok, crc_calc, crc_file = check_frame(parsed)
            if ok:
                okcount += 1
            else:
                bad_lines.append(f"Ligne {lineno}: CRC {crc_calc:04X} attendu {crc_file:04X}")
    msg = f"Trames totales: {total}\nCRC corrects: {okcount}\nCRC incorrects: {total-okcount}"
    if bad_lines:
        msg += "\n\nDétails erreurs:\n" + "\n".join(bad_lines[:20])
        if len(bad_lines) > 20:
            msg += f"\n... et {len(bad_lines)-20} autres."
    messagebox.showinfo("Résultat analyse fichier", msg)

btn = tk.Button(root, text="Calculer", command=on_calculate)
btn.grid(row=1, column=1, padx=6, pady=6)

btn_file = tk.Button(root, text="Ouvrir fichier…", command=on_open_file)
btn_file.grid(row=2, column=0, columnspan=2, padx=6, pady=(0,6))

result_label = tk.Label(root, text="---", width=40, relief="sunken", bg="lightgray")
result_label.grid(row=3, column=0, columnspan=2, padx=6, pady=(0,6), sticky="we")

root.bind("<Return>", on_calculate)
root.mainloop()
