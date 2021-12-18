//drawflow init
var id = document.getElementById("drawflow");

const editor = new Drawflow(id);

editor.reroute = true;
editor.reroute_fix_curvature = true;

var node_created_id = null;
var node_selected_id = null;

var start_indicated = false;
var start_indicated_id = -1;

var textarea_is_selected = false;

var mobile_item_selec = '';
var mobile_last_move = null;
var transform = '';

var bar_zoom_text = document.getElementById("bar-zoom text");

//editor init
editor.start();

// editor.import(dataToImport);
// editor.addModule('Other');

//Local storage
var retrievedObject = localStorage.getItem('user_workflow');

if (typeof retrievedObject !== 'undefined') {
    if (retrievedObject != null) {
        editor.import(JSON.parse(retrievedObject))
        console.log(retrievedObject)
    } else {
        localStorage.setItem('user_workflow', JSON.stringify(editor.export()));
        retrievedObject = localStorage.getItem('user_workflow');
    }
}

//Templates
var textarea_template = 'Введите ваш текст...';

function set_node_template(key, text='', height='100') {
    var nodes_template = {
        'start': node_html_setter("title-box start noselect", "set_start(event)", "fas fa-play-circle", "Начало", text, height),
        'finish': node_html_setter("title-box finish noselect", "set_finish(event)", "fas fa-stop-circle", "Конец", text, height),
        'question': node_html_setter("title-box noselect", "set_start(event)", "fas fa-question-circle", "Вопрос", text, height),
        'question_not_connected': node_html_setter("title-box not_connected noselect", "set_start(event)", "fas fa-question-circle", "Вопрос", text, height),
        'answer': node_html_setter("title-box noselect", "set_finish(event)", "fas fa-comment-dots", "Ответ", text, height),
        'answer_not_connected': node_html_setter("title-box not_connected noselect", "set_finish(event)", "fas fa-comment-dots", "Ответ", text, height),
        'link': node_html_setter("title-box link not_connected noselect", "", "fas fa-link", "Переход", text, height),
    }
    return nodes_template[key];
}

function node_html_setter(title_box, node_func, node_icon, node_text, text, height) {
    let header = `<div class="${title_box}" ondblclick="${node_func}"><i class="${node_icon}"></i> ${node_text}</div>`;
    let body = `<div class="box noselect">` + textarea_setter(text, height) + `</div>`;
    if(title_box.includes('link') == true) {body = `<div class="box" ondblclick="${node_func}">Двойной клик, чтобы назначить переход...</div>`;}
    let template = `<div>` + header + body + `</div>`;
    return template;
}

function textarea_setter(t, h) {
    text = '';
    if (t != '') { text = t;}
    return `<textarea df-template class="vertical" style="height:${h}px;" placeholder="${textarea_template}">${text}</textarea>`;
}


// Events!
const observer = new ResizeObserver(observerCallback, { threshold: 1.0 });

function observerCallback(entries, observer) {
    for (let entry of entries) {
        const height = Math.floor(entry.contentRect.height);
        //console.log(height);
        if(height == 0) {
            observer.unobserve(entry.target);
            update_resize_observers();
            break;
        }
        let parent_id = getParentNode(entry.target, 4).id;
        let id = parent_id.split('-')[1];
        if(typeof editor.drawflow.drawflow.Home.data[id] !== "undefined") {
            let node = editor.getNodeFromId(id);
            text = set_node_template(node.name, node.data['template'], height);
            editor.drawflow.drawflow.Home.data[id].html = text;
            editor.updateConnectionNodes(`node-${id}`);
        }
    }
    localStorage.setItem('user_workflow', JSON.stringify(editor.export()));
}

function update_resize_observers() {
    let textareas = document.querySelectorAll('.vertical');
    textareas.forEach(ta => {
        observer.observe(ta);
    });
}
update_resize_observers();

editor.on('nodeCreated', function(id) {
    node_created_id = id;
    //console.log("Node created " + id);
    dr.disable(); dr.enable();
    update_resize_observers();
    localStorage.setItem('user_workflow', JSON.stringify(editor.export()));
})

editor.on('nodeRemoved', function(id) {
    //console.log("Node removed " + id);
    dr.disable(); dr.enable();
    let textareas = document.querySelectorAll('.vertical');
    update_resize_observers();
    localStorage.setItem('user_workflow', JSON.stringify(editor.export()));
})

editor.on('nodeSelected', function(id) {
    node_selected_id = id;
    //console.log("Node selected " + id);
    localStorage.setItem('user_workflow', JSON.stringify(editor.export()));
})

editor.on('nodeDataChanged', function(id) {
    //console.log("Node value updated " + id);
    dr.disable(); dr.enable();
    localStorage.setItem('user_workflow', JSON.stringify(editor.export()));
})

