var id = document.getElementById("drawflow");
const editor = new Drawflow(id);
editor.reroute = true;

var retrievedObject = localStorage.getItem('user_workflow');

editor.start();

// editor.import(dataToImport);

if (typeof retrievedObject !== 'undefined') {
    if (retrievedObject != null) {
        editor.import(JSON.parse(retrievedObject))
        console.log(retrievedObject)
    } else {
        localStorage.setItem('user_workflow', JSON.stringify(editor.export()));
        retrievedObject = localStorage.getItem('user_workflow');
    }
}

// editor.addModule('Other');

// Events!
var node_created_id = null;
editor.on('nodeCreated', function(id) {
    localStorage.setItem('user_workflow', JSON.stringify(editor.export()));
    node_created_id = id;
    console.log("Node created " + id);
})

editor.on('nodeRemoved', function(id) {
    localStorage.setItem('user_workflow', JSON.stringify(editor.export()));
    console.log("Node removed " + id);
})

var node_selected_id = null;
editor.on('nodeSelected', function(id) {
    localStorage.setItem('user_workflow', JSON.stringify(editor.export()));
    node_selected_id = id;
    console.log("Node selected " + id);
})

editor.on('nodeDataChanged', function(id) {
    localStorage.setItem('user_workflow', JSON.stringify(editor.export()));
    console.log("Node value updated " + id);
})

editor.on('moduleCreated', function(name) {
    console.log("Module Created " + name);
})

editor.on('moduleChanged', function(name) {
    console.log("Module Changed " + name);
})

editor.on('connectionCreated', function(connection) {
    localStorage.setItem('user_workflow', JSON.stringify(editor.export()));
    console.log('Connection created');
    console.log(connection);
})

editor.on('connectionRemoved', function(connection) {
    localStorage.setItem('user_workflow', JSON.stringify(editor.export()));
    console.log('Connection removed');
    console.log(connection);
})

editor.on('mouseMove', function(position) {
    //console.log('Position mouse x:' + position.x + ' y:'+ position.y);
    //pass
})

editor.on('nodeMoved', function(id) {
    localStorage.setItem('user_workflow', JSON.stringify(editor.export()));
    console.log("Node moved " + id);
})

var bar_zoom_text = document.getElementById("bar-zoom text");
editor.on('zoom', function(zoom) {
    //console.log('Zoom level ' + zoom);
    bar_zoom_text.innerHTML = 100 * Math.floor(zoom*10)/10 + '%';
})

editor.on('translate', function(position) {
    //localStorage.setItem('user_workflow', JSON.stringify(editor.export()));
    //console.log('Translate x:' + position.x + ' y:'+ position.y);
    //pass
})

editor.on('addReroute', function(id) {
    localStorage.setItem('user_workflow', JSON.stringify(editor.export()));
    console.log("Reroute added " + id);
})

editor.on('removeReroute', function(id) {
    localStorage.setItem('user_workflow', JSON.stringify(editor.export()));
    console.log("Reroute removed " + id);
})

/* DRAG EVENT */

/* Mouse and Touch Actions */

var elements = document.getElementsByClassName('drag-drawflow');
for (var i = 0; i < elements.length; i++) {
    elements[i].addEventListener('touchend', drop, false);
    elements[i].addEventListener('touchmove', positionMobile, false);
    elements[i].addEventListener('touchstart', drag, false );
}

var mobile_item_selec = '';
var mobile_last_move = null;
function positionMobile(ev) {
    mobile_last_move = ev;
}

function allowDrop(ev) {
    ev.preventDefault();
}

function drag(ev) {
    if (ev.type === "touchstart") {
        mobile_item_selec = ev.target.closest(".drag-drawflow").getAttribute('data-node');
    } else {
        ev.dataTransfer.setData("node", ev.target.getAttribute('data-node'));
    }
}

function drop(ev) {
    if (ev.type === "touchend") {
        var parentdrawflow = document.elementFromPoint( mobile_last_move.touches[0].clientX, mobile_last_move.touches[0].clientY).closest("#drawflow");
        if(parentdrawflow != null) {
            addNodeToDrawFlow(mobile_item_selec, mobile_last_move.touches[0].clientX, mobile_last_move.touches[0].clientY);
        }
        mobile_item_selec = '';
    } else {
        ev.preventDefault();
        var data = ev.dataTransfer.getData("node");
        addNodeToDrawFlow(data, ev.clientX, ev.clientY);
    }
}

