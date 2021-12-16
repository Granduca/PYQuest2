var is_multiselect = false;
var mult_arr = [];

var multiselect_dict = {};
var drag_start = false;
var active_node_id = null;

dr = new Selectables({
    zone:'#drawflow',
    elements: ['.drawflow-node', '.title-box'],

    selectedClass: 'active',

    key: 'altKey',
    moreUsing: 'altKey',

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
        //console.log('Finished selecting   ' + this.elements + ' in ' + this.zone);
    },

    onSelect: function (el) {
        if(el.id.includes('node-') == true) {
            let id = parseInt(el.id.charAt(el.id.length-1));
            document.getElementById("node-"+id).addEventListener('mousedown', node_mousedown, false);
            document.getElementById("node-"+id).addEventListener('mouseup', node_mouseup, false);
            mult_arr.push(id);
        }
        //console.log('onselect', el);
    },

    onDeselect: function (el) {
        node_remove_listener(el);
        //console.log('ondeselect', el);
    },

    enabled: true
});

function node_remove_listener(el) {
    if(el.id.includes('node-') == true) {
        let temp_arr = [];
        for(value of mult_arr) {
            let id = parseInt(el.id.split('-')[1]);
            if(value == id) {
                document.getElementById("node-"+value).removeEventListener('mousedown', node_mousedown, false);
                document.getElementById("node-"+value).removeEventListener('mouseup', node_mouseup, false);
                temp_arr.push(value);
            }
        }
        for(value of temp_arr) {
            mult_arr = mult_arr.filter(function(ele){return ele != value;});
        }
    }
}

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