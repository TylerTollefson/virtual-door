/**
 * Created by hrobohboy on 12/19/16.
 */
openBurger();
enableClose();
var widget_type = "No widget found";
var serializedData = [];
var options = {};
$('.grid-stack').gridstack(options);
var grid = $('.grid-stack').data('gridstack');
var schedule = new Image();
schedule.src = "Untitled.png";
var originalwidth = schedule.width;
var originalheight = schedule.height;
if(window.innerWidth < schedule.width){
    var ratio = window.innerWidth/schedule.width;
    schedule.width = window.innerWidth;
    schedule.height = schedule.height*ratio;
}
else{
    schedule.width = originalwidth;
    schedule.height = originalheight;
}

$(window).on('resize', function(){
    $$('calendar1').resize();
    $$('sticky1').resize();
    $$('schedule1').resize();
    if($$('win3')){
        if(window.innerWidth < schedule.width){
            var ratio = window.innerWidth/schedule.width;
            schedule.width = window.innerWidth;
            schedule.height = schedule.height*ratio;
        }
        else{
            schedule.width = originalwidth;
            schedule.height = originalheight;
        }
        $$('win3').close();
        scheduleWindow();
    }

});

$(window).scroll( function(){
    if($$('win3')){
        $$('win3').close();
        scheduleWindow();
    }
});

$('.grid-stack').on('resizestop', function(event, ui) {
    setTimeout(
        function()
        {
            $$('calendar1').resize();
            $$('sticky1').resize();
            $$('schedule1').resize();
        }, 10);
});


$(function () {
    new function () {
        this.disableGrid = function(){
            closeBurger();
            grid.movable('.grid-stack-item', false);
            grid.resizable('.grid-stack-item', false);
        }.bind(this);

        this.enableGrid = function(){
            closeBurger();
            grid.movable('.grid-stack-item', true);
            grid.resizable('.grid-stack-item', true);
        }.bind(this);


        this.loadGrid = function () {
            closeBurger();
            grid.removeAll();
            var items = GridStackUI.Utils.sort(serializedData);
            _.each(items, function (node) {
                var gridContent = "no widget found: ";
                if(node.content == "calendar") {
                    gridContent = getCalendar();
                } else if(node.content == "schedule") {
                    gridContent = getSchedule();
                } else if(node.content == "stickynote") {
                    gridContent = getStickynote();
                } else{
                    gridContent += node.content;
                }
                grid.addWidget($('<div><div class="grid-stack-item-content" id=' + node.content + '>' + gridContent  + '</div><div/>'),
                    node.x, node.y, node.width, node.height);
            }, this);
            loadCalendar();
            loadSticky();
            loadSchedule();
            return false;
        }.bind(this);

        this.saveGrid = function () {
            closeBurger();
            var counter = 0;
            serializedData = _.map($('.grid-stack > .grid-stack-item:visible'), function (el) {
                el = $(el);
                var node = el.data('_gridstack_node');
                return {
                    x: node.x,
                    y: node.y,
                    width: node.width,
                    height: node.height,
                    content: $('.grid-stack-item-content')[counter++].id
                };
            }, this);
            $('#saved-data').val(JSON.stringify(serializedData, null, '    '));
            return false;
        }.bind(this);

        this.clearGrid = function () {
            closeBurger();
            grid.removeAll();
            return false;
        }.bind(this);

        this.addNewWidget = function () {
            if (serializedData.length == 3){
                return false;
            } else {
                closeBurger();
                loadWSelect();

            }
            return false;
        }.bind(this);

        $('#add-widget').click(this.addNewWidget);
        $('#save-grid').click(this.saveGrid);
        $('#load-grid').click(this.loadGrid);
        $('#clear-grid').click(this.clearGrid);
        $('#disable-grid').click(this.disableGrid);
        $('#enable-grid').click(this.enableGrid);

        //this.loadGrid();
    };
});

function makeWidget() {
    if (widget_type =="calendar"){
        var node = {
            x: Math.random() * (5 - 1) + 1,
            y: Math.random() * (5 - 1) + 1,
            width: 3,
            height: 4,
            content: widget_type
        };
        serializedData.push(node);
        grid.addWidget($('<div><div class="grid-stack-item-content" id=' + node.content + '></div><div/>'),
            node.x, node.y, node.width, node.height);
        loadCalendar();
    } else if (widget_type == "stickynote"){
        node = {
            x: Math.random() * (5 - 1) + 1,
            y: Math.random() * (5 - 1) + 1,
            width: 2,
            height: 2,
            content: widget_type
        };
        serializedData.push(node);
        grid.addWidget($('<div><div class="grid-stack-item-content" id=' + node.content + '></div><div/>'),
            node.x, node.y, node.width, node.height);
        loadSticky();
    } else if (widget_type == "schedule"){
        node = {
            x: Math.random() * (5 - 1) + 1,
            y: Math.random() * (5 - 1) + 1,
            width: 2,
            height: 2,
            content: widget_type
        };
        serializedData.push(node);
        grid.addWidget($('<div><div class="grid-stack-item-content" id=' + node.content + '></div><div/>'),
            node.x, node.y, node.width, node.height);
        loadSchedule();
    }
}

function closeBurger(){
    $( ".menu" ).slideToggle( "slow", function() {
            $( ".cross" ).hide();
            $( ".hamburger" ).show();
    });
}

function enableClose(){
    $( ".cross" ).click(function() {
        $( ".menu" ).slideToggle( "slow", function() {
            $( ".cross" ).hide();
            $( ".hamburger" ).show();
        });
    });
}

function openBurger(){
    $( ".cross" ).hide();
    $( ".menu" ).hide();
    $( ".hamburger" ).click(function() {
        $( ".menu" ).slideToggle( "slow", function() {
            $( ".hamburger" ).hide();
            $( ".cross" ).show();
        });
    });
}