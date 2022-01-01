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
                title: 'Сохранение',
                message: 'Квест успешно сохранен!',
            });
        }
    }

    import() {
        iziToast.success({
            title: 'Импорт',
            message: 'Cохраненные данные успешно импортированы!',
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
            title: 'Очистка',
            message: 'Вы уверены, что хотите очистить редактор? Все несохраненные изменения будут потеряны!',
            position: 'center',
            buttons: [
                ['<button>ДА</button>', function (instance, toast) {
                    instance.hide({ transitionOut: 'fadeOut' }, toast, 'btn_accept');
                    editor.clearModuleSelected();
                    pyq_console.save();
                }, true],
                ['<button><b>НЕТ</b></button>', function (instance, toast) {
                    instance.hide({ transitionOut: 'fadeOut' }, toast, 'btn_cancel');
                }],
            ],
            onClosing: function(instance, toast, closedBy){
                if(closedBy == 'btn_accept') {
                    iziToast.success({
                        title: 'Очистка',
                        message: 'Редактор успешно очищен!',
                    });
                }
            }
        });
    }

    error(msg="Undefined error") {
        iziToast.error({
            title: 'Ошибка',
            message: msg,
            overlay: true,
            position: 'center',
            timeout: 10000
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
