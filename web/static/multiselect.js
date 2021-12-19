var is_multiselect = false;
var mult_arr = [];

var multiselect_dict = {};
var drag_start = false;
var active_node_id = null;

dr = new Selectables({
    zone:'#drawflow',
    elements: '.title-box',

    selectedClass: 'active',

    key: 'altKey',
    moreUsing: 'altKey',

    start: function (e) {
        if (e.altKey) {
            drag_start = false;
            is_multiselect = true;
            editor.editor_selected = false;
            editor.editor_mode = 'fixed';
            //console.log('Starting selection on ' + this.elements + ' in ' + this.zone);
       }
    },

    stop: function (e) {
        editor.editor_mode='edit';
        is_multiselect = false;
        //console.log('Finished selecting   ' + this.elements + ' in ' + this.zone);
    },

    onSelect: function (el) {      //TODO: пофиксить странности при переселектах
        let node = el.closest('.drawflow-node');
        let id = parseInt(node.id.split('-')[1]);
        if(!mult_arr.includes(id)) {
            document.getElementById("node-"+id).addEventListener('mousedown', node_mousedown, false);
            document.getElementById("node-"+id).addEventListener('mouseup', node_mouseup, false);
            mult_arr.push(id);
        }
        multiselect_dict = {};
        //console.log('onselect', el);
    },

    onDeselect: function (el) {
        node_remove_listener(el);
        multiselect_dict = {};
        //console.log('ondeselect', el);
    },

    enabled: true
});

function node_remove_listener(el) {
    let node = el.closest('.drawflow-node');
    let id = parseInt(node.id.split('-')[1]);
    document.getElementById("node-" + id).removeEventListener('mousedown', node_mousedown, false);
    document.getElementById("node-" + id).removeEventListener('mouseup', node_mouseup, false);
    let arr_index = mult_arr.indexOf(id);
    mult_arr.splice(arr_index, 1);
}

function node_mousedown(e) {
    if(e.type === 'mousedown') {
        drag_start = true;
        active_node_id = parseInt(e.currentTarget.id.split('-')[1]);
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