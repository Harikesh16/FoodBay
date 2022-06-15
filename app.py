import psycopg2
from flask import Flask, render_template,request,redirect,url_for

app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(
    host="10.17.50.232",
    port = 5432,
    database = "group_44",
    user = "group_44",
    password = "0I5nnozTCaEaw")

    return conn

@app.route('/',methods=['GET','POST'])
def home():
    conn = get_db_connection()
    db = conn.cursor()

    # form = Form()
    
    db.execute('SELECT DISTINCT country FROM rest;')
    result = db.fetchall()
    data=[]
    for x in result :
        data.append({'name':x[0]})
    data.sort(key = lambda i: i['name'])
    # print(data)
    db.close()
    conn.close()
    # form.country.choices = [(item['name']) for item in data]
    if(request.method=='POST'):
        print(request.form['country'])
    return render_template('country.html',data=data,country = country)

@app.route('/<country>',methods=['GET','POST'])
def country(country):
    if(request.method=='POST'):
        country = request.form['country']
    conn = get_db_connection()
    db = conn.cursor()
    cityArray =[]
    conds = [country]
    stmt = 'SELECT DISTINCT city FROM rest WHERE country IN ({})'.format(','.join(['%s']*len(conds)))
    db.execute(stmt,tuple(conds))
    result = db.fetchall()
    for x in result :
        cityArray.append({'name':x[0]})
    cityArray.sort(key = lambda i: i['name'])
    # print(cityArray)
    db.close()
    conn.close()
    return render_template('city.html',data = cityArray,country=country,city=city)  

@app.route('/<country>/<city>',methods=['GET','POST'])
def city(country,city):
    if(request.method=='POST'):
        city = request.form['city']
    conn = get_db_connection()
    db = conn.cursor()
    addressArray =[]
    # print(city)
    conds = [city]
    stmt = 'SELECT restaurant_name,locality,aggre_rat,rest.cuisines,average_cost,currency,restaurant_id FROM rest WHERE city IN ({}) '.format(','.join(['%s']*len(conds)))
    db.execute(stmt,tuple(conds))
    result = db.fetchall()
    for x in result :
        if(x[2]):
            addressArray.append({'Name':x[0],'locality':x[1],'rating':x[2],'cuisines':x[3],'cost':str(x[4])+"  "+x[5],'id':x[6]})
        else:
            addressArray.append({'Name':x[0],'locality':x[1],'rating':-1.0,'cuisines':x[3],'cost':str(x[4])+"  "+x[5],'id':x[6]})
    addressArray.sort(key = lambda i: i['rating'],reverse=True)
    # print(addressArray)
    db.close()
    conn.close()
    return render_template('cuisines.html',data = addressArray,city = city,country=country)    

