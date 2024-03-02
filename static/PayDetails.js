function delete1() {
    let v = confirm("Want to delete:");
    if (v == true) {
        return true;
    }
    else {
        return false;
    }
}

let x = document.getElementById('hide1')
x.style.display = 'none'
function update1() {
    if (x.style.display == 'none') {
        x.style.display = 'flex'
    }
    else {
        x.style.display = 'none'
    }
}


