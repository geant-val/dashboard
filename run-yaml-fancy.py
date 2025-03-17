import yaml
from urllib.parse import quote

# Function to read YAML file
def read_yaml(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

# Function to generate Shields.io URL
def generate_shields_url(test_name, geant4_version, compiler_version, stage, result):
    base_url = "https://img.shields.io/static/v1"
    message = result.capitalize()
    if result == "success": color = "brightgreen"
    if result == "failure": color = "red"
    if result == "skipped": color = "grey"
    # Setting label to an empty string
    return f"{base_url}?label=&message={message}&color={color}"

# Function to generate Markdown table
def generate_markdown_table(data):
    table = "| Test Name | Geant4 Version | Compiler Version | Configure Result | Build Result | Run Result |\n"
    table += "|:----------|:--------------:|:----------------:|:----------------:|:------------:|:------------:|\n"

    last_test_name = ""
    for test in sorted(data['tests'], key=lambda x: x['name']):
        for version in sorted(test['geant4_versions'], key=lambda x: x['version']):
            for compiler in sorted(version['compilers'], key=lambda x: x['compiler_version']):
                configure_result = compiler['results']['configure']
                build_result = compiler['results']['build']
                run_result = compiler['results']['run']
                configure_badge = f"![{configure_result}]({generate_shields_url(test['name'], version['version'], compiler['compiler_version'], 'configure', configure_result)})"
                build_badge = f"![{build_result}]({generate_shields_url(test['name'], version['version'], compiler['compiler_version'], 'build', build_result)})"
                run_badge = f"![{run_result}]({generate_shields_url(test['name'], version['version'], compiler['compiler_version'], 'run', run_result)})"
                test_name_display = test['name'] if test['name'] != last_test_name else ""
                row = f"| {test_name_display} | {version['version']} | gcc{compiler['compiler_version']} | {configure_badge} | {build_badge} | {run_badge} |\n"
                table += row
                last_test_name = test['name']
    return table

# Main execution
if __name__ == "__main__":
    yaml_data = read_yaml("results_ci.yaml")
    markdown_table = generate_markdown_table(yaml_data)
    print(markdown_table)
    with open("output.md", "w") as md_file:
        md_file.write(markdown_table)