editor.on('moduleCreated', function(name) {
    console.log("Module Created " + name);
})

editor.on('moduleChanged', function(name) {
    console.log("Module Changed " + name);
})

editor.on('connectionCreated', function(connection) {
    //console.log('Connection created');
    //console.log(connection);
    check_connection(connection['input_id']);
    check_connection(connection['output_id']);
    dr.disable(); dr.enable();
//    update_resize_observers();
    localStorage.setItem('user_workflow', JSON.stringify(editor.export()));
})

editor.on('connectionRemoved', function(connection) {
    console.log('Connection removed');
    console.log(connection);
    check_connection(connection['input_id']);
    check_connection(connection['output_id']);
    dr.disable(); dr.enable();
//    update_resize_observers();
    localStorage.setItem('user_workflow', JSON.stringify(editor.export()));
})

editor.on('mouseMove', function(position) {
    if(drag_start == true) {
        for (i of mult_arr) {
            if(i != active_node_id) {
                if(typeof editor.drawflow.drawflow.Home.data[i] !== "undefined") {
                    let node = editor.getNodeFromId(active_node_id);
                    let elem = document.getElementById("node-"+i).children[1].children[0];
                    let pos_x = multiselect_dict[i]['pos_x'];
                    let pos_y = multiselect_dict[i]['pos_y'];
                    editor.drawflow.drawflow.Home.data[i].pos_x = node.pos_x + pos_x;
                    editor.drawflow.drawflow.Home.data[i].pos_y = node.pos_y + pos_y;
                    document.getElementById(`node-${i}`).style.left = (node.pos_x + pos_x) + "px";
                    document.getElementById(`node-${i}`).style.top = (node.pos_y + pos_y) + "px";
                    editor.updateConnectionNodes(`node-${i}`);
                }
            }
        }
    }
    //console.log('Position mouse x:' + position.x + ' y:'+ position.y);
    //pass
})

editor.on('nodeMoved', function(id) {
//    console.log("Node moved " + id);
    localStorage.setItem('user_workflow', JSON.stringify(editor.export()));
})

editor.on('zoom', function(zoom) {
    //console.log('Zoom level ' + zoom);
    bar_zoom_text.innerHTML = 100 * Math.floor(zoom*10)/10 + '%';
})

editor.on('translate', function(position) {
    //localStorage.setItem('user_workflow', JSON.stringify(editor.export()));
    //pass
})

editor.on('addReroute', function(id) {
    console.log("Reroute added " + id);
    localStorage.setItem('user_workflow', JSON.stringify(editor.export()));
})

editor.on('removeReroute', function(id) {
    console.log("Reroute removed " + id);
    localStorage.setItem('user_workflow', JSON.stringify(editor.export()));
})

document.getElementById('drawflow').addEventListener('dblclick', clear_selection, false);
function clear_selection(e) {
    dr.foreach(dr.items, function (el) {
        el.classList.remove(dr.options.selectedClass);
        node_remove_listener(el);
    });
}

editor.on('click', (e) => {
    if(e.target.tagName == 'TEXTAREA') {
        textarea_is_selected = true;
        editor.editor_mode='fixed';
    } else {
        if(textarea_is_selected == true) {
            textarea_is_selected = false;
            editor.editor_mode='edit';
        }
    }
})

/* DRAG EVENT */

/* Mouse and Touch Actions */

var elements = document.getElementsByClassName('drag-drawflow');
for (var i = 0; i < elements.length; i++) {
    elements[i].addEventListener('touchend', drop, false);
    elements[i].addEventListener('touchmove', positionMobile, false);
    elements[i].addEventListener('touchstart', drag, false );
}

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
            editor.addNode('start', 0, 1, pos_x, pos_y, 'start', { "template": data}, set_node_template('start'));
            break;

        case 'finish':
            editor.addNode('finish', 1, 0, pos_x, pos_y, 'finish', { "template": data}, set_node_template('finish'));
            break;

        case 'question':
            editor.addNode('question', 1, 1, pos_x, pos_y, 'question', { "template": data}, set_node_template('question'));
            break;

        case 'question_not_connected':
            editor.addNode('question_not_connected', 1, 1, pos_x, pos_y, 'question_not_connected', { "template": data}, set_node_template('question_not_connected'));
            break;

        case 'answer':
            editor.addNode('answer', 1, 1, pos_x, pos_y, 'answer', { "template": data}, set_node_template('answer'));
            break;

        case 'answer_not_connected':
            editor.addNode('answer_not_connected', 1, 1, pos_x, pos_y, 'answer_not_connected', { "template": data}, set_node_template('answer_not_connected'));
            break;

        case 'link':
            editor.addNode('link', 1, 0, pos_x, pos_y, 'link', { "template": data}, set_node_template('link'));
            break;
    }
}

