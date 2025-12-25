import zlib
import struct

input_filename = "black.pnt"
output_filename = "file_decompressato.bin"

try:
    with open(input_filename, "rb") as f:
        # 1. Salta i primi 244 byte
        f.seek(244)
        compressed_data_raw = f.read()

    # 2. Decompressione (usando -15 per raw DEFLATE)
    decompressed_data = zlib.decompress(compressed_data_raw, -15)

    # 3. Flip dei byte a gruppi di 4 (Little-endian <-> Big-endian)
    # Verifichiamo che la lunghezza sia multipla di 4 per evitare errori
    padding = len(decompressed_data) % 4
    if padding != 0:
        # Se non è multiplo, aggiungiamo dei byte nulli o gestiamo il rimasuglio
        decompressed_data += b'\x00' * (4 - padding)

    flipped_data = bytearray()
    
    # Iteriamo i dati a salti di 4 byte
    for i in range(0, len(decompressed_data), 4):
        chunk = decompressed_data[i:i+4]
        # Invertiamo l'ordine dei 4 byte: [0, 1, 2, 3] -> [3, 2, 1, 0]
        flipped_data.extend(chunk[::-1])

    # 4. Salvataggio
    with open(output_filename, "wb") as f_out:
        f_out.write(decompressed_data)
    
    print(f"Successo! File invertito e salvato come: {output_filename}")

except zlib.error as e:
    print(f"Errore durante la decompressione: {e}")
except Exception as e:
    print(f"Errore generico: {e}")