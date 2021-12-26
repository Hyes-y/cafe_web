

        /* Set the width of the side navigation to 250px and the left margin of the page content to 250px and add a black background color to body */
        function openNav() {
          document.getElementById("mySidenav").style.width = "250px";
          document.getElementById("main").style.marginLeft = "250px";
          document.body.style.backgroundColor = "rgba(0,0,0,0.4)";
        }

        /* Set the width of the side navigation to 0 and the left margin of the page content to 0, and the background color of body to white */
        function closeNav() {
          document.getElementById("mySidenav").style.width = "0";
          document.getElementById("main").style.marginLeft = "0";
          document.body.style.backgroundColor = "white";
        }

        function pointCheck() {
          var point = document.getElementById("payPoint").innerText;
          var usePoint = document.getElementById("point").value;
          var possible = parseInt(parseInt(usePoint) / 100);
          var check = parseInt(usePoint) % 100;

          if (parseInt(usePoint) < 0){
            alert("포인트는 0 이상의 양수 범위에서 사용 가능합니다.");
            document.getElementById("point").value = = 0;
          }
          if (parseInt(point) < parseInt(usePoint)){
              alert("사용 포인트 범위를 초과하였습니다.");
              document.getElementById("point").value = = 0;
          }

          if (check != 0){
              alert("포인트는 백점 단위로 사용 가능합니다.");
              document.getElementById("point").value = possible * 100;
          }

        }

        function allPoint() {
            var point = document.getElementById("payPoint").innerText;
            var possible = parseInt(parseInt(point) / 100);
            var total = document.getElementById("total").innerText;
            var usePoint = document.getElementById("point").value;

            if (parseInt(possible) > parseInt(total)) {
                document.getElementById("point").value = parseInt(total);
            }
            else {
                document.getElementById("point").value = possible * 100;
            }
        }