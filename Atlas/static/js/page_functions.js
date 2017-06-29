/**
 * Created by hrobohboy on 12/19/16.
 */
/* TODO:

 */
 // Initalize starting variables 
var serializedData = [];
var test_config = [];
var widgets = [];
var options = {};
var d = new Date();
var months = ['January','February','March','April','May','June','July','August','September','October','November','December'];
var days = ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'];
var dd =  (days[d.getDay()]+' '+months[d.getMonth()]+' '+d.getDate()+' '+d.getFullYear()).toString();
var events = [];
var elements = [];
var picture_text = "<p>Please upload a picture!</p>";
var sticky_text = "Edit your sticky note using the edit icon above!";
var is_loaded = false;


//Event handler that handles responsive widgets
//resizes each of the widgets that are on the page at the time of resize
//TODO: Come up with a more efficient way of writing this handler
$(window).on('resize', function(){
    if (widgets.includes('calendar')){
        $$('calendar1').resize();
    }
    if (widgets.includes('sticky')){
        $$('sticky1').resize();
    }
    if (widgets.includes('picture')){
        $$('picture1').resize();
    }
    if (widgets.includes('notification')){
        $$('notification1').resize();
    }

});

//after a gridstack widget is resized this handles resizing all visible widgets on the page
//new widgets will have to be entered into here to allow webix widget resizing
//TODO: Come up with a more efficient way of writing this handler
$('.grid-stack').on('resizestop', function(event, ui) {
    setTimeout(
        function()
        {
            if (widgets.includes('calendar')){
                $$('calendar1').resize();
            }
            if (widgets.includes('sticky')){
                $$('sticky1').resize();
            }
            if (widgets.includes('picture')){
                $$('picture1').resize();
            }
            if (widgets.includes('notification')){
                $$('notification1').resize();
            }
        }, 10);
});


//After every 30 seconds, save the current widget configuration
var timerID = setInterval(function() {
    saveGrid();
}, 30 * 1000); 


//function that takes a JSON array and populates user door based on the configuration
//will be modified to take in a serialized array from Django framework
function loadGrid() {
    if (serializedData.length == 0) {
        webix.message("No door configuration to load.");
    } else if (is_loaded == false){
        var items = GridStackUI.Utils.sort(serializedData);
        _.each(items, function (node) {
            if (node.type == "calendar") {
                widgets.push('calendar');
                var element = $("<div><div class='grid-stack-item-content' id=" + node.type + "></div></div>");
                elements.push({type:"calendar", node:grid.addWidget(element, node.x, node.y, node.width, node.height)});
                grid.maxHeight(element, 6); grid.minHeight(element, 4); grid.maxWidth(element, 6); grid.minWidth(element,4);
                $$('icon_cal').disable();
                loadCalendar();
                calendar.show();
            } else if (node.type == "picture") {
                widgets.push('picture');
                var element = $("<div><div class='grid-stack-item-content' id=" + node.type + "></div></div>");
                elements.push({type:"picture", node:grid.addWidget(element, node.x, node.y, node.width, node.height)});
                grid.maxHeight(element, 6); grid.minHeight(element, 4); grid.maxWidth(element, 6); grid.minWidth(element,4);
                $$('icon_pic').disable();
                loadPicture();
                picture.show();
            } else if (node.type == "sticky") {
                widgets.push('sticky');
                element = $('<div><div class="grid-stack-item-content" id=' + node.type + '></div></div>');
                elements.push({type:"sticky", node:grid.addWidget(element, node.x, node.y, node.width, node.height)});
                grid.maxHeight(element, 3); grid.minHeight(element, 2); grid.maxWidth(element, 3); grid.minWidth(element, 2);
                $$('icon_sticky').disable();
                loadSticky();
                sticky.show();
            } else if (node.type == "notification") {
                widgets.push('notification');
                element = $('<div><div class="grid-stack-item-content" id=' + node.type + '></div></div>');
                elements.push({type:"notification", node:grid.addWidget(element, node.x, node.y, node.width, node.height)});
                grid.maxHeight(element, 2); grid.minHeight(element, 2); grid.maxWidth(element, 3); grid.minWidth(element, 3);
                $$('icon_notify').disable();
                loadNotify();
                notify.show();
            }
        });
        is_loaded = true;
        adminOrGuest(a_or_g);
    }
    
}

