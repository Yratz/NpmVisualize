import requests
import json
import sys

path = "https://registry.npmjs.org"
list_dependencies = dict()


def constructing_package_links(packet_name, packet_version):
    if not packet_name in list_dependencies:
        list_dependencies[packet_name] = []
    else:
        return
    new_path = path + "/" + packet_name + "/" + packet_version
    response_2 = requests.get(new_path)
    result_2 = json.loads(response_2.content)  # Содержимое страницы с новым путем
    if "dependencies" in result_2:
        dependencies_k = list(((result_2["dependencies"]).keys()))
        dependencies_v = list(((result_2["dependencies"]).values()))
    else:
        return

    for i in range(len(dependencies_v)):
        if not dependencies_k[i] in list_dependencies[packet_name]:
            list_dependencies[packet_name].append(dependencies_k[i])
            constructing_package_links(dependencies_k[i], dependencies_v[i][1:])


def convert_to_grapfViz():
    graphCode = "digraph G {\n"
    for parent in list_dependencies:
        for child in list_dependencies[parent]:
            graphCode += "\"" + parent + "\" -> \"" + child + "\";\n"
    graphCode += "}"
    return graphCode


def main():
    start_packet = sys.argv[1]
    response = requests.get(path + "/" + start_packet)
    result = json.loads(response.content)
    versions = list(result["versions"].keys())

    # берем последнюю версию пакета
    constructing_package_links(start_packet, versions[-1])

    # print(list_dependencies)
    code_for_graphViz = convert_to_grapfViz()
    print(code_for_graphViz)


if __name__ == "__main__":
    main()
