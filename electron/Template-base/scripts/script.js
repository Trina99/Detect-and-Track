var slider = document.getElementById("range");
var output = document.getElementById("text_value");
output.value = slider.value;

// Update the current slider value (each time you drag the slider handle)
slider.oninput = function () {
    output.value = this.value;
}

output.oninput = function () {
    slider.value = this.value;
}

// $('.slidecontainer').css('background-size', $(this).val() + '% 14px');