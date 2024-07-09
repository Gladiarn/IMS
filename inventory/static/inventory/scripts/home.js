document.addEventListener('DOMContentLoaded', function(){
    // Initialize the display content to the dashboard upon loading the page
    DisplayContent('/dashboard');

    // Setup sidebar navigation: manage active state and load new content on click
    let list = Array.from(document.getElementsByClassName('list'));
    list.forEach((li) => {
        li.addEventListener('click', () => {
            console.log('clicked');
            // Remove active class from all items, then add to the clicked one
            list.forEach((li) => {
                li.classList.remove('active');
            });
            li.classList.add('active');
            const url = li.querySelector('a').getAttribute('href');
            DisplayContent(url);
        });
    });

    // Toggle sidebar visibility and main content expansion
    let toggle = document.querySelector('#toggle');
    let sidebar = document.querySelector('#side-bar');
    let main = document.querySelector('#main');
    toggle.addEventListener('click', () => {
        toggle.classList.toggle('toggled');
        sidebar.classList.toggle('closed');
        main.classList.toggle('expand');
    });

    // Setup anchors to prevent default behavior and manually handle navigation
    let anchors = Array.from(document.getElementsByClassName("anchor"));
    anchors.forEach(link => {
        link.addEventListener('click', (event) => {
            event.preventDefault();
            const url = event.target.closest('a').getAttribute('href');
            DisplayContent(url);
        });
    });

    // Function to fetch and display content based on URL, execute any script tags found in the response
    async function DisplayContent(url) {
        try {
            const response = await fetch(url);
            if (!response.ok) {
                throw new Error('Response Not Ok');
            }
            // Insert the processed response into the container's inner html
            const processed = await response.text();
            const container = document.getElementById('components');
            container.innerHTML = processed;

            // Execute scripts within the fetched content
            const scripts = Array.from(container.querySelectorAll('script'));
            scripts.forEach(script => {
                const newScript = document.createElement('script');
                if (script.src) {
                    newScript.src = script.src;
                    document.head.appendChild(newScript);
                    newScript.onload = () => document.head.removeChild(newScript);
                } else {
                    newScript.textContent = script.innerText;
                    document.head.appendChild(newScript);
                    document.head.removeChild(newScript); // Remove after execution
                }
            });

            // Ensure the graph display function is only called when necessary
            if (url.endsWith('dashboard')) { // Check if the loaded URL is the dashboard
                DisplayGraph(); // Only call DisplayGraph if the dashboard is loaded
            }
            else if(url.endsWith('users')){
                renderRecord();
            }
            else if(url.endsWith('products')){
                renderProduct();
            }
            else if(url.endsWith('categories')){
                renderCategory();
            }
            else if(url.endsWith('suppliers')){
                renderSuppliers();
            }
            
        } catch (error) {
            console.error('Error:', error);
        }
    }

});
