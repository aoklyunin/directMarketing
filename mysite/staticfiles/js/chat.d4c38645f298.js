var fromAvatar = "";
var toAvatar = "";

function formatAMPM(date) {
    var hours = date.getHours();
    alert(hours);
    var minutes = date.getMinutes();
    minutes = minutes < 10 ? '0'+minutes : minutes;
    var strTime = hours + ':' + minutes;
    return strTime;
}

//-- No use time. It is a javaScript effect.
function insertChat(who, text, isUsers, date, time = 0){
    var control = "";
    if (isUsers){
        control = '<li style="width:100%">' +
                        '<div class="msj macro">' +
                        '<div class="avatarChat"><img class="img-circle" style="width:100%;" src="'+ toAvatar +'" /></div>' +
                            '<div class="text text-l">' +
                                '<p>'+ text +'</p>' +
                                '<p><small>'+date+'</small></p>' +
                            '</div>' +
                        '</div>' +
                    '</li>';
    }else{
        control = '<li style="width:100%;"class="li_chat">' +
                        '<div class="msj-rta macro">' +
                            '<div class="text text-r">' +
                                '<p>'+text+'</p>' +
                                '<p><small>'+date+'</small></p>' +
                            '</div>' +
                        '<div class="avatarChat" style="padding:0px 0px 0px 10px !important"><img class="img-circle" style="width:100%;" src="'+fromAvatar+'" /></div>' +
                  '</li>';
    }
    setTimeout(
        function(){
            $("ul.messageList").append(control);

        }, time);
    $

}
var name = "";
var target = "";

function setStats(mname,mfromAvatar,mtoAvatar,mtarget){
    target = mtarget;
    name = mname;
    fromAvatar = mfromAvatar
    toAvatar = mtoAvatar
}



function resetChat(){
    $("ul.messageList").empty();
}

$(".mytext").on("keyup", function(e){
    if (e.which == 13){
        var text = $(this).val();
        if (text !== ""){
            date = new Date();
            insertChat(name, text,false,moment(date).format('HH:mm'));
            df = moment(date).format('YYYY-MM-DD HH:mm');
            $.ajax({ url: target,data: {"value":text,"dt":df},
                 type: "POST" });
            $(this).val('');
        }
    }
});

//-- Clear Chat
resetChat();

// using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

$.ajaxSetup({
     beforeSend: function(xhr, settings) {
         function getCookie(name) {
             var cookieValue = null;
             if (document.cookie && document.cookie != '') {
                 var cookies = document.cookie.split(';');
                 for (var i = 0; i < cookies.length; i++) {
                     var cookie = jQuery.trim(cookies[i]);
                     // Does this cookie string begin with the name we want?
                     if (cookie.substring(0, name.length + 1) == (name + '=')) {
                         cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                         break;
                     }
                 }
             }
             return cookieValue;
         }
         if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
             // Only send the token to relative URLs i.e. locally.
             xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
         }
     }
});