@app.route('/<country>/<city>/cuisines',methods=['GET','POST'])
def cuisines(country,city):
    conn = get_db_connection()
    db = conn.cursor()
    addressArray1 =[]
    addressArray2 =[]
    addressArray3 =[]
    addressArray4 =[]
    store_array = ['Both','Both','Both','Both']
    sort_by = 'rating'
    if(request.method=='POST'):
        p = request.form['pork']
        v = request.form['veg']
        s = request.form['spicy']
        l = request.form['lactose']

        store_array[0] = p[0]
        store_array[1] = v[0]
        store_array[2] = s[0]
        store_array[3] = l[0]

        if(p!='Both'):
            conds = [(country,city,p)]
            stmt = 'SELECT restaurant_name,locality,aggre_rat,rest.cuisines,average_cost,currency,restaurant_id FROM rest INNER JOIN cuisines ON(rest.cuisines=cuisines.cuisines) WHERE (country,city,pork) IN ({}) '.format(','.join(['%s']*len(conds)))
            db.execute(stmt,tuple(conds))
            result = db.fetchall()
            for x in result :
                if(x[2]):
                    addressArray1.append({'Name':x[0],'locality':x[1],'rating':x[2],'cuisines':x[3],'cost':str(x[4])+"  "+x[5],'id':x[6]})
                else:
                    addressArray1.append({'Name':x[0],'locality':x[1],'rating':-1.0,'cuisines':x[3],'cost':str(x[4])+"  "+x[5],'id':x[6]})
            addressArray1.sort(key = lambda i: i[sort_by],reverse=True)
        else:
            conds = [(country,city)]
            stmt = 'SELECT restaurant_name,locality,aggre_rat,rest.cuisines,average_cost,currency,restaurant_id FROM rest INNER JOIN cuisines ON(rest.cuisines=cuisines.cuisines) WHERE (country,city) IN ({}) '.format(','.join(['%s']*len(conds)))
            db.execute(stmt,tuple(conds))
            result = db.fetchall()
            for x in result :
                if(x[2]):
                    addressArray1.append({'Name':x[0],'locality':x[1],'rating':x[2],'cuisines':x[3],'cost':str(x[4])+"  "+x[5],'id':x[6]})
                else:
                    addressArray1.append({'Name':x[0],'locality':x[1],'rating':-1.0,'cuisines':x[3],'cost':str(x[4])+"  "+x[5],'id':x[6]})
            addressArray1.sort(key = lambda i: i[sort_by],reverse=True)

        
        if(v!='Both'):
            conds = [(country,city,v)]
            stmt = 'SELECT restaurant_name,locality,aggre_rat,rest.cuisines,average_cost,currency,restaurant_id FROM rest INNER JOIN cuisines ON(rest.cuisines=cuisines.cuisines) WHERE (country,city,veg) IN ({}) '.format(','.join(['%s']*len(conds)))
            db.execute(stmt,tuple(conds))
            result = db.fetchall()
            for x in result :
                if(x[2]):
                    addressArray2.append({'Name':x[0],'locality':x[1],'rating':x[2],'cuisines':x[3],'cost':str(x[4])+"  "+x[5],'id':x[6]})
                else:
                    addressArray2.append({'Name':x[0],'locality':x[1],'rating':-1.0,'cuisines':x[3],'cost':str(x[4])+"  "+x[5],'id':x[6]})
            addressArray2.sort(key = lambda i: i[sort_by],reverse=True)
        else:
            conds = [(country,city)]
            stmt = 'SELECT restaurant_name,locality,aggre_rat,rest.cuisines,average_cost,currency,restaurant_id FROM rest INNER JOIN cuisines ON(rest.cuisines=cuisines.cuisines) WHERE (country,city) IN ({}) '.format(','.join(['%s']*len(conds)))
            db.execute(stmt,tuple(conds))
            result = db.fetchall()
            for x in result :
                if(x[2]):
                    addressArray2.append({'Name':x[0],'locality':x[1],'rating':x[2],'cuisines':x[3],'cost':str(x[4])+"  "+x[5],'id':x[6]})
                else:
                    addressArray2.append({'Name':x[0],'locality':x[1],'rating':-1.0,'cuisines':x[3],'cost':str(x[4])+"  "+x[5],'id':x[6]})
            addressArray2.sort(key = lambda i: i[sort_by],reverse=True)

        
        if(s!='Both'):
            conds = [(country,city,s)]
            stmt = 'SELECT restaurant_name,locality,aggre_rat,rest.cuisines,average_cost,currency,restaurant_id FROM rest INNER JOIN cuisines ON(rest.cuisines=cuisines.cuisines) WHERE (country,city,spicy) IN ({}) '.format(','.join(['%s']*len(conds)))
            db.execute(stmt,tuple(conds))
            result = db.fetchall()
            for x in result :
                if(x[2]):
                    addressArray3.append({'Name':x[0],'locality':x[1],'rating':x[2],'cuisines':x[3],'cost':str(x[4])+"  "+x[5],'id':x[6]})
                else:
                    addressArray3.append({'Name':x[0],'locality':x[1],'rating':-1.0,'cuisines':x[3],'cost':str(x[4])+"  "+x[5],'id':x[6]})
            addressArray3.sort(key = lambda i: i[sort_by],reverse=True)
        else:
            conds = [(country,city)]
            stmt = 'SELECT restaurant_name,locality,aggre_rat,rest.cuisines,average_cost,currency,restaurant_id FROM rest INNER JOIN cuisines ON(rest.cuisines=cuisines.cuisines) WHERE (country,city) IN ({}) '.format(','.join(['%s']*len(conds)))
            db.execute(stmt,tuple(conds))
            result = db.fetchall()
            for x in result :
                if(x[2]):
                    addressArray3.append({'Name':x[0],'locality':x[1],'rating':x[2],'cuisines':x[3],'cost':str(x[4])+"  "+x[5],'id':x[6]})
                else:
                    addressArray3.append({'Name':x[0],'locality':x[1],'rating':-1.0,'cuisines':x[3],'cost':str(x[4])+"  "+x[5],'id':x[6]})
            addressArray3.sort(key = lambda i: i[sort_by],reverse=True)

        
        if(l!='Both'):
            conds = [(country,city,l)]
            stmt = 'SELECT restaurant_name,locality,aggre_rat,rest.cuisines,average_cost,currency,restaurant_id FROM rest INNER JOIN cuisines ON(rest.cuisines=cuisines.cuisines) WHERE (country,city,lactose) IN ({}) '.format(','.join(['%s']*len(conds)))
            db.execute(stmt,tuple(conds))
            result = db.fetchall()
            for x in result :
                if(x[2]):
                    addressArray4.append({'Name':x[0],'locality':x[1],'rating':x[2],'cuisines':x[3],'cost':str(x[4])+"  "+x[5],'id':x[6]})
                else:
                    addressArray4.append({'Name':x[0],'locality':x[1],'rating':-1.0,'cuisines':x[3],'cost':str(x[4])+"  "+x[5],'id':x[6]})
            addressArray4.sort(key = lambda i: i[sort_by],reverse=True)
        else:
            conds = [(country,city)]
            stmt = 'SELECT restaurant_name,locality,aggre_rat,rest.cuisines,average_cost,currency,restaurant_id FROM rest INNER JOIN cuisines ON(rest.cuisines=cuisines.cuisines) WHERE (country,city) IN ({}) '.format(','.join(['%s']*len(conds)))
            db.execute(stmt,tuple(conds))
            result = db.fetchall()
            for x in result :
                if(x[2]):
                    addressArray4.append({'Name':x[0],'locality':x[1],'rating':x[2],'cuisines':x[3],'cost':str(x[4])+"  "+x[5],'id':x[6]})
                else:
                    addressArray4.append({'Name':x[0],'locality':x[1],'rating':-1.0,'cuisines':x[3],'cost':str(x[4])+"  "+x[5],'id':x[6]})
            addressArray4.sort(key = lambda i: i[sort_by],reverse=True)

    addressArray = intersection(addressArray1,addressArray2,addressArray3,addressArray4)
    # print(addressArray)
    db.close()
    conn.close()
    return render_template('address.html',data=addressArray,country=country,city=city,sa=store_array)

