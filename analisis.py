import xml.etree.ElementTree as ET

xml_string = '''<?xml version="1.0"?>
<MENSAJES>
    <MENSAJE>
        <FECHA> Guatemala, 15/01/2023 15:25 hrs. </FECHA>
        <TEXTO> Bienvenido a USAC @estudiante01 @estudiante02,
            enojo Neg malo
            #bienvenidaUSAC#
        </TEXTO>
    </MENSAJE>
    <MENSAJE>
        <FECHA> Guatemala, 15/01/2023 15:25 hrs. </FECHA>
        <TEXTO> SEGUNDO TUIT @natalia_1 @estudiante02,
            PROBANDO EL 2 HASHTAG #SEGUNDO# Satisfecho  pos
            #bienvenidaUSAC#
        </TEXTO>
    </MENSAJE>
    <MENSAJE>
        <FECHA> Guatemala, 08/08/2023 15:25 hrs. </FECHA>
        <TEXTO> Bienvenido a USAC @tercertuit @cuartous,hola
            estoy probando el 3 hastag TERCER TUIT bueno pos
        </TEXTO>
    </MENSAJE>
    <MENSAJE>
        <FECHA> Guatemala, 02/10/2023 15:25 hrs. </FECHA>
        <TEXTO> CUARTO TUIT @tercertuit gdkgjkldjgd,bueno
            PROBANDO malo cool N #ultimoPrueba# hhkakkahh @ultimousuario
        </TEXTO>
    </MENSAJE>
</MENSAJES>'''


root = ET.fromstring(xml_string)

stored_data = {}


for mensaje in root.findall('MENSAJE'):
    fecha = mensaje.find('FECHA').text.split(',')[1].strip()[:10]
    texto = mensaje.find('TEXTO').text
    users = set()
    hashtags = set()

    words = texto.split()
    for word in words:
        if word.startswith('@'):
            users.add(word[1:])
        elif word.startswith('#') and word.endswith('#'):
            hashtags.add(word[1:-1])

    if fecha in stored_data:
        stored_data[fecha]['messages'] += 1
        stored_data[fecha]['users'] |= users
        stored_data[fecha]['hashtags'] |= hashtags
    else:
        stored_data[fecha] = {'messages': 1, 'users': users, 'hashtags': hashtags}


def get_info_for_date(date_to_check):
    if date_to_check in stored_data:
        users = stored_data[date_to_check]['users']
        hashtags = stored_data[date_to_check]['hashtags']
        user_counts = {user: 0 for user in users}
        hashtag_counts = {hashtag: 0 for hashtag in hashtags}

        for mensaje in root.findall('MENSAJE'):
            fecha = mensaje.find('FECHA').text.split(',')[1].strip()[:10]
            if fecha == date_to_check:
                texto = mensaje.find('TEXTO').text
                words = texto.split()
                for word in words:
                    if word.startswith('@') and word[1:] in user_counts:
                        user_counts[word[1:]] += 1
                    elif word.startswith('#') and word.endswith('#') and word[1:-1] in hashtag_counts:
                        hashtag_counts[word[1:-1]] += 1

        return users, user_counts, hashtags, hashtag_counts
    else:
        return set(), {}, set(), {}


date_to_check = '15/01/2023'
users, user_counts, hashtags, hashtag_counts = get_info_for_date(date_to_check)

if users:
    print(f"USUARIOS DE LA FECHA: {date_to_check}: {', '.join(users)}")
    print(f"numero de menciones: {len(users)}")
    print("usuarios:")
    for user, count in user_counts.items():
        print(f"{user}: {count}")
else:
    print(f"sin usuarios mencionados en la fecha: {date_to_check}.")

if hashtags:
    print(f"Hashtags usados en {date_to_check}: {', '.join(hashtags)}")
    print(f"numero de menciones: {len(hashtags)}")
    print("Hashtag:")
    for hashtag, count in hashtag_counts.items():
        print(f"#{hashtag}#: {count}")
else:
    print(f"sin usuarios mencionados en la fecha: {date_to_check}.")