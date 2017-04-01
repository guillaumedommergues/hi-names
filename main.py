#!/usr/bin/python
# encoding: utf-8
from flask import  render_template, json, jsonify,request,Response, Flask
from google.cloud import datastore
#import stripe

myLocations = [
{"lat":22.19302, "lng":-156.880043, "locationName":' Hawai\'i', "locationExplained":'from Hawai\'iloa, discoverer of the Islands',"type":'state',"link":''},
{"lat":22.268688, "lng":-159.482253, "locationName":' Kauai', "locationExplained":'Debated - perhaps "food season"',"type":'county',"link":''},
{"lat":21.762660, "lng":-158.021439, "locationName":' Oahu', "locationExplained":'Hawaiian for "gathering place"',"type":'county',"link":''},
{"lat":21.2, "lng":-156.994772, "locationName":' Molokai', "locationExplained":'still to be discovered',"type":'county',"link":''},
{"lat":20.85, "lng":-157.242275, "locationName":' Lanai', "locationExplained":'from Hawaiian Lana\'i o Kaulua\'au "day of the conquest of Kaulua\'au"',"type":'county',"link":''},
{"lat":21, "lng":-156.081844, "locationName":' Maui', "locationExplained":'Son of Hawai\'iloa, discoverer of the Islands',"type":'county',"link":''},
{"lat":19.9, "lng":-155, "locationName":' Hawai\'i', "locationExplained":'from Hawai\'iloa, discoverer of the Islands',"type":'county',"link":''},
{"lat":21.310490, "lng":-157.861096, "locationName":' Honolulu', "locationExplained":'Hawaiian hono "port" + lulu"calm"',"type":'city',"link":''},
{"lat":21.400578, "lng":-157.739451, "locationName":' Kailua', "locationExplained":'Hawaiian kai "sea" + lua "two"',"type":'town',"link":''},
{"lat":21.313, "lng":-157.808, "locationName":' Manoa', "locationExplained":'Hawaiian for "deep, vast, thick"',"type":'valley',"link":''},
{"lat":21.313, "lng":-157.835, "locationName":' Makiki', "locationExplained":'Hawaiian for "cool, refreshing"',"type":'valley',"link":''}
]


app = Flask(__name__)








datastore_client = datastore.Client('hi-names')

#datastore_client = datastore.Client('gdtestflaskapp')



@app.route('/')
def homepage():
	return render_template('map.html')


@app.route('/about')
def about():
	return render_template('about.html'
		# ,key=stripe_keys['publishable_key']
		)

@app.route('/editMap')
def editMap():
	return render_template('editMap.html')

@app.route('/analysis')
def analysis():
	return render_template('analysis.html')


query = datastore_client.query(kind='Location')
@app.route('/json',methods=['POST'])
def getCalls():
	count = 0
	dataStoreLocations=[]
	while (count < 9 and len(dataStoreLocations)<1):
		count=count+1
		dataStoreLocations = list(query.fetch())
		dbLocations=[]
		for x in dataStoreLocations:
			temp={}
			temp['id']=format(x.key.id)
			temp['lat']=format(x['lat'])
			temp['lng']=format(x['lng'])
			temp['locationName']=format(x['locationName'])
			temp['locationExplained']=format(x['locationExplained'])
			temp['type']=format(x['type'])
			dbLocations.append(temp)
	result=dbLocations
	print(result)
	return Response(json.dumps(result), mimetype='/json')





# LOCATION EDITING

@app.route('/jsonNewLocation',methods=['GET','POST'])
def addNewLocation():
	location_key = datastore_client.key('Location', auto_now_add=True)
	myNewLocation = datastore.Entity(key=location_key)
	myNewLocation['lat'] = request.args.get('lat', '',type=float)
	myNewLocation['lng'] = request.args.get('lng', 0, type=float)
	myNewLocation['locationName'] = request.args.get('locationName', 0, type=unicode)
	myNewLocation['locationExplained'] = request.args.get('locationExplained', 0, type=unicode  )
	myNewLocation['type'] = request.args.get('type', 0, type=unicode)

	datastore_client.put(myNewLocation)
	return jsonify(**myNewLocation)



@app.route('/jsonEditLocation',methods=['GET','POST'])
def editOneLocation():
	dummyDictionary={}
	locationToEdit=request.args.get('id', '',type=int)
	key = datastore_client.key('Location', locationToEdit)
	a=datastore_client.get(key)
	myNewLocation = datastore.Entity(key=key)
	myNewLocation['lat'] = a['lat']
	myNewLocation['lng'] = a['lng']
	myNewLocation['locationName'] = request.args.get('locationName', 0, type=unicode )
	myNewLocation['locationExplained'] = request.args.get('locationExplained', 0, type=unicode )
	myNewLocation['type'] =  request.args.get('type', 0, type=unicode)
	datastore_client.put(myNewLocation)
	return jsonify(**dummyDictionary)


@app.route('/jsonRemoveOneLocation',methods=['GET','POST'])
def RemoveOneLocation():
	dummyDictionary={}
	locationToRemove=request.args.get('id', '',type=int)
	key = datastore_client.key('Location', locationToRemove)
	datastore_client.delete(key)
	return jsonify(**dummyDictionary)









# ADMINISTRATION


@app.route('/removelocation')
def removeLocation():
	return render_template('removelocation.html')


@app.route('/jsonRemoveLocation',methods=['GET','POST'])
def removeOldLocation():
	myNewLocation={}
	myLength = int(request.args.get('length', '',type=int))
	try:
		for i in range(0,myLength):
			locationToRemove=request.args.get(str(i), '',type=int)
			key = datastore_client.key('Location', locationToRemove)
			datastore_client.delete(key)
	except:
		print("error")


	return jsonify(**myNewLocation)



if __name__ == "__main__":
    app.run(threaded=True)

# DONATIONS


# test key that always works stripe.api_key = "YOURAPIKEY"
# test keys
# stripe_keys = {
#   'secret_key': 'YOURAPIKEY',
#   'publishable_key': 'YOURAPIKEY'
# }
# stripe_keys = {
#   'secret_key': 'YOURAPIKEY',
#   'publishable_key': 'YOURAPIKEY'
# }



# stripe.api_key = stripe_keys['secret_key']


# @app.route('/stripePayment',methods=['GET','POST'])
# def stripePayment():
# 	dummyDictionary={}
# 	# Set your secret key: remember to change this to your live secret key in production
# 	# See your keys here: https://dashboard.stripe.com/account/apikeys
# 	# Token is created using Stripe.js or Checkout!
# 	# Get the payment token submitted by the form:
# 	token = request.args.get('stripeToken', '', type=str)
# 	# Charge the user's card!
# 	donationAmount = request.args.get('donationAmount', '', type=int)

# 	charge = stripe.Charge.create(
#   		amount=donationAmount,
#   		currency="usd",
#   		description="Example charge",
#   		source=token,
# 	)

# 	return jsonify(**dummyDictionary)
