from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory database
contacts = []
next_id = 1

# Add a contact
@app.route('/contacts', methods=['POST'])
def add_contact():
    global next_id
    data = request.get_json()
    contact = {'id': next_id, 'name': data['name'], 'email': data['email']}
    contacts.append(contact)
    next_id += 1
    return jsonify(contact), 201

# Get all contacts
@app.route('/contacts', methods=['GET'])
def get_contacts():
    return jsonify(contacts), 200

# Update a contact
@app.route('/contacts/<int:id>', methods=['PUT'])
def update_contact(id):
    data = request.get_json()
    for contact in contacts:
        if contact['id'] == id:
            contact.update(data)
            return jsonify(contact), 200
    return jsonify({'error': 'Contact not found'}), 404

# Delete a contact
@app.route('/contacts/<int:id>', methods=['DELETE'])
def delete_contact(id):
    global contacts
    contacts = [contact for contact in contacts if contact['id'] != id]
    return jsonify({'message': 'Contact deleted'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
