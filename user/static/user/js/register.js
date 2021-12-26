
        function get_data(){
            var id = document.getElementById('user_id');
            alert(id.value);
        }

        function check_pwd(){
            var pwd1 = document.getElementById('pwd1');
            var pwd2 = document.getElementById('pwd2');
            console.log(pwd1+","+pwd2);
            if(pwd1.value!=pwd2.value){
                alert("비밀번호를 다시 확인해주세요");
            }
        }


        function check_email(){
            var email = document.getElementById('email2');
            document.getElementById('email1').value = email.value;
        }

        function id_overlap_check(){
//           아이디 다시 입력 시 중복확인 버튼 활성화
              $('.id_input').change(function () {
              $('#id_check_success').hide();
              $('.id_overlap_button').show();
              $('.id_input').attr("check_result", "fail");
            })

//          아이디를 입력하지 않았을 때 alert창
            if ($('.id_input').val() == '') {
              alert('아이디를 입력해주세요.')
              return;
            }

            id_overlap_input = document.querySelector('input[name="id"]');
            alert(id_overlap_input.value)

            $.ajax({
                    url : "/user/id_overlap_check",
                    data: {
                        'id': id_overlap_input.value
                    },
                  datatype: 'json',

                  success: function (data) {
                    console.log(data['overlap']);
                    if (data['overlap'] == "fail") {
                      alert("이미 존재하는 아이디 입니다.");
                      id_overlap_input.focus();
                      return;
                    } else {
                      alert("사용가능한 아이디 입니다");
                      $('.id_input').attr("check_result", "success");
                      $('#id_check_success').show();
                      $('.id_overlap_button').hide();
                      return;
                    }
                  }
            });
        }