def intersection(arr1,arr2,arr3,arr4):
    lst = [val for val in arr1 if val in arr2 if val in arr3 if val in arr4]
    return lst

@app.route('/<country>/<city>/<sa>',methods=['GET','POST'])
def choice(country,city,sa):
    conn = get_db_connection()
    db = conn.cursor()
    addressArray1 =[]
    addressArray2 =[]
    addressArray3 =[]
    addressArray4 =[]
    sort_by = 'rating'
    p = sa[2]
    v = sa[7]
    s = sa[12]
    l = sa[17]
    if(request.method=='POST'):
        if(request.form['rating']=='Order By Rating'):
            sort_by = 'rating'
        elif(request.form['rating']=='Order By Price'):
            sort_by = 'cost'
        else:
            sort_by = 'rating'

        if(p!='B'):
            if(p=='Y'):
                p='Yes'
            else:
                p = 'No'
            conds = [(country,city,p)]
            stmt = 'SELECT restaurant_name,locality,aggre_rat,rest.cuisines,average_cost,currency,restaurant_id FROM rest INNER JOIN cuisines ON(rest.cuisines=cuisines.cuisines) WHERE (country,city,pork) IN ({}) '.format(','.join(['%s']*len(conds)))
            db.execute(stmt,tuple(conds))
            result = db.fetchall()
            for x in result :
                if(x[2]):
                    addressArray1.append({'Name':x[0],'locality':x[1],'rating':x[2],'cuisines':x[3],'cost':str(x[4])+"  "+x[5],'id':x[6]})
                else:
                    addressArray1.append({'Name':x[0],'locality':x[1],'rating':-1.0,'cuisines':x[3],'cost':str(x[4])+"  "+x[5],'id':x[6]})
            addressArray1.sort(key = lambda i: i[sort_by],reverse=True)
        else:
            conds = [(country,city)]
            stmt = 'SELECT restaurant_name,locality,aggre_rat,rest.cuisines,average_cost,currency,restaurant_id FROM rest INNER JOIN cuisines ON(rest.cuisines=cuisines.cuisines) WHERE (country,city) IN ({}) '.format(','.join(['%s']*len(conds)))
            db.execute(stmt,tuple(conds))
            result = db.fetchall()
            for x in result :
                if(x[2]):
                    addressArray1.append({'Name':x[0],'locality':x[1],'rating':x[2],'cuisines':x[3],'cost':str(x[4])+"  "+x[5],'id':x[6]})
                else:
                    addressArray1.append({'Name':x[0],'locality':x[1],'rating':-1.0,'cuisines':x[3],'cost':str(x[4])+"  "+x[5],'id':x[6]})
            addressArray1.sort(key = lambda i: i[sort_by],reverse=True)

        
        if(v!='B'):
            if(v=='Y'):
                v='Yes'
            else:
                v = 'No'
            conds = [(country,city,v)]
            stmt = 'SELECT restaurant_name,locality,aggre_rat,rest.cuisines,average_cost,currency,restaurant_id FROM rest INNER JOIN cuisines ON(rest.cuisines=cuisines.cuisines) WHERE (country,city,veg) IN ({}) '.format(','.join(['%s']*len(conds)))
            db.execute(stmt,tuple(conds))
            result = db.fetchall()
            for x in result :
                if(x[2]):
                    addressArray2.append({'Name':x[0],'locality':x[1],'rating':x[2],'cuisines':x[3],'cost':str(x[4])+"  "+x[5],'id':x[6]})
                else:
                    addressArray2.append({'Name':x[0],'locality':x[1],'rating':-1.0,'cuisines':x[3],'cost':str(x[4])+"  "+x[5],'id':x[6]})
            addressArray2.sort(key = lambda i: i[sort_by],reverse=True)
        else:
            conds = [(country,city)]
            stmt = 'SELECT restaurant_name,locality,aggre_rat,rest.cuisines,average_cost,currency,restaurant_id FROM rest INNER JOIN cuisines ON(rest.cuisines=cuisines.cuisines) WHERE (country,city) IN ({}) '.format(','.join(['%s']*len(conds)))
            db.execute(stmt,tuple(conds))
            result = db.fetchall()
            for x in result :
                if(x[2]):
                    addressArray2.append({'Name':x[0],'locality':x[1],'rating':x[2],'cuisines':x[3],'cost':str(x[4])+"  "+x[5],'id':x[6]})
                else:
                    addressArray2.append({'Name':x[0],'locality':x[1],'rating':-1.0,'cuisines':x[3],'cost':str(x[4])+"  "+x[5],'id':x[6]})
            addressArray2.sort(key = lambda i: i[sort_by],reverse=True)

        
        if(s!='B'):
            if(s=='Y'):
                s='Yes'
            else:
                s = 'No'
            conds = [(country,city,s)]
            stmt = 'SELECT restaurant_name,locality,aggre_rat,rest.cuisines,average_cost,currency,restaurant_id FROM rest INNER JOIN cuisines ON(rest.cuisines=cuisines.cuisines) WHERE (country,city,spicy) IN ({}) '.format(','.join(['%s']*len(conds)))
            db.execute(stmt,tuple(conds))
            result = db.fetchall()
            for x in result :
                if(x[2]):
                    addressArray3.append({'Name':x[0],'locality':x[1],'rating':x[2],'cuisines':x[3],'cost':str(x[4])+"  "+x[5],'id':x[6]})
                else:
                    addressArray3.append({'Name':x[0],'locality':x[1],'rating':-1.0,'cuisines':x[3],'cost':str(x[4])+"  "+x[5],'id':x[6]})
            addressArray3.sort(key = lambda i: i[sort_by],reverse=True)
        else:
            conds = [(country,city)]
            stmt = 'SELECT restaurant_name,locality,aggre_rat,rest.cuisines,average_cost,currency,restaurant_id FROM rest INNER JOIN cuisines ON(rest.cuisines=cuisines.cuisines) WHERE (country,city) IN ({}) '.format(','.join(['%s']*len(conds)))
            db.execute(stmt,tuple(conds))
            result = db.fetchall()
            for x in result :
                if(x[2]):
                    addressArray3.append({'Name':x[0],'locality':x[1],'rating':x[2],'cuisines':x[3],'cost':str(x[4])+"  "+x[5],'id':x[6]})
                else:
                    addressArray3.append({'Name':x[0],'locality':x[1],'rating':-1.0,'cuisines':x[3],'cost':str(x[4])+"  "+x[5],'id':x[6]})
            addressArray3.sort(key = lambda i: i[sort_by],reverse=True)

        
        if(l!='B'):
            if(l=='Y'):
                l='Yes'
            else:
                l = 'No'
            conds = [(country,city,l)]
            stmt = 'SELECT restaurant_name,locality,aggre_rat,rest.cuisines,average_cost,currency,restaurant_id FROM rest INNER JOIN cuisines ON(rest.cuisines=cuisines.cuisines) WHERE (country,city,lactose) IN ({}) '.format(','.join(['%s']*len(conds)))
            db.execute(stmt,tuple(conds))
            result = db.fetchall()
            for x in result :
                if(x[2]):
                    addressArray4.append({'Name':x[0],'locality':x[1],'rating':x[2],'cuisines':x[3],'cost':str(x[4])+"  "+x[5],'id':x[6]})
                else:
                    addressArray4.append({'Name':x[0],'locality':x[1],'rating':-1.0,'cuisines':x[3],'cost':str(x[4])+"  "+x[5],'id':x[6]})
            addressArray4.sort(key = lambda i: i[sort_by],reverse=True)
        else:
            conds = [(country,city)]
            stmt = 'SELECT restaurant_name,locality,aggre_rat,rest.cuisines,average_cost,currency,restaurant_id FROM rest INNER JOIN cuisines ON(rest.cuisines=cuisines.cuisines) WHERE (country,city) IN ({}) '.format(','.join(['%s']*len(conds)))
            db.execute(stmt,tuple(conds))
            result = db.fetchall()
            for x in result :
                if(x[2]):
                    addressArray4.append({'Name':x[0],'locality':x[1],'rating':x[2],'cuisines':x[3],'cost':str(x[4])+"  "+x[5],'id':x[6]})
                else:
                    addressArray4.append({'Name':x[0],'locality':x[1],'rating':-1.0,'cuisines':x[3],'cost':str(x[4])+"  "+x[5],'id':x[6]})
            addressArray4.sort(key = lambda i: i[sort_by],reverse=True)

    addressArray = intersection(addressArray1,addressArray2,addressArray3,addressArray4)
    addressArray.sort(key = lambda i: float(str(i[sort_by]).split(' ')[0]),reverse=True)
    # print(addressArray)
    db.close()
    conn.close()
    return render_template('address.html',data=addressArray,country=country,city=city,sa = sa)

