'''
Created on 12/10/2018

@author: Jiaming
'''
from collections import defaultdict
import docx
import re

shape_inventory = {"prismatoid", "pyramid", "bipyramid", "wedge", "parallelepiped", "cupola", "frustum", "cylindroid",
                    "sheet", "ellipsoid", "hemiellipsoid", "hemi ellipsoid", "hemi-ellipsoid", "semiellipsoid", "paraboloid",
                   "semi ellipsoid", "semi-ellipsoid", "rectangular prism", "rectangular-prism", "toroid"}
axis_inventory = {"x-axis", "y-axis", "z-axis", "xy-axis", "yz-axis", "xz-axis",
                    "x axis", "y axis", "z axis", "xy axis", "yz axis", "xz axis"}


def lex_process(text):

    lex_dic = defaultdict(list)

    pred_pattern = re.compile(r"object.*")
    pred_match = pred_pattern.findall(text)
    if len(pred_match) != 0:
        obj_name = pred_match[0].split(':')[-1].strip()
        lex_dic['Pred'] = [obj_name.split("(")[0].strip()]
        if len(re.compile(r"artificial.*").findall(obj_name)) != 0:
            lex_dic['Type'] = ["physobj*artifact"]
        else:
            lex_dic['Type'] = ["physobj"]

    return lex_dic


def tpy_process(text):

    typ_dic = defaultdict(list)

    head_pattern = re.compile(r"shape of.*?\.")
    head_match = head_pattern.findall(text)
    if head_match is not None:
        shape = [x for x in shape_inventory if x in str(head_match)]
        typ_dic["Head"] = [" ".join(shape)]

    comp_pattern = re.compile(r"components:.*")
    comp_match = comp_pattern.findall(text)
    if comp_match is not None:
        comp_lst = [["Component", "Value"]]
        for comp in comp_match[0].split(","):
            comp_lst.append([re.sub(r"components:", "", comp).strip()])
        typ_dic["Components"] = comp_lst

    # ! need more clues to determine concavity, or in the other way annotate the concavity directly !
    concv_pattern = re.compile(r"(inside.*?\.|scoop.*?\.|concave.*?\.)")
    concv_match = concv_pattern.findall(text)
    if len(concv_match) != 0:
        typ_dic.update({"Concavity": ["Concave"]})
    elif len(re.compile(r"flat.*?\.").findall(text)) != 0:
        typ_dic.update({"Concavity": ["Flat"]})
    else:
        typ_dic.update({"Concavity": ["Convex"]})

    rotat_pattern = re.compile(r"rotat.*?[,\.]")
    rotat_match = rotat_pattern.findall(text)
    if len(rotat_match) != 0:
        rotat = [x for x in axis_inventory if x in str(rotat_match)]
        typ_dic.update({"RotatSym": [" ".join(rotat)]})

    refl_pattern = re.compile(r"refl.*?[,\.]")
    refl_match = refl_pattern.findall(text)
    if len(refl_match) != 0:
        refl = [x for x in axis_inventory if x in str(refl_match)]
        typ_dic.update({"ReflSym": [" ".join(refl)]})

    return typ_dic


def habt_process(text):

    habt_dic = defaultdict(list)

    habt_pattern = re.compile(r"\scan\s.*?[,\.]")
    habt_match = habt_pattern.findall(text)
    if len(habt_match) != 0:
        habt_lst = [["Intr", "Value"]]
        for habt in habt_match:
            habt_lst.append([habt.strip()])
        habt_dic["Intrinsic"] = habt_lst

    return habt_dic


def afford_process(text):

    afford_dic = defaultdict(list)

    affd_pattern = re.compile(r"\sif\s.*?\.")
    affd_match = affd_pattern.findall(text)
    if len(affd_match) != 0:
        affd_lst = [["Affordance", "Formula"]]
        for affd in affd_match:
            affd_lst.append([affd.strip()])
        afford_dic["Affordances"] = affd_lst

    return afford_dic


def get_runs(filename):
    doc = docx.Document(filename)
    runs_list = []
    new_runs = []
    count = 0
    for paragraph in doc.paragraphs:
        for x in range(0, len(paragraph.runs)):
            if paragraph.runs[x].underline is True:
                count += 1
                runs_list.append([paragraph.runs[x].text])
            else:
                runs_list[count-1].append(paragraph.runs[x].text)
    for run in runs_list:
        new_runs.append(' '.join(run))

    return new_runs


lex_text = ""
typ_text = ""
habt_text = ""
afford_text = ""
embd_text = ""
enty_dic = defaultdict()
embd_dic = defaultdict(list)


for paragraph in get_runs("bowl_annotation.docx"):
    if re.match(r"\bObject", paragraph) is not None:
        lex_text = paragraph.lower()
        enty_dic["Type"] = "Object"
    if re.match(r"\bComponent", paragraph) is not None:
        typ_text += " " + paragraph.lower()
    if re.match(r"\bDescription", paragraph) is not None:
        typ_text += " " + paragraph.lower()
    if re.match(r"\bState", paragraph) is not None:
        habt_text += " " + paragraph.lower()
        afford_text += " " + paragraph.lower()
    if re.match(r"\b(Action|Activit)", paragraph) is not None:
        habt_text += " " + paragraph.lower()
        afford_text += " " + paragraph.lower()

final_enty = enty_dic
final_lex = lex_process(lex_text)
final_typ = tpy_process(typ_text)
final_habt = habt_process(habt_text)
final_afford = afford_process(afford_text)

