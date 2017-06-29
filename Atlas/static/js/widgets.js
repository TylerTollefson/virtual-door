/**
 * Created by Tyler Tollefson on 12/19/16.
 */

//TODO:
/*
duplicate widget plan:
1. Creating the duplicates
    Use webix copy method, define new id, define new container, add to serializedData/widgets arrays
2. Moving the duplicates is done by gridstack containers, need to handle resizing though by adding if statements 
    in those conditionals to handle it
3. posting and getting data would need revamp of the different APIs and serializers
    Posts would need to include the specific widget's ID, same with Get
    No clue how this would be done on the backend
4. Loading widgets would have to be changed to handle multiple of the same widget
5. Need to create new unique gridstack containers based on how many of a specific widget is there
6. Need to change how popups are currently functioning, possibly put them inside of functions instead, so widget IDs could be passed in?
7. Need to modify how the layout is done and stored to make sure duplicate widgets don't accidentally take the place of another of same type

 */

/*
NOTE: 
All webix objects are JSON objects, all properties and views can be found in the webix docs.
Any kind of function that has been implemented was created by hand.
*/


/*
Function: loadCalendar
Creates the main calendar webix object and stores it into the calendar variable for use later
*/
var calendar;
function loadCalendar(){
    calendar = webix.ui({
        container: "calendar",
        id: "calendar1",
        autoConfig: true,
        view:"window",
        head:{
            cols:[
                {view: "label", label: dd},
                {view:"icon", icon:"plus", id:"add_e", popup: "add_event", tooltip:"Add Event"},
                {view:"icon", icon:"minus", id:"del_event", tooltip:"Delete Event", click:function(){
                    var selected = $$("event_space").getSelectedItem();
                    //webix.message(JSON.stringify(selected));
                    if(selected){
                        var post_dformat = webix.Date.dateToStr("%Y-%m-%d");
                        var post_tformat = webix.Date.dateToStr("%H:%i:00");
                        var d_parser = webix.Date.strToDate("%F %j, %Y");
                        var t_parser = webix.Date.strToDate("%g:%i %A");
                        var temp_date = d_parser(selected["e_date"]);
                        var temp_time = t_parser(selected["d_time"]);
                        selected["e_date"] = post_dformat(temp_date);
                        selected["d_time"] = post_tformat(temp_time);


                        $.post("../api/calendardelete/"+username+"/", 
                        {"data":JSON.stringify(selected, null, ""), "csrfmiddlewaretoken":csrf_tok});
                        $$("event_space").remove(selected.id);
                        
                        JSONfindAndRemove(events, "message", selected.message.toString());

                    }}},
                {view:"icon", icon:"edit", id:"edit_e", popup:"edit_event", tooltip:"Edit Event"},
                {view:"icon", icon:"times", id:"close_cal", width:75, tooltip:"Delete Calendar widget", click:function(){
                    $$('calendar1').hide();
                    $$('icon_cal').enable();
                    widgetRemove("calendar");
                }}
                ]
        },
        body: {
            view:"list",
            id: "event_space",
            template: "#message# <span style = 'float:right;'>#d_time# on #e_date#</span>",
            data: events,
            autoheight:true,
            select:true

        },
        width: "auto",
        height: "auto"
    });
}

