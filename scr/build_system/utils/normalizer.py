#!/usr/bin/env python3
"""
Utilitário de Normalização de Nomes
=================================
Funções para normalizar nomes de arquivos e diretórios.

Autor: Sistema Build  
Data: Setembro 2025
"""

import re
from pathlib import Path

def normalize_filename(name):
    """
    Normaliza nome do arquivo para comparação e uso interno.
    
    Args:
        name (str): Nome original do arquivo
        
    Returns:
        str: Nome normalizado
    """
    # Remove extensão se houver
    if '.' in name:
        name = Path(name).stem
        
    # Converte para minúsculas
    name = name.lower()
    
    # Mapeamento de caracteres acentuados
    char_map = {
        'ã': 'a', 'á': 'a', 'à': 'a', 'â': 'a', 'ä': 'a',
        'é': 'e', 'ê': 'e', 'è': 'e', 'ë': 'e',
        'í': 'i', 'î': 'i', 'ì': 'i', 'ï': 'i',
        'ó': 'o', 'ô': 'o', 'õ': 'o', 'ò': 'o', 'ö': 'o',
        'ú': 'u', 'û': 'u', 'ù': 'u', 'ü': 'u',
        'ç': 'c', 'ñ': 'n'
    }
    
    # Aplica mapeamento
    for old_char, new_char in char_map.items():
        name = name.replace(old_char, new_char)
    
    # Remove caracteres especiais e substitui por underscore
    name = re.sub(r'[^a-z0-9_]', '_', name)
    
    # Remove underscores múltiplos
    name = re.sub(r'_+', '_', name)
    
    # Remove underscores no início e fim
    name = name.strip('_')
    
    return name

def extract_date_from_filename(filename):
    """
    Extrai data do nome do arquivo no formato YYYY_MM_DD.
    
    Args:
        filename (str): Nome do arquivo
        
    Returns:
        tuple: (ano, mês, dia) ou None se não encontrar
    """
    date_pattern = r'^(\d{4})_(\d{2})_(\d{2})_'
    match = re.match(date_pattern, filename)
    
    if match:
        year, month, day = match.groups()
        return int(year), int(month), int(day)
    
    return None

def extract_title_from_filename(filename):
    """
    Extrai título do nome do arquivo removendo data e extensão.
    
    Args:
        filename (str): Nome do arquivo
        
    Returns:
        str: Título extraído e formatado
    """
    # Remove extensão
    name = Path(filename).stem
    
    # Remove data do início se existir
    name = re.sub(r'^\d{4}_\d{2}_\d{2}_', '', name)
    
    # Substitui underscores por espaços
    title = name.replace('_', ' ')
    
    # Capitaliza primeira letra de cada palavra
    title = ' '.join(word.capitalize() for word in title.split())
    
    return title

def generate_slug(title):
    """
    Gera slug a partir do título.
    
    Args:
        title (str): Título do artigo
        
    Returns:
        str: Slug normalizado
    """
    return normalize_filename(title)

def safe_filename(filename):
    """
    Cria um nome de arquivo seguro para o sistema de arquivos.
    
    Args:
        filename (str): Nome original
        
    Returns:
        str: Nome de arquivo seguro
    """
    # Mantém extensão se houver
    path = Path(filename)
    name = path.stem
    extension = path.suffix
    
    # Normaliza apenas o nome
    safe_name = normalize_filename(name)
    
    return f"{safe_name}{extension}" if extension else safe_name
