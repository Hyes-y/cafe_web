function test_str(){
   var data = '123456';
   var sum = 0;
   for(var i=0;i<data.length;i++){
        console.log(data[i]);
        sum = sum + parseInt(data[i]);
    }
    console.log(sum);

//    for (var d in data){
//            console.log(d);
//    }
}

function test_fuc(){
    var val = document.getElementById('user_id').value;
    var dan = val;
    for(var i=0;i<9;i++){
        console.log(dan+'X'+(i+1)+'='+(dan*(i+1)));
    }
}

function gugudan(){
    for(var k=0;k<8;k++){
        var dan = k+2;
        for(var i=0;i<9;i++){
            console.log(dan+'X'+(i+1)+'='+(dan*(i+1)));
        }
    }
}