/*
Creating the add event popup, custom webix popup
This popup also handles posting the new event to the DB
*/
webix.ui({
    view:"popup",
    id: "add_event",
    head: "Add event",
    width:300, height:250,
    head:{
        template:"Add Event"
    },
    body:{
        view: "form",
        scroll:false,
        elements:[
            {view:"text", name:"message", id:"event", required: true, label:"Event: "},
            {view:"datepicker", label:"Date: ", name:"e_date", id:"e_date", required:true},
            {view:"datepicker", type:"time", label:"Time: ", name:"d_time", required:true, id:"d_time"},
            { view:"button", type:"form", value:"Add Event", click: function(){
                var d_format = webix.Date.dateToStr("%F %j, %Y");
                var post_dformat = webix.Date.dateToStr("%Y-%m-%d");

                var t_format = webix.Date.dateToStr("%g:%i %A");
                var post_tformat = webix.Date.dateToStr("%H:%i:00");

                var current_date = new Date();
                current_date.setDate(current_date.getDate() - 1);
                if ($$("e_date").getValue() <= current_date){
                    webix.message("Invalid Date: Event needs to take place either on or after today.");
                } else {
                    //Posting event
                    var event = {message:$$("event").getValue(), e_date:post_dformat($$("e_date").getValue()),
                        d_time:post_tformat($$("d_time").getValue())};
                    events.push(event);
                    $.post("../api/calendar/"+username+"/", 
                        {"data":JSON.stringify(event, null, ""), "csrfmiddlewaretoken":csrf_tok});

                    //adding event to event space
                    var disp_event = {message:$$("event").getValue(), e_date:d_format($$("e_date").getValue()),
                        d_time:t_format($$("d_time").getValue())};
                    

                    $$("event_space").add(disp_event);
                    $$('add_event').hide();
                }
            }}
        ],
    }
});

/*
Creating the edit event popup, custom webix popup
This popup takes the currently selected event, allows the user to change the message, date and time
Then posts the old event and the new event to the DB where the old event is replaced by the new one
*/
webix.ui({
    view:"popup",
    id: "edit_event",
    head: "Edit event",
    width:300, height:250,
    head:{
        template:"Add Event"
    },
    body:{
        view: "form",
        scroll:false,
        elements:[
            {view:"text", name:"message_edit", id:"event_edit", required:true, label:"Event: "},
            {view:"datepicker", label:"Date: ", name:"e_date_edit", required:true, id:"e_date_edit"},
            {view:"datepicker", type:"time", label:"Time: ", required:true, name:"d_time_edit", id:"d_time_edit"},
            { view:"button", type:"form", value:"Edit Event", click: function(){
                var d_format = webix.Date.dateToStr("%F %j, %Y");
                var post_dformat = webix.Date.dateToStr("%Y-%m-%d");

                var t_format = webix.Date.dateToStr("%g:%i %A");
                var post_tformat = webix.Date.dateToStr("%H:%i:00");
                
                var d_parser = webix.Date.strToDate("%F %j, %Y");
                var t_parser = webix.Date.strToDate("%g:%i %A");

                var current_date = new Date();
                current_date.setDate(current_date.getDate() - 1);
                
                var selected = $$("event_space").getSelectedItem();
                var old_selected = jQuery.extend({}, selected);
                JSONfindAndRemove(events, "message", old_selected.message.toString());
                $$("event_space").remove(selected.id);

                if ($$("e_date_edit").getValue() <= current_date){
                    webix.message("Invalid Date: Event needs to take place either on or after today.");
                } else {
                    selected["message"] = $$("event_edit").getValue();
                    selected["e_date"] = post_dformat($$("e_date_edit").getValue());
                    selected["d_time"] = post_tformat($$("d_time_edit").getValue());

                    var old_date = d_parser(old_selected["e_date"]);
                    var old_time = t_parser(old_selected["d_time"]);

                    old_selected["e_date"] = post_dformat(old_date);
                    old_selected["d_time"] = post_tformat(old_time);

                    var event = {message: selected["message"], e_date: selected["e_date"], d_time: selected["d_time"]};
                    events.push(event);

                    var post_event = {oldmessage: old_selected["message"], olde_date: old_selected["e_date"], oldd_time: old_selected["d_time"], 
                    message: selected["message"], e_date: selected["e_date"], d_time: selected["d_time"]};
                    
                    $.post("../api/calendaredit/"+username+"/", 
                        {"data": JSON.stringify(post_event, null, ""), "csrfmiddlewaretoken":csrf_tok});

                    var disp_event = {message:$$("event_edit").getValue(), e_date:d_format($$("e_date_edit").getValue()),
                        d_time:t_format($$("d_time_edit").getValue())}

                    $$("event_space").add(disp_event);
                    $$('edit_event').hide();
                }
            }}
        ]
    }
});


