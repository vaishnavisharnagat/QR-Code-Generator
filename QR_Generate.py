import tkinter as tk
from tkinter import messagebox, filedialog, colorchooser
import qrcode
from PIL import Image, ImageTk
import cv2
import os


# =========================================================
# GLOBAL VARIABLES
# =========================================================

qr_image_original = None
logo_path = None

dark_mode = False

qr_color = "black"
bg_color = "white"


# =========================================================
# GENERATE QR CODE
# =========================================================

def generate_qr(data=None):

    global qr_image_original

    if data is None:
        data = entry.get().strip()

    if not data:
        messagebox.showwarning(
            "Warning",
            "Please enter text or a URL!"
        )
        return

    try:

        # Create QR Code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4
        )

        qr.add_data(data)
        qr.make(fit=True)

        img = qr.make_image(
            fill_color=qr_color,
            back_color=bg_color
        ).convert("RGB")

        # =================================================
        # ADD LOGO
        # =================================================

        if logo_path and os.path.exists(logo_path):

            try:

                logo = Image.open(logo_path).convert("RGBA")

                qr_width, qr_height = img.size

                logo_size = qr_width // 5

                logo.thumbnail(
                    (logo_size, logo_size),
                    Image.Resampling.LANCZOS
                )

                padding = 8

                logo_background = Image.new(
                    "RGBA",
                    (
                        logo.width + padding * 2,
                        logo.height + padding * 2
                    ),
                    "white"
                )

                logo_background.alpha_composite(
                    logo,
                    (padding, padding)
                )

                position = (
                    (qr_width - logo_background.width) // 2,
                    (qr_height - logo_background.height) // 2
                )

                img = img.convert("RGBA")

                img.alpha_composite(
                    logo_background,
                    position
                )

                img = img.convert("RGB")

            except Exception as e:

                messagebox.showerror(
                    "Logo Error",
                    f"Could not add logo.\n\n{e}"
                )

        # Store original image
        qr_image_original = img

        # Automatically save
        img.save("my_qr_code.png")

        # =================================================
        # DISPLAY QR CODE
        # =================================================

        display_img = img.copy()

        # Smaller preview so it fits completely
        display_img.thumbnail(
            (230, 230),
            Image.Resampling.LANCZOS
        )

        qr_image = ImageTk.PhotoImage(
            display_img
        )

        qr_label.config(
            image=qr_image
        )

        qr_label.image = qr_image

        status_label.config(
            text="✓ QR Code Generated Successfully!"
        )

    except Exception as e:

        messagebox.showerror(
            "Error",
            f"Could not generate QR code.\n\n{e}"
        )


# =========================================================
# SAVE QR CODE
# =========================================================

def save_qr():

    if qr_image_original is None:

        messagebox.showwarning(
            "Warning",
            "Please generate a QR code first!"
        )

        return

    file_path = filedialog.asksaveasfilename(
        title="Save QR Code",
        defaultextension=".png",
        filetypes=[
            ("PNG Image", "*.png"),
            ("JPEG Image", "*.jpg"),
            ("All Files", "*.*")
        ]
    )

    if file_path:

        try:

            qr_image_original.save(file_path)

            messagebox.showinfo(
                "Saved",
                f"QR Code saved successfully!\n\n"
                f"{file_path}"
            )

        except Exception as e:

            messagebox.showerror(
                "Error",
                f"Could not save QR code.\n\n{e}"
            )


# =========================================================
# WI-FI QR CODE
# =========================================================

