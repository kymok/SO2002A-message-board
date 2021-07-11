from flask import Flask, render_template, request, jsonify
from marshmallow import Schema, fields, ValidationError
import SO2002A
import string

# validation

class BaseSchema(Schema):
    value = fields.List(fields.String, required=True)

printable = set(string.printable)


# initialise

app = Flask(__name__)
message = []
SO2002A.reset()


# App

def write_to_oled(value):
    SO2002A.reset()
    SO2002A.write_lines(value)

@app.route('/')
def index():
    return render_template('index.htm', message=message)

@app.route('/set', methods=['POST'])
def set_display():
    global message
    data = request.get_json()
    
    # validate response
    schema = BaseSchema()
    try:
        result = schema.load(data)
    except ValidationError as err:
        return (jsonify(err.messages), 400)
    value = [''.join(filter(lambda x : x in printable, line)) for line in data['value']]
    message = value

    # write to OLED
    write_to_oled(value)
    return ('OK', 200)

if (__name__ == '__main__'):
    app.run(host='0.0.0.0')