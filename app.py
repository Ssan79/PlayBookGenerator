import yaml
from flask import Flask, render_template, request, jsonify, send_file

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/generate', methods=['POST'])
def generate_playbook():
    try:
        tasks = request.form.getlist('tasks')
        actions = request.form.getlist('actions')

        playbook_content = []

        for task_name, action in zip(tasks, actions):
            try:
                action_yaml = yaml.safe_load(action) if action else {}
            except yaml.YAMLError as e:
                return jsonify({'error': f'YAML syntax error in Task "{task_name}": {str(e)}'}), 400

            playbook_content.append({
                'name': task_name,
                'tasks': [action_yaml] if action_yaml else []
            })

        playbook_path = "playbook.yml"
        with open(playbook_path, 'w') as file:
            yaml.dump(playbook_content, file)

        return send_file(playbook_path, as_attachment=True)

    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500


if __name__ == '__main__':
    app.run(debug=True)
