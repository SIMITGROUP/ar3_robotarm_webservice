teensy = "/dev/ttyACM0"
arduino = "/dev/ttyUSB0"
def index():
    return '{"status":"OK","msg":"Welcome index page of AR3 webservice, you can call /help, /info now"}'

def controlServo(servo,angle):
    return '{"status":"OK","msg":"this servo '+servo+' will set ' +angle+ ' degree"}'