//MISC
function check_connection(id) {
    node = editor.getNodeFromId(id);
    let elem = document.getElementById("node-"+id).children[1];
    let height = null;
    if(!elem.parentElement.classList.contains('link')) {
        height = parseInt(elem.querySelector('.vertical').style.height);
    }
    if (node.class.includes('question') == true) {
        if ((node.inputs['input_1']['connections'].length == 0) || (node.outputs['output_1']['connections'].length == 0)) {
            text = set_node_template('question_not_connected', node.data['template'], height);
            elem.innerHTML = text;
            editor.drawflow.drawflow.Home.data[id].html = text;
            editor.drawflow.drawflow.Home.data[id].class = 'question_not_connected';
        } else {
            text = set_node_template('question', node.data['template'], height);
            elem.innerHTML = text;
            editor.drawflow.drawflow.Home.data[id].html = text;
            editor.drawflow.drawflow.Home.data[id].class = 'question';
        }
    }else if (node.class.includes('answer') == true) {
        if ((node.inputs['input_1']['connections'].length == 0) || (node.outputs['output_1']['connections'].length == 0)) {
            text = set_node_template('answer_not_connected', node.data['template'], height);
            elem.innerHTML = text;
            editor.drawflow.drawflow.Home.data[id].html = text;
            editor.drawflow.drawflow.Home.data[id].class = 'answer_not_connected';
        } else {
            text = set_node_template('answer', node.data['template'], height);
            elem.innerHTML = text;
            editor.drawflow.drawflow.Home.data[id].html = text;
            editor.drawflow.drawflow.Home.data[id].class = 'answer';
        }
    }else if (node.class.includes('link') == true) {
        if (node.inputs['input_1']['connections'].length == 0) {
            if(!elem.children[0].children[0].classList.contains('not_connected')) {
                elem.children[0].children[0].classList.add('not_connected');    //TODO: добавить режим выбора
            }
        } else {
            if(elem.children[0].children[0].classList.contains('not_connected')) {
                elem.children[0].children[0].classList.remove('not_connected');
            }
        }
    }
    editor.updateConnectionNodes("node-"+id);
}

function set_start(e) {
    e.stopPropagation();
    node = editor.getNodeFromId(node_selected_id)
    if (node.class.includes('question') == true) {
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
    } else if (node.class == 'start') {
        if (start_indicated == true) {
            change_node_type(node_selected_id, 'question_not_connected', 'output')
            start_indicated = false;
            start_indicated_id = -1;
        }
    }
    localStorage.setItem('user_workflow', JSON.stringify(editor.export()));
}

function set_finish(e) {
    e.stopPropagation();
    node = editor.getNodeFromId(node_selected_id)
    if (node.class.includes('answer') == true) {
        change_node_type(node_selected_id, 'finish', 'input')
    } else if (node.class == 'finish') {
        change_node_type(node_selected_id, 'answer_not_connected', 'input')
    }
    localStorage.setItem('user_workflow', JSON.stringify(editor.export()));
}

function change_node_type(old_id, node_class, side) {
    node = editor.getNodeFromId(old_id);
    addNodeToDrawFlow(node_class, node.pos_x, node.pos_y, node.data['template'], true);

    let elem = document.getElementById("node-"+old_id).children[1];
    let new_elem = document.getElementById("node-"+node_created_id).children[1];

    let height = parseInt(elem.querySelector('.vertical').style.height);

    let new_node = editor.getNodeFromId(node_created_id);
    text = set_node_template(new_node.class, new_node.data['template'], height);

    new_elem.innerHTML = text;
    editor.drawflow.drawflow.Home.data[node_created_id].html = text;

    if (side == 'input') {
        //console.log(node.inputs['input_1']['connections']);
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

function export_json() {
    $.ajax({url: 'data',
            method: 'POST',
            data: JSON.stringify(editor.export()),
            contentType: 'application/json;charset=UTF-8',
            success: function(data) {console.log(data);}});
    localStorage.setItem('user_workflow', JSON.stringify(editor.export()));
    Swal.fire({title: 'Export',
               html: '<textarea rows="30" cols="50">'+JSON.stringify(editor.export(),null,4).replace(/<[^>]*>/g, '')+'</textarea>'})
}

function editor_clear() {
    editor.clearModuleSelected();
    localStorage.setItem('user_workflow', JSON.stringify(editor.export()));
}

function getParentNode(element, level = 1) {
    while (level-- > 0) {
      element = element.parentNode;
      if (!element) return null;
    }
    return element;
}