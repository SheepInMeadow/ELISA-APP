// function myFunction(choice) {
//     if (choice === 'mod/non') {
//         document.getElementById("input").style.display = 'inline';
//         document.getElementById("mod").style.display = 'inline';
//     } else if (choice === 'general') {
//         document.getElementById("input").style.display = 'inline';
//         document.getElementById("mod").style.display = 'none';
//     }
// }


function referenceSelect() {
    if(document.getElementById('row').checked) {
        document.getElementById('row_input').removeAttribute("disabled")
        document.getElementById('column_input').setAttribute("disabled", true)
    }else if(document.getElementById('column').checked) {
        document.getElementById('column_input').removeAttribute("disabled")
        document.getElementById('row_input').setAttribute("disabled", true)
    }
}