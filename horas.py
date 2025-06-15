import re

def normalizaHoras(ficEntrada, ficSalida):
    formato_hora = [
        # Formato HH:MM
        (r'\b(\d{1,2}):(\d{2})\b', lambda h, m: f'{int(h):02}:{int(m):02}' if 0 <= int(h) < 24 and 0 <= int(m) < 60 else f'{h}:{m}'),

        # Formato con letras: 9h45m
        (r'\b(\d{1,2})h(\d{1,2})m\b', lambda h, m: f'{int(h):02}:{int(m):02}' if 0 <= int(h) < 24 and 0 <= int(m) < 60 else f'{h}h{m}m'),

        # Formato simple con h: 6h
        (r'\b(\d{1,2})h\b', lambda h: f'{int(h):02}:00' if 0 <= int(h) < 24 else f'{h}h'),

        # Expresiones tipicas
        (r'\b(\d{1,2}) en punto\b', lambda h: f'{int(h) % 12 or 12:02}:00'),
        (r'\b(\d{1,2}) y media\b', lambda h: f'{int(h) % 12 or 12:02}:30'),
        (r'\b(\d{1,2}) y cuarto\b', lambda h: f'{int(h) % 12 or 12:02}:15'),
        (r'\b(\d{1,2}) menos cuarto\b', lambda h: f'{(int(h) - 1) % 12 or 12:02}:45'),
        (r'\b(\d{1,2}) y media de la tarde\b', lambda h: f'{(int(h) + 12) % 24:02}:30'),
        (r'\b(\d{1,2}) y cuarto de la tarde\b', lambda h: f'{(int(h) + 12) % 24:02}:15'),
        (r'\b(\d{1,2}) menos cuarto de la tarde\b', lambda h: f'{(int(h) + 11) % 24:02}:45'),

        # Hora de la mañana
        (r'\b(\d{1,2})h de la mañana\b', lambda h: f'{int(h) % 12:02}:00'),

        # Medianoche
        (r'\b12 de la noche\b', lambda: '00:00')
    ]

    with open(ficEntrada, 'r', encoding='utf-8') as origen, open(ficSalida, 'w', encoding='utf-8') as destino:
        for linea in origen:
            linea_original = linea
            for patron, transformador in formato_hora:
                def reemplazo(match):
                    try:
                        return transformador(*match.groups())
                    except:
                        return match.group(0)
                linea = re.sub(patron, reemplazo, linea)
            destino.write(linea)

if __name__ == "__main__":
    normalizaHoras("horas.txt", "horasCorrectas.txt")