from flask import Flask, render_template, url_for, request, redirect, flash, jsonify
import sqlite3

app = Flask(__name__)


def getConnection():
    conn = sqlite3.connect("restaurantmenu.db")
    c = conn.cursor()
    return c, conn


# API
@app.route("/restaurant/<int:restaurantId>/json")
def restaurantMenuJson(restaurantId):
    c, conn = getConnection()
    c.execute('SELECT * FROM menu_item WHERE restaurant_id = "' + str(restaurantId) + '"')
    menu = c.fetchall()
    menuList = []
    for item in menu:
        menuDict = {
            'name': item[0],
            'id': item[1],
            'description': item[2],
            'price': item[3],
            'course': item[4]
        }
        menuList.append(menuDict)
    return jsonify(MenuItem=[menuList])


@app.route("/")
def restaurants():
    c, conn = getConnection()
    c.execute("SELECT * FROM restaurant")
    return render_template('restaurants.html', restaurants=c.fetchall())


@app.route("/newRestaurant", methods=['POST', 'GET'])
def newRestaurant():
    if request.method == 'POST':
        restaurant = request.form['newRestaurant']
        c, conn = getConnection()
        c.execute('INSERT INTO restaurant(name) VALUES ("' + restaurant + '")')
        conn.commit()
        flash("Restaurant added")
        c.execute('SELECT id from restaurant WHERE name="' + restaurant + '"')
        id = c.fetchall()
        id = id[0][0]
        # print(id)
        return redirect(url_for("newMenuItem", restaurantId=id))
    return render_template("newRestaurant.html")


@app.route("/restaurant/<int:restaurantId>/editRestaurant", methods=['POST', 'GET'])
def editRestaurant(restaurantId):
    if request.method == 'POST':
        c, conn = getConnection()
        editedName = request.form['editedName']
        c.execute('UPDATE restaurant SET name = "' + editedName + '" WHERE id = "' + str(restaurantId) + '"')
        conn.commit()
        return redirect(url_for('restaurants'))
    c, conn = getConnection()
    c.execute('SELECT name FROM restaurant WHERE id="' + str(restaurantId) + '"')
    return render_template("editRestaurant.html", restaurantId=restaurantId, name=c.fetchall()[0][0])


@app.route("/restaurants/<int:restaurantId>/deleteRestaurant", methods=['POST', 'GET'])
def deleteRestaurant(restaurantId):
    if request.method == 'POST':
        c, conn = getConnection()
        c.execute('DELETE FROM restaurant WHERE id = "' + str(restaurantId) + '"')
        conn.commit()
        flash("Restaurant deleted")
        return redirect(url_for('restaurants'))
    c, conn = getConnection()
    c.execute('SELECT name FROM restaurant WHERE id = "' + str(restaurantId) + '"')
    name = c.fetchall()[0][0]
    return render_template('deleteRestaurant.html', restaurantId=restaurantId, name=name)

@app.route("/restaurant/<int:restaurantId>/menu")
def menu(restaurantId):
    try:
        c, conn = getConnection()
        c.execute("SELECT name FROM restaurant WHERE id= " + str(restaurantId))
        title = c.fetchall()[0]
        c.execute('SELECT * FROM menu_item WHERE restaurant_id =' + str(restaurantId))
        return render_template('index.html', menu=c.fetchall(), title=title[0], restaurantId=restaurantId)
    except Exception as e:
        print(e)


@app.route("/restaurant/<int:restaurantId>/new", methods=['GET', 'POST'])
def newMenuItem(restaurantId):
    if request.method == "POST":
        name = request.form['menuItem']
        description = request.form['description']
        price = request.form['price']
        c, conn = getConnection()
        c.execute(
            'INSERT INTO menu_item(name,description,price,course,restaurant_id) VALUES ("' + name + '","' + description + '","$' + price + '","Main","' + str(
                restaurantId) + '")')
        conn.commit()
        flash("New Item added")
        return redirect(url_for('menu', restaurantId=restaurantId))
    else:
        c, conn = getConnection()
        c.execute("SELECT * FROM restaurant WHERE id=" + str(restaurantId))
        title = c.fetchall()[0][1]
        return render_template("newMenuItem.html", restaurantId=restaurantId, restaurant=title)


@app.route("/restaurant/<int:restaurantId>/<int:menuId>/edit", methods=['GET', 'POST'])
def editMenuItem(restaurantId, menuId):
    if request.method == "POST":
        name = request.form['rename']
        print(name)
        c, conn = getConnection()
        c.execute('UPDATE menu_item SET name="' + name + '" WHERE id = "' + str(menuId) + '" AND restaurant_id="' + str(
            restaurantId) + '"')
        conn.commit()
        flash("Menu item edited")
        return redirect(url_for('menu', restaurantId=restaurantId))
    c, conn = getConnection()
    c.execute('SELECT name FROM menu_item WHERE id="' + str(menuId) + '" AND restaurant_id="' + str(restaurantId) + '"')
    name = c.fetchall()[0][0]
    return render_template("editMenuItem.html", restaurantId=restaurantId, menuId=menuId, name=name)


@app.route("/restaurant/<int:restaurantId>/<int:menuId>/delete", methods=['GET', 'POST'])
def deleteMenuItem(restaurantId, menuId):
    c, conn = getConnection()
    c.execute('SELECT name FROM menu_item where id="' + str(menuId) + '" AND restaurant_id="' + str(restaurantId) + '"')
    name = c.fetchall()[0][0]
    if request.method == 'POST':
        c.execute('DELETE FROM menu_item WHERE name = "' + name + '" AND id = "' + str(
            menuId) + '" AND restaurant_id = "' + str(restaurantId) + '"')
        conn.commit()
        flash("Item deleted")
        return redirect(url_for('menu', restaurantId=restaurantId))
    return render_template("deleteMenuItem.html", restaurantId=restaurantId, menuId=menuId, name=name)


if __name__ == '__main__':
    app.secret_key = "my_secret_key"
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
