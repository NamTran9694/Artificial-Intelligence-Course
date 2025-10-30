# INSTALL REQUIRED LIBRARIES
* Once you download the qr_generator.py, qr_generator_gui.py, requirements.txt, open a terminal in the project folder and type:
  `pip install -r requirements.txt`


# RUN WITHOUT GUI (COMMAND LINE MODE)
* In the project folder saving qr_generator.py file.
* In CLI, Command: `python qr_generator.py --url https://https://www.bioxsystems.com/`

| Argument     | Description                                              | Example               |
| ------------ | -------------------------------------------------------- | --------------------- |
| `--url`      | (Required) URL to encode into a QR code                  | `https://example.com` |
| `--out`      | (Optional) Output file name (PNG)                        | `out/qr_example.png`  |
| `--ec`       | (Optional) Error correction level: `L`, `M`, `Q`, or `H` | `M`                   |
| `--box-size` | (Optional) Pixel size of each QR box                     | `10`                  |
| `--border`   | (Optional) White border around the QR code               | `4`                   |
| `--fill`     | (Optional) QR color                                      | `black`               |
| `--back`     | (Optional) Background color                              | `white`               |

# RUN WITH GUI (TKINTER MODE)
* You must save qr_generator.py and qr_generator_gui.py in same folder.
* In the project folder saving qr_generator_gui.py file.
* In CLI, Command: `python qr_generator_gui.py`
