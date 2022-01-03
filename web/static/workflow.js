//drawflow init
var id = document.getElementById("drawflow");

const editor = new Drawflow(id);

editor.zoom_min = 0.2;
editor.reroute = true;
editor.reroute_fix_curvature = true;

var node_created_id = null;
var node_selected_id = null;

var start_indicated = false;
var start_indicated_id = -1;

var textarea_is_selected = false;

var active_link_node = null;
var link_mode = false;

var mobile_item_selec = '';
var mobile_last_move = null;
var transform = '';

var bar_zoom_text = document.getElementById("bar-zoom text");

//editor init
editor.start();
var pyq_console = new Console('PyQuest2 console:', 'user_workflow');

// editor.import(dataToImport);
// editor.addModule('Other');

//Local storage and import
editor.on('import', function(msg){
    pyq_console.import();
})

var retrievedObject = localStorage.getItem(pyq_console.local_storage_var);

if (typeof retrievedObject !== 'undefined') {
    if (retrievedObject != null) {
        editor.import(JSON.parse(retrievedObject));
        pyq_console.log(retrievedObject);
    } else {
        pyq_console.save();
        retrievedObject = localStorage.getItem(pyq_console.local_storage_var);
    }
}

function check_start_node() {
    for (let i = 1; i <= editor.nodeId; i++) {
        let node = editor.drawflow.drawflow.Home.data[i]
        if(typeof node !== "undefined") {
            if(node.class == 'start') {
                start_indicated = true;
                start_indicated_id = node.id;
                break;
            }
        }
    }
}
check_start_node();

//Templates
var textarea_template = 'Введите ваш текст...';
var link_template = 'Двойной клик, чтобы назначить переход...';

function set_node_template(key, text='', height='100') {
    let link_status = ' not_connected';
    if(key == 'link'){if(text != ''){text = 'node-' + text; link_status = '';}else{text = link_template;}}
    let nodes_template = {
        'start': node_html_setter("title-box start noselect", "set_start(event)", "fas fa-play-circle", "Начало", text, height),
        'finish': node_html_setter("title-box finish noselect", "set_finish(event)", "fas fa-stop-circle", "Конец", text, height),
        'question': node_html_setter("title-box noselect", "set_start(event)", "fas fa-question-circle", "Вопрос", text, height),
        'question_not_connected': node_html_setter("title-box not_connected noselect", "set_start(event)", "fas fa-question-circle", "Вопрос", text, height),
        'answer': node_html_setter("title-box noselect", "set_finish(event)", "fas fa-comment-dots", "Ответ", text, height),
        'answer_not_connected': node_html_setter("title-box not_connected noselect", "set_finish(event)", "fas fa-comment-dots", "Ответ", text, height),
        'link': node_html_setter("title-box link" + link_status + " noselect", "set_link(event)", "fas fa-link", "Переход", text, height),
    }
    return nodes_template[key];
}

function node_html_setter(title_box, node_func, node_icon, node_text, text, height) {
    let header = `<div class="${title_box}" ondblclick="${node_func}"><i class="${node_icon}"></i> ${node_text}</div>`;
    let body = `<div class="box noselect">` + textarea_setter(text, height) + `</div>`;
    if(title_box.includes('link') == true) {body = `<div class="box noselect">${text}</div>`;}
    let template = `<div>` + header + body + `</div>`;
    return template;
}

function textarea_setter(t, h) {
    let text = '';
    if (t != '') { text = t;}
    return `<textarea df-template class="vertical" style="height:${h}px;" placeholder="${textarea_template}">${text}</textarea>`;
}


// Events!
const observer = new ResizeObserver(observerCallback, { threshold: 1.0 });

function observerCallback(entries, observer) {
    for (let entry of entries) {
        const height = Math.floor(entry.contentRect.height);
        //pyq_console.log(height);
        if(height == 0) {
            observer.unobserve(entry.target);
            update_resize_observers();
            break;
        }
        let parent_id = getParentNode(entry.target, 4).id;
        let id = parent_id.split('-')[1];
        if(typeof editor.drawflow.drawflow.Home.data[id] !== "undefined") {
            let node = editor.getNodeFromId(id);
            let text = set_node_template(node.name, node.data['template'], height);
            editor.drawflow.drawflow.Home.data[id].html = text;
            editor.updateConnectionNodes(`node-${id}`);
        }
    }
    pyq_console.save();
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
    // pyq_console.log("Node created " + id);
    dr.disable(); dr.enable();
    update_resize_observers();
    pyq_console.save();
})

