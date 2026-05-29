import numpy as np
import matplotlib.pyplot as plt
import serial
import os
import pandas as pd
from datetime import datetime
from tkinter import Tk, filedialog, ttk, messagebox, StringVar, Label, Button
from serial.tools import list_ports

def convert_16bit_signed(lo, hi):
    combined = (hi.astype(np.uint16) << 8) | lo.astype(np.uint16)
    return combined.view(np.int16)


def conv_imu(arr):
    x = convert_16bit_signed(arr[:, 0], arr[:, 1]) / (2**15) * 2
    y = convert_16bit_signed(arr[:, 2], arr[:, 3]) / (2**15) * 2
    z = convert_16bit_signed(arr[:, 4], arr[:, 5]) / (2**15) * 2
    return x, y, z


def conv_gyro(arr):
    x = convert_16bit_signed(arr[:, 0], arr[:, 1]) / (2**15) * 250
    y = convert_16bit_signed(arr[:, 2], arr[:, 3]) / (2**15) * 250
    z = convert_16bit_signed(arr[:, 4], arr[:, 5]) / (2**15) * 250
    return x, y, z


# For MAX30205
def conv_temp_max30205(msb, lsb):
    raw = (msb << 8) | lsb

    if raw & 0x8000:
        raw -= 0x10000

    return raw / 256.0


# For MAX30101
def conv_24bit_ppg(b0, b1, b2):
    return ((b0 << 16) | (b1 << 8) | b2) & 0x3FFFF


def receive_and_save_data(ser, bin_filename, packet_size=4096, max_packets=2048 * 64):
    """Riceve pacchetti via seriale e li salva in binario."""
    with open(bin_filename, "wb") as f:
        for packet_count in range(max_packets):
            data = ser.read(packet_size)

            if not data:
                continue

            if data == b"T":  # terminatore
                print("Received Terminator Character.")
                break

            f.write(data)
            print(f"📥 Received packet {packet_count + 1}")

    ser.close()
    print("📴 Serial COM Port Closed.")


