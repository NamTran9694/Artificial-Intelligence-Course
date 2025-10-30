import argparse
import os
from pathlib import Path
from urllib.parse import urlparse
import qrcode
from qrcode.constants import ERROR_CORRECT_L, ERROR_CORRECT_M, ERROR_CORRECT_Q, ERROR_CORRECT_H

# DEFINE THE ERROR - CORRECTION DICTIONARY
EC_MAP ={
    "L": ERROR_CORRECT_L,
    "M": ERROR_CORRECT_M,
    "Q": ERROR_CORRECT_Q,
    "H":ERROR_CORRECT_H,
}

# CHECKING IF USER ENTER VALID URL
def is_valid_url(url: str) -> bool:
    try:
            parsed = urlparse(url)
            return bool(parsed.scheme) and bool(parsed.netloc)
    except Exception:
        return False
    
# ENSURE THE FILE NAME END WITH .PNG
def ensure_png_suffix(path: Path) -> Path:
     return path if path.suffix.lower() == ".png" else path.with_suffix(".png")

# GENERATING QR CODE - MAIN FUNCTION
def generate_qr(
          url: str,
          out_path: Path,
          error_correction: str ="M",
          box_size: int =20,
          border: int = 4,
          fill_color: str = "black",
          back_color: str ="white",) -> Path:
     
     if not is_valid_url(url):  # Check if the URL  is valid - if not the program stops and warns the user.
          raise ValueError(f"Invalid URL: '{url}'")
     
     if error_correction not in EC_MAP:  # Make sure the user picked a valid error correction level (L/M/Q/H).
          raise ValueError(f"error-correction must be one of {list(EC_MAP.keys())}")
     
     out_path = ensure_png_suffix(out_path) # Ensure the folder (like out/) exists before saving the image.
     out_path.parent.mkdir(parents= True, exist_ok= True)

     # Creating QR object:
     qr = qrcode.QRCode(
          version = None,
          error_correction= EC_MAP[error_correction],
          box_size= box_size,
          border= border,)
     
     qr.add_data(url)
     qr.make(fit=True)
     img = qr.make_image(fill_color = fill_color, back_color = back_color)
     img.save(out_path)

     return out_path

# DEFINE ALL THE COMMAND-LINE OPTIONS USERS CAN PASS IN.
def parse_args() -> argparse.Namespace:
     parser = argparse.ArgumentParser(description= "Generate a QR code PNG for a given URL.")

     parser.add_argument("--url", required= True, help= "URL to encode (e.g., https://example.com).",)

     parser.add_argument("--out", default= "out/qrcode.png", help= "Output PNG path (default: out/qrcode.png).",)

     parser.add_argument("--ec", choices= list(EC_MAP.keys()), default= "M", help= "Error-correction level: L(7%), M(15%), Q(25%), H(30%). Default: M",)
     
     parser.add_argument("--box-size", type=int, default=10, help="Pixel size of each QR box. Default: 10",)
     
     parser.add_argument("--border", type=int, default=4, help="Border width (boxes). Default: 4",)
     
     parser.add_argument("--fill", default="black", help='Foreground color (e.g., "black", "#000000").',)
     
     parser.add_argument("--back", default="white", help='Background color (e.g., "white", "#FFFFFF").',) 

     return parser.parse_args()

# ENTRY POINT
def main() -> int:
     args = parse_args()
     try:
          out_path = generate_qr(
               url= args.url,
               out_path= Path(args.out),
               error_correction= args.ec,
               box_size= args.box_size,
               border= args.border,
               fill_color= args.fill,
               back_color= args.back,)
          
          print(f"Sucesful!! QR code generated: {out_path.resolve()}")
          return 0
     except Exception as exc:
         print(f"Fail!! Error: {exc}", file=sys.stderr)
         return 1
     
# PROGRAM ENTRY CHECK:
if __name__ == "__main__":
     SystemExit(main())

     