def wifi_qr():

    wifi_window = tk.Toplevel(root)

    wifi_window.title(
        "Wi-Fi QR Code"
    )

    wifi_window.geometry(
        "400x390"
    )

    wifi_window.resizable(
        False,
        False
    )

    tk.Label(
        wifi_window,
        text="Wi-Fi QR Code",
        font=("Arial", 20, "bold")
    ).pack(pady=15)

    tk.Label(
        wifi_window,
        text="Wi-Fi Name (SSID):",
        font=("Arial", 11)
    ).pack()

    ssid_entry = tk.Entry(
        wifi_window,
        width=35,
        font=("Arial", 11)
    )

    ssid_entry.pack(
        pady=6
    )

    tk.Label(
        wifi_window,
        text="Wi-Fi Password:",
        font=("Arial", 11)
    ).pack()

    password_entry = tk.Entry(
        wifi_window,
        width=35,
        font=("Arial", 11),
        show="*"
    )

    password_entry.pack(
        pady=6
    )

    tk.Label(
        wifi_window,
        text="Security Type:",
        font=("Arial", 11)
    ).pack()

    security = tk.StringVar(
        value="WPA"
    )

    security_menu = tk.OptionMenu(
        wifi_window,
        security,
        "WPA",
        "WEP",
        "nopass"
    )

    security_menu.pack(
        pady=6
    )

    def create_wifi():

        ssid = ssid_entry.get().strip()

        password = password_entry.get().strip()

        security_type = security.get()

        if not ssid:

            messagebox.showwarning(
                "Warning",
                "Please enter Wi-Fi name!"
            )

            return

        if security_type == "nopass":

            wifi_data = (
                f"WIFI:T:nopass;"
                f"S:{ssid};;"
            )

        else:

            wifi_data = (
                f"WIFI:T:{security_type};"
                f"S:{ssid};"
                f"P:{password};;"
            )

        wifi_window.destroy()

        entry.delete(
            0,
            tk.END
        )

        entry.insert(
            0,
            wifi_data
        )

        generate_qr(
            wifi_data
        )

    tk.Button(
        wifi_window,
        text="Generate Wi-Fi QR",
        font=("Arial", 12, "bold"),
        command=create_wifi
    ).pack(
        pady=18
    )


# =========================================================
# CONTACT / VCARD QR
# =========================================================

def contact_qr():

    contact_window = tk.Toplevel(root)

    contact_window.title(
        "Contact / vCard QR"
    )

    contact_window.geometry(
        "400x530"
    )

    contact_window.resizable(
        False,
        False
    )

    tk.Label(
        contact_window,
        text="Contact / vCard",
        font=("Arial", 20, "bold")
    ).pack(
        pady=12
    )

    fields = {}

    field_names = [
        "Name",
        "Phone",
        "Email",
        "Organization",
        "Website"
    ]

    for field in field_names:

        tk.Label(
            contact_window,
            text=field + ":",
            font=("Arial", 10)
        ).pack()

        fields[field] = tk.Entry(
            contact_window,
            width=35,
            font=("Arial", 11)
        )

        fields[field].pack(
            pady=5
        )

    def create_contact():

        name = fields["Name"].get().strip()

        phone = fields["Phone"].get().strip()

        email = fields["Email"].get().strip()

        organization = fields[
            "Organization"
        ].get().strip()

        website = fields[
            "Website"
        ].get().strip()

        if not name:

            messagebox.showwarning(
                "Warning",
                "Please enter contact name!"
            )

            return

        vcard = (
            "BEGIN:VCARD\n"
            "VERSION:3.0\n"
            f"FN:{name}\n"
            f"TEL:{phone}\n"
            f"EMAIL:{email}\n"
            f"ORG:{organization}\n"
            f"URL:{website}\n"
            "END:VCARD"
        )

        contact_window.destroy()

        entry.delete(
            0,
            tk.END
        )

        entry.insert(
            0,
            vcard
        )

        generate_qr(
            vcard
        )

    tk.Button(
        contact_window,
        text="Generate Contact QR",
        font=("Arial", 12, "bold"),
        command=create_contact
    ).pack(
        pady=18
    )


# =========================================================
# QR COLOR
# =========================================================

def choose_qr_color():

    global qr_color

    color = colorchooser.askcolor(
        title="Choose QR Code Color"
    )

    if color[1]:

        qr_color = color[1]

        qr_color_button.config(
            bg=qr_color
        )


# =========================================================
# BACKGROUND COLOR
# =========================================================

def choose_background_color():

    global bg_color

    color = colorchooser.askcolor(
        title="Choose Background Color"
    )

    if color[1]:

        bg_color = color[1]

        bg_color_button.config(
            bg=bg_color
        )


# =========================================================
# SELECT LOGO
# =========================================================

