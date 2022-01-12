class Console {
    constructor(prefix, local_storage_var) {
        this.prefix = prefix;
        this.local_storage_var = local_storage_var;
        iziToast.settings({
            position: 'bottomLeft'
        });
    }

    save(logging=false) {
        localStorage.setItem(this.local_storage_var, JSON.stringify(editor.export()));
        if(logging === true) {
            iziToast.success({
                title: lang.t("console_save"),
                message: lang.t("console_save_quest_success"),
            });
        }
    }

    import() {
        iziToast.success({
            title: lang.t("console_import"),
            message: lang.t("console_import_success"),
        });
    }

    clear() {
        iziToast.question({
            timeout: 20000,
            close: false,
            overlay: true,
            displayMode: 'once',
            id: 'question',
            zindex: 999,
            title: lang.t("console_clear"),
            message: lang.t("console_clear_warning"),
            position: 'center',
            buttons: [
                ['<button>' + lang.t("console_btn_yes") + '</button>', function (instance, toast) {
                    instance.hide({ transitionOut: 'fadeOut' }, toast, 'btn_accept');
                    editor.clearModuleSelected();
                    pyq_console.save();
                }, true],
                ['<button><b>' + lang.t("console_btn_no") + '</b></button>', function (instance, toast) {
                    instance.hide({ transitionOut: 'fadeOut' }, toast, 'btn_cancel');
                }],
            ],
            onClosing: function(instance, toast, closedBy){
                if(closedBy == 'btn_accept') {
                    iziToast.success({
                        title: lang.t("console_clear"),
                        message: lang.t("console_clear_success"),
                    });
                }
            }
        });
    }

    error(msg="Undefined error") {
        iziToast.error({
            title: lang.t("console_error"),
            message: msg,
            overlay: true,
            position: 'center',
            timeout: 10000
        });
    }

    info(msg="...", timeout=10000) {
        iziToast.info({
            message: msg,
            timeout: timeout
        });
    }

    log(msg) {
        if(typeof msg === 'string') {
            console.log(this.prefix + ' ' + msg);
        } else {
            console.log(this.prefix);
            console.log(msg);
        }
    }

    post(params) {
        params["self"] = this;
        $.ajax({url: params["url"],
                method: 'POST',
                data: params["data"],
                contentType: 'application/json;charset=UTF-8',
                success: function(response) {
                    params["self"].log(response.category.toUpperCase() + ' [' + response.status + ']: ' + response.message);
                    if(response.status == 200) {
                        params["success"]();
                    } else if(response.status == 500) {
                        params["self"].error(response.category.toUpperCase() + ' [' + response.status + ']: ' + response.message);
                    } else {
                        params["self"].error(response.category.toUpperCase() + ' [' + response.status + ']: ' + response.message);
                    }
                },
                statusCode: {
                    500: function(response) {
                        params["self"].error('[' + response.status + ']: ' + response.statusText);
                    }
                }
        });
    }
}
