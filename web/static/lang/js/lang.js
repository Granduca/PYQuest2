// lang init
class PYQLang {
    constructor(lang) {
        this.lang = lang;
        this.path = "http://127.0.0.1:5000/static/lang/js/";
        this.translation = {};
    }

    init() {
        this.#load_json(function(response, self) {
            self.translation = JSON.parse(response);
        });
    }

    #load_json(callback) {
        let xobj = new XMLHttpRequest();
        let self = this;
        xobj.overrideMimeType("application/json");
        xobj.open('GET', this.path + this.lang + '.json', true);
        xobj.onreadystatechange = function () {
            if (xobj.readyState == 4 && xobj.status == "200") {
                callback(xobj.responseText, self);
            }
        };
        xobj.send(null);
    }

    t(key) {
        return this.translation[key];
    }

    change_lang(lang) {
        this.lang = lang;
        this.init();
    }
}

var lang = new PYQLang('ru');
lang.init();