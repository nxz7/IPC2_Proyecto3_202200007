import base64
from flask import Flask, request, jsonify
from flask_cors import CORS
import xml.etree.ElementTree as ET
import xml.dom.minidom

app = Flask(__name__)
CORS(app)

stored_data = {}

@app.route("/")
def index():
    return "<h1> PRUEBA FLASK!!! </h1>"

def get_info_for_date(date_to_check):
    if date_to_check in stored_data:
        users = stored_data[date_to_check]['users']
        hashtags = stored_data[date_to_check]['hashtags']
        user_counts = {user: 0 for user in users}
        hashtag_counts = {hashtag: 0 for hashtag in hashtags}

        for mensaje in stored_data[date_to_check]['messages']:
            texto = mensaje['text']
            for word in texto.split():
                if word.startswith('@') and word[1:] in user_counts:
                    user_counts[word[1:]] += 1
                elif word.startswith('#') and word.endswith('#') and word[1:-1] in hashtag_counts:
                    hashtag_counts[word[1:-1]] += 1

        return users, user_counts, hashtags, hashtag_counts
    else:
        return set(), {}, set(), {}

@app.route('/cargarXml', methods=['POST'])
def cargar_xml():
    data = request.get_json()
    if 'xml' not in data:
        return jsonify({'error': 'FORMATO INVALIDO >>  Expected JSON object with "xml" field.'}), 400
    try:
        xml_string = base64.b64decode(data['xml']).decode('utf-8')
        xml_root = ET.fromstring(xml_string)
        global stored_data
        stored_data = {}
        for mensaje in xml_root.findall('MENSAJE'):
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
                stored_data[fecha]['messages'].append({'text': texto})
                stored_data[fecha]['users'] |= users
                stored_data[fecha]['hashtags'] |= hashtags
            else:
                stored_data[fecha] = {'messages': [{'text': texto}], 'users': users, 'hashtags': hashtags}

        # HACER EL DE SALIDA DE UNA
        xml_output = ET.Element('MENSAJES_RECIBIDOS')
        for date, data in stored_data.items():
            tiempo = ET.SubElement(xml_output, 'TIEMPO')
            fecha_element = ET.SubElement(tiempo, 'FECHA')
            fecha_element.text = date
            mensajes_recibidos = ET.SubElement(tiempo, 'MSJ_RECIBIDOS')
            mensajes_recibidos.text = str(len(data['messages']))
            usuarios_mencionados = ET.SubElement(tiempo, 'USR_MENCIONADOS')
            usuarios_mencionados.text = str(len(data['users']))
            hashtags_incluidos = ET.SubElement(tiempo, 'HASH_INCLUIDOS')
            hashtags_incluidos.text = str(len(data['hashtags']))

        xmlstr = xml.dom.minidom.parseString(ET.tostring(xml_output)).toprettyxml(indent="    ")
        with open("resumenMensajes.xml", "w") as f:
            f.write(xmlstr)

        return jsonify({'message': 'XML CARGADO Y ANALIZADO CON EXITO >>> resumen de mensajes creado.'}), 200
    except Exception as e:
        return jsonify({'error': f'Error procesando el XML: {str(e)}'}), 500


#---------- USUARIOS
@app.route('/devolverUsuarios', methods=['GET'])
def devolver_usuarios():
    date_to_check = request.args.get('date')
    if not date_to_check:
        return jsonify({'error': 'No selecciono fecha.'}), 400

    users, user_counts, _, _ = get_info_for_date(date_to_check)

    if users:
        return jsonify({'Menciones': list(users), 'user_cuenta': user_counts}), 200
    else:
        return jsonify({'message': f'No hay users mencionados: {date_to_check}.'}), 404


#----------HASHTAGS
@app.route('/devolverHashtags', methods=['GET'])
def devolver_hashtags():
    date_to_check = request.args.get('date')
    if not date_to_check:
        return jsonify({'error': 'No selecciono fecha.'}), 400

    _, _, hashtags, hashtag_counts = get_info_for_date(date_to_check)

    if hashtags:
        return jsonify({'hashtags': list(hashtags), 'hashtag_cuenta': hashtag_counts}), 200
    else:
        return jsonify({'message': f'No hay hashtags mencionados: {date_to_check}.'}), 404

if __name__ == '__main__':
    app.run(threaded=True, port=5000, debug=True)
