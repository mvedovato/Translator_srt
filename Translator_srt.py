import os
import sys
from deep_translator import GoogleTranslator

BLOCK_SIZE = 20
def print_banner():
    print("""
    ================================================
    🚀 Script de Traducción SRT a Español con Google Translate
    ================================================
    Usage: python3 Translator_srt.py archivo.srt
    Bloques de traducción: """ + str(BLOCK_SIZE))
    print("""
    ===============================================\n""")
    
def detect_file_type(filename):
    _, ext = os.path.splitext(filename)
    if ext.lower() == ".srt":
        return "srt"
    return "txt"

def translate_block(text_block, src_lang="en", dest_lang="es"):
    try:
        translation = GoogleTranslator(source=src_lang, target=dest_lang).translate(text_block)
        if translation is None:
            print(f"⚠️ Aviso: La traducción devolvió None para:\n{text_block}\nSe conservará el original.\n")
            return text_block
        return translation
    except Exception as e:
        print(f"❌ Error durante la traducción: {e}")
        return text_block

def translate_srt_file_in_blocks(input_file, output_file, block_size=BLOCK_SIZE):
    try:
        with open(input_file, "r", encoding="utf-8") as f:
            lines = f.readlines()

        translated_lines = []
        block = []
        block_counter = 0

        for line in lines:
            if line.strip() == "":
                # Fin de un bloque (subtítulo completo), agregamos al bloque actual
                block.append(line)
                block_counter += 1

                if block_counter == block_size:
                    # Traducir el bloque de diálogos
                    translated_block = process_block(block)
                    translated_lines.extend(translated_block)
                    block = []
                    block_counter = 0
            else:
                block.append(line)

        # Traducir cualquier bloque restante
        if block:
            translated_block = process_block(block)
            translated_lines.extend(translated_block)

        # Guardar el archivo traducido
        with open(output_file, "w", encoding="utf-8") as f:
            f.writelines(translated_lines)

        print(f"✅ Traducción completada. Archivo guardado en {output_file}")

    except FileNotFoundError:
        print(f"❌ Error: No se encontró el archivo {input_file}")
    except Exception as e:
        print(f"❌ Error: {e}")

def process_block(block_lines):
    """
    Toma un bloque de subtítulos, extrae solo los textos (sin timestamps),
    los traduce en lote y reconstruye el bloque con los timestamps intactos.
    """
    dialogue_lines = []
    timestamp_lines = []
    final_block = []

    for line in block_lines:
        if "-->" in line or line.strip().isdigit() or line.strip() == "":
            # Timestamps, numeración o líneas en blanco
            timestamp_lines.append(line)
        else:
            dialogue_lines.append(line.strip())

    # Unimos las líneas de diálogo para traducirlas como un solo bloque
    combined_text = "\n".join(dialogue_lines)

    if combined_text.strip():
        translated_text = translate_block(combined_text)
        translated_lines = translated_text.split("\n")
    else:
        translated_lines = dialogue_lines  # No hay diálogo que traducir

    # Reconstruir el bloque con timestamps intactos y el texto traducido
    dialogue_index = 0
    for line in block_lines:
        if "-->" in line or line.strip().isdigit() or line.strip() == "":
            final_block.append(line)  # Dejamos igual timestamps y numeración
        else:
            final_block.append(translated_lines[dialogue_index] + "\n")
            dialogue_index += 1

    return final_block

if __name__ == "__main__":
    print_banner()
    if len(sys.argv) != 2:
        print("Uso: python3 Translator.py archivo.srt")
        sys.exit(1)

    input_file = sys.argv[1]
    file_type = detect_file_type(input_file)

    if file_type == "srt":
        print(f"📄 Detectado archivo SRT: {input_file}")
        output_file = input_file.replace(".srt", "_es.srt")
        translate_srt_file_in_blocks(input_file, output_file, block_size=BLOCK_SIZE)
    else:
        print("⚠️ Este script está preparado solo para archivos SRT por ahora.")
        sys.exit(1)

