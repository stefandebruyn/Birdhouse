import xml.etree.ElementTree as ET
tree = ET.parse('zillow.xml')
root = tree.getroot()

# one specific item attribute
print('Item #2 attribute:')
print(root[0][1].attrib)

# all item attributes
print('\nAll attributes:')
for elem in root:
    for subelem in elem:
        print(subelem.attrib)

# one specific item's data
print('\nItem #2 data:')
print(root[0][1].text)

# all items data
print('\nAll item data:')
for elem in root:
    for subelem in elem:
        print(subelem.text)