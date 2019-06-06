'''
Created on 10/31/2018

@author: Jiaming
'''

from xml.etree.ElementTree import Element, SubElement
import xml.etree.ElementTree as etree
from xml.dom import minidom
from file_processing_v2 import final_enty, final_lex, final_typ, final_habt, final_afford, embd_dic


def prettify(elem):
    ''' Return a pretty-print XML string '''
    rough_string = etree.tostring(elem, 'utf-8')
    reparesed = minidom.parseString(rough_string)
    return reparesed.toprettyxml(indent="  ")


def append_sub_element(input_root, dic):
    for elm in dic:

        sub = SubElement(input_root, elm)

        if len(dic[elm]) == 1 and type(dic[elm][0]) == str:
            sub.text = dic[elm][0]
        elif len(dic[elm]) > 1 and type(dic[elm][0]) == list and len(dic[elm][0]) > 1:
            value_class = dic[elm][0][0]
            value_title = dic[elm][0][1:]
            for value in dic[elm][1:]:
                if len(value) == len(dic[elm][0]) - 1:
                    sub_value = SubElement(sub, value_class)
                    for x in range(0, len(value_title)):
                        sub_value.set(value_title[x], value[x])
                else:
                    raise Exception('Numbers of attributes do not match: {}'.format(elm))
        else:
            raise Exception('Syntax does not match: {}'.format(elm))


root = Element("VoxML")
root.set("xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")
root.set("xmlns:xsd", "http://www.w3.org/2001/XMLSchema")


'''Create Entity node and set its attribute'''
vox_enty = SubElement(root, "Entity")
vox_enty.set("Type", final_enty.get("Type"))

'''Lexical'''
vox_lex = SubElement(root, "Lex")
append_sub_element(vox_lex, final_lex)

'''Type'''
vox_typ = SubElement(root, "Type")
append_sub_element(vox_typ, final_typ)

'''Habitat'''
vox_habt = SubElement(root, "Habitat")
append_sub_element(vox_habt, final_habt)

'''Afforfance structure'''
vox_afford = SubElement(root, "Afford_Str")
append_sub_element(vox_afford, final_afford)

'''Embodied'''
vox_embd = SubElement(root, "Embodiment")
append_sub_element(vox_embd, embd_dic)

# these lines write the readable element tree(root) as a string into the new file
output_file = open("xml_output.xml", 'wb')
output_file.write(minidom.parseString(etree.tostring(root, 'utf-8')).toprettyxml(indent="  ", encoding="ascii"))
output_file.close() 

print(prettify(root))

