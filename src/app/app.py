#!/usr/bin/env python
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from werkzeug.utils import secure_filename
from flask import Flask, request, send_file
import os
import time
import yaml

ALLOWED_EXTENSIONS = {'yaml', 'yml'}

app = Flask(__name__)

if os.environ.get('URL'):
    app.config['URL'] = os.environ.get('URL')
else:
    app.config['URL'] = 'http://go.drawthe.net/'

if os.environ.get('UPLOAD_FOLDER'):
    app.config['UPLOAD_FOLDER'] = os.environ.get('UPLOAD_FOLDER')
else:
    app.config['UPLOAD_FOLDER'] = 'upload'
absolute_path_upload_file_dir = os.path.join(os.getcwd(), app.config['UPLOAD_FOLDER'])

if os.environ.get('SAVE_FOLDER'):
    app.config['SAVE_FOLDER'] = os.environ.get('UPLOAD_FOLDER')
else:
    app.config['SAVE_FOLDER'] = 'save'
absolute_path_save_rendered_image_dir = os.path.join(os.getcwd(), app.config['SAVE_FOLDER'])

if os.environ.get('DRIVER_PATH'):
    app.config['DRIVER_PATH'] = os.environ.get('DRIVER_PATH')
else:
    app.config['DRIVER_PATH'] = '/usr/local/lib/python3.6/site-packages/chromedriver_binary/chromedriver'

if os.environ.get('CHROME_WINDOW_SIZE'):
    app.config['CHROME_WINDOW_SIZE'] = os.environ.get('CHROME_WINDOW_SIZE')
else:
    app.config['CHROME_WINDOW_SIZE'] = '1920,1080'

if os.environ.get('LISTEN_PORT'):
    app.config['LISTEN_PORT'] = os.environ.get('LISTEN_PORT')
else:
    app.config['LISTEN_PORT'] = '8080'


def render_diagram(yaml_data, filename):
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--window-size=' + app.config['CHROME_WINDOW_SIZE'])
    chrome_options.add_experimental_option('prefs', {
        'download.default_directory': absolute_path_save_rendered_image_dir,
        'download.prompt_for_download': False,
        'download.directory_upgrade': True
    })
    driver = webdriver.Chrome(executable_path=app.config['DRIVER_PATH'], options=chrome_options)

    # Get site contents for the drawthe
    driver.get(app.config['URL'])
    draw = driver.find_element_by_id('draw')
    save = driver.find_element_by_id('saveimage')

    # Clear the textare of ACE editor
    text_area = driver.find_elements_by_xpath('//textarea[@class="ace_text-input"]').pop()
    text_area.send_keys(Keys.CONTROL + "a")
    text_area.send_keys(Keys.DELETE)

    # Input yaml lines to the textare of ACE editor
    for line in yaml_data.split('\n'):
        text_area.send_keys(line + Keys.ENTER)
        text_area.send_keys(Keys.LEFT)
        text_area.send_keys(Keys.ENTER)

    # Generate a NW diagram
    draw.click()
    save.click()

    # Check of the existence of the rendered NW diagram
    absolute_path_save_rendered_image_file = os.path.join(absolute_path_save_rendered_image_dir, filename)
    while True:
        if os.path.isfile(absolute_path_save_rendered_image_file):
            break
        else:
            time.sleep(1)

    driver.quit()
    return absolute_path_save_rendered_image_file


def allowed_file(file_name):
    if '.'.join(file_name.rsplit('.', 2)[1:3]).lower() in ALLOWED_EXTENSIONS:
        return True

    return False


def valid_yaml(yaml_data):
    try:
        yaml_parse = yaml.safe_load(yaml_data)
    except Exception as e:
        return e

    return True, yaml_parse


@app.route('/api/render', methods=['POST'])
def render():
    # check an upload file
    if not request.files:
        return 'found not a yaml file', 400

    for key in request.files.keys():
        ret_val = allowed_file(request.files[key].filename)
        if ret_val is False:
            return "found not allowed extensions", 400

    # save an upload file
    for key in request.files.keys():
        file = request.files[key]
        yaml_file_name = secure_filename(file.filename)
        absolute_path_save_upload_file = os.path.join(absolute_path_upload_file_dir, yaml_file_name)
        file.save(absolute_path_save_upload_file)

    with open(absolute_path_save_upload_file, 'r') as f:
        yaml_data = f.read()

    valid_result, yaml_parse = valid_yaml(yaml_data)
    if not isinstance(valid_result, bool):
        return valid_result, 500

    if 'title' in yaml_parse and 'text' in yaml_parse['title']:
        image_file_name = yaml_parse['title']['text'] + '.png'
    else:
        image_file_name = 'unknown.png'

    absolute_path_save_rendered_image_file = render_diagram(yaml_data, image_file_name)
    return send_file(absolute_path_save_rendered_image_file, as_attachment=True,
                     attachment_filename=image_file_name,
                     mimetype='image/png')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=app.config['LISTEN_PORT'])
