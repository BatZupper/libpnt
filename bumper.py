#DEV TEST FILE HERE WILL BE REMOVED SOON PLS DON'T USE IT

import zlib
import struct

input_filename = "black.pnt"
output_filename = "file_decompressato.bin"

try:
    with open(input_filename, "rb") as f:
        f.seek(244)
        compressed_data_raw = f.read()

    decompressed_data = zlib.decompress(compressed_data_raw, -15)

    padding = len(decompressed_data) % 4
    if padding != 0:
        decompressed_data += b'\x00' * (4 - padding)

    flipped_data = bytearray()
    
    for i in range(0, len(decompressed_data), 4):
        chunk = decompressed_data[i:i+4]
        flipped_data.extend(chunk[::-1])

    # 4. Salvataggio
    with open(output_filename, "wb") as f_out:
        f_out.write(decompressed_data)
    
    print(f"Successo! File invertito e salvato come: {output_filename}")

except zlib.error as e:
    print(f"Errore durante la decompressione: {e}")
except Exception as e:
    print(f"Errore generico: {e}")