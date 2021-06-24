import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from twocaptcha import TwoCaptcha

api_key = os.getenv('APIKEY_2CAPTCHA', 'd27951bbc5b0ef54114aa65e82bd0dc0')

solver = TwoCaptcha(api_key)

try:
    result = solver.normal('path/to/captcha.jpg')

except Exception as e:
    sys.exit(e)

else:
    sys.exit('solved: ' + str(result))