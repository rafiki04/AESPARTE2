def imprimir_bytes(titulo, datos, ancho_hex=16):
    print(f"\n{titulo}:")
    for i in range(0, len(datos), ancho_hex):
        trozo = datos[i:i+ancho_hex]
        cadena_hex = ' '.join(f"{byte:02x}" for byte in trozo)
        print(cadena_hex)


S_BOX = [0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76,
    0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0,
    0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15,
    0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75,
    0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84,
    0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf,
    0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8,
    0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2,
    0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73,
    0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb,
    0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79,
    0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08,
    0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a,
    0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e,
    0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf,
    0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16
]

RCON = [0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36]

MATRIZ_MEZCLA_COLUMNAS = [
    [0x02, 0x03, 0x01, 0x01],
    [0x01, 0x02, 0x03, 0x01],
    [0x01, 0x01, 0x02, 0x03],
    [0x03, 0x01, 0x01, 0x02]
]

def sustituir_bytes(estado):
    
    print("\nSubBytes:")
    for i in range(len(estado)):
        for j in range(len(estado[i])):
            estado[i][j] = S_BOX[estado[i][j]]
            print(f"estado[{i}][{j}] = {estado[i][j]:02x}")
    return estado

def desplazar_filas(estado):
    """Desplaza las filas del estado según el algoritmo AES"""
    print("\nShiftRows:")
    # Fila 0: no se desplaza
    # Fila 1: desplazamiento de 1 byte
    estado[1][0], estado[1][1], estado[1][2], estado[1][3] = estado[1][1], estado[1][2], estado[1][3], estado[1][0]
    # Fila 2: desplazamiento de 2 bytes
    estado[2][0], estado[2][1], estado[2][2], estado[2][3] = estado[2][2], estado[2][3], estado[2][0], estado[2][1]
    # Fila 3: desplazamiento de 3 bytes
    estado[3][0], estado[3][1], estado[3][2], estado[3][3] = estado[3][3], estado[3][0], estado[3][1], estado[3][2]
    
    for i in range(4):
        print(f"Fila {i}: {' '.join(f'{x:02x}' for x in estado[i])}")
    return estado

def multiplicacion_galois(a, b):
    """Multiplicación en el campo Galois GF(2^8)"""
    p = 0
    for _ in range(8):
        if b & 1:
            p ^= a
        bit_alto = a & 0x80
        a <<= 1
        if bit_alto:
            a ^= 0x1b  # Polinomio irreducible x^8 + x^4 + x^3 + x + 1
        b >>= 1
    return p % 256

def mezclar_columnas(estado):
    """multiplicación matricial en GF(2^8)"""
    print("\nMixColumns:")
    nuevo_estado = [[0 for _ in range(4)] for _ in range(4)]
    for i in range(4):
        for j in range(4):
            nuevo_estado[j][i] = (
                multiplicacion_galois(MATRIZ_MEZCLA_COLUMNAS[j][0], estado[0][i]) ^
                multiplicacion_galois(MATRIZ_MEZCLA_COLUMNAS[j][1], estado[1][i]) ^
                multiplicacion_galois(MATRIZ_MEZCLA_COLUMNAS[j][2], estado[2][i]) ^
                multiplicacion_galois(MATRIZ_MEZCLA_COLUMNAS[j][3], estado[3][i])
            )
            print(f"nuevo_estado[{j}][{i}] = {nuevo_estado[j][i]:02x}")
    return nuevo_estado

def añadir_clave_ronda(estado, clave_ronda):
   
    print("\nAddRoundKey:")
    for i in range(4):
        for j in range(4):
            estado[i][j] ^= clave_ronda[i][j]
            print(f"estado[{i}][{j}] ^= clave_ronda[{i}][{j}] = {estado[i][j]:02x}")
    return estado

def expansion_clave(clave):

    print("\nKey Expansion:")
    tamaño_clave = 16
    tamaño_clave_expandida = 176  # 16 * 11 (10 rondas + clave inicial)
    
    # Convertir la clave en una lista de bytes
    bytes_clave = list(clave)
    
    # Inicializar la clave expandida con la clave original
    clave_expandida = [0] * tamaño_clave_expandida
    for i in range(tamaño_clave):
        clave_expandida[i] = bytes_clave[i]
    
    # Variables para el algoritmo de expansión
    iteracion_rcon = 1
    bytes_generados = tamaño_clave
    
    while bytes_generados < tamaño_clave_expandida:
        # Obtener los 4 bytes anteriores
        temp = clave_expandida[bytes_generados-4:bytes_generados]
        
        # Realizar la operación de clave
        if bytes_generados % tamaño_clave == 0:
            # Rotar palabra
            temp = [temp[1], temp[2], temp[3], temp[0]]
            
            # Sustituir bytes usando S-box
            temp = [S_BOX[b] for b in temp]
            
            # XOR con Rcon
            temp[0] ^= RCON[iteracion_rcon-1]
            iteracion_rcon += 1
        
        # XOR con la palabra 16 bytes antes
        for i in range(4):
            clave_expandida[bytes_generados] = clave_expandida[bytes_generados - tamaño_clave] ^ temp[i]
            bytes_generados += 1
    
    # Convertir la clave expandida en claves de ronda (11 claves de 16 bytes)
    claves_ronda = []
    for i in range(11):
        clave_ronda = [[0 for _ in range(4)] for _ in range(4)]
        for j in range(4):
            for k in range(4):
                clave_ronda[k][j] = clave_expandida[i*16 + j*4 + k]
        claves_ronda.append(clave_ronda)
        print(f"\nClave de Ronda {i}:")
        for fila in clave_ronda:
            print(' '.join(f'{x:02x}' for x in fila))
    
    return claves_ronda

def bytes_a_estado(arreglo_bytes):
    """Convierte un array de 16 bytes en una matriz de estado 4x4"""
    estado = [[0 for _ in range(4)] for _ in range(4)]
    for i in range(4):
        for j in range(4):
            estado[j][i] = arreglo_bytes[i*4 + j]
    return estado

def estado_a_bytes(estado):
    """Convierte una matriz de estado 4x4 en un array de 16 bytes"""
    arreglo_bytes = [0] * 16
    for i in range(4):
        for j in range(4):
            arreglo_bytes[i*4 + j] = estado[j][i]
    return arreglo_bytes

def cifrar_bloque_aes(texto_plano, clave):
    """Cifra un bloque de 128 bits usando AES-128"""
    print("\nIniciando cifrado AES-128...")
    imprimir_bytes("Texto plano", texto_plano)
    imprimir_bytes("Clave", clave)
    
    # Expandir la clave
    claves_ronda = expansion_clave(clave)
    
    # Convertir el texto plano en estado
    estado = bytes_a_estado(texto_plano)
    
    print("\nEstado inicial:")
    for fila in estado:
        print(' '.join(f'{x:02x}' for x in fila))
    
    # Ronda inicial (solo AddRoundKey)
    print("\nRonda inicial:")
    estado = añadir_clave_ronda(estado, claves_ronda[0])
    
    # 9 rondas principales
    for numero_ronda in range(1, 10):
        print(f"\nRonda {numero_ronda}:")
        estado = sustituir_bytes(estado)
        estado = desplazar_filas(estado)
        estado = mezclar_columnas(estado)
        estado = añadir_clave_ronda(estado, claves_ronda[numero_ronda])
    
    # Ronda final (sin MixColumns)
    print("\nRonda final (10):")
    estado = sustituir_bytes(estado)
    estado = desplazar_filas(estado)
    estado = añadir_clave_ronda(estado, claves_ronda[10])
    
    # Convertir el estado a bytes
    texto_cifrado = estado_a_bytes(estado)
    imprimir_bytes("\nTexto cifrado resultante", texto_cifrado)
    
    return texto_cifrado

# Ejemplo de uso
if __name__ == "__main__":
    # Clave de 128 bits (16 bytes)
    clave = [0x2b, 0x7e, 0x15, 0x16, 0x28, 0xae, 0xd2, 0xa6, 
            0xab, 0xf7, 0x15, 0x88, 0x09, 0xcf, 0x4f, 0x3c]
    
    # Texto plano de 128 bits (16 bytes)
    texto_plano = [0x32, 0x43, 0xf6, 0xa8, 0x88, 0x5a, 0x30, 0x8d, 
                 0x31, 0x31, 0x98, 0xa2, 0xe0, 0x37, 0x07, 0x34]
    
    print("=== CIFRADO AES-128 ===")
    texto_cifrado = cifrar_bloque_aes(texto_plano, clave)
    
    print("\nResultado final:")
    print("Texto original:", ' '.join(f'{x:02x}' for x in texto_plano))
    print("Texto cifrado: ", ' '.join(f'{x:02x}' for x in texto_cifrado))