/*
Function: loadSticky
Simple window with a template that is updated in the body. Editing the body is handled in the popup.
*/
var sticky;
function loadSticky(){
    sticky = webix.ui({
        container:"sticky",
        id: "sticky1",
        view: "window",
        width: "auto",
        height: "auto",
        autoConfig: true,
        head: {
            view: "toolbar", margin: 2, cols: [
                {view: "icon", icon: "edit", id:"edit_t", tooltip:"Edit Sticky Text", width:50, popup: "edit_text"},
                {view:"icon", icon:"times", id:"close_sticky", tooltip:"Delete Sticky Note widget", width:50, click:function(){
                    $$('sticky1').hide();
                    $$('icon_sticky').enable();
                    widgetRemove("sticky");
                }}
            ]
        },
        body: {
            template: function(){
                if (typeof sticky_text == 'undefined'){
                    sticky_text = "Edit your sticky note using the edit icon above!";
                    return sticky_text;
                } else {
                    return sticky_text;
                }
            }
        }
    });
}


/*
Custom made popup to handle editing the sticky note text
Handles posting the sticky note data to the DB and updating the text in the main widget
*/
webix.ui({
    view:"popup",
    id:"edit_text",
    head:"Edit note",
    width:300, height: 100,
    body:{ rows:[
        {view:"text", id:"input", label:"New note: "},
        {view:"button", value:"Update",
            click:function(){
                var temp = $$('sticky1').getBody();
                var newtext = ($$('input').getValue());
                var url = "../api/sticky/"+username+"/";
                $.post(url, {"data":JSON.stringify({"notedata":newtext},null,""), "csrfmiddlewaretoken":csrf_tok});
                    //add below to remove all html tags from sticky note text
                    //.toString().replace(/(<([^>]+)>)/ig,"");
                temp.define('template',newtext);
                $$('input').setValue("");
                temp.refresh();
                $$('edit_text').hide();
            }
        }
    ]
    }
});

/*
Function: loadNotify
Basically a window with a form inside of it, used to allow guest users to sign up for notifications from door edits
Outsources the actual validation of an email and posting to the DB to an external functions, in page_functions.js
*/
var notify;
function loadNotify(){
    notify = webix.ui({
        container: "notification",
        view:"window",
        id:"notification1",
        width: "auto",
        height: 137,
        autoConfig: true,
        head:{
           view:"toolbar", margin:-2, cols:[
                {view:"icon", icon:"envelope", id:"notify_all", tooltip:"Notify Subscribers", width:50, click:function(){
                    var url = "../api/notify/";
                    $.post(url, {"data":JSON.stringify({"foo":"bar"},null,""), "csrfmiddlewaretoken":csrf_tok});
                }},
                {view:"icon", icon:"times", id: "close_notify", tooltip:"Delete Notification widget", width:75, click:function(){
                    $$('notification1').hide();
                    $$('icon_notify').enable();
                    widgetRemove("notification");
                }}
            ]
        },
        body:{
            view:"form",
            elements: [
                {view:"text", id: "email", label: "Email:", height:25},
                {cols:[
                    {view:"button", id:"sub", value:"Subscribe",type:"form",
                        click:function(){
                            validateEmail($$('email').getValue());
                        }},
                    {view:"button", id:"unsub", value:"Unsubscribe", type:"form", click:function(){
                        validateEmail($$('email').getValue());
                    }}

                ]},
                {view:"label", value:""}
            ]
        }
    });
}

/*
Function: loadPicture
Creates the picture widget which is just a simple webix window with a template that has the picture in it
*/
var picture;
function loadPicture() {
    picture = webix.ui({
        container:"picture",
        id:"picture1",
        view:"window",
        width:"auto",
        height:"auto",
        autoConfig: true,
        head:{
            view:"toolbar", margin:-2, cols:[
                {view:"icon", icon:"picture-o", id:"p_add", tooltip:"Upload a Picture", popup:"upload_pic"},
                {view:"icon", icon:"times", id:"close_pic", tooltip:"Delete Picture widget", width:50, click:function(){
                    $$('picture1').hide();
                    $$('icon_pic').enable();
                    widgetRemove("picture");
                }}
            ]
        },

        body:{
            view: "template",
            id: "picture_body",
            template: function(){
                try{
                    return picture_text;
                } catch(err){
                    return "Please post a picture!";
                }
            }
        }
    });
}

