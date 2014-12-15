function match_up(self){
    answerTexts = document.getElementsByClassName('answerTexts');
    for(var i = 0; i < answerTexts.length; i++){
        if(answerTexts[i].value == ""){
            answerTexts[i].value = self.value;
            if (answerTexts[i].value == answerTexts[i].name){
                answerTexts[i].style.cssText = "width:40px;background-color:green;color:white;"
            }else{
                answerTexts[i].style.cssText = "width:40px;background-color:red;color:white;"
            }
            return;
        }
    }
}

function clear_all(){
    answerTexts = document.getElementsByClassName('answerTexts');
    for(var i = 0; i < answerTexts.length; i++){
        answerTexts[i].value  = "";
        answerTexts[i].style.cssText = "width:40px;"
    }
}
