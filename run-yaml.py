import yaml
from operator import itemgetter

# Function to read YAML file
def read_yaml(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

# Function to generate Markdown table
def generate_markdown_table(data):
    table = "| Test Name | Geant4 Version | Compiler Version | Configure Result | Build Result |\n"
    table += "|-----------|----------------|------------------|------------------|--------------|\n"

    for test in sorted(data['tests'], key=lambda x: x['name']):
        for version in sorted(test['geant4_versions'], key=lambda x: x['version']):
            for compiler in sorted(version['compilers'], key=lambda x: x['compiler_version']):
                row = f"| {test['name']} | {version['version']} | gcc{compiler['compiler_version']} | {compiler['results']['configure'].capitalize()} | {compiler['results']['build'].capitalize()} |\n"
                table += row
    return table

# Main execution
if __name__ == "__main__":
    yaml_data = read_yaml("results.yaml")
    markdown_table = generate_markdown_table(yaml_data)
    print(markdown_table)
    with open("output.md", "w") as md_file:
        md_file.write(markdown_table)