//saves a copy of the current grid configuration into a separate array
//can store one previous door configuration
//once a new configuration is saved, the old one is overwritten, functionality not implemented yet.
function saveGrid(){
    var counter = 0;
    widget_select.hide();
    if (serializedData.length == 0){
        dbPostLayout(JSON.stringify(serializedData, null, '    '));
    } else {
        serializedData = _.map($('.grid-stack > .grid-stack-item:visible'), function (el) {
            el = $(el);
            var node = el.data('_gridstack_node');
            return {
                x: node.x,
                y: node.y,
                width: node.width,
                height: node.height,
                type: $('.grid-stack-item-content')[counter++].id
            };
        }, this);
        dbPostLayout(JSON.stringify(serializedData, null, '    '));
    }
}

//function that determines if there is room on the office door
//if there isn't room then it will not allow wigets to be added
//if there is room then show the widget select
function addNewWidget(){
    if (serializedData.length == 4){
        webix.message("No more room for widgets!");
    } else {
        widget_select.show();

    }
}

//this function is called by the widget selector
//creates a new node to be inserted into the serialized data array
//also sets max and min widget sizes
function makeWidget(widget_type) {
    if (widget_type == null){
        console.log('No widget type found.');
    }
    else if (widget_type =="calendar"){
        var node = {
            x: Math.random() * (5 - 1) + 1,
            y: Math.random() * (5 - 1) + 1,
            width: 3,
            height: 4,
            type: widget_type
        };
        serializedData.push(node);
        widgets.push('calendar');
        var element = $("<div><div class='grid-stack-item-content' id=" + node.type + "></div></div>");
        elements.push({type:"calendar", node:grid.addWidget(element, node.x, node.y, node.width, node.height)});
        grid.maxHeight(element, 6); grid.minHeight(element, 4); grid.maxWidth(element, 6); grid.minWidth(element,4);
        loadCalendar();
        calendar.show();
    } else if (widget_type == "sticky"){
        node = {
            x: Math.random() * (5 - 1) + 1,
            y: Math.random() * (5 - 1) + 1,
            width: 2,
            height: 2,
            type: widget_type
        };
        serializedData.push(node);
        widgets.push('sticky');
        element = $('<div><div class="grid-stack-item-content" id=' + node.type + '></div></div>');
        elements.push({type:"sticky", node:grid.addWidget(element, node.x, node.y, node.width, node.height)});
        grid.maxHeight(element, 3); grid.minHeight(element, 2); grid.maxWidth(element, 3); grid.minWidth(element, 2);
        loadSticky();
        sticky.show();
    } else if (widget_type == "picture"){
        node = {
            x: Math.random() * (5 - 1) + 1,
            y: Math.random() * (5 - 1) + 1,
            width: 2,
            height: 2,
            type: widget_type
        };
        serializedData.push(node);
        widgets.push('picture');
        element = $('<div><div class="grid-stack-item-content" id=' + node.type + '></div></div>');
        elements.push({type:"picture", node:grid.addWidget(element, node.x, node.y, node.width, node.height)});
        grid.maxHeight(element, 6); grid.minHeight(element, 2); grid.maxWidth(element, 6); grid.minWidth(element, 2);
        loadPicture();
        picture.show();
    } else if (widget_type == "notification"){
        node = {
            x: Math.random() * (5 - 1) + 1,
            y: Math.random() * (5 - 1) + 1,
            width: 3,
            height: 2,
            type: widget_type
        };
        serializedData.push(node);
        widgets.push('notification');
        element = $('<div><div class="grid-stack-item-content" id=' + node.type + '></div></div>');
        elements.push({type:"notification", node:grid.addWidget(element, node.x, node.y, node.width, node.height)});
        grid.maxHeight(element, 2); grid.minHeight(element, 2); grid.maxWidth(element, 3); grid.minWidth(element, 3);
        loadNotify();
        notify.show();
    }
}

