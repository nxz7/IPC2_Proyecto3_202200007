import xml.etree.ElementTree as ET
import xml.dom.minidom

class XMLHandler:
    @staticmethod
    def generate_xml(stored_data):
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

    def generate_configxml(pos, neg):
        try:
            positive_set = set(pos)
            negative_set = set(neg)
            common_elements = positive_set.intersection(negative_set)

            positive_counter = len(positive_set) - len(common_elements)
            negative_counter = len(negative_set) - len(common_elements)
            neutro_counter = len(common_elements)

            root = ET.Element("CONFIG_RECIBIDA")
            ET.SubElement(root, "PALABRAS_POSITIVAS").text = str(positive_counter)
            ET.SubElement(root, "PALABRAS_POSITIVAS_RECHAZADA").text = str(neutro_counter)
            ET.SubElement(root, "PALABRAS_NEGATIVAS").text = str(negative_counter)
            ET.SubElement(root, "PALABRAS_NEGATIVAS_RECHAZADA").text = str(neutro_counter)

            rough_string = ET.tostring(root, 'utf-8')
            reparsed = xml.dom.minidom.parseString(rough_string)
            with open("resumenConfig.xml", "w") as f:
                f.write(reparsed.toprettyxml(indent="\t"))

            return True, 'Archivo XML creado exitosamente.'
        except Exception as e:
            return False, f'Error al crear el archivo XML: {str(e)}'