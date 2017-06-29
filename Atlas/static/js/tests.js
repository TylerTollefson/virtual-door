function testPostEvent(){
    //test if HTML tags are handled with post requests
    var calendar_input = {message:'Hello <p>World</p>', e_date:'2017-12-20', d_time:'12:59:00'};
    try {
        $.post("../api/calendar/" + username + "/",
            {"data": JSON.stringify(calendar_input, null, ""), "csrfmiddlewaretoken": csrf_tok},
            function (data) {
                console.log("Event posted." + data);
            });
    } catch (err) {
        throw "HTML input not supported by DB."
    }
}














testPostEvent();