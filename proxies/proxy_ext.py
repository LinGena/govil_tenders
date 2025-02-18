import os


def load_proxy(proxy: str, plugin_path: str) -> None:
    proxy = proxy.replace('https://', '').replace('http://', '')
    PROXY_HOST = proxy.split('@')[1].split(':')[0]
    PROXY_PORT = proxy.split('@')[1].split(':')[1]
    PROXY_USER = proxy.split('@')[0].split(':')[0]
    PROXY_PASS = proxy.split('@')[0].split(':')[1]

    manifest_json = """
    {
        "version": "1.0.0",
        "manifest_version": 2,
        "name": "Chrome Proxy",
        "permissions": [
            "proxy",
            "tabs",
            "unlimitedStorage",
            "storage",
            "<all_urls>",
            "webRequest",
            "webRequestBlocking"
        ],
        "background": {
            "scripts": ["background.js"]
        },
        "minimum_chrome_version":"22.0.0"
    }
    """

    background_js = """
    var config = {
            mode: "fixed_servers",
            rules: {
            singleProxy: {
                scheme: "http",
                host: "%s",
                port: parseInt(%s)
            },
            bypassList: ["localhost"]
            }
        };

    chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

    function callbackFn(details) {
        return {
            authCredentials: {
                username: "%s",
                password: "%s"
            }
        };
    }

    chrome.webRequest.onAuthRequired.addListener(
   callbackFn,
    {urls: ["<all_urls>"]},
    ['blocking']
    );
    """ % (PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS)
    
    os.makedirs(plugin_path, exist_ok=True)

    with open(os.path.join(plugin_path, "manifest.json"), "w") as manifest_file:
        manifest_file.write(manifest_json)

    with open(os.path.join(plugin_path, "background.js"), "w") as background_file:
        background_file.write(background_js)