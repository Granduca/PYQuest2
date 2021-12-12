var is_multiselect = false;
dr = new Selectables({
    zone:'#drawflow',
    elements: 'div',

    selectedClass: 'active',

    key: 'altKey',

    start: function (e) {
        if (e.altKey) {
            is_multiselect = true;
            editor.editor_selected = false;
            editor.editor_mode = 'fixed';
            //console.log('Starting selection on ' + this.elements + ' in ' + this.zone);
       }
    },

    stop: function (e) {
        editor.editor_mode='edit';
        //console.log('Finished selecting   ' + this.elements + ' in ' + this.zone);
    },

    onSelect: function (el) {
        //pass
        //console.log(el)
        //console.log('onselect', el);
    },

    onDeselect: function (el) {
        editor.editor_selected = true;
        is_multiselect = false;
        //console.log('ondeselect', el);
    },

    enabled: true
});