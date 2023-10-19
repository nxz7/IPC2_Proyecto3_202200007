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