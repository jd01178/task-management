// Utils functions:

function urlBase64ToUint8Array (base64String) {
        var padding = '='.repeat((4 - base64String.length % 4) % 4)
        var base64 = (base64String + padding)
                .replace(/\-/g, '+')
                .replace(/_/g, '/')

        var rawData = window.atob(base64)
        var outputArray = new Uint8Array(rawData.length)

        for (var i = 0; i < rawData.length; ++i) {
                outputArray[i] = rawData.charCodeAt(i)
        }
        return outputArray;
}

function loadVersionBrowser () {
        if ("userAgentData" in navigator) {
                // navigator.userAgentData is not available in
                // Firefox and Safari
                const uaData = navigator.userAgentData;
                // Outputs of navigator.userAgentData.brands[n].brand are e.g.
                // Chrome: 'Google Chrome'
                // Edge: 'Microsoft Edge'
                // Opera: 'Opera'
                let browsername;
                let browserversion;
                let chromeVersion = null;
                for (var i = 0; i < uaData.brands.length; i++) {
                        let brand = uaData.brands[i].brand;
                        browserversion = uaData.brands[i].version;
                        if (brand.match(/opera|chrome|edge|safari|firefox|msie|trident/i) !== null) {
                                // If we have a chrome match, save the match, but try to find another match
                                // E.g. Edge can also produce a false Chrome match.
                                if (brand.match(/chrome/i) !== null) {
                                        chromeVersion = browserversion;
                                }
                                // If this is not a chrome match return immediately
                                else {
                                        browsername = brand.substr(brand.indexOf(' ')+1);
                                        return {
                                                name: browsername,
                                                version: browserversion
                                        }
                                }
                        }
                }
                // No non-Chrome match was found. If we have a chrome match, return it.
                if (chromeVersion !== null) {
                        return {
                                name: "chrome",
                                version: chromeVersion
                        }
                }
        }
        // If no userAgentData is not present, or if no match via userAgentData was found,
        // try to extract the browser name and version from userAgent
        const userAgent = navigator.userAgent;
        var ua = userAgent, tem, M = ua.match(/(opera|chrome|safari|firefox|msie|trident(?=\/))\/?\s*(\d+)/i) || [];
        if (/trident/i.test(M[1])) {
                tem = /\brv[ :]+(\d+)/g.exec(ua) || [];
                return {name: 'IE', version: (tem[1] || '')};
        }
        if (M[1] === 'Chrome') {
                tem = ua.match(/\bOPR\/(\d+)/);
                if (tem != null) {
                        return {name: 'Opera', version: tem[1]};
                }
        }
        M = M[2] ? [M[1], M[2]] : [navigator.appName, navigator.appVersion, '-?'];
        if ((tem = ua.match(/version\/(\d+)/i)) != null) {
                M.splice(1, 1, tem[1]);
        }
        return {
                name: M[0],
                version: M[1]
        };
};
var applicationServerKey = "BEFuGfKKEFp-kEBMxAIw7ng8HeH_QwnH5_h55ijKD4FRvgdJU1GVlDo8K5U5ak4cMZdQTUJlkA34llWF0xHya70";

// In your ready listener
if ('serviceWorker' in navigator) {
        // The service worker has to store in the root of the app
        // http://stackoverflow.com/questions/29874068/navigator-serviceworker-is-never-ready
        var browser = loadVersionBrowser();
        navigator.serviceWorker.register('navigatorPush.service.js?version=1.0.0').then(function (reg) {
                reg.pushManager.subscribe({
                        userVisibleOnly: true,
                        applicationServerKey: urlBase64ToUint8Array(applicationServerKey)
                }).then(function (sub) {
                        var endpointParts = sub.endpoint.split('/');
                        var registration_id = endpointParts[endpointParts.length - 1];
                        var data = {
                                'browser': browser.name.toUpperCase(),
                                'p256dh': btoa(String.fromCharCode.apply(null, new Uint8Array(sub.getKey('p256dh')))),
                                'auth': btoa(String.fromCharCode.apply(null, new Uint8Array(sub.getKey('auth')))),
                                'name': 'XXXXX',
                                'registration_id': registration_id
                        };
                        requestPOSTToServer(data);
                })
        }).catch(function (err) {
                console.log(':^(', err);
        });


// Example navigatorPush.service.js file

        var getTitle = function (title) {
                if (title === "") {
                        title = "TITLE DEFAULT";
                }
                return title;
        };
        var getNotificationOptions = function (message, message_tag) {
                var options = {
                        body: message,
                        icon: '/img/icon_120.png',
                        tag: message_tag,
                        vibrate: [200, 100, 200, 100, 200, 100, 200]
                };
                return options;
        };

        self.addEventListener('install', function (event) {
                self.skipWaiting();
        });

        self.addEventListener('push', function (event) {
                try {
                        // Push is a JSON
                        var response_json = event.data.json();
                        var title = response_json.title;
                        var message = response_json.message;
                        var message_tag = response_json.tag;
                } catch (err) {
                        // Push is a simple text
                        var title = "";
                        var message = event.data.text();
                        var message_tag = "";
                }
                self.registration.showNotification(getTitle(title), getNotificationOptions(message, message_tag));
                // Optional: Comunicating with our js application. Send a signal
                self.clients.matchAll({includeUncontrolled: true, type: 'window'}).then(function (clients) {
                        clients.forEach(function (client) {
                                client.postMessage({
                                        "data": message_tag,
                                        "data_title": title,
                                        "data_body": message
                                });
                        });
                });
        });

// Optional: Added to that the browser opens when you click on the notification push web.
        self.addEventListener('notificationclick', function (event) {
                // Android doesn't close the notification when you click it
                // See http://crbug.com/463146
                event.notification.close();
                // Check if there's already a tab open with this URL.
                // If yes: focus on the tab.
                // If no: open a tab with the URL.
                event.waitUntil(clients.matchAll({
                            type: 'window',
                            includeUncontrolled: true
                    }).then(function (windowClients) {
                            for (var i = 0; i < windowClients.length; i++) {
                                    var client = windowClients[i];
                                    if ('focus' in client) {
                                            return client.focus();
                                    }
                            }
                    })
                );
        });
}

