import math
from flask import Flask, render_template, request, jsonify
import sqlite3 as sql
app = Flask(__name__)

DATABASE_FILE = "database.db"
DEFAULT_BUGGY_ID = "1"

BUGGY_RACE_SERVER_URL = "http://rhul.buggyrace.net"

#new save
#------------------------------------------------------------
# the index page
#------------------------------------------------------------
@app.route('/')
def home():
    return render_template('index.html', server_url=BUGGY_RACE_SERVER_URL)


#------------------------------------------------------------
# creating a new buggy:
#  if it's a POST request process the submitted data
#  but if it's a GET request, just show the form
#------------------------------------------------------------
@app.route('/new', methods=['POST', 'GET'])
def create_buggy():
    if request.method == 'GET':
        con = sql.connect(DATABASE_FILE)
        con.row_factory = sql.Row
        cur = con.cursor()
        cur.execute("SELECT * FROM buggies")
        record = cur.fetchone()

        #return render_template("buggy-form.html", buggy=record)
        return render_template("buggy-form.html", buggy=None)#This removed the ability to pre-load the form however, the video said it is okay to be None

    elif request.method == 'POST':
        msg = ""        
        qty_wheels = request.form['qty_wheels']
        #msg = f"qty_wheels={qty_wheels}"
        flag_color = request.form['flag_color']
        flag_color_secondary = request.form['flag_color_secondary']
        qty_tyres = request.form['qty_tyres']
        buggy_id = request.form['id'] #new1
        flag_pattern = request.form['flag_pattern']
        power_type = request.form['power_type']
        armour = request.form['armour']
        attack = request.form['attack']
        aux_power_type = request.form['aux_power_type']
        aux_power_units = request.form['aux_power_units']
        power_units = request.form['power_units']
        #msg = f"flag_pattern={flag_pattern}"
        

        if not qty_wheels.isdigit():
            msg1 = f"no! This is not a number: {qty_wheels}. this will not be saved. Please start again "
            return render_template("updated.html", msg=msg1,) # buggy.html did not work due to an error with venv
        elif int(qty_wheels) % 2 > 0:
            msg2 = f"this is an odd number: {qty_wheels}.This will not be saved. Please start again."
            return render_template("updated.html", msg=msg2)
        elif int(qty_wheels) < 4 :
          msg3 = f"The number of wheels can not be less than 4.This will not be saved. Please start again."
          return render_template("updated.html", msg=msg3)
          

        #if int(qty_wheels) % 2 > 0:
            #msg2 = f"this is an odd number: {qty_wheels}.This will not be saved. Please start again."
            #return render_template("updated.html", msg=msg2)

        #if int(qty_wheels) < 4 :
          #msg3 = f"The number of wheels can not be less than 4.This will not be saved. Please start again."
          #return render_template("updated.html", msg=msg3)

        if flag_color == flag_color_secondary:
          msg4 = f"You must select 2 different colours. This will not be saved. Please start again."
          return render_template("updated.html", msg=msg4)



        if not qty_tyres.isdigit():
          msg10=f"This is not a number: {qty_tyres}. This will not be saved. Please start again."
          return render_template("updated.html", msg=msg10)
        elif int(qty_tyres) < int(qty_wheels):
          msg5 = f"The number of tyres must be the same as or greater than the number of wheels. This will not be saved. Please start again."
          return render_template("updated.html", msg=msg5) 
        



        if not aux_power_units.isdigit():
          msg9 = f"This is not a number: {aux_power_units}. This will not be saved. Please start again"
          return render_template("updated.html", msg=msg9)
        elif int(aux_power_units) < 0 :
          msg6 = f"The number of back-up power units must be either equal to or greater than 0. This will not be saved. please start again."
          return render_template("updated.html", msg=msg6)
        
        #if int(power_units) < 1 :
          #msg7 = f"The quantity of power units must be greater than or equal to 1. This will not be saved. Please start again."
          #return render_template("updated.html", msg=msg7)
        if not power_units.isdigit():
          msg7 = f"no! This is not a number: {power_units}. this will not be saved. Please start again "
          return render_template("updated.html", msg=msg7,)
        elif int(power_units) <1:
          msg8 = f"no!. Must be greater than 1.this will not be saved. Please start again "
          return render_template("updated.html", msg=msg8)
  
          





          

          






        try:
          #flag_pattern = request.form['flag_pattern']
          #power_type = request.form['power_type']
          #armour = request.form['armour']
          #attack = request.form['attack']
          #aux_power_type = request.form['aux_power_type']
          #aux_power_units = request.form['aux_power_units']
          #power_units = request.form['power_units']
          
          #qty_tyres = request.form['qty_tyres']
            #msg = f"qty_wheels={qty_wheels}"
          with sql.connect(DATABASE_FILE) as con:
              cur = con.cursor()
              if buggy_id.isdigit():#new1
                cur.execute("UPDATE buggies set qty_wheels=?, flag_color=?, flag_color_secondary=?, flag_pattern=?, power_type=?, qty_tyres=?, armour=?, attack=?, aux_power_type=?, aux_power_units=?, power_units=? WHERE id=?",
                (qty_wheels, flag_color, flag_color_secondary, flag_pattern, power_type, qty_tyres, armour, attack, aux_power_type, aux_power_units, power_units, buggy_id ))
              else:
                abc = ("INSERT INTO buggies (qty_wheels, flag_color,flag_color_secondary,flag_pattern,power_type,qty_tyres,armour, attack, aux_power_type, aux_power_units, power_units) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)")
                gg= [(qty_wheels, flag_color, flag_color_secondary, flag_pattern, power_type, qty_tyres, armour, attack, aux_power_type, aux_power_units, power_units, )] 
              #cur.execute(
                  #"UPDATE buggies set qty_wheels=?, flag_color=?, flag_color_secondary=?, flag_pattern=?, power_type=?, qty_tyres=?, armour=? WHERE id=?",
                  #(qty_wheels, flag_color, flag_color_secondary, flag_pattern, power_type, qty_tyres, armour, DEFAULT_BUGGY_ID))
              #cur.execute("INSERT INTO buggies (qty_wheels) VALUES (?)", (qty_wheels,))
              #cur.execute("INSERT INTO buggies (flag_color) VALUES (?)", (flag_color,)) 
                cur.executemany(abc,gg)              
              con.commit()
              msg = "Record successfully saved"
        except:
            con.rollback()
            msg = "error in update operation"
        finally:
            con.close()
            return render_template("updated.html", msg=msg)


