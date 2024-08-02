from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()

    hosts = data['hosts']
    become = data['become']
    tasks = data['tasks']
    tags = data['tags']

    yaml_output = "---\n- hosts: {}\n".format(hosts)

    if become.lower() == "yes":
        yaml_output += "  become: yes\n"

    yaml_output += "  tasks:\n"

    for task in tasks:
        yaml_output += "  - name: {}\n".format(task['name'])
        yaml_output += "    command: {}\n".format(task['command'])
        if task.get('become'):
            yaml_output += "    become: {}\n".format(task['become'])
        if task.get('tags'):
            yaml_output += "    tags: {}\n".format(task['tags'])
        yaml_output += "\n"  # Add a newline between tasks for readability

    return jsonify(yaml_output=yaml_output)


if __name__ == '__main__':
    app.run(debug=True)