/*
This popup handles posting the uploaded picture, via a webix uploader
to the DB and then populating the template above with a picture
*/
webix.ui({
    view:"popup", 
    id: "upload_pic",
    body:{rows:[
        {view:"form", rows:[
                {
                view:"uploader",
                id: "upl1",
                value:"Upload Image",
                accept:"image/png, image/gif, image/jpeg",
                upload:"../api/picture/"+username+"/",
                datatype:"json",
                formData:{
                    csrfmiddlewaretoken:csrf_tok
                }
            }, 
            {view:"button", value:"Refresh Image", click:function(){
                getpicture();
                setTimeout(function(){
                    var temp = $$('picture1').getBody();
                    temp.define('template',picture_text);
                    temp.refresh();
                    $$('upload_pic').hide();
            }, 1000)
                

            }}
        ]}
    ]}
});

/*
Function: loadWSelect
Loads the widget select popup, handles hiding the different icons that represent the widget types
*/
var widget_select;
function loadWSelect() {
    widget_select = webix.ui({
        view:"window",
        id:"widget_select",
        container: 'widgetselect',
        height:200, width:350,
        position:"top",
        head:{
            view: "toolbar", margin:-4, cols:[
                {view:"label", label:"Widget Select"},
                {view: "icon", icon: "times-circle", css:"alter",
                    click:function(){
                        $$('widget_select').hide();
                    }}
            ]
        },
        body:{
            cols:[
                {
                    view:"icon", icon:"calendar", tooltip:"Calendar widget", id:"icon_cal", width:50, height:50,
                    click:function(){
                        makeWidget('calendar');
                        $$('icon_cal').disable();
                        $$('widget_select').hide();
                    }
                },
                {
                    view: "icon", icon: "edit", id: "icon_sticky" ,tooltip:"Sticky Note widget", width:50, height:50,
                    click:function(){
                        makeWidget('sticky');
                        $$('icon_sticky').disable();
                        $$('widget_select').hide();
                    }
                },
                {
                    view: "icon", icon: "picture-o", id: "icon_pic", tooltip:"Picture widget", width:50, height:50,
                    click:function(){
                        makeWidget('picture');
                        $$('icon_pic').disable();
                        $$('widget_select').hide();
                    }
                },
                {
                    view: "icon", icon: "envelope", id:"icon_notify", tooltip:"Notifications widget", width:50, height:50,
                    click:function(){
                        makeWidget('notification');
                        $$('icon_notify').disable();
                        $$('widget_select').hide();
                    }
                }
            ]
        },
    });
}

/*
The below functions are the GET and POST request functions for the different widgets
*/

//Calendar get request
function getCalendar(){
    var url = "../api/calendar/"+username+"/";
    $.ajax({
        type: 'GET',
        url: url,
        jsonp: 'callback',
        success: function (data){
            getCalData(data);
        }
    });
}

function getCalData(data){
    events = data;
    var d_format = webix.Date.dateToStr("%F %j, %Y");
    var t_format = webix.Date.dateToStr("%g:%i %A");
    var d_parser = webix.Date.strToDate("%Y-%m-%d");
    var t_parser = webix.Date.strToDate("%H:%i:00");
    events.forEach(function(result, index) {
        var temp_date = d_parser(result["e_date"]);
        var temp_time = t_parser(result["d_time"]);
        result["e_date"] = d_format(temp_date);
        result["d_time"] = t_format(temp_time);


    });
}


//picture get request
function getpicture(){
    var url = "../api/picture/"+username+"/";
    $.ajax({
        type:'GET',
        url:url,
        jsonp:'callback',
        success:function(data){

            getPict(data['image']);

        }
    });
}

function getPict(param){
    picture_text = "<img id='picture' src='.."+param.substring(5)+"' style='max-width:100%;max-height:100%;'/>";
}

//stickynote get request
function getsticky(){
    //get the sticky content
    var url = "../api/sticky/"+username+"/";
    $.ajax({
        type: 'GET',
        url: url,
        jsonp: 'callback',
        success: function (data){
            getStickyData(data['notedata']);
        },
    });
    
}

function getStickyData(param){
    sticky_text = param;
}