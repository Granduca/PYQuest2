// lang init
class PYQLang {
    constructor(lang, path) {
        this.lang = lang;
        this.path = path;
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
