        function test(){
            alert('welcome outside file');
            console.log('hi');
        }

        function fortest(){
            for(var i=0;i<10;i++){
                console.log('2X'+(i+1)+'='+(2*(i+1)));
            }
        }

        function get_data(){
            var id = document.getElementById('user_id');
            alert(id.value);
        }

        function check_pwd(){
            //alert('pwd');
            var pwd1 = document.getElementById('pwd1');
            var pwd2 = document.getElementById('pwd2');
            console.log(pwd1+","+pwd2);
            if(pwd1.value==pwd2.value){
                alert("==");
            } else {
                alert("동일하지 않습니다.");
            }
        }

        function check_email(){
            var email = document.getElementById('email');
            alert(email.value);
            document.getElementById('domain').value = email.value;
        }

        function check_hobby(){
            var data = document.getElementsByName("hobby");
            alert(data.length);
            for(var i=0;i<data.length;i++){
                if(data[i].checked){
                    alert(data[i].value);
                }
            }
        }

