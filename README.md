# prose-to-xml
Prose to VoxML XML converter

Setting the input annotated document and running ```xml_building.py``` will output an VoxML Object model in XML format. 

The annotated document must meet the following requirments, otherwise errors will occur: 
  1. The document is written in docx. 
  2. The writter has to mark up each part's subtitle in the document with underline, meanwhile please avoid using underline in other places. 
  
The annotated document is recommened to be written in the following format: 

  For ```Object name```: 
    If the object is artificial, mention it after the object’s name. For example: ```iPhone (artificial)```.
    
  For ```Description```:
  1. Directly mention the concavity, rotation and reflection symmetric axis of the object.
  2. When describing the shape of the object, choose words from the following inventory: 
  ```text
     prismatoid, pyramid, wedge, parallelepiped, cupola, frustum, cylindroid, 
     ellipsoid, hemiellipsoid, bipyramid, rectangular prism, toroid, sheet
   ```
  
  For ```Components```: 
  List each compunents of the object with comma. 
  
  For ```States```, ```Actions```, ```Activities```:
  1. When describing an action on the object lead to a result, write sentence in pattern ```If ...(action), ...(result).```
  2. Describing attributes of the object with pattern ```...(object/agent) can ...(functions).```
