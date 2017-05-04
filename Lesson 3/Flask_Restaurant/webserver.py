from flask import Flask , render_template , url_for,request,redirect
import sqlite3

def getConnection():
    conn = sqlite3.connect("restaurantmenu.db")
    c = conn.cursor()
    return c,conn



app = Flask(__name__)


@app.route("/")
@app.route("/restaurant/<int:restaurantId>/menu")
def menu(restaurantId):
    try:
        c , conn = getConnection()
        c.execute("SELECT name FROM restaurant WHERE id= " + str(restaurantId))
        title = c.fetchall()[0]
        c.execute('SELECT * FROM menu_item WHERE restaurant_id =' + str(restaurantId))
        return render_template('index.html', menu = c.fetchall() , title = title[0] , restaurantId = restaurantId )
    except Exception as e:
        print(e)


@app.route("/restaurant/<int:restaurantId>/new" , methods=['GET','POST'])
def newMenuItem(restaurantId):
    if request.method == "POST":
        name = request.form['menuItem']
        c , conn = getConnection()
        c.execute('INSERT INTO menu_item(name,description,price,course,restaurant_id) VALUES ("'+name+'","Chicken Chicken","$12","Main","'+str(restaurantId)+'")')
        conn.commit()
        return redirect(url_for('menu',restaurantId=restaurantId))
    else:
        return render_template("newMenuItem.html" , restaurantId=restaurantId)


@app.route("/restaurant/<int:restaurantId>/<int:menuId>/edit", methods=['GET','POST'])
def editMenuItem(restaurantId, menuId):
    if request.method == "POST":
        name = request.form['rename']
        print(name)
        c , conn=getConnection()
        c.execute('UPDATE menu_item SET name="'+name+'" WHERE id = "'+str(menuId)+'" AND restaurant_id="'+str(restaurantId)+'"')
        conn.commit()
        return redirect(url_for('menu',restaurantId=restaurantId))
    c =getConnection()
    c.execute('SELECT name FROM menu_item WHERE id="'+str(menuId)+'" AND restaurant_id="'+str(restaurantId)+'"')
    name = c.fetchall()[0][0]
    return render_template("editMenuItem.html" , restaurantId = restaurantId , menuId = menuId,name = name)


@app.route("/restaurant/<int:restaurantId>/<int:menuId>/delete" , methods=['GET', 'POST'])
def deleteMenuItem(restaurantId, menuId):
    c , conn = getConnection()
    c.execute('SELECT name FROM menu_item where id="'+str(menuId)+'" AND restaurant_id="'+str(restaurantId)+'"')
    name = c.fetchall()[0][0]
    if request.method == 'POST':
        c.execute('DELETE FROM menu_item WHERE name = "'+name+'" AND id = "'+str(menuId)+'" AND restaurant_id = "'+str(restaurantId)+'"')
        conn.commit()
        print("DOne")
        return redirect(url_for('menu', restaurantId=restaurantId))
    return render_template("deleteMenuItem.html",restaurantId = restaurantId , menuId = menuId, name=name)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
