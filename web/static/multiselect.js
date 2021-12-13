var is_multiselect = false;
var mult_arr = [];

var multiselect_dict = {};
var drag_start = false;
var active_node_id = null;

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
        is_multiselect = false;
//        console.log('Finished selecting   ' + this.elements + ' in ' + this.zone);
    },

    onSelect: function (el) {
        if(el.id.includes('node-') == true) {
            let id = parseInt(el.id.charAt(el.id.length-1));
            document.getElementById("node-"+id).addEventListener('mousedown', node_mousedown, false);
            document.getElementById("node-"+id).addEventListener('mouseup', node_mouseup, false);
            mult_arr.push(id);
        }
//        console.log(mult_arr);
        //pass
        //console.log(el)
//        console.log('onselect', el);
    },

    onDeselect: function (el) {     //TODO: Не работает! Обязательно пофиксить! Иначе будут плодиться листнеры.
        editor.editor_selected = true;
        is_multiselect = false;
        for(value of mult_arr) {
            document.getElementById("node-"+value).removeEventListener('mousedown', node_mousedown, false);
            document.getElementById("node-"+value).removeEventListener('mouseup', node_mouseup, false);
        }
        mult_arr = [];
//        console.log('ondeselect', el);
    },

    enabled: true
});


function node_mousedown(e) {
    if(e.type === 'mousedown') {
        drag_start = true;
        active_node_id = parseInt(e.currentTarget.id.charAt(e.currentTarget.id.length-1));
        for (i=1; i<=editor.nodeId; i++) {
            if(typeof editor.drawflow.drawflow.Home.data[i] !== "undefined") {
                let node = editor.getNodeFromId(active_node_id);
                multiselect_dict[i] = {'pos_x': editor.drawflow.drawflow.Home.data[i].pos_x - node.pos_x,
                                        'pos_y': editor.drawflow.drawflow.Home.data[i].pos_y - node.pos_y,};
            }
        }
    }
}


function node_mouseup(e) {
    if(e.type === 'mouseup') {
        drag_start = false;
        active_node_id = null;
        multiselect_dict = {};
    }
}