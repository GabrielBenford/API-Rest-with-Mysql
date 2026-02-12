from flask import Flask, jsonify, request
from Database.db_connection import connect_db
app=Flask(__name__)

@app.route('/store',methods=['GET'])
def index():
    connect = connect_db()
    cursor = connect.cursor(dictionary=True)
    cursor.execute("SELECT * FROM hardware_store")
    result=cursor.fetchall()
    connect.close()
    return jsonify(result)

@app.route('/store/<int:id>',methods=['GET'])
def get_row_by_id(id):
     connect = connect_db()
     cursor = connect.cursor(dictionary=True)
     cursor.execute("SELECT * FROM hardware_store WHERE id=%s",(id,))
     result=cursor.fetchall()
     connect.close()
     if cursor.rowcount == 0:
         return jsonify({'Error':'No id founded'})
     return jsonify(result[0]),200

@app.route('/store/<int:id>',methods=['PUT'])
def update_values(id):
    connect = connect_db()
    cursor = connect.cursor(dictionary=True)
    data=request.json
    cursor.execute("UPDATE hardware_store SET Customer=%s,Products=%s,Price=%s WHERE id=%s",
    (data['Customer'], data['Products'], data['Price'],id,))
    if cursor.rowcount == 0:
        return jsonify({'Error!':'Id not found'})
    connect.commit()
    connect.close()
    return jsonify({'Congratulations!':'Item updated!'}),200


@app.route('/store',methods=['POST'])
def add_new_values():
    connect = connect_db()
    cursor = connect.cursor(dictionary=True)
    data=request.json
    cursor.execute("INSERT INTO hardware_store(Customer, Products, Price) VALUES (%s, %s, %s)",
    (data['Customer'], data['Products'], data['Price']))
    if cursor.rowcount == 0:
       return jsonify({'Error':'These items cannot be null'})
    connect.commit()
    connect.close()
    return jsonify({'Congratulations!':'Item added successfully'}),201
@app.route('/store/<int:id>',methods=['DELETE'])
def delete_row_by_id(id):
    connect = connect_db()
    cursor = connect.cursor(dictionary=True)
    cursor.execute("DELETE FROM hardware_store WHERE id=%s",(id,))
    if cursor.rowcount == 0:
        return jsonify({'Error!': "This row doesn't exist"})
    connect.commit()
    connect.close()
    return jsonify({'Congratulations!':'Item deleted successfully'}),200

if __name__=='__main__':
    app.run(debug=True)