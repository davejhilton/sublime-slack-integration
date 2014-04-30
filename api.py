import json
import subprocess
import sublime

try:
    from urllib.parse import urlencode
    from urllib.request import urlopen
except ImportError:
    from urllib import urlencode, urlopen

BASE_URL = 'https://slack.com/api/'


def api_call(method, call_args={}, loading=None, filename=None, icon=None):

    if icon:
        call_args['icon_url'] = icon
        print('icon', icon)
    URL = BASE_URL + method + "?" + urlencode(call_args)
    print('calling:', URL)
    try:
        if filename:
            f = open(filename, 'rb')
            filebody = f.read()
            f.close()
            data = urlencode({'content': filebody})

            response = urlopen(
                url=URL,
                data=data.encode('utf8')
            ).read().decode('utf8')
        else:
            response = urlopen(url=URL).read().decode('utf8')
    except:
        # fallback for sublime bug with urlopen (on linux only)
        if filename:  # upload filename
            proc = subprocess.Popen(
                ['curl', '-X', 'POST', '-F', 'file=@'+filename, URL],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE)
        else:
            proc = subprocess.Popen(
                ['curl', '-s', URL],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE)
        out, err = proc.communicate()

        response = out.decode('utf8')

    response = json.loads(response)

    if not response['ok']:
        sublime.error_message("SLACK Api error: " + response['error'])
        if loading:
            loading.done = True
        return False

    return response