#------------------------------------------------------------
# a page for displaying the buggy
#------------------------------------------------------------
@app.route('/buggy')
def show_buggies():
    con = sql.connect(DATABASE_FILE)
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM buggies")
    #record = cur.fetchone()
    records = cur.fetchall()
    return render_template("buggy.html", buggies = records)


#------------------------------------------------------------
# a page for edit the buggy
#------------------------------------------------------------
#@app.route('/new')
#def edit_buggy():
#    return render_template("buggy-form.html")
@app.route('/edit/<buggy_id>')
def edit_buggy(buggy_id):
  con = sql.connect(DATABASE_FILE)
  con.row_factory = sql.Row
  cur = con.cursor()
  cur.execute("SELECT * FROM buggies WHERE id=?",(buggy_id,))
  records = cur.fetchone();
  #return "FIXME I want to edit buggy with id {}".format(buggy_id)
  return render_template("buggy-form.html", buggy=records)



#------------------------------------------------------------
# get JSON from current record
#   this is still probably right, but we won't be
#   using it because we'll be dipping diectly into the
#   database
#------------------------------------------------------------
@app.route('/json')
def summary():
    con = sql.connect(DATABASE_FILE)
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM buggies WHERE id=? LIMIT 1", (DEFAULT_BUGGY_ID))
    return jsonify({
        k: v
        for k, v in dict(
            zip([column[0]
                 for column in cur.description], cur.fetchone())).items()
        if (v != "" and v is not None)
    })


#------------------------------------------------------------
# delete the buggy
#   don't want DELETE here, because we're anticipating
#   there always being a record to update (because the
#   student needs to change that!)
#------------------------------------------------------------
@app.route('/delete/<buggy_id>')
def delete_buggy(buggy_id):
    try:
        msg = "deleting buggy"
        with sql.connect(DATABASE_FILE) as con:
            cur = con.cursor()
            #cur.execute("DELETE FROM buggies")
            cur.execute('DELETE FROM buggies WHERE id=?',(buggy_id,))
            con.commit()
            msg = "Buggy deleted"
    except:
        con.rollback()
        msg = "error in delete operation"
    finally:
        con.close()
        return render_template("updated.html", msg=msg)


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
