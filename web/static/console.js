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

    log(msg) {
        console.log(this.prefix + ' ' + msg);
    }
}