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
            console.log(data)
            for (var i = data.data.length - 1; i >= 0; i--) {
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
    socket.on('stream_upload', function (msg, cb) {
        // $('#log').append('<br>' + $('<div/>').text('Received #' + msg.count + ': ' + msg.data).html());
        console.log(msg.data)
        addImage(msg.data)
    });

    // var socket2 = io("http://139.9.158.194:8080");
    // console.log("prepared to connect to cloud.")
    // socket2.on('connect', function () {
    //     socket.emit('my_event', {data: 'I\'m connected222!'});
    //     console.log("connected22222222222")
    // });
    // socket2.on('model_transmit', function (msg, cb) {
    //     // $('#log').append('<br>' + $('<div/>').text('Received #' + msg.count + ': ' + msg.data).html());
    //     console.log("model_transmit")
    //     socket.emit("model_transmit", msg)
    //     console.log(msg)
    // });
    // socket2.on('my_response', function (msg, cb) {
    //     console.log("my_response")
    //     console.log(msg)
    // });


}

function takePhoto(e) {
    e.preventDefault();
    ifStayLocal = $("#if_stay_local").get(0).checked
    var url = "/picUpload/takePhoto?ifStayLocal=" + ifStayLocal;
    $.ajax({
        type: "get",
        url: url,
        success: (data) => {
            printPrompt(data, "common")
            setTimeout(function () {

                printPrompt("Welcome", "common")

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
    // console.log("addImage")
    // console.log(pic)
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

    var itemInfo = document.createElement("div")
    itemInfo.innerText = pic.timeNow
    item.appendChild(itemInfo)
    var itemInfo2 = document.createElement("span")
    itemInfo2.innerText = getMaskInfo(pic.ismasked)
    item.appendChild(itemInfo2)

    if (pic.pictureurl.startsWith("..")) {
        var uploadButton = document.createElement("button")
        uploadButton.innerHTML = "上传至云端"
        uploadButton.id = "button" + images.length
        uploadButton.style.cssText="display:inline;margin-left:2px;"
        item.appendChild(uploadButton)
        uploadButton.addEventListener("click", activeUpload)
    }

    $("#images").prepend(item);
    images.push(pic);


}

function activeUpload(e) {
    var src = e.srcElement
    srcId = src.id.substr(6)
    pic = images[srcId]
    console.log(pic)
    $.ajax({
        type: "POST",
        url: "/picUpload/activeUpload",
        contentType: "application/json", //必须这样写
        dataType: "json",
        data: JSON.stringify(pic),
        success: () => {
            console.log(document.getElementById(src.id))
            document.getElementById(src.id).remove()
            console.log("sssssssssssss")
        }
    });
}

function getMaskInfo(maskNo) {
    if (maskNo == 0) {
        return "未佩戴口罩";
    } else if (maskNo == 1) {
        return "已佩戴口罩";
    } else {
        return "未正确佩戴口罩"
    }
}
