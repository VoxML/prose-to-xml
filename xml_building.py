'''
Created on 10/31/2018

@author: Jiaming
'''
from xml.etree.ElementTree import Element, SubElement
import xml.etree.ElementTree as etree
from xml.dom import minidom
from file_processing import test_entity, test_lex_dic, test_typ_dic, test_habt_dic, test_afford_dic, test_embd_dic
from file_processing import entity, lex_dic, typ_dic, habt_dic, afford_dic, embd_dic


def prettify(elem):
    ''' Return a pretty-print XML string '''
    rough_string = etree.tostring(elem, 'utf-8')
    reparesed = minidom.parseString(rough_string)
    return reparesed.toprettyxml(indent="  ")


def append_sub_element(input_root, dic):
    for elm in dic:
        sub = SubElement(input_root, elm)
        if len(dic.get(elm)) == 1:
            sub.text = dic.get(elm)[0]
        else:
            value_class = dic.get(elm)[0][0]
            value_title = dic.get(elm)[0][1:]
            for value in dic.get(elm)[1:]:
                sub_value = SubElement(sub, value_class)
                for x in range(0, len(value_title)):
                 sub_value.set(value_title[x], value[x])


root = Element("VoxML")
root.set("xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")
root.set("xmlns:xsd", "http://www.w3.org/2001/XMLSchema")


'''Create Entity node and set its attribute '''
vox_enty = SubElement(root, "Entity")
vox_enty.set("Type", entity.get("Type"))
# vox_enty.set("Type", test_entity.get("Type"))


'''Lexical meaning of this entity '''
vox_lex = SubElement(root, "Lex")
append_sub_element(vox_lex, lex_dic)
# append_sub_element(vox_lex, test_lex_dic)

'''Properties of the object's type '''
vox_typ = SubElement(root, "Type")
append_sub_element(vox_typ, typ_dic)
# append_sub_element(vox_typ, test_typ_dic)


'''Habitat of this entity '''
vox_habt = SubElement(root, "Habitat")
append_sub_element(vox_habt, habt_dic)
# append_sub_element(vox_habt, test_habt_dic)


'''Afforfance structure of this entity '''
vox_afford = SubElement(root, "Afford_Str")
append_sub_element(vox_afford, afford_dic)
# append_sub_element(vox_afford, test_afford_dic)

'''How this entity will be embodied '''
vox_embd = SubElement(root, "Embodiment")
append_sub_element(vox_embd, embd_dic)
# append_sub_element(vox_embd, test_embd_dic)


# these lines write the readable element tree(root) as a string into the new file
output_file = open("xml_output.xml", 'wb')
output_file.write(minidom.parseString(etree.tostring(root, 'utf-8')).toprettyxml(indent="  ", encoding="ascii"))
output_file.close() 

print(prettify(root))
print(entity)
