window.call = function (url, method, data) {
    return fetch(url, {
        method: "POST",
        body: JSON.stringify(data),
        redirect: "follow"
    });
};

var global_pointers = {};
var global_data_sources = {};

var createObject = (obj) => {
    /*
    the initial object creator,
    iterates over and creates the objects into the dom
    */
    var current_node;
    if (obj.tag == "body") {
        current_node = document.getElementsByTagName("body")[0];
    } else {
        current_node = document.createElement(obj.tag);
    }

    current_node.setAttribute("id", obj.id);
    current_node.className += obj.class;

    return current_node;
}

var defineObject = () => { }

var isText = (obj) => (typeof obj.traits.text !== 'undefined') ? true : false
var isMedia = (obj) => (typeof obj.traits.src !== 'undefined') ? true : false
var isVar = (obj) => (typeof obj.traits.sourceId !== 'undefined') ? true : false
var isState = (obj) => (typeof obj.traits.state !== 'undefined') ? true : false
var isAction = (obj) => (typeof obj.traits.actionId !== 'undefined') ? true : false
var isInput = (obj) => (typeof obj.traits.input !== 'undefined') ? true : false

var render = (obj) => {
    /*
    add a state to the global pointers then return so it doesnt try and render a state
    */
    if (isState(obj)) {
        global_pointers[obj.traits.state.actionId] = obj.traits.state.actionVars;
        return null;
    }
    /* the initial object creator, iterates over and creates the objects into the dom */
    let current_node = createObject(obj);

    /*
    A set of conditions to handle the different types of primitives.
    In particular the onclick stuff and variable updating functions
    Code quality really needs to improve ...
    */

    if (isText(obj)) {
        current_node.innerHTML = obj.traits.text;
    }

    if (isMedia(obj)) {
        /* this is for objects that have a src, i.e img, video */
        current_node.setAttribute("src", obj.traits.src);
    }

    if (isInput(obj)) {
        current_node.setAttribute("type", obj.traits.input);
    }

    if (isVar(obj)) {
        if (global_data_sources[obj.traits.sourceId] instanceof Array) {
            global_data_sources[obj.traits.sourceId].push(obj.id);
        } else {
            global_data_sources[obj.traits.sourceId] = [obj.id];
        }
    }

    if (isAction(obj)) {
        if (global_pointers[obj.traits.actionId] !== 'undefined')
            global_pointers[obj.traits.actionId] = obj.traits.actionVars;
        global_pointers[obj.traits.actionId].traits.actionVars.forEach(item => {
            // register the variable into the global variables
            global_pointers[item] = global_pointers[obj.traits.actionId].children[item];
        });
        // some sanitation :)

        delete global_pointers[obj.traits.actionId].children

        current_node.addEventListener(
            obj.traits.actionEvent,
            async () => {
                // for every variable id in list conc the fetched value from pointers to a dict
                // use this dict for the fetch
                var setter = {};
                var query = {};

                global_pointers[obj.traits.actionId].traits.actionVars.forEach(variable => {
                    key = Object.keys(global_pointers[variable])[0];
                    setter[key] = variable;

                    query = {
                        ...query,
                        ...global_pointers[variable]
                    }
                });
                var tmp = await call("state/" + obj.traits.actionId, obj.traits.method, query);
                var res = await tmp.json();

                Object.keys(res).forEach(k => {
                    global_pointers[setter[k]] = {
                        [k]: res[k]
                    };
                    var gs = global_data_sources[setter[k]];
                    gs.forEach(
                        dest => {
                            // TODO: make it done using a dict call instead of a variable call
                            document.getElementById(dest).innerHTML = res[k];
                        }
                    )
                });
            }
        )
    }

    /*
    This just iterates over the whole tree
    */
    for (child of obj.children) {
        var new_child = render(child)
        current_node.appendChild(new_child);
    }

    return current_node;
}