editor.on('nodeRemoved', function(id) {
    if(id == active_link_node) {
        active_link_node = null;
        if(link_mode == true) {
            link_mode = false;
        }
    }
    if(id == start_indicated_id) {
        start_indicated_id = -1;
        start_indicated = false;
    }
    //pyq_console.log("Node removed " + id);
    dr.disable(); dr.enable();
    // let textareas = document.querySelectorAll('.vertical');
    update_resize_observers();
    pyq_console.save();
})

editor.on('nodeSelected', function(id) {
    node_selected_id = id;
    //pyq_console.log("Node selected " + id);
    pyq_console.save();
})

editor.on('nodeDataChanged', function(id) {
    //pyq_console.log("Node value updated " + id);
    dr.disable(); dr.enable();
    pyq_console.save();
})

editor.on('moduleCreated', function(name) {
    pyq_console.log("Module Created " + name);
})

editor.on('moduleChanged', function(name) {
    pyq_console.log("Module Changed " + name);
})

editor.on('connectionCreated', function(connection) {
    //pyq_console.log('Connection created');
    //pyq_console.log(connection);
    check_connection(connection['input_id']);
    check_connection(connection['output_id']);
    dr.disable(); dr.enable();
    //update_resize_observers();
    pyq_console.save();
})

editor.on('connectionRemoved', function(connection) {
    pyq_console.log('Connection removed');
    pyq_console.log(connection);
    check_connection(connection['input_id']);
    check_connection(connection['output_id']);
    dr.disable(); dr.enable();
    //update_resize_observers();
    pyq_console.save();
})

