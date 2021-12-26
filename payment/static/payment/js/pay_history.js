        window.onload = function(){
            document.getElementById('fromDate').value = new Date().toISOString().substring(0, 10);;
            document.getElementById('toDate').value = new Date().toISOString().substring(0, 10);;

            var acc = document.getElementsByClassName("accordion");
            var i;

            for (i = 0; i <= acc.length; i++) {
                acc[i].addEventListener("click", function() {
                    this.classList.toggle("active");
                    var panel = this.nextElementSibling;
                    if (panel.style.display === "block") {
                        panel.style.display = "none";
                    } else {
                        panel.style.display = "block";
                    }
                });
            }

        }


        function previousDate(){
            var from_date = document.getElementById('fromDate');
            var to_date = document.getElementById('toDate');
            if (from_date.value > to_date.value){
                from_date.value = to_date.value;
                alert('날짜를 확인해주세요');
            }
            else{
                to_date.min = from_date.value;
            }
        }
        function currentDate(){
            var current_date = new Date().toISOString().substring(0, 10);
            var from_date = document.getElementById('fromDate');
            var to_date = document.getElementById('toDate');
            if (to_date.value > current_date){
                to_date.value = current_date;
                alert('날짜를 확인해주세요')
            }
            else{
                from_date.max = to_date.value;
            }
        }