//validation function that once validation is complete sends the email to the db
//TODO: Implement unscribe button feature, mitchell needs to fix sunsub feature
function validateEmail(email){
    var re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    if (re.test(email)){
        webix.message("Valid email. Subscribing...");
        var db_email = {"email":email};
        var url = "../api/notification/"+username+"/";
        $.post(url, {"data":JSON.stringify(db_email), "csrfmiddlewaretoken":csrf_tok}, function(){
            webix.message("Subscribed!");
        });

    } else {
        webix.message("Invalid email, please try again.");
    }
}


//determine if the current vistor to the door is a door owner or a guest
//flag is set in the officedoor.html file
function adminOrGuest(flag){
    //if the user is a guest, hide all admin features
    if (flag == 1){
        grid.movable('.grid-stack-item', false);
        grid.resizable('.grid-stack-item', false);
        elements.forEach(function(result, index) {
            if(result["type"] === "calendar") {
                $$('add_e').hide();
                $$('del_event').hide();
                $$('edit_e').hide();
                $$('close_cal').hide();
                $$('calendar1').getBody().define("select", false);
            } else if (result["type"] == "sticky"){
                $$('edit_t').hide();
                $$('close_sticky').hide();
            } else if (result["type"] == "notification"){
                $$('notify_all').hide();
                $$('close_notify').hide();
            } else if (result["type"] == "picture"){
                $$('p_add').hide();
                $$('close_pic').hide();
            }
        });
    }
    //if the user is an owner, enable all admin features
    else if (flag == 0){
        
    }
}


//Post function for sending data to db
//10.18.92.5:8000/api/
function dbPostLayout(data){
    var url = "../api/layout/"+username+"/";
    $.post(url, {"data":data, "csrfmiddlewaretoken":csrf_tok}, function(){
        webix.message("Door layout saved.");
    });
}

//get function for acquiring data from the db
function dbGetLayout(){
    var url = "../api/layout/"+username+"/";
    $.get(url, function( data ) {
        serializedData = data;
    }, "json");
}

//functions used to remove widgets and widget data from arrays
function JSONfindAndRemove(array, property, value) {
    array.forEach(function(result, index) {
        if(result[property] === value) {
            //Remove from array
            array.splice(index, 1);
        }
    });
}

function widgetRemove(widget){
    elements.forEach(function(result, index) {
        if(result["type"] === widget) {
            //Remove from array
            grid.removeWidget(result["node"]);
            elements.splice(index, 1);
            serializedData.splice(index, 1);
            widgets.splice(index, 1);
        }
    });
}

//bind widget adding function and saving layout functions
$('#add-widget').click(addNewWidget);
$('#save-grid').click(saveGrid);

//make it so that the widget select will hide when not in focus
// WARNING: Does throw an error when dealing with the widget select, but it does not break the application
webix.attachEvent("onFocusChange", function(to, from){  
        if (!to || to.getTopParentView().name !== "window"){
            webix.blockEvent();
            widget_select.hide();
            webix.unblockEvent();
        }
    });

//stop widget configuration saving when the office door is navigated away from
window.onbeforeunload = function(event) {
    clearInterval(timerID);
};

//load all widgets and get all widget data
//sets a timeout to allow get requests to fully process before loading data
document.addEventListener("DOMContentLoaded", function(event) { 
    loadWSelect();
    dbGetLayout();
    getsticky();
    getpicture();
    getCalendar();
    setTimeout(function(){
        loadGrid();
        is_loaded = true;
    }, 1000)
});

