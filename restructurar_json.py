import os
import json

# ¡MUY IMPORTANTE! La ruta a tu carpeta de idiomas.
# Asume que el script está en la raíz del proyecto.
LANG_DIR = os.path.join('static', 'json', 'lang')

# Lista de claves que se moverán a la sección "common" (extraída de tus logs).
COMMON_KEYS = [
    "header_title", "home", "mi_cv", "work_exp", "tech", "edu",
    "lang", "int", "have_fun", "keyphrase", "seasonality",
    "whatsapp", "world_bank", "read", "algo_trad", "lin_alg",
    "macro", "ds_trends", "vector_norms"
]

def restructurar_json_files():
    # Primero, verifica si el directorio existe
    if not os.path.isdir(LANG_DIR):
        print(f"Error: El directorio '{LANG_DIR}' no fue encontrado.")
        print("Asegúrate de que el script se está ejecutando desde la carpeta raíz de tu proyecto.")
        return

    # Obtiene la lista de todos los archivos .json en el directorio
    json_files = [f for f in os.listdir(LANG_DIR) if f.endswith('.json')]

    if not json_files:
        print(f"No se encontraron archivos .json en '{LANG_DIR}'.")
        return

    print(f"Procesando {len(json_files)} archivos de idioma...")

    # Itera sobre cada archivo de idioma
    for filename in json_files:
        filepath = os.path.join(LANG_DIR, filename)
        
        try:
            # Abre y lee el contenido del JSON original
            with open(filepath, 'r', encoding='utf-8') as f:
                original_data = json.load(f)

            # Prepara la nueva estructura con una sección "common"
            new_data = {"common": {}}
            
            # Recorre todas las secciones del archivo original (ej: "mi_cv", "home", etc.)
            for page_key, translations in original_data.items():
                
                # Crea la sección de la página en la nueva estructura si no es "common"
                if page_key not in new_data:
                    new_data[page_key] = {}
                
                # Recorre cada par clave-valor de traducción
                for key, value in translations.items():
                    if key in COMMON_KEYS:
                        # Si es una clave común, la movemos a la sección "common"
                        new_data["common"][key] = value
                    else:
                        # Si no, la dejamos en su sección de página original
                        new_data[page_key][key] = value

            # Sobrescribe el archivo original con la nueva estructura
            with open(filepath, 'w', encoding='utf-8') as f:
                # json.dump escribe el diccionario en el archivo con formato bonito
                # indent=2 para que sea legible, ensure_ascii=False para caracteres especiales
                json.dump(new_data, f, indent=2, ensure_ascii=False)
            
            print(f"  - Archivo '{filename}' reestructurado con éxito.")

        except Exception as e:
            print(f"  - ERROR al procesar el archivo '{filename}': {e}")
            
    print("\n¡Proceso completado!")

# ¡Asegúrate de hacer una copia de seguridad antes de ejecutar!
print("--- Script de Reestructuración de JSON ---")
print(f"Este script modificará los archivos en la carpeta: {LANG_DIR}")
backup_confirm = input("¿Has hecho una copia de seguridad de la carpeta? (s/n): ")

if backup_confirm.lower() == 's':
    restructurar_json_files()
else:
    print("Operación cancelada. Por favor, haz una copia de seguridad y vuelve a intentarlo.")