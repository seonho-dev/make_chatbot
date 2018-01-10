#!/usr/bin/env python3
import cgi
from botengine import make_reply

# 입력 양식의 글자 추출하기 --- (※1)
form = cgi.FieldStorage()

# 메인 처리 --- (※2)
def main():
    m = form.getvalue("m", default="")
    if   m == "" : show_form()
    elif m == "say" : api_say()

# 사용자의 입력에 응답하기 --- (※3)
def api_say():
    print("Content-Type: text/plain; charset=utf-8")
    print("")
    txt = form.getvalue("txt", default="")
    if txt == "": return
    res = make_reply(txt)
    print(res)

# 입력 양식 출력하기 --- (※4)
def show_form():
    print("Content-Type: text/html; charset=utf-8")
    print("")
    print("""
    <html>
        <meta charset="utf-8">
        <script src="https://code.jquery.com/jquery-3.1.1.min.js"></script>
        <style>
            h1   { background-color: #ffe0e0; }
            div  { padding:10px; }
            span { border-radius: 10px; background-color: #ffe0e0; padding:8px; }
            .bot { text-align: left; }
            .usr { text-align: right; }
        </style>
        <body>
        <h1>&nbsp;&nbsp;&nbsp;&nbsp;생성모델형(컨셉)챗봇</h1>
        <div id="chat"></div>
        <div class='usr'><input id="txt" size="40" onkeypress="if(event.keyCode==13) {say();send.focus(); return false;}">
        <button id="snd" onclick="say();this.focus();">전송</button></div>
        <script>
            var send = document.getElementById("snd");
            var url = "./chatbot.py";
            function say() {
              var txt = $('#txt').val();
              $.get(url, {"m":"say","txt":txt},
                function(res) {
                  var res = res; 
                  if( !res ){ console.log("비어 있음"); 
                    alert("입력해 주세요!");
                  }else{ console.log("값이 있음"); 
                        if(esc(res).substring(0,0)=='"'){
                            alert("대답에 에러가 있어요!!!");
                        } else {
                            var html = '<div class="usr"><span>' + esc(txt) +
                            '</span>: 나</div><div class="bot"> 봇:<span>' + 
                            esc(res) + '</span></div>';
                            $('#chat').html($('#chat').html()+html);
                            $('#txt').val('').focus();
                        }
                        

                  }
                });
            }
            function esc(s) {
                try {
                    return s.replace('&', '&amp;').replace('<','&lt;').replace('>', '&gt;').replace('"', ' ');
                }
                catch(err) {
                    alert("대답에 에러가 있음");
                    console.log("값이 있음");
                    return s;
                }
            }
        </script>
        </body>
    </html>
    """)

main()
