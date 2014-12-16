function match_up(self){
    var answerTexts = document.getElementsByClassName('answerTexts');
    for(var i = 0; i < answerTexts.length; i++){
        if(answerTexts[i].value == ""){
            answerTexts[i].value = self.value;
            if (answerTexts[i].value == answerTexts[i].name){
                answerTexts[i].style.cssText = "width:40px;margin:3px;background-color:green;color:white;"
            }else{
                answerTexts[i].style.cssText = "width:40px;margin:3px;background-color:red;color:white;"
            }
            return;
        }
    }
}

function clear_all(){
    answerTexts = document.getElementsByClassName('answerTexts');
    for(var i = 0; i < answerTexts.length; i++){
        answerTexts[i].value  = "";
        answerTexts[i].style.cssText = "width:40px;margin:3px;"
    }
}

function onQuestAnswer(){
   var guest_ans = document.getElementById('guest_answer');
   var answerTexts = document.getElementsByClassName('answerTexts');
   for(var i = 0; i < answerTexts.length;i++){
        guest_ans.value += answerTexts[i].value;
   }
}
