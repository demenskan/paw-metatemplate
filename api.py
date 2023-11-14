from flask import *
from methods import *
import os
from dotenv import load_dotenv

app = Flask(__name__)
generator=Generator()


#I used two functions because flask needs a trailing slash
#For root
@app.route("/")
def RootRequest():
    return generator.getPage("index.json", {})
#For anything else
@app.route("/<path:uri_request>")
def GeneralRequest(uri_request):
    #split the request
    uri_request=uri_request.split("/")
    controller = uri_request[0]
    #look on pages definition file for a match
    config=generator.read_file("json/system/config.json","json","//")
    if config == "FileNotFoundError":
        return ("Config File not found")
    routes=generator.read_file(config["ROUTES_FILE"],"json","//")
    #no matches? return 404
    if controller not in routes:
        if '404_ERROR_INSTRUCTOR' not in config:
            abort(404)
        else:
            return generator.getPage(config['404_ERROR_INSTRUCTOR'],{})
    else:
        if 'arguments' not in routes[controller]:
            argument_number=0
        else:
            argument_number=len(routes[controller]['arguments'])
        if  argument_number != len(uri_request[1:]):
            return "Wrong number of arguments! (Must be " + str(len(routes[controller]['arguments'])) + ")"
        else:
            arguments = {}
            if argument_number > 0:
                argindex=1
                for arg in routes[controller]['arguments']:
                    arguments[arg]=uri_request[argindex]
                    argindex+=1
            return generator.getPage(routes[controller]['instructor'],arguments)

"""
@app.route("/test")
def Test():
    config=generator.read_file("json/murakatasssystem/config.json","json","//")
    if config.split()[0] == "FileNotFoundError:":
        return ("Config File not found")
"""
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)