function addNodeToDrawFlow(name, pos_x, pos_y, data='', auto=false) {
    if(editor.editor_mode === 'fixed') {
        return false;
    }
    if (auto != true) {
        pos_x = pos_x * ( editor.precanvas.clientWidth / (editor.precanvas.clientWidth * editor.zoom)) - (editor.precanvas.getBoundingClientRect().x * ( editor.precanvas.clientWidth / (editor.precanvas.clientWidth * editor.zoom)));
        pos_y = pos_y * ( editor.precanvas.clientHeight / (editor.precanvas.clientHeight * editor.zoom)) - (editor.precanvas.getBoundingClientRect().y * ( editor.precanvas.clientHeight / (editor.precanvas.clientHeight * editor.zoom)));
    }

    switch (name) {
        case 'start':
            var start = `
                <div>
                    <div class="title-box start" ondblclick="set_start(event)"><i class="fas fa-play-circle"></i> ????????????</div>
                    <div class="box">
                        <textarea df-template placeholder='?????????????? ?????? ??????????...'></textarea>
                    </div>
                </div>
            `;
            editor.addNode('start', 0, 1, pos_x, pos_y, 'start', { "template": data}, start);
            break;

        case 'finish':
            var finish = `
                <div>
                    <div class="title-box finish" ondblclick="set_finish(event)"><i class="fas fa-stop-circle"></i> ??????????</div>
                    <div class="box">
                        <textarea df-template placeholder='?????????????? ?????? ??????????...'></textarea>
                    </div>
                </div>
            `;
            editor.addNode('finish', 1, 0, pos_x, pos_y, 'finish', { "template": data}, finish);
            break;

        case 'question':
            var question = `
                <div>
                    <div class="title-box" ondblclick="set_start(event)"><i class="fas fa-question-circle"></i> ????????????</div>
                    <div class="box">
                        <textarea df-template placeholder='?????????????? ?????? ??????????...'></textarea>
                    </div>
                </div>
            `;
            editor.addNode('question', 1, 1, pos_x, pos_y, 'question', { "template": data}, question);
            break;

        case 'answer':
            var answer = `
                <div>
                    <div class="title-box" ondblclick="set_finish(event)"><i class="fas fa-comment-dots"></i> ??????????</div>
                    <div class="box">
                        <textarea df-template placeholder='?????????????? ?????? ??????????...'></textarea>
                    </div>
                </div>
            `;
            editor.addNode('answer', 1, 1, pos_x, pos_y, 'answer', { "template": data}, answer);
            break;
    }
}

var start_indicated = false;
var start_indicated_id = -1;
function set_start(e) {
    node = editor.getNodeFromId(node_selected_id)
    if (node.class == 'question') {
        if (start_indicated == false) {
            change_node_type(node_selected_id, 'start', 'output')
            start_indicated = true;
            start_indicated_id = node_created_id;
        } else {
            change_node_type(start_indicated_id, 'question', 'output')
            change_node_type(node_selected_id, 'start', 'output')
            start_indicated = true;
            start_indicated_id = node_created_id;
        }
    }
    if (node.class == 'start') {
        if (start_indicated == true) {
            console.log('ok')
            change_node_type(node_selected_id, 'question', 'output')
            start_indicated = false;
            start_indicated_id = -1;
        }
    }
    localStorage.setItem('user_workflow', JSON.stringify(editor.export()));
}

function set_finish(e) {
    node = editor.getNodeFromId(node_selected_id)
    if (node.class == 'answer') {
        change_node_type(node_selected_id, 'finish', 'input')
    }
    if (node.class == 'finish') {
        change_node_type(node_selected_id, 'answer', 'input')
    }
    localStorage.setItem('user_workflow', JSON.stringify(editor.export()));
}

function change_node_type(old_id, node_class, side) {
    node = editor.getNodeFromId(old_id);
    addNodeToDrawFlow(node_class, node.pos_x, node.pos_y, node.data['template'], true);
    if (side == 'input') {
        for (let value of node.inputs['input_1']['connections']) {
            editor.addConnection(value['node'], node_created_id, 'output_1', 'input_1');
        }
    }
    if (side == 'output') {
        for (let value of node.outputs['output_1']['connections']) {
            editor.addConnection(node_created_id, value['node'], 'output_1', 'input_1');
        }
    }
    editor.removeNodeId('node-' + old_id);
}

var transform = '';
function showpopup(e) {
    e.target.closest(".drawflow-node").style.zIndex = "9999";
    e.target.children[0].style.display = "block";
    //document.getElementById("modalfix").style.display = "block";

    //e.target.children[0].style.transform = 'translate('+translate.x+'px, '+translate.y+'px)';
    transform = editor.precanvas.style.transform;
    editor.precanvas.style.transform = '';
    editor.precanvas.style.left = editor.canvas_x +'px';
    editor.precanvas.style.top = editor.canvas_y +'px';
    console.log(transform);

    //e.target.children[0].style.top  =  -editor.canvas_y - editor.container.offsetTop +'px';
    //e.target.children[0].style.left  =  -editor.canvas_x  - editor.container.offsetLeft +'px';
    editor.editor_mode = "fixed";
}

function closemodal(e) {
    e.target.closest(".drawflow-node").style.zIndex = "2";
    e.target.parentElement.parentElement.style.display  ="none";
    //document.getElementById("modalfix").style.display = "none";
    editor.precanvas.style.transform = transform;
    editor.precanvas.style.left = '0px';
    editor.precanvas.style.top = '0px';
    editor.editor_mode = "edit";
}

function changeModule(event) {
    var all = document.querySelectorAll(".menu ul li");
    for (var i = 0; i < all.length; i++) {
        all[i].classList.remove('selected');
    }
    event.target.classList.add('selected');
}

function changeMode(option) {
//console.log(lock.id);
    if(option == 'lock') {
        lock.style.display = 'none';
        unlock.style.display = 'block';
    } else {
        lock.style.display = 'block';
        unlock.style.display = 'none';
    }
}