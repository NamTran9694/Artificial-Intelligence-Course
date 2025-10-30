import io
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import ImageTk
import qrcode
from qrcode.constants import ERROR_CORRECT_L, ERROR_CORRECT_M, ERROR_CORRECT_Q, ERROR_CORRECT_H
from qr_generator import generate_qr

# DEFINE ERROR-CORRECTION LEVEL
EC_MAP = {
    "L": ERROR_CORRECT_L,
    "M": ERROR_CORRECT_M,
    "Q": ERROR_CORRECT_Q,
    "H": ERROR_CORRECT_H,
}

# READ VALUE IN THE TEXT BOX AND SAFELY CONVERT IT TO AN INTEGER.
def _parse_int(entry: tk.Entry, default: int) ->int:
    text = (entry.get() or "").strip()
    return int(text) if text else default

# CREATE A PIL IMAGE OBJECT OF THE QR CODE - NOT SAVED YET, ONLY USED FOR REVIEW
def _make_qr_pil(url, ec_key, box, border, fill, back):
    qr = qrcode.QRCode(
        version= None,
        error_correction= EC_MAP[ec_key],
        box_size= box,
        border= border,
    )
    qr.add_data(url)
    qr.make(fit= True)
    return qr.make_image(fill_color = fill, back_color = back).convert("RGB")

# ADD REVIEW BUTTON
def on_preview(url_e, ec_c, box_e, border_e, fill_e, back_e, preview_lbl, status_lbl, root):
    try:
        url = url_e.get().strip()
        ec = (ec_c.get() or "M").strip()
        box = _parse_int(box_e, 10)
        border = _parse_int(border_e, 4)
        fill = (fill_e.get() or "black").strip()
        back = (back_e.get() or "white").strip()

        img = _make_qr_pil(url, ec, box, border, fill, back)

        # Resize preview to a reasonable size if large
        max_px = 256
        w, h = img.size
        scale = min(max_px / max(w, h), 1.0)
        if scale < 1.0:
            img = img.resize((int(w * scale), int(h * scale)))

        # Keep a reference so PhotoImage isn't GC'd
        preview = ImageTk.PhotoImage(img)
        preview_lbl.image = preview
        preview_lbl.configure(image=preview, text="")

        status_lbl.config(text="Preview updated ✅")
        root.update_idletasks()
    except Exception as e:
        preview_lbl.configure(image="", text="(no preview)")
        preview_lbl.image = None
        status_lbl.config(text=f"Preview error: {e}")
        messagebox.showerror("Preview Error", str(e))

# ADD "GENERATE & SAVE" BUTTON
def on_generate(url_e, ec_c, box_e, border_e, fill_e, back_e, status_lbl):
    try:
        url = url_e.get().strip()
        ec = (ec_c.get() or "M").strip()
        box = _parse_int(box_e, 10)
        border = _parse_int(border_e, 4)
        fill = (fill_e.get() or "black").strip()
        back = (back_e.get() or "white").strip()

        out_file = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG Image", "*.png")],
            initialfile="qrcode.png",
            title="Save QR Code"
        )
        if not out_file:
            status_lbl.config(text="Save cancelled")
            return

        result = generate_qr(
            url=url,
            out_path=Path(out_file),
            error_correction=ec,
            box_size=box,
            border=border,
            fill_color=fill,
            back_color=back,
        )
        status_lbl.config(text=f"Saved: {result}")
        messagebox.showinfo("Success", f"Saved: {result}")
    except ValueError as ve:
        status_lbl.config(text="Validation error")
        messagebox.showerror("Invalid Input", str(ve))
    except Exception as e:
        status_lbl.config(text="Unexpected error")
        messagebox.showerror("Error", str(e))

# MAIN WINDOW FUNCTION
def main():
    root = tk.Tk()
    root.title("QR Code Generator")
    root.geometry("600x420")

    frm = ttk.Frame(root, padding=12)
    frm.grid(sticky="nsew")
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    # Grid config
    for c in range(4):
        frm.columnconfigure(c, weight=1)

    # URL
    ttk.Label(frm, text="URL:").grid(row=0, column=0, sticky="e", padx=6, pady=4)
    url_e = ttk.Entry(frm)
    url_e.grid(row=0, column=1, columnspan=3, sticky="we", pady=4)
    url_e.insert(0, "https://example.com")

    # Error correction
    ttk.Label(frm, text="Error Correction:").grid(row=1, column=0, sticky="e", padx=6, pady=4)
    ec_c = ttk.Combobox(frm, values=["L", "M", "Q", "H"], width=6, state="readonly")
    ec_c.set("M")
    ec_c.grid(row=1, column=1, sticky="w")

    # Box & Border
    ttk.Label(frm, text="Box Size:").grid(row=2, column=0, sticky="e", padx=6, pady=4)
    box_e = ttk.Entry(frm, width=10)
    box_e.insert(0, "10")
    box_e.grid(row=2, column=1, sticky="w")

    ttk.Label(frm, text="Border:").grid(row=2, column=2, sticky="e", padx=6, pady=4)
    border_e = ttk.Entry(frm, width=10)
    border_e.insert(0, "4")
    border_e.grid(row=2, column=3, sticky="w")

    # Colors
    ttk.Label(frm, text="Fill Color:").grid(row=3, column=0, sticky="e", padx=6, pady=4)
    fill_e = ttk.Entry(frm, width=12)
    fill_e.insert(0, "black")
    fill_e.grid(row=3, column=1, sticky="w")

    ttk.Label(frm, text="Background:").grid(row=3, column=2, sticky="e", padx=6, pady=4)
    back_e = ttk.Entry(frm, width=12)
    back_e.insert(0, "white")
    back_e.grid(row=3, column=3, sticky="w")

    # Buttons
    status_lbl = ttk.Label(frm, text="Ready", anchor="w")
    status_lbl.grid(row=5, column=0, columnspan=4, sticky="we", pady=(6, 2))

    btn_row = ttk.Frame(frm)
    btn_row.grid(row=6, column=0, columnspan=4, pady=8)
    preview_btn = ttk.Button(
        btn_row, text="Preview",
        command=lambda: on_preview(url_e, ec_c, box_e, border_e, fill_e, back_e, preview_lbl, status_lbl, root)
    )
    preview_btn.grid(row=0, column=0, padx=6)

    gen_btn = ttk.Button(
        btn_row, text="Generate & Save…",
        command=lambda: on_generate(url_e, ec_c, box_e, border_e, fill_e, back_e, status_lbl)
    )
    gen_btn.grid(row=0, column=1, padx=6)

    # Preview area
    preview_frame = ttk.LabelFrame(frm, text="Preview")
    preview_frame.grid(row=4, column=0, columnspan=4, sticky="nsew", pady=8)
    frm.rowconfigure(4, weight=1)

    preview_lbl = ttk.Label(preview_frame, text="(no preview)", anchor="center")
    preview_lbl.pack(expand=True, fill="both", padx=8, pady=8)

    root.mainloop()

if __name__ == "__main__":
    main()