def process_bin_file(bin_filename, csv_filename=None):
    hh_list, mm_list, ss_list, sss_list = [], [], [], []
    acc_x_list, acc_y_list, acc_z_list = [], [], []
    gyro_x_list, gyro_y_list, gyro_z_list = [], [], []
    temp_list = []
    ppg_red_list, ppg_ir_list, ppg_green_list = [], [], []

    Sample_Size = 28

    with open(bin_filename, "rb") as f:
        while True:
            pagina = f.read(4096)

            if len(pagina) < 4096:
                break

            # considera solo i primi 4060 byte because it is divisible by 28
            valid_bytes = pagina[:4060]

            for i in range(0, len(valid_bytes), Sample_Size):
                subpkt = valid_bytes[i:i + Sample_Size]

                if len(subpkt) < Sample_Size:
                    continue

                # timestamp: bytes 0-4
                hh = subpkt[0]
                mm = subpkt[1]
                ss = subpkt[2]
                sss = subpkt[3] | (subpkt[4] << 8)

                hh_list.append(hh)
                mm_list.append(mm)
                ss_list.append(ss)
                sss_list.append(sss)

                # accelerometer: bytes 5-10
                acc_arr = np.frombuffer(subpkt[5:11], dtype=np.uint8).reshape(1, 6)
                acc_x, acc_y, acc_z = conv_imu(acc_arr)

                acc_x_list.append(acc_x[0])
                acc_y_list.append(acc_y[0])
                acc_z_list.append(acc_z[0])

                # gyroscope: bytes 11-16
                gyro_arr = np.frombuffer(subpkt[11:17], dtype=np.uint8).reshape(1, 6)
                gyro_x, gyro_y, gyro_z = conv_gyro(gyro_arr)

                gyro_x_list.append(gyro_x[0])
                gyro_y_list.append(gyro_y[0])
                gyro_z_list.append(gyro_z[0])

                # temperature MAX30205: bytes 17-18
                #temp = conv_temp_max30205(subpkt[17], subpkt[18])
                #temp_list.append(temp)

                # PPG MAX30101: bytes 17-25
                red = conv_24bit_ppg(subpkt[17], subpkt[18], subpkt[19])
                ir = conv_24bit_ppg(subpkt[20], subpkt[21], subpkt[22])
                green = conv_24bit_ppg(subpkt[23], subpkt[24], subpkt[25])

                ppg_red_list.append(red)
                ppg_ir_list.append(ir)
                ppg_green_list.append(green)
                
                # temperature MAX30205: bytes 26,27
                temp = conv_temp_max30205(subpkt[26], subpkt[27])
                temp_list.append(temp)

    df = pd.DataFrame({
        "hh": hh_list,
        "mm": mm_list,
        "ss": ss_list,
        "sss": sss_list,
        "acc_x": acc_x_list,
        "acc_y": acc_y_list,
        "acc_z": acc_z_list,
        "gyro_x": gyro_x_list,
        "gyro_y": gyro_y_list,
        "gyro_z": gyro_z_list,
        "temperature_c": temp_list,
        "ppg_red": ppg_red_list,
        "ppg_ir": ppg_ir_list,
        "ppg_green": ppg_green_list
    })

    # rimuove eventuali righe vuote / non scritte
    df = df[
        ~(
            (df["hh"] == 0) &
            (df["mm"] == 0) &
            (df["ss"] == 0) &
            (df["sss"] == 0) &
            (df["acc_x"] == 0) &
            (df["acc_y"] == 0) &
            (df["acc_z"] == 0) &
            (df["gyro_x"] == 0) &
            (df["gyro_y"] == 0) &
            (df["gyro_z"] == 0) &
            (df["temperature_c"] == 0) &
            (df["ppg_red"] == 0) &
            (df["ppg_ir"] == 0) &
            (df["ppg_green"] == 0)
        )
    ].reset_index(drop=True)

    if df.empty:
        print("⚠️ No valid samples found.")
        return

    # asse tempo in secondi
    time_s = (
        df["hh"] * 3600 +
        df["mm"] * 60 +
        df["ss"] +
        df["sss"] / 1000.0
    )

    time_s = time_s - time_s.iloc[0]

    # filtro solo per il plot temperatura
    temp_mask = (df["temperature_c"] > 20) & (df["temperature_c"] < 45)

        # ==============================
    # All plots in one window
    # ==============================

    fig, axs = plt.subplots(6, 1, figsize=(15, 18), sharex=True)

    # Accelerometer
    axs[0].plot(time_s, df["acc_x"], label="acc_x")
    axs[0].plot(time_s, df["acc_y"], label="acc_y")
    axs[0].plot(time_s, df["acc_z"], label="acc_z")
    axs[0].set_title("Accelerometer")
    axs[0].set_ylabel("g")
    axs[0].legend()
    axs[0].grid(True)

    # Gyroscope
    axs[1].plot(time_s, df["gyro_x"], label="gyro_x")
    axs[1].plot(time_s, df["gyro_y"], label="gyro_y")
    axs[1].plot(time_s, df["gyro_z"], label="gyro_z")
    axs[1].set_title("Gyroscope")
    axs[1].set_ylabel("deg/s")
    axs[1].legend()
    axs[1].grid(True)

    # Temperature
    axs[2].plot(time_s, df["temperature_c"], label="temperature_c")
    axs[2].set_title("MAX30205 Temperature")
    axs[2].set_ylabel("°C")
    axs[2].legend()
    axs[2].grid(True)

    # PPG RED
    axs[3].plot(time_s, df["ppg_red"], color="red", label="red")
    axs[3].set_title("MAX30101 PPG RED")
    axs[3].set_ylabel("Raw ADC")
    axs[3].legend()
    axs[3].grid(True)

    # PPG IR
    axs[4].plot(time_s, df["ppg_ir"], label="ir")
    axs[4].set_title("MAX30101 PPG IR")
    axs[4].set_ylabel("Raw ADC")
    axs[4].legend()
    axs[4].grid(True)

    # PPG GREEN
    axs[5].plot(time_s, df["ppg_green"],color="green", label="green")
    axs[5].set_title("MAX30101 PPG GREEN")
    axs[5].set_xlabel("Time [s]")
    axs[5].set_ylabel("Raw ADC")
    axs[5].legend()
    axs[5].grid(True)

    # ==============================
    # IR raw PPG with estimated beats
    # ==============================

    # Plot only the first 10 seconds, similar to the reference figure.
    plot_duration_s = 10
    ir_time_mask = time_s <= plot_duration_s

    # Raw IR signal in the selected time window.
    ir_time = time_s[ir_time_mask].reset_index(drop=True)
    ir_raw_10s = df.loc[ir_time_mask, "ppg_ir"].astype(float).reset_index(drop=True)

    # Smooth the raw IR signal slightly for beat detection.
    # The raw signal is still used for plotting; smoothing is only for finding beat positions.
    ir_smooth = ir_raw_10s.rolling(window=7, center=True, min_periods=1).mean()

    # Remove slow drift only for beat detection.
    # This helps detect the pulse dips/peaks without changing the plotted raw waveform.
    ir_baseline = ir_smooth.rolling(window=80, center=True, min_periods=1).mean()
    ir_ac = ir_smooth - ir_baseline

    # In our signal, heart beats usually appear as downward dips in IR.
    # Therefore, we detect peaks on the inverted AC signal.
    beat_signal = ir_ac

    # Simple threshold-based local peak detection.
    # Increase threshold_factor if too many beats are detected.
    # Decrease threshold_factor if too few beats are detected.
    threshold_factor = 0.4
    threshold = beat_signal.mean() + threshold_factor * beat_signal.std()

    # Minimum distance between beats in seconds.
    # 0.45 s corresponds to about 133 bpm max.
    min_distance_s = 0.45

    if len(ir_time) > 1:
        dt = np.median(np.diff(ir_time))
        min_distance_samples = max(1, int(min_distance_s / dt))
    else:
        min_distance_samples = 1

    beat_indices = []
    last_beat_index = -min_distance_samples

    for i in range(1, len(beat_signal) - 1):
        is_local_peak = beat_signal[i] > beat_signal[i - 1] and beat_signal[i] >= beat_signal[i + 1]
        is_above_threshold = beat_signal[i] > threshold
        is_far_enough = (i - last_beat_index) >= min_distance_samples

        if is_local_peak and is_above_threshold and is_far_enough:
            beat_indices.append(i)
            last_beat_index = i

    # Create a separate figure similar to the reference plot.
    plt.figure(figsize=(12, 4))
    plt.plot(ir_time, ir_raw_10s, label="PPG")

    if beat_indices:
        plt.scatter(
            ir_time.iloc[beat_indices],
            ir_raw_10s.iloc[beat_indices],
            s=80,
            facecolors="none",
            edgecolors="red",
            linewidths=1.8,
            label="Beats"
        )

    plt.title("IR raw PPG and estimated HR beats with calibration")
    plt.xlabel("Time [s]")
    plt.ylabel("Amplitude")
    plt.legend()
    plt.grid(True)

    # Zoom the y-axis around the useful raw IR range.
    ir_low = ir_raw_10s.quantile(0.02)
    ir_high = ir_raw_10s.quantile(0.98)
    margin = 0.1 * (ir_high - ir_low)
    plt.ylim(ir_low - margin, ir_high + margin)

    plt.tight_layout()
    plt.show()

    if csv_filename:
        df.to_csv(csv_filename, index=False)
        print(f"📄 Data saved in CSV: {csv_filename}")


