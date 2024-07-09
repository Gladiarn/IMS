document.addEventListener('DOMContentLoaded', function(){

    let signin = document.getElementById('sign-in-container');
    let signup = document.getElementById('sign-up-container');

    let blocker = document.getElementById('blocker');
    let button = document.getElementById('blocker-btn');

    let head = document.getElementById('blocker-head');
    let body = document.getElementById('blocker-body');







    button.addEventListener('click', ()=>{
        
        if(blocker.classList.contains('right-blocker')){
            blocker.classList.remove('right-blocker');
            blocker.classList.add('left-blocker');

            signup.classList.remove('hide-signup');
            signin.classList.add('hide-signin');

            button.innerHTML = "SIGN IN";

            head.innerHTML = "Sign In now!";
            body.innerHTML = "Already have an account? Sign in!";

        }
        else if(blocker.classList.contains('left-blocker')){
            blocker.classList.remove('left-blocker');
            blocker.classList.add('right-blocker');

            signup.classList.add('hide-signup');
            signin.classList.remove('hide-signin');

            button.innerHTML = "SIGN UP";
            head.innerHTML = "Join us now!";
            body.innerHTML = "No account yet? Create one, it's free!";


        }


    })
    









    


















});