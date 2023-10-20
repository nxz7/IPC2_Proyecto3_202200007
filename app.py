import base64
from flask import Flask, request, jsonify
from flask_cors import CORS
import xml.etree.ElementTree as ET
import xml.dom.minidom
from XmlHandler import XMLHandler

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

#----------------------------------- CARGAR EL XML DE BASE ----------------------------

@app.route('/cargarXml', methods=['POST'])
def cargar_xml():
    if 'file' not in request.files:
        return jsonify({'error': 'FORMATO INVALIDO >>  Expected XML file.'}), 400
    try:
        xml_file = request.files['file']
        xml_string = xml_file.read().decode('utf-8')
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
        print(xml_string)
        XMLHandler.generate_xml(stored_data)

        return jsonify({'message': 'XML CARGADO Y ANALIZADO CON EXITO >>> resumen de mensajes creado.'}), 200
    except Exception as e:
        return jsonify({'error': f'Error procesando el XML: {str(e)}'}), 500


#-------------------------------------- USUARIOS ------------------------------------------
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


#-------------------------------------- HASHTAGS ------------------------------------------
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

#---------------------------- DICCIONARIO POS/NEG ------------------------------------------
pos = []
neg = []

@app.route('/almacenarInfoXml', methods=['POST'])
def almacenar_info_xml():
    if 'xml' not in request.files:
        return jsonify({'error': 'FORMATO INVALIDO >>  No file part in the request.'}), 400

    try:
        xml_file = request.files['xml']
        xml_string = xml_file.read().decode('utf-8')
        xml_root = ET.fromstring(xml_string)

        global pos, neg

        for word in xml_root.find('sentimientos_positivos'):
            pos.append(word.text.strip())
        
        for word in xml_root.find('sentimientos_negativos'):
            neg.append(word.text.strip())
        print("diccionario cargado")
        XMLHandler.generate_configxml(pos, neg)
        return jsonify({'positivas': pos, 'negativas': neg}), 200
    except Exception as e:
        return jsonify({'error': f'Error procesando el XML: {str(e)}'}), 500

#--------------------------- clasificar mensajes positivo/negativo -------------------------
@app.route('/clasificarMensajes', methods=['GET'])
def clasificar_mensajes():
    date_to_check = request.args.get('date')
    if not date_to_check:
        return jsonify({'error': 'No selecciono fecha.'}), 400

    if date_to_check not in stored_data:
        return jsonify({'message': f'No hay mensajes para la fecha: {date_to_check}.'}), 404

    cuenta_positivos = 0
    cuenta_neg = 0
    cuenta_neutral = 0

    global pos, neg

    for message_data in stored_data[date_to_check]['messages']:
        message_text = message_data['text']
        cuenta_palabras_positivos = sum(message_text.count(word) for word in pos)
        cuenta_palabras_neg = sum(message_text.count(word) for word in neg)
#CLASIFICACION >>>>>>>>
        if cuenta_palabras_positivos > cuenta_palabras_neg:
            cuenta_positivos += 1
        elif cuenta_palabras_neg > cuenta_palabras_positivos:
            cuenta_neg += 1
        else:
            cuenta_neutral += 1

    return jsonify({'mensajes_positivos': cuenta_positivos, 'mensajes_negativos': cuenta_neg, 'mensajes_neutros': cuenta_neutral}), 200

#-------------------------------------------------
@app.route('/clearData', methods=['POST'])
def clear_data():
    global stored_data, pos, neg
    stored_data = {}
    pos = []
    neg = []
    print(stored_data)
    return jsonify({'message': 'Data cleared successfully.'}), 200


if __name__ == '__main__':
    app.run(threaded=True, port=5000, debug=True)