@app.route('/country/city/<id>',methods=['GET','POST'])
def address(id):
    if(request.method=='POST'):
        id = request.form['id']
    conn = get_db_connection()
    db = conn.cursor()
    addressArray =[]
    # print(address)
    conds = [id]
    stmt = 'SELECT adress,restaurant_name,cuisines,average_cost,currency,hastable,hasonline,isdelv,aggre_rat,votes FROM rest WHERE restaurant_id IN ({}) '.format(','.join(['%s']*len(conds)))
    db.execute(stmt,tuple(conds))
    result = db.fetchall()
    for x in result :
        addressArray.append({'rad':x[0],'rnam':x[1],'cu':x[2],'ac':str(x[3])+" "+x[4],'ht':x[5],'ho':x[6],'delv':x[7],'rating':round(x[8],1),'votes':x[9]})
    # print(addressArray)
    db.close()
    conn.close()
    return render_template('hotel.html',data = addressArray,id = id)

@app.route('/country/city/rating/<id>',methods=['GET','POST'])
def rating(id):
    conn = get_db_connection()
    db = conn.cursor()
    if(request.method=='POST'):
        stars = int(request.form['ratin'])
    
    conds = [id]
    stmt = 'SELECT aggre_rat,votes FROM rest WHERE restaurant_id IN ({}) '.format(','.join(['%s']*len(conds)))
    db.execute(stmt,tuple(conds))
    result = db.fetchall()
    votes = [x[1] for x in result]
    rating = [x[0] for x in result]
    rating[0] *= votes[0]
    votes[0]+=1
    rating[0] += stars
    rating[0] /= votes[0]
    # rating[0] = round(rating[0],1)

    stmt1 = 'UPDATE rest SET votes = %s,aggre_rat = %s WHERE restaurant_id = %s'
    db.execute(stmt1,(votes[0],rating[0],id))

    db.close()
    conn.commit()
    conn.close()
    return redirect(url_for('address',id=id))

if __name__ == "__main__":
    app.run(debug=True,port=5044)