editor.on('mouseMove', function(position) {
    if(drag_start == true) {
        for (let i of mult_arr) {
            if(i != active_node_id) {
                if(typeof editor.drawflow.drawflow.Home.data[i] !== "undefined") {
                    let node = editor.getNodeFromId(active_node_id);
                    // let elem = document.getElementById("node-"+i).children[1].children[0];
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
    //pyq_console.log('Position mouse x:' + position.x + ' y:'+ position.y);
    //pass
})

editor.on('nodeMoved', function(id) {
//    pyq_console.log("Node moved " + id);
    pyq_console.save();
})

editor.on('zoom', function(zoom) {
    //pyq_console.log('Zoom level ' + zoom);
    bar_zoom_text.innerHTML = 100 * Math.floor(zoom*10)/10 + '%';
})

editor.on('translate', function(position) {
    document.querySelector('.parent-drawflow').style.backgroundPosition = position.x + 'px ' + position.y + 'px';
    //pyq_console.save();
    //pass
})

editor.on('addReroute', function(id) {
    pyq_console.log("Reroute added " + id);
    pyq_console.save();
})

editor.on('removeReroute', function(id) {
    pyq_console.log("Reroute removed " + id);
    pyq_console.save();
})

document.getElementById('drawflow').addEventListener('dblclick', clear_selection, false);
function clear_selection(e) {
    if(link_mode == true) {
        cancel_link_mode();
    }
    if(mult_arr != null) {
        dr.foreach(dr.items, function (el) {
            el.classList.remove(dr.options.selectedClass);
            node_remove_listener(el);
        });
        mult_arr = [];
    }
}

document.onkeydown = function(evt) {
    evt = evt || window.event;
    var isEscape = false;
    if ("key" in evt) {
        isEscape = (evt.key === "Escape" || evt.key === "Esc");
    } else {
        isEscape = (evt.keyCode === 27);
    }
    if (isEscape) {
        if(link_mode == true) {
            cancel_link_mode();
        }   
    }
};

  function cancel_link_mode() {
    document.getElementById("node-" + active_link_node).classList.remove('link-mode');
    active_link_node = null;
    link_mode = false;
    dr.disable(); dr.enable();
  }

editor.on('click', (e) => {
    if(link_mode != true) {
        if(e.target.tagName == 'TEXTAREA') {
            textarea_is_selected = true;
            editor.editor_mode='fixed';
        } else {
            if(textarea_is_selected == true) {
                textarea_is_selected = false;
                editor.editor_mode='edit';
            }
        }
    } else {
        let target = e.target.closest('.drawflow-node');
        if(target != null) {
            let node = editor.getNodeFromId(active_link_node);
            let id = parseInt(target.id.split('-')[1]);
            if(id != active_link_node && !target.classList.contains('link')) {
                node.data['template'] = id;
                editor.drawflow.drawflow.Home.data[active_link_node].data['template'] = id;
                pyq_console.log('node-' + node.id + ' link setted as ' + 'node-' + node.data['template']);
                // document.querySelector('.parent-drawflow').style.filter = "saturate(1)";
                let text = set_node_template('link', node.data['template']);
                document.getElementById(`node-${active_link_node}`).children[1].innerHTML = text;
                editor.drawflow.drawflow.Home.data[active_link_node].html = text;
                document.getElementById("node-" + active_link_node).classList.remove('link-mode');
                active_link_node = null;
                link_mode = false;
                dr.disable(); dr.enable();
                pyq_console.save();
            }
        }
    }
})

/* DRAG EVENT */

/* Mouse and Touch Actions */

let elements = document.getElementsByClassName('drag-drawflow');
for (let i = 0; i < elements.length; i++) {
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
        let parentdrawflow = document.elementFromPoint( mobile_last_move.touches[0].clientX, mobile_last_move.touches[0].clientY).closest("#drawflow");
        if(parentdrawflow != null) {
            addNodeToDrawFlow(mobile_item_selec, mobile_last_move.touches[0].clientX, mobile_last_move.touches[0].clientY);
        }
        mobile_item_selec = '';
    } else {
        ev.preventDefault();
        let data = ev.dataTransfer.getData("node");
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
    let node = editor.getNodeFromId(id);
    let elem = document.getElementById("node-"+id).children[1];
    let height = null;
    if(!elem.parentElement.classList.contains('link')) {
        height = parseInt(elem.querySelector('.vertical').style.height);
    }
    if (node.class.includes('question') == true) {
        if ((node.inputs['input_1']['connections'].length == 0) || (node.outputs['output_1']['connections'].length == 0)) {
            let text = set_node_template('question_not_connected', node.data['template'], height);
            elem.innerHTML = text;
            editor.drawflow.drawflow.Home.data[id].html = text;
            editor.drawflow.drawflow.Home.data[id].class = 'question_not_connected';
        } else {
            let text = set_node_template('question', node.data['template'], height);
            elem.innerHTML = text;
            editor.drawflow.drawflow.Home.data[id].html = text;
            editor.drawflow.drawflow.Home.data[id].class = 'question';
        }
    }else if (node.class.includes('answer') == true) {
        if ((node.inputs['input_1']['connections'].length == 0) || (node.outputs['output_1']['connections'].length == 0)) {
            let text = set_node_template('answer_not_connected', node.data['template'], height);
            elem.innerHTML = text;
            editor.drawflow.drawflow.Home.data[id].html = text;
            editor.drawflow.drawflow.Home.data[id].class = 'answer_not_connected';
        } else {
            let text = set_node_template('answer', node.data['template'], height);
            elem.innerHTML = text;
            editor.drawflow.drawflow.Home.data[id].html = text;
            editor.drawflow.drawflow.Home.data[id].class = 'answer';
        }
    }
    editor.updateConnectionNodes("node-"+id);
}

function set_link(e) {
    e.stopPropagation();
    if(link_mode != true) {
        link_mode = true;
        let target = e.target.closest('.drawflow-node');
        active_link_node = parseInt(target.id.split('-')[1]);
        // document.querySelector('.parent-drawflow').style.filter = "saturate(20%)";
        let text = set_node_template('link');
        document.getElementById(`node-${active_link_node}`).children[1].innerHTML = text;
        editor.drawflow.drawflow.Home.data[active_link_node].html = text;
        target.classList.add('link-mode');
    }
}

function set_start(e) {
    e.stopPropagation();
    let node = editor.getNodeFromId(node_selected_id)
    if (node.class.includes('question') == true) {
        if (start_indicated == false) {
            change_node_type(node_selected_id, 'start', 'output')
            start_indicated = true;
            start_indicated_id = node_created_id;
        } else {
            change_node_type(start_indicated_id, 'question_not_connected', 'output')
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
    pyq_console.save();
}

function set_finish(e) {
    e.stopPropagation();
    let node = editor.getNodeFromId(node_selected_id)
    if (node.class.includes('answer') == true) {
        change_node_type(node_selected_id, 'finish', 'input')
    } else if (node.class == 'finish') {
        change_node_type(node_selected_id, 'answer_not_connected', 'input')
    }
    pyq_console.save();
}

function change_node_type(old_id, node_class, side) {
    let node = editor.getNodeFromId(old_id);
    addNodeToDrawFlow(node_class, node.pos_x, node.pos_y, node.data['template'], true);

    let elem = document.getElementById("node-" + old_id).children[1];
    let new_elem = document.getElementById("node-" + node_created_id).children[1];

    let height = parseInt(elem.querySelector('.vertical').style.height);

    let new_node = editor.getNodeFromId(node_created_id);
    let text = set_node_template(new_node.class, new_node.data['template'], height);

    new_elem.innerHTML = text;
    editor.drawflow.drawflow.Home.data[node_created_id].html = text;

    if (side == 'input') {
        //pyq_console.log(node.inputs['input_1']['connections']);
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
    pyq_console.log(transform);

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
    let all = document.querySelectorAll(".menu ul li");
    for (let i = 0; i < all.length; i++) {
        all[i].classList.remove('selected');
    }
    event.target.classList.add('selected');
}

function changeMode(option) {
    //pyq_console.log(lock.id);
    if(option == 'lock') {
        lock.style.display = 'none';
        unlock.style.display = 'block';
    } else {
        lock.style.display = 'block';
        unlock.style.display = 'none';
    }
}

function export_json() {
    //pyq_console.log(JSON.stringify(editor.export()));
    let export_data = editor.export();
    let nodes = [];
    if(export_data["drawflow"][editor.module]["data"] !== undefined) {
        for(let key in export_data["drawflow"][editor.module]["data"]) {
            let value = export_data["drawflow"][editor.module]["data"][key];
            let node = {"connections": {"input": [], "output": []}};
            if("id" in value) {
                node["id"] = value["id"];
            }
            if("class" in value) {
                node["class"] = value["class"];
                if("data" in value) {
                    if(node["class"] == "link") {
                        node["link"] = parseInt(value["data"]["template"]);
                    } else {
                        node["data"] = value["data"]["template"];
                    }
                }
            }
            if("pos_x" in value) {
                node["x"] = value["pos_x"];
            }
            if("pos_y" in value) {
                node["y"] = value["pos_y"];
            }
            if(value["inputs"]["input_1"] !== undefined) {
                if(value["inputs"]["input_1"]["connections"].length !== 0) {
                    for(let item in value["inputs"]["input_1"]["connections"]) {
                        let connection = value["inputs"]["input_1"]["connections"][item];
                        if(connection["points"] !== undefined) {
                            if(connection["points"].length !== 0) {
                                let points = [];
                                for(let i in connection["points"]) {
                                    let point = connection["points"][i];
                                    points.push({"x": point["pos_x"], "y": point["pos_y"]});
                                }
                                node["connections"]["input"].push({"node": parseInt(connection["node"]), "points": points});
                            }
                        } else {
                            node["connections"]["input"].push({"node": parseInt(connection["node"])});
                        }
                    }
                }
            }
            if(value["outputs"]["output_1"] !== undefined) {
                if(value["outputs"]["output_1"]["connections"].length !== 0) {
                    for(let item in value["outputs"]["output_1"]["connections"]) {
                        let connection = value["outputs"]["output_1"]["connections"][item];
                        if(connection["points"] !== undefined) {
                            if(connection["points"].length !== 0) {
                                let points = [];
                                for(let i in connection["points"]) {
                                    let point = connection["points"][i];
                                    points.push({"x": point["pos_x"], "y": point["pos_y"]});
                                }
                                node["connections"]["output"].push({"node": parseInt(connection["node"]), "points": points});
                            }
                        } else {
                            node["connections"]["output"].push({"node": parseInt(connection["node"])});
                        }
                    }
                }
            }
            nodes.push(node);
        }
    };

    let converted_data = {"quest": editor.module, "description": "", "nodes": nodes};

    //pyq_console.log(JSON.stringify(converted_data));

    pyq_console.post({
        "url": 'quest_editor/data',
        "data": JSON.stringify(converted_data),
        "success": function() {
            pyq_console.save(true);
            Swal.fire({title: 'Export', html: '<textarea rows="30" cols="50">'+JSON.stringify(converted_data, null, 4).replace(/<[^>]*>/g, '')+'</textarea>'})
        }
    });
}

function editor_clear() {
    pyq_console.clear();
}

function getParentNode(element, level = 1) {
    while (level-- > 0) {
        element = element.parentNode;
        if (!element) return null;
    }
    return element;
}
