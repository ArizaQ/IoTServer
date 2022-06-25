var submit=document.getElementsByClassName('login_button')[0];
console.log("submit");
submit.addEventListener("click",submit_login);


$('#email_input').on('change',function(e){
    var email_input=document.getElementsByClassName('username_input')[0];
    var email=email_input.value;
        checkEmail(email);
});

// 登录提交
function submit_login(e){
    e.preventDefault();
    var email_input=document.getElementsByClassName('username_input')[0];
    var email=email_input.value;
    var password_input=document.getElementsByClassName('password_input')[0];
    var password=password_input.value;
    if(!checkEmail(email)){
        return;
    }
    if(!checkPassword(password)){
        return;
    }
    send_login_info(email,password);
}
function send_login_info(email,password,authcode){
    // password=getAES(password)
    var auth_prompt=document.getElementsByClassName('auth_prompt')[0];
    printRequestErrorInfo("");
    printPrompt(auth_prompt,"");
    printRequestErrorInfo("")
    // var url='login/login?email='+email+"&password="+password+"&authcode="+authcode;
    // console.log(url);
    $.ajax({
        type: "POST",
        url: '/login/login',
        contentType: "application/json",
        data:JSON.stringify({
            "email": email,
            "password":password,
        }),
        dataType:"json",
        success:function(data){
            console.log("data"+data)
            console.log("登录Ajax")
            console.log(data.responseText)

            if (data == "success") {
                gotoAdmin();
            } else if (data == 'password error') {
                printRequestErrorInfo("邮箱或密码错误，请重试。")
            } else if (data == 'auth code error') {
                printPrompt(auth_prompt, "验证码错误");
            } else if (data == "email does not exist") {
                printRequestErrorInfo("邮箱或密码错误，请重试。")
            }
        },
        error: (err) =>{
            var dataText=err.responseText;
            console.log("err")
            if (dataText == "success") {
                gotoAdmin();
            } else if (dataText == 'password error') {
                printRequestErrorInfo("邮箱或密码错误，请重试。")
            } else if (dataText == 'auth code error') {
                printPrompt(auth_prompt, "验证码错误");
            } else if (dataText == "email does not exist") {
                printRequestErrorInfo("邮箱或密码错误，请重试。")
            }
        }
    });
}
function encryptPassword(plainPassword){
    var hash = CryptoJS.MD5(plainPassword);
    console.log("test:",hash.toString());
    return hash;
}
function getAesString(data,key,iv){//加密
    var key  = CryptoJS.enc.Utf8.parse(key);
    var iv   = CryptoJS.enc.Utf8.parse(iv);
    var encrypted =CryptoJS.AES.encrypt(data,key,
        {
            iv:iv,
            mode:CryptoJS.mode.CBC,
            padding:CryptoJS.pad.Pkcs7
        });
    return encrypted.toString();    //返回的是base64格式的密文
}
function getDAesString(encrypted,key,iv){//解密
    var key  = CryptoJS.enc.Utf8.parse(key);
    var iv   = CryptoJS.enc.Utf8.parse(iv);
    var decrypted =CryptoJS.AES.decrypt(encrypted,key,
        {
            iv:iv,
            mode:CryptoJS.mode.CBC,
            padding:CryptoJS.pad.Pkcs7
        });
    return decrypted.toString(CryptoJS.enc.Utf8);
}

function getAES(data){ //加密
    var key  = 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA';  //密钥
    var iv   = '1234567812345678';
    var encrypted =getAesString(data,key,iv); //密文
    var encrypted1 =CryptoJS.enc.Utf8.parse(encrypted);
    return encrypted;
}

function getDAes(data){//解密
    var key  = 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA';  //密钥
    var iv   = '1234567812345678';
    var decryptedStr =getDAesString(data,key,iv);
    return decryptedStr;
}
function getAuthCode(){
    var auth_prompt=document.getElementsByClassName('auth_prompt')[0];
    printPrompt(auth_prompt,"");
    show_auth_code.text="刷新"
    var captchaWrap = $(".cap_box")
    $.ajax({
        type: "get",
        url: "/login/captcha",
        success: (data) => {
            console.log("验证码数据");
            captchaWrap.html(data.data)
            authCode=data.text.toLowerCase();
        }
    });
}

// 辅助函数：check print 跳转
function checkEmail(email){
    var emailR=/^\w+@\w+\.\w+$/i;
    var emailPrompt=document.getElementsByClassName("email_prompt")[0];
    if(!emailR.test(email)){
        printPrompt(emailPrompt,"邮箱格式有误。");
        return false;
    }
    printPrompt(emailPrompt,"");
    return true;
}
function checkPassword(password){
    if(password.length<8){
        printPasswordPrompt("密码长度应该至少达到8个字符。");
        // printRequestErrorInfo("ddddddddddddddd");
        return false;
    }
    printPasswordPrompt("");
    return true;
}
function printPasswordPrompt(prompt){
    var passwordPrompt=document.getElementsByClassName("password_prompt")[0];
    console.log(prompt);
    passwordPrompt.innerHTML=prompt;
}
function printPrompt(element,prompt){
    // var emailPrompt=document.getElementsByClassName("email_prompt")[0];
    element.innerHTML=prompt;
}
function printRequestErrorInfo(errorInfo){
    var info=document.getElementsByClassName("login_type_a")[0];
    info.style.color="red";
    info.innerHTML=errorInfo;
}
function gotoAdmin(){
    window.location.href="/admin";
}
