import yaml
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/generate', methods=['POST'])
def generate():
    hosts = request.form.get('hosts', '')
    become = request.form.get('become', 'no')

    tasks = []
    task_names = request.form.getlist('tasks')
    actions = request.form.getlist('actions')
    messages = request.form.getlist('messages')
    conditions = request.form.getlist('conditions')
    conditions_type = request.form.getlist('conditions_type')
    conditions_value = request.form.getlist('conditions_value')
    tags = request.form.getlist('tags')
    tags_name = request.form.getlist('tags_name')

    for i in range(len(task_names)):
        task = {
            'name': task_names[i],
            'command': actions[i]
        }
        if conditions[i] == 'yes' and conditions_type[i] and conditions_value[i]:
            task[conditions_type[i]] = conditions_value[i]
        if tags[i] == 'yes' and tags_name[i]:
            task['tags'] = [tags_name[i]]
        tasks.append(task)
        if messages[i]:
            tasks.append({
                'debug': {
                    'msg': messages[i]
                }
            })

    playbook = [{
        'hosts': hosts,
        'become': become,
        'tasks': tasks
    }]

    yaml_output = yaml.dump(playbook, sort_keys=False)

    # Return YAML content as response
    return jsonify({'yaml': yaml_output})


if __name__ == '__main__':
    app.run(debug=True)
