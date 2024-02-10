$(document).ready(function(){
    let speciesInput = $('#species');
    if(speciesInput)
        speciesInput.keyup(function(){
            this.value = this.value.toLowerCase();
        });
});