import Levenshtein
import os
import xml.etree.ElementTree as ET

def similarities(inp):
    max_distance=int((30/100)*len(inp))
    data=[]
    min=100
    str=""

    for filename in os.listdir("aiml"):
        filepath = os.path.join("aiml", filename)
        if os.path.isfile(filepath):
            root = ET.parse(filepath)
            x = {}
            for category in root.findall('category'):
                pattern = category.find('pattern').text.strip()
                data.append(pattern)

    for index in data :
        if Levenshtein.distance(index.upper(),inp.upper())<min:
            min=Levenshtein.distance(index.upper(),inp.upper())
            str=index
    return str

print(similarities("how are y"))