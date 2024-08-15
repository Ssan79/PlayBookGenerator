from flask import Flask, render_template, request, jsonify
import yaml

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/generate', methods=['POST'])
def generate_playbook():
    tasks = []

    num_tasks = len(request.form.getlist('tasks'))

    for i in range(num_tasks):
        task = {}
        task_name = request.form.getlist('tasks')[i]
        task_details = request.form.getlist('actions')[i]
        hosts = request.form.getlist('hosts')[i]
        become_task = request.form.getlist('become_task')[i]
        condition = request.form.getlist('conditions')[i]
        condition_type = request.form.getlist('conditions_type')[i]
        condition_value = request.form.getlist('conditions_value')[i]
        message = request.form.getlist('messages')[i]
        tags = request.form.getlist('tags')[i]
        tags_name = request.form.getlist('tags_name')[i]

        task['hosts'] = hosts
        if become_task == 'yes':
            task['become'] = True
        task['tasks'] = [{'name': task_name}]

        task_details_list = task_details.split('\n')
        task['tasks'][0].update({'action': task_details_list})

        if condition == 'yes' and condition_type and condition_value:
            task['tasks'][0][condition_type] = condition_value

        if tags == 'yes' and tags_name:
            task['tasks'][0]['tags'] = tags_name

        if message:
            task['tasks'].append({'debug': {'msg': message}})

        tasks.append(task)

    playbook_yaml = yaml.dump(tasks, sort_keys=False, default_flow_style=False)

    return jsonify({'playbook': playbook_yaml})


if __name__ == '__main__':
    app.run(debug=True)
