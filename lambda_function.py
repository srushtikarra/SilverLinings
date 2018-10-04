from ask import alexa
import urllib2
import json

customerId = '5925e4eaa73e4942cdafd61a'
apiKey = '61892e8b6b69dca102737332a828661c'

def lambda_handler(request_obj, context={}):
    return alexa.route_request(request_obj) 

@alexa.default_handler()
def default_handler(request):
    return launch_request_handler(request)

@alexa.request_handler("LaunchRequest")
def launch_request_handler(request):
    return alexa.create_response(message="Welcome to Silver Lining!",
                                 reprompt_message='Which banking action would you like to complete today?')

@alexa.request_handler(request_type="SessionEndedRequest")
def session_ended_request_handler(request):
    return alexa.create_response(message="Bye!", end_session=True)

@alexa.intent_handler("AMAZON.HelpIntent")
def help_intent_handler(request):
    return alexa.create_response(message="This skill tells you a fun fact!", end_session=False)

@alexa.intent_handler("AMAZON.StopIntent")
def stop_intent_handler(request):
    return alexa.create_response(message="Bye!", end_session=True)

@alexa.intent_handler("AMAZON.CancelIntent")
def cancel_intent_handler(request):
    return alexa.create_response(message="Bye!", end_session=True)

@alexa.intent_handler("SetBillReminderIntent")
def set_bill_reminder_intent_handler(request):
    payee = request.get_slot_value("payee")
    payee_str = str(payee)

    payment_amount = request.get_slot_value("payment_amount")
    payment_str = str(payment_amount)
    payment_double = (int(payment_str)/1.0)

    headers = { 'Content-Type': 'application/json' }
    url = 'http://api.reimaginebanking.com/accounts/5925e4eca73e4942cdafd61d/bills?key=61892e8b6b69dca102737332a828661c'
    req = urllib2.Request(url, data='{"status": "recurring", "payee": "%s", "payment_date": "2017-05-25", "payment_amount": %d, "recurring_date": 1}' % (payee_str,payment_double), headers = headers)
    resp = urllib2.urlopen(req)
    code = json.load(resp)['code']

    if code == 201:
        success_str = "A bill has been created for " + payee_str + " in the amount of " + payment_str + " dollars."
        return alexa.create_response(message=success_str, end_session=True)
    return alexa.create_response(message="An Error Occurred. The Bill was not created. Try again.", end_session=True)

@alexa.intent_handler("UpdateBillIntent")
def update_bill_intent_handler(request):
    payee = str(request.get_slot_value("payee"))
    url = 'http://api.reimaginebanking.com/accounts/5925e4eca73e4942cdafd61d/bills?key=61892e8b6b69dca102737332a828661c'
    bill_response = urllib2.urlopen(url)
    jsn = json.load(bill_response)
    for bill in jsn:
        if (bill['payee'] == payee):
            new_payment_date = bill['upcoming_payment_date']
            opener = urllib2.build_opener(urllib2.HTTPHandler)
            data='{"payment_date": "%s"}' % (new_payment_date)
            #print (new_payment_date)
            request = urllib2.Request('http://api.reimaginebanking.com/bills/{}?key=61892e8b6b69dca102737332a828661c'.format(bill['_id']), data)
            request.add_header('Content-Type', 'application/json')
            request.get_method = lambda: 'PUT'
            url = opener.open(request)
    return alexa.create_response(message="You have paid the bill.", end_session=True)
