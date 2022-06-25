console.log(1);
var submit = document.getElementById('feedback_submit');
submit.addEventListener("click", submitFeedback);
var takePhotoElement = document.getElementById('take_photo');
takePhotoElement.addEventListener("click", takePhoto);
var maskPrompt = document.getElementById("mask_prompt")
var noMaskPrompt = document.getElementById("no_mask_prompt")
var imagesNumPerLoad = 15;
var images = [];
var currentImage = null;
/*
* style:
*   - common
*   - danger
*
*
* */
$(window).on("resize scroll", function () {

    var windowHeight = $(window).height();//当前窗口的高度
    var scrollTop = $(window).scrollTop();//当前滚动条从上往下滚动的距离
    var docHeight = $(document).height(); //当前文档的高度

});
window.onload = function () {
    pictures = [];
    var url = "/api/getPictures";
    $.ajax({
        type: "get",
        url: url,
        success: (data) => {
            for (var i = 0; i < data.data.length; i++) {
                addImage(data.data[i])
            }
        }
    });


    var socket = io("http://localhost:5000");
    socket.on('connect', function () {
        socket.emit('my_event', {data: 'I\'m connected!'});
        console.log("connected")
    });
    socket.on('picture_upload', function (msg, cb) {
        // $('#log').append('<br>' + $('<div/>').text('Received #' + msg.count + ': ' + msg.data).html());
        console.log(msg.data)
        addToBigImage(msg.data)
    });

    var socket2 = io("http://localhost:8080");
    socket2.on('connect', function () {
        socket.emit('my_event', {data: 'I\'m connected222!'});
        console.log("connected22")
    });
    socket2.on('model_transmit', function (msg, cb) {
        // $('#log').append('<br>' + $('<div/>').text('Received #' + msg.count + ': ' + msg.data).html());
        console.log("model_transmit")
        socket.emit("model_transmit",msg)
        console.log(msg)
    //     $.ajax({
    //     type: "POST",
    //     url: 'http://localhost:5000/picUpload/modelTransmit',
    //     contentType: "application/json",
    //     data: msg,
    //     dataType: "json",
    //     success: function (data) {
    //         console.log("模型下发成功")
    //     },
    //     error: (err) => {
    //         console.log("模型下发失败")
    //     }
    // });
    });
}

function takePhoto(e) {
    e.preventDefault();
    ifStayLocal=$("#if_stay_local").get(0).checked
    var url = "/picUpload/takePhoto?ifStayLocal="+ifStayLocal;
    $.ajax({
        type: "get",
        url: url,
        success: (data) => {
            printPrompt(data, "common")
            setTimeout(function () {

                printPrompt("Welcome","common")

            }, 1500)
        }
    });
}

function submitFeedback(e) {
    e.preventDefault();
    var feedbackValue = $('#feedback').val()
    console.log(feedbackValue)
    $.ajax({
        type: "POST",
        url: '/picUpload/feedback',
        contentType: "application/json",
        data: JSON.stringify({
            "feedback": feedbackValue,
            "message": "反馈"
        }),
        dataType: "json",
        success: function (data) {
            var json = data;//获取到json字符串，还需解析
            if (json == "success") {
                printPrompt("谢谢您的反馈", "common")
            } else {
                printPrompt("设备错误，请重试", "danger");
            }
        },
        error: (err) => {
            console.log("err")
        }
    });
}

function printPrompt(prompt, style) {
    if (style == "common") {
        maskPrompt.innerText = prompt
        noMaskPrompt.innerText = ""
    } else if (style == "danger") {
        noMaskPrompt.innerText = prompt
        maskPrompt.innerText = ""
    }
}

function addToBigImage(pic) {
    if (currentImage != null)
        addImage(currentImage)
    var mainPic = document.getElementById("main_pic")
    mainPic.setAttribute("src", pic.pictureurl)
    if (pic.ismasked == 0) {
        printPrompt("请佩戴口罩", "danger")
    } else if (pic.ismasked == 1) {
        printPrompt("欢迎！", "common")
    } else {
        printPrompt("请正确佩戴口罩", "danger")
    }
    currentImage = pic
}

function addImage(pic) {
    console.log("addImage")
    console.log(pic)
    var item = document.createElement("div");
    item.setAttribute("class", "item");

    var imageHref = document.createElement("a");
    // imageHref.setAttribute("href","bigimage.html");
    imageHref.setAttribute("href", "bigimage.html");
    var image = document.createElement("img");
    image.setAttribute("src", pic.pictureurl);
    imageHref.appendChild(image)
    item.appendChild(imageHref);

    var imageHref = document.createElement("a");

    var itemInfo = document.createElement("text")
    itemInfo.innerText = pic.timeNow
    item.appendChild(itemInfo)


    $("#images").append(item);
    images.push(item);


}
