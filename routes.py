"""HTTP Routes pro Flask aplikaci"""

from flask import render_template_string, request, jsonify, redirect, url_for
from app import app, config_manager, udocker, container_manager
from templates.html_template import HTML_TEMPLATE
import time

@app.route('/')
def index():
    all_containers = container_manager.get_all_containers_info()
    images = udocker.get_images()
    return render_template_string(HTML_TEMPLATE, containers=all_containers, images=images)

@app.route('/create', methods=['POST'])
def create_container():
    container_config = {
        'name': request.form['name'],
        'image': request.form['image'],
        'ports': [p.strip() for p in request.form.get('ports', '').split('\n') if p.strip()],
        'volumes': [v.strip() for v in request.form.get('volumes', '').split('\n') if v.strip()],
        'env': [e.strip() for e in request.form.get('env', '').split('\n') if e.strip()],
        'command': request.form.get('command', '').strip(),
        'autostart': request.form.get('autostart') == '1'
    }
    
    success, message, container_id = container_manager.create_and_start_container(container_config)
    
    if success:
        return jsonify({'success': True, 'message': message, 'redirect': '/'})
    else:
        return jsonify({'success': False, 'message': message})

@app.route('/get-config/<container_id>', methods=['GET'])
def get_config(container_id):
    """Získá konfiguraci kontejneru pro editaci"""
    config = config_manager.get_container_config(container_id)
    if config:
        return jsonify({
            'success': True,
            'config': {
                'name': config.get('name', ''),
                'image': config.get('image', ''),
                'ports': '\n'.join(config.get('ports', [])),
                'volumes': '\n'.join(config.get('volumes', [])),
                'env': '\n'.join(config.get('env', [])),
                'command': config.get('command', ''),
                'autostart': config.get('autostart', False)
            }
        })
    else:
        return jsonify({'success': False, 'message': 'Konfigurace nenalezena'})

@app.route('/update/<container_id>', methods=['POST'])
def update_container(container_id):
    """Aktualizuje konfiguraci kontejneru - smaže starý a vytvoří nový"""
    new_config = {
        'name': request.form['name'],
        'image': request.form['image'],
        'ports': [p.strip() for p in request.form.get('ports', '').split('\n') if p.strip()],
        'volumes': [v.strip() for v in request.form.get('volumes', '').split('\n') if v.strip()],
        'env': [e.strip() for e in request.form.get('env', '').split('\n') if e.strip()],
        'command': request.form.get('command', '').strip(),
        'autostart': request.form.get('autostart') == '1'
    }
    
    success, message = container_manager.update_container(container_id, new_config)
    
    if success:
        return jsonify({'success': True, 'message': message})
    else:
        return jsonify({'success': False, 'message': message})

@app.route('/start/<container_id>', methods=['POST'])
def start_container(container_id):
    success, message = container_manager.start_container(container_id)
    return jsonify({'success': success, 'message': message})

@app.route('/stop/<container_id>', methods=['POST'])
def stop_container(container_id):
    success, message = container_manager.stop_container(container_id)
    return jsonify({'success': success, 'message': message})

@app.route('/delete/<container_id>', methods=['POST'])
def delete_container(container_id):
    success, message = container_manager.delete_container(container_id)
    return jsonify({'success': success, 'message': message})

@app.route('/save/<container_id>', methods=['POST'])
def save_container(container_id):
    success, message = container_manager.save_running_container(container_id)
    return jsonify({'success': success, 'message': message})

@app.route('/pull', methods=['POST'])
def pull_image():
    image = request.form['image']
    return jsonify({'image': image})

@app.route('/pull-progress/<path:image>', methods=['GET'])
def pull_progress(image):
    """Server-sent events pro progress pull operace"""
    def generate():
        yield f"data: {{'progress': 10, 'message': 'Připojuji se k registru...'}}\n\n"
        time.sleep(0.5)
        
        yield f"data: {{'progress': 30, 'message': 'Stahuji metadata...'}}\n\n"
        time.sleep(0.5)
        
        yield f"data: {{'progress': 50, 'message': 'Stahuji vrstvy image...'}}\n\n"
        
        success, message = udocker.pull_image(image)
        
        if success:
            yield f"data: {{'progress': 90, 'message': 'Rozbaluji image...'}}\n\n"
            time.sleep(0.3)
            yield f"data: {{'progress': 100, 'message': 'Hotovo!', 'success': true}}\n\n"
        else:
            yield f"data: {{'error': '{message}'}}\n\n"
    
    return app.response_class(generate(), mimetype='text/event-stream')

@app.route('/prune-images', methods=['POST'])
def prune_images():
    success, message = udocker.prune_unused_images()
    return jsonify({'success': success, 'message': message})

@app.route('/delete-image', methods=['POST'])
def delete_image():
    image_name = request.form['image']
    success, message = udocker.delete_image(image_name)
    return jsonify({'success': success, 'message': message})

@app.route('/check-image/<path:image>', methods=['GET'])
def check_image(image):
    """Kontrola, zda image existuje"""
    exists = udocker.image_exists(image)
    return jsonify({'exists': exists})