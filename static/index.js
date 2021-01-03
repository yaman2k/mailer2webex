function check_form(){
  var mname= document.getElementById("mailer").value.trim().toUpperCase();

  if(mname=== '' || mname=== null) {

    alert("Mailer cannot be blank.  Please try again");
    document.querySelector("label").style.color="red";
    return false;
  }else document.getElementById("mailer").style.color = "black";

  return true;
}

