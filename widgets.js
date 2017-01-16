/**
 * Created by hrobohboy on 12/19/16.
 */
function scheduleWindow(){

    webix.ui({
        view:"window",
        id:"win3",
        height: 355,
        width: 439,
        left: 100, top: 50,
        move:true,
        head:{
            view:"toolbar", cols:[
                {view:"label", label: "Schedule" },
                { view:"button", label: 'X', width: 100, align: 'right', click:"$$('win3').close();"}
            ]
        }
        ,
        body:{
            template:"<img src='Untitled.png' width='439px' height='355px'/>"
        }
    }).show();
}

function loadCalendar(){
    webix.ui({
        container:"calendar",
        id: "calendar1",
        autoConfig: true,
        view:"calendar",
        weekHeader:true,
        weekNumber:true,
        date:new Date(),
        events:webix.Date.isHoliday,
        width: "auto",
        height: "auto",
        autoConfig: true
    }).show();
}


function loadSticky(){
    webix.ui({
        container:"stickynote",
        id: "sticky1",
        view: "window",
        width: "auto",
        height: "auto",
        autoConfig: true,
        head: {
            view: "toolbar", margin: -2, cols: [
                {view: "icon", icon: "edit", popup: "edit_text"}
            ]
        },
        body: {
            template: " "
        }
    }).show();
}

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
                temp.define('template',$$('input').getValue());
                sticky_text = $$('input').getValue();
                temp.refresh();
                $$('edit_text').hide();
            }
        }
    ]
    }
});


function loadSchedule() {
    webix.ui({
        container: "schedule",
        id: "schedule1",
        width: "auto",
        height: "auto",
        autoConfig: true,
        template: '<button id="schedulebtn" class="btn btn-default" onclick="scheduleWindow();">View Schedule</button>'
    }).show();
}

function loadWSelect() {
    webix.ui({
        view:"window",
        id:"widget_select",
        height:200, width:350,
        left:25, top:200,
        head:{
            view: "toolbar", margin:-4, cols:[
                {view:"label", label:"Widget Select"},
                {view: "icon", icon: "times-circle", css:"alter",
                    click:"$$('widget_select').hide();"}
            ]
        },
        body:{
            view: "toolbar", margin: -2, cols:[
                {
                    view:"icon", icon:"calendar", width:50, height:50,
                    click:"widget_type = 'calendar'; makeWidget(); $$('widget_select').hide();"},
                {
                    view: "icon", icon: "edit", width:50, height:50,
                    click:"widget_type = 'stickynote'; makeWidget(); $$('widget_select').hide();"},
                {
                    view: "icon", icon: "picture-o", width:50, height:50,
                    click:"widget_type = 'schedule'; makeWidget(); $$('widget_select').hide();"
                }
            ]
        }
    }).show();
}

function getCalendar(){
    value = '';
    //get the calendar content
    return value;
}
function getSchedule(){
    value = '';
    //get the schedule content
    return value;
}
function getStickynote(){
    value = "";
    //get the stickynote content
    return value;
}