def select_logo():

    global logo_path

    file_path = filedialog.askopenfilename(
        title="Select Logo",
        filetypes=[
            (
                "Image Files",
                "*.png *.jpg *.jpeg"
            ),
            (
                "PNG Files",
                "*.png"
            ),
            (
                "JPEG Files",
                "*.jpg *.jpeg"
            )
        ]
    )

    if file_path:

        logo_path = file_path

        logo_label.config(
            text=(
                "Logo: "
                + os.path.basename(file_path)
            )
        )

        status_label.config(
            text="Logo selected. Generate QR to apply it."
        )


# =========================================================
# REMOVE LOGO
# =========================================================

def remove_logo():

    global logo_path

    logo_path = None

    logo_label.config(
        text="No Logo Selected"
    )

    status_label.config(
        text="Logo removed."
    )


# =========================================================
# QR SCANNER
# =========================================================

def scan_qr():

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():

        messagebox.showerror(
            "Camera Error",
            "Could not open camera.\n\n"
            "Please check that your webcam is connected."
        )

        return

    detector = cv2.QRCodeDetector()

    detected_data = None

    messagebox.showinfo(
        "QR Scanner",
        "Camera will open now.\n\n"
        "Show a QR code to the camera.\n"
        "Press Q to close the scanner."
    )

    while True:

        ret, frame = cap.read()

        if not ret:
            break

        data, points, _ = (
            detector.detectAndDecode(frame)
        )

        if points is not None:

            points = points.astype(int)

            for i in range(4):

                cv2.line(
                    frame,
                    tuple(points[0][i]),
                    tuple(
                        points[0][
                            (i + 1) % 4
                        ]
                    ),
                    (0, 255, 0),
                    3
                )

        if data:

            detected_data = data

            cv2.putText(
                frame,
                "QR Code Detected!",
                (20, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2
            )

            cv2.imshow(
                "QR Code Scanner",
                frame
            )

            cv2.waitKey(1500)

            break

        cv2.imshow(
            "QR Code Scanner",
            frame
        )

        if cv2.waitKey(1) & 0xFF == ord("q"):

            break

    cap.release()

    cv2.destroyAllWindows()

    if detected_data:

        messagebox.showinfo(
            "QR Code Detected",
            f"Data:\n\n{detected_data}"
        )

        entry.delete(
            0,
            tk.END
        )

        entry.insert(
            0,
            detected_data
        )

    else:

        messagebox.showinfo(
            "Result",
            "No QR code detected."
        )


# =========================================================
# CLEAR
# =========================================================

def clear_qr():

    global qr_image_original
    global logo_path

    entry.delete(
        0,
        tk.END
    )

    qr_label.config(
        image=""
    )

    qr_label.image = None

    qr_image_original = None

    logo_path = None

    logo_label.config(
        text="No Logo Selected"
    )

    status_label.config(
        text="Ready"
    )


# =========================================================
# DARK / LIGHT MODE
# =========================================================

def toggle_theme():

    global dark_mode

    dark_mode = not dark_mode

    widgets = [
        generate_button,
        wifi_button,
        contact_button,
        qr_color_button,
        bg_color_button,
        logo_button,
        remove_logo_button,
        save_button,
        scan_button,
        clear_button,
        theme_button
    ]

    if dark_mode:

        background = "#1e1e1e"
        foreground = "white"

        root.config(
            bg=background
        )

        title.config(
            bg=background,
            fg=foreground
        )

        label.config(
            bg=background,
            fg=foreground
        )

        logo_label.config(
            bg=background,
            fg=foreground
        )

        status_label.config(
            bg=background,
            fg="#00ff88"
        )

        qr_label.config(
            bg=background
        )

        entry.config(
            bg="#333333",
            fg="white",
            insertbackground="white"
        )

        for button in widgets:

            button.config(
                bg="#333333",
                fg="white"
            )

        theme_button.config(
            text="☀ Light Mode"
        )

    else:

        background = "SystemButtonFace"
        foreground = "black"

        root.config(
            bg=background
        )

        title.config(
            bg=background,
            fg=foreground
        )

        label.config(
            bg=background,
            fg=foreground
        )

        logo_label.config(
            bg=background,
            fg=foreground
        )

        status_label.config(
            bg=background,
            fg="green"
        )

        qr_label.config(
            bg=background
        )

        entry.config(
            bg="white",
            fg="black",
            insertbackground="black"
        )

        for button in widgets:

            button.config(
                bg="SystemButtonFace",
                fg="black"
            )

        theme_button.config(
            text="🌙 Dark Mode"
        )


# =========================================================
# MAIN WINDOW
# =========================================================

root = tk.Tk()

root.title(
    "Advanced QR Code Generator"
)

# Updated smaller window
root.geometry(
    "550x780"
)

root.resizable(
    False,
    False
)


# =========================================================
# TITLE
# =========================================================

title = tk.Label(
    root,
    text="QR Code Generator",
    font=("Arial", 22, "bold")
)

title.pack(
    pady=10
)


# =========================================================
# INPUT LABEL
# =========================================================

label = tk.Label(
    root,
    text="Enter Text or URL:",
    font=("Arial", 12)
)

label.pack(
    pady=3
)


# =========================================================
# INPUT BOX
# =========================================================

entry = tk.Entry(
    root,
    width=48,
    font=("Arial", 11)
)

entry.pack(
    pady=5
)


# =========================================================
# GENERATE BUTTON
# =========================================================

generate_button = tk.Button(
    root,
    text="Generate QR Code",
    font=("Arial", 11, "bold"),
    command=generate_qr
)

generate_button.pack(
    pady=4
)


# =========================================================
# WI-FI BUTTON
# =========================================================

wifi_button = tk.Button(
    root,
    text="📶 Wi-Fi QR Code",
    font=("Arial", 10, "bold"),
    command=wifi_qr
)

wifi_button.pack(
    pady=3
)


# =========================================================
# CONTACT BUTTON
# =========================================================

contact_button = tk.Button(
    root,
    text="👤 Contact / vCard QR",
    font=("Arial", 10, "bold"),
    command=contact_qr
)

contact_button.pack(
    pady=3
)


# =========================================================
# QR COLOR
# =========================================================

qr_color_button = tk.Button(
    root,
    text="🎨 QR Color",
    font=("Arial", 9),
    command=choose_qr_color
)

qr_color_button.pack(
    pady=3
)


# =========================================================
# BACKGROUND COLOR
# =========================================================

bg_color_button = tk.Button(
    root,
    text="🖌 Background Color",
    font=("Arial", 9),
    command=choose_background_color
)

bg_color_button.pack(
    pady=3
)


# =========================================================
# LOGO
# =========================================================

logo_button = tk.Button(
    root,
    text="🖼 Select Logo",
    font=("Arial", 9),
    command=select_logo
)

logo_button.pack(
    pady=3
)


remove_logo_button = tk.Button(
    root,
    text="Remove Logo",
    font=("Arial", 9),
    command=remove_logo
)

remove_logo_button.pack(
    pady=2
)


logo_label = tk.Label(
    root,
    text="No Logo Selected",
    font=("Arial", 8)
)

logo_label.pack(
    pady=1
)


# =========================================================
# SAVE BUTTON
# =========================================================

save_button = tk.Button(
    root,
    text="💾 Save QR Code As",
    font=("Arial", 10, "bold"),
    command=save_qr
)

save_button.pack(
    pady=3
)


# =========================================================
# SCAN BUTTON
# =========================================================

scan_button = tk.Button(
    root,
    text="📷 Scan QR Code",
    font=("Arial", 10, "bold"),
    command=scan_qr
)

scan_button.pack(
    pady=3
)


# =========================================================
# CLEAR BUTTON
# =========================================================

clear_button = tk.Button(
    root,
    text="🗑 Clear",
    font=("Arial", 9),
    command=clear_qr
)

clear_button.pack(
    pady=2
)


# =========================================================
# QR DISPLAY
# =========================================================

qr_label = tk.Label(
    root
)

qr_label.pack(
    pady=4
)


# =========================================================
# STATUS
# =========================================================

status_label = tk.Label(
    root,
    text="Ready",
    font=("Arial", 9)
)

status_label.pack(
    pady=1
)


# =========================================================
# THEME BUTTON
# =========================================================

theme_button = tk.Button(
    root,
    text="🌙 Dark Mode",
    font=("Arial", 9, "bold"),
    command=toggle_theme
)

theme_button.pack(
    pady=2
)


# =========================================================
# START APPLICATION
# =========================================================

root.mainloop()