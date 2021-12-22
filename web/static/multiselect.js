var is_multiselect = false;
var mult_arr = [];

var multiselect_dict = {};
var drag_start = false;
var active_node_id = null;

var dr = new Selectables({
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
            //pyq_console.log('Starting selection on ' + this.elements + ' in ' + this.zone);
       }
    },

    stop: function (e) {
        editor.editor_mode='edit';
        is_multiselect = false;
        //pyq_console.log('Finished selecting   ' + this.elements + ' in ' + this.zone);
    },

    onSelect: function (el) {
        let node = el.closest('.drawflow-node');
        let id = parseInt(node.id.split('-')[1]);
        if(!mult_arr.includes(id)) {
            document.getElementById("node-"+id).addEventListener('mousedown', node_mousedown, false);
            document.getElementById("node-"+id).addEventListener('mouseup', node_mouseup, false);
            mult_arr.push(id);
        }
        multiselect_dict = {};
        //pyq_console.log('onselect', el);
    },

    onDeselect: function (el) {
        node_remove_listener(el);
        multiselect_dict = {};
        //pyq_console.log('ondeselect', el);
    },

    enabled: true
});

let rb = function () {
    return document.getElementById('s-rectBox');
};

let cross = function (a, b) {
    let aTop = offset(a).top, aLeft = offset(a).left, bTop = offset(b).top, bLeft = offset(b).left;
    return !(((aTop + a.offsetHeight) < (bTop)) || (aTop > (bTop + b.offsetHeight * editor.zoom)) || ((aLeft + a.offsetWidth) < bLeft) || (aLeft > (bLeft + b.offsetWidth * editor.zoom)));
};

let offset = function (el) {
    let r = el.getBoundingClientRect();
    return {top: r.top + document.body.scrollTop, left: r.left + document.body.scrollLeft}
};

dr.select = function (e) {
    let a = rb();
    if (!a) {
        return;
    }
    delete(dr.ipos);
    document.body.classList.remove('s-noselect');
    document.body.removeEventListener('mousemove', dr.rectDraw);
    window.removeEventListener('mouseup', dr.select);
    let s = dr.options.selectedClass;
    dr.foreach(dr.items, function (el) {
        if (cross(a, el) === true) {
            if (el.classList.contains(s)) {
                el.classList.remove(s);
                dr.options.onDeselect && dr.options.onDeselect(el);
            } else {
                el.classList.add(s);
                dr.options.onSelect && dr.options.onSelect(el);
            }
        }
        setTimeout(function () {
            el.removeEventListener('click', dr.suspend, true);
        }, 100);
    });
    a.parentNode.removeChild(a);
    dr.options.stop && dr.options.stop(e);
}

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
        let node = editor.getNodeFromId(active_node_id);
        for (let i = 1; i <= editor.nodeId; i++) {
            if(typeof editor.drawflow.drawflow.Home.data[i] !== "undefined") {
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