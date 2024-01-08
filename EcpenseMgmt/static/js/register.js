const usernameFiled = document.querySelector('#usernameFiled');
const feedBackArea = document.querySelector('.invalid_feedback');
const emailField = document.querySelector('#emailField');
const passwordField = document.querySelector('#passwordField');
const emailfeedBackArea = document.querySelector('.emailfeedBackArea'); 
const usernameSuccessOutput = document.querySelector('.usernameSuccessOutput');
const showPasswordToggle = document.querySelector('.showPasswordToggle');
const submitBtn = document.querySelector('.submit-btn')





const handleToggleInput = (e) => {
    if (showPasswordToggle.textContent === "SHOW") {
      showPasswordToggle.textContent = "HIDE";
      passwordField.setAttribute("type", "text");
    } else {
      showPasswordToggle.textContent = "SHOW";
      passwordField.setAttribute("type", "password");
    }
  };
  
showPasswordToggle.addEventListener("click", handleToggleInput);
  
  
emailField.addEventListener('keyup', (e)=>{
    const emailval = e.target.value; 
    emailField.classList.remove('is-invalid');
    emailfeedBackArea.style.display = 'none';
 
    if(emailval.length>0){
        fetch('/authenitcation/validate-email', {
            body: JSON.stringify({email:emailval}),
            method:'POST',
        })    
        .then((res)=>res.json())
        .then((data)=>{
            console,console.log('data', data);
            if (data.email_erorr){
                submitBtn.disabled = true
                emailField.classList.add('is-invalid');
                emailfeedBackArea.style.display = 'block';
                emailfeedBackArea.innerHTML = `<p>${data.email_erorr}</p>`;

            }else{
                submitBtn.removeAttribute('disabled')
            }
        });
    }
});



usernameFiled.addEventListener('keyup', (e)=>{
    const usernameval = e.target.value; 
    usernameSuccessOutput.textContent = `Checking ${usernameval}`

    usernameFiled.classList.remove('is-invalid');
    feedBackArea.style.display = 'none';
    if(usernameval.length>0){
        fetch('/authenitcation/validate-username', {
            body:JSON.stringify({username:usernameval}),
            method:'POST',
        })
        .then((res)=>res.json())
        .then((data)=>{
            usernameSuccessOutput.style.display = 'none';
            if (data.username_erorr){
                submitBtn.disabled = true
                usernameFiled.classList.add('is-invalid');
                feedBackArea.style.display = 'block';
                feedBackArea.innerHTML = `<p>${data.username_erorr}</p>`;

            }else{
                submitBtn.removeAttribute('disabled')
            }
        });
    }
});