def gui_select_com_and_folder():
    """Apre una piccola GUI per selezionare COM e cartella."""
    root = Tk()
    root.title("IMU Data Logger - Configuration")
    root.geometry("400x400")
    root.resizable(False, False)

    Label(root, text="🔌 Select the COM Port:", font=("Segoe UI", 10)).pack(pady=5)

    com_var = StringVar()
    ports = [p.device for p in list_ports.comports()]

    if not ports:
        ports = ["No COM Port found"]

    com_box = ttk.Combobox(root, textvariable=com_var, values=ports, state="readonly", width=30)
    com_box.pack(pady=5)
    com_box.current(0)

    def browse_folder():
        folder = filedialog.askdirectory(title="📂 Select the folder")
        if folder:
            folder_var.set(folder)

    folder_var = StringVar()

    Label(root, text="📁 Folder:", font=("Segoe UI", 10)).pack(pady=5)
    Button(root, text="Select folder...", command=browse_folder).pack()
    Label(root, textvariable=folder_var, fg="blue", wraplength=350).pack(pady=5)

    def confirm():
        if not folder_var.get() or "No COM Port found" in com_var.get():
            messagebox.showerror("Error", "Select a valid COM Port and a folder.")
            return
        root.destroy()

    Button(root, text="✅ Confirm", command=confirm, bg="#4CAF50", fg="white").pack(pady=10)
    root.mainloop()

    return com_var.get(), folder_var.get()


# ==============================
# Main
# ==============================

def main():
    com_port, save_path = gui_select_com_and_folder()

    if not com_port or not save_path:
        print("❌ Application Stopped.")
        return

    base_filename = datetime.now().strftime("IMUData_%Y%m%d_%H%M%S")
    bin_filename = os.path.join(save_path, f"{base_filename}.bin")
    csv_filename = os.path.join(save_path, f"{base_filename}_imu.csv")

    BAUD_RATE = 250000

    try:
        ser = serial.Serial(com_port, BAUD_RATE, timeout=10)
        print(f"🔌 Connected to {com_port}")
        receive_and_save_data(ser, bin_filename)
    except serial.SerialException as e:
        print(f"⚠️ Serial Error: {e}")
        return

    process_bin_file(bin_filename, csv_filename)


# ==============================
# Entry point
# ==============================

if __name__ == "__main__":
    main()