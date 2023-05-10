import xml.etree.ElementTree as ET

root = ET.parse('Scanbot.Xamarin.SDK.Dependencies.nuspec').getroot()

links = "<ul>"
for tag in root.findall('metadata/dependencies/group/dependency'):
    id = tag.get('id')
    version = tag.get('version')
    links += f"\n<li><a href=\"https://www.nuget.org/packages/{id}/{version}#supportedframeworks-body-tab\">{id}@{version}</a></li>"
links += "\n</ul>"

with open('links.html', 'w+') as f:
    f.write(links)