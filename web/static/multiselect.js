dr = new Selectables({
    zone:'#drawflow',
    elements: 'div',

    selectedClass: 'active',

    key: 'altKey',

    start: function (e) {
       if (e.altKey) {
            editor.editor_mode = 'fixed';
            console.log('Starting selection on ' + this.elements + ' in ' + this.zone);
       }
    },

    stop: function (e) {
       editor.editor_mode='edit';
       console.log('Finished selecting   ' + this.elements + ' in ' + this.zone);
    },

    onSelect: function (el) {
        console.log(el)
       console.log('onselect', el);
    },

    onDeselect: function (el) {
       console.log('ondeselect', el);
    },

    enabled: true
});