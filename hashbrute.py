#!/usr/bin/env python3
"""
Hash Cracker - Cracker de hashes MD5, SHA1, SHA256
CREADOR: phishbroker
CONTACTO: https://x.com/phishbroker
"""

import hashlib
import argparse
import sys
from pathlib import Path
import time

class HashCracker:
    
    ALGORITHMS = {
        'md5': hashlib.md5,
        'sha1': hashlib.sha1,
        'sha256': hashlib.sha256,
        'sha512': hashlib.sha512
    }
    
    def __init__(self, hash_value, algorithm='md5', wordlist=None):
        self.hash_value = hash_value.lower()
        self.algorithm = algorithm.lower()
        self.wordlist = wordlist
        self.attempts = 0
        
        if self.algorithm not in self.ALGORITHMS:
            raise ValueError(f"Algoritmo no soportado: {algorithm}")
    
    def hash_string(self, text):
        """
        Genera el hash de un string usando el algoritmo especificado
        """
        hash_func = self.ALGORITHMS[self.algorithm]
        return hash_func(text.encode('utf-8')).hexdigest()
    
    def crack_with_wordlist(self):
        """
        Intenta crackear el hash usando un wordlist
        """
        if not self.wordlist or not Path(self.wordlist).exists():
            print(f"[-] Error: Wordlist no encontrado: {self.wordlist}")
            return None
        
        print(f"[*] Iniciando ataque de diccionario...")
        print(f"[*] Hash: {self.hash_value}")
        print(f"[*] Algoritmo: {self.algorithm.upper()}")
        print(f"[*] Wordlist: {self.wordlist}\n")
        
        start_time = time.time()
        
        with open(self.wordlist, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                password = line.strip()
                self.attempts += 1
                
                if self.attempts % 10000 == 0:
                    print(f"[*] Intentos: {self.attempts:,}")
                
                if self.hash_string(password) == self.hash_value:
                    elapsed = time.time() - start_time
                    print(f"\n[+] ¡HASH CRACKEADO!")
                    print(f"[+] Password: {password}")
                    print(f"[+] Intentos: {self.attempts:,}")
                    print(f"[+] Tiempo: {elapsed:.2f} segundos")
                    return password
        
        elapsed = time.time() - start_time
        print(f"\n[-] Hash no encontrado")
        print(f"[-] Intentos totales: {self.attempts:,}")
        print(f"[-] Tiempo: {elapsed:.2f} segundos")
        return None
    
    def brute_force(self, max_length=4, charset='abcdefghijklmnopqrstuvwxyz0123456789'):
        """
        Ataque de fuerza bruta (solo para hashes débiles)
        """
        print(f"[!] ADVERTENCIA: Fuerza bruta puede tomar mucho tiempo")
        print(f"[*] Longitud máxima: {max_length}")
        print(f"[*] Charset: {charset}\n")
        
        from itertools import product
        
        start_time = time.time()
        
        for length in range(1, max_length + 1):
            print(f"[*] Probando combinaciones de longitud {length}...")
            
            for combo in product(charset, repeat=length):
                password = ''.join(combo)
                self.attempts += 1
                
                if self.attempts % 10000 == 0:
                    print(f"[*] Intentos: {self.attempts:,}")
                
                if self.hash_string(password) == self.hash_value:
                    elapsed = time.time() - start_time
                    print(f"\n[+] ¡HASH CRACKEADO!")
                    print(f"[+] Password: {password}")
                    print(f"[+] Intentos: {self.attempts:,}")
                    print(f"[+] Tiempo: {elapsed:.2f} segundos")
                    return password
        
        elapsed = time.time() - start_time
        print(f"\n[-] Hash no encontrado")
        print(f"[-] Intentos totales: {self.attempts:,}")
        print(f"[-] Tiempo: {elapsed:.2f} segundos")
        return None

def create_sample_wordlist():
    """
    Crea un wordlist de muestra con passwords comunes
    """
    common_passwords = [
        'password', '123456', '12345678', 'qwerty', 'abc123', 'monkey',
        'letmein', 'trustno1', 'dragon', 'baseball', 'iloveyou', 'master',
        'sunshine', 'ashley', 'bailey', 'passw0rd', 'shadow', '123123',
        '654321', 'superman', 'qazwsx', 'michael', 'football', 'password1',
        '123456789', 'password123', 'admin', 'root', 'toor', 'administrator',
        'welcome', 'login', 'guest', 'test', 'oracle', 'cisco', 'linux',
        'windows', 'default', 'changeme', 'letmein', 'passw0rd', 'P@ssw0rd',
        'admin123', 'root123', 'qwerty123', 'welcome123', 'pass123'
    ]
    
    wordlist_file = 'passwords.txt'
    with open(wordlist_file, 'w') as f:
        for pwd in common_passwords:
            f.write(f"{pwd}\n")
    
    return wordlist_file

def main():
    parser = argparse.ArgumentParser(
        description='Hash Cracker by phishbroker',
        epilog='CREADOR: phishbroker | CONTACTO: phishbroker@proton.me',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument('hash', help='Hash a crackear')
    parser.add_argument('-a', '--algorithm', 
                       choices=['md5', 'sha1', 'sha256', 'sha512'],
                       default='md5',
                       help='Algoritmo de hash (default: md5)')
    parser.add_argument('-w', '--wordlist', 
                       help='Archivo wordlist para ataque de diccionario')
    parser.add_argument('-b', '--brute-force', action='store_true',
                       help='Usar fuerza bruta')
    parser.add_argument('-l', '--length', type=int, default=4,
                       help='Longitud máxima para fuerza bruta (default: 4)')
    parser.add_argument('-c', '--charset', 
                       default='abcdefghijklmnopqrstuvwxyz0123456789',
                       help='Charset para fuerza bruta')
    
    args = parser.parse_args()
    
    print("="*70)
    print("HASH CRACKER")
    print(f"CREADOR: phishbroker")
    print(f"CONTACTO: phishbroker@proton.me")
    print("="*70 + "\n")
    
    cracker = HashCracker(args.hash, args.algorithm, args.wordlist)
    
    if args.brute_force:
        cracker.brute_force(args.length, args.charset)
    else:
        if not args.wordlist:
            print("[!] No se especificó wordlist, usando diccionario básico...")
            args.wordlist = create_sample_wordlist()
            cracker.wordlist = args.wordlist
        
        cracker.crack_with_wordlist()

if __name__ == "__main__":
    main()
