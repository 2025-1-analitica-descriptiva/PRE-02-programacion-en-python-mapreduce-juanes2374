"""Taller evaluable"""

# pylint: disable=broad-exception-raised

import fileinput
import glob
import os
import shutil
import time
from itertools import groupby


def copy_raw_files_to_input_folder(n):
    """
    Genera n copias de los archivos .txt en files/raw y las guarda en files/input
    con sufijos numerados.
    """
    input_dir = "files/raw"
    output_dir = "files/input"
    os.makedirs(output_dir, exist_ok=True)

    for filepath in glob.glob(os.path.join(input_dir, "*.txt")):
        filename = os.path.basename(filepath)
        with open(filepath, "r", encoding="utf-8") as file:
            content = file.read()
        for i in range(1, n + 1):
            new_filename = f"{os.path.splitext(filename)[0]}_{i}.txt"
            new_filepath = os.path.join(output_dir, new_filename)
            with open(new_filepath, "w", encoding="utf-8") as new_file:
                new_file.write(content)


def load_input(input_directory):
    """
    Lee todos los archivos de una carpeta y retorna una lista de tuplas
    (nombre_archivo, línea).
    """
    result = []
    for filepath in glob.glob(os.path.join(input_directory, "*.txt")):
        filename = os.path.basename(filepath)
        with open(filepath, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if line:
                    result.append((filename, line))
    return result


def line_preprocessing(sequence):
    """
    Preprocesa líneas separando palabras y devolviendo tuplas (archivo, palabra).
    """
    result = []
    for filename, line in sequence:
        words = line.strip().split()
        for word in words:
            cleaned = word.strip('.,:;!?()[]{}"\'').lower()
            if cleaned:
                result.append((filename, cleaned))
    return result


def mapper(sequence):
    """
    Convierte (archivo, palabra) en (palabra, 1) para contar.
    """
    return [(word, 1) for _, word in sequence]


def shuffle_and_sort(sequence):
    """
    Ordena por palabra clave para agrupar fácilmente.
    """
    return sorted(sequence, key=lambda x: x[0])


def reducer(sequence):
    """
    Reduce la lista ordenada sumando valores por clave (palabra).
    """
    result = []
    for key, group in groupby(sequence, key=lambda x: x[0]):
        total = sum(value for _, value in group)
        result.append((key, total))
    return result


def create_ouptput_directory(output_directory):
    """
    Crea el directorio de salida, eliminando si ya existe.
    """
    if os.path.exists(output_directory):
        shutil.rmtree(output_directory)
    os.makedirs(output_directory)


def save_output(output_directory, sequence):
    """
    Guarda el resultado del reducer en un archivo llamado part-00000,
    con formato: palabra \t cantidad.
    """
    filepath = os.path.join(output_directory, "part-00000")
    with open(filepath, "w", encoding="utf-8") as file:
        for key, value in sequence:
            file.write(f"{key}\t{value}\n")


def create_marker(output_directory):
    """
    Crea el archivo _SUCCESS en el directorio de salida.
    """
    open(os.path.join(output_directory, "_SUCCESS"), "w").close()


def run_job(input_directory, output_directory):
    """
    Ejecuta todas las funciones en orden lógico.
    """
    create_ouptput_directory(output_directory)
    data = load_input(input_directory)
    processed = line_preprocessing(data)
    mapped = mapper(processed)
    sorted_data = shuffle_and_sort(mapped)
    reduced = reducer(sorted_data)
    save_output(output_directory, reduced)
    create_marker(output_directory)


if __name__ == "__main__":

    copy_raw_files_to_input_folder(n=1000)

    start_time = time.time()

    run_job(
        "files/input",
        "files/output",
    )

    end_time = time.time()
    print(f"Tiempo de ejecución: {end_time - start_time:.2f} segundos")
