console.log("Script is running .....")
document.querySelector('.cross').style.display = 'none';
document.querySelector('.hamberger').addEventListener("click",()=>{
    document.querySelector('.sidebar').classList.toggle('sidebarGo');
    if(document.querySelector('.sidebar').classList.contains('sidebarGo')){
        document.querySelector('.ham').style.display='inline';
        document.querySelector('.cross').style.display='none';
        aconsole.log("Script is running...");

// Sidebar Logic
const hamburger = document.querySelector('.hamberger');
const sidebar = document.querySelector('.sidebar');
const hamIcon = document.querySelector('.ham');
const crossIcon = document.querySelector('.cross');

hamburger.addEventListener("click", () => {
    sidebar.classList.toggle('sidebarGo');
    
    // Toggle Icons
    if (sidebar.classList.contains('sidebarGo')) {
        // Sidebar is hidden (Desktop default: shown, so this logic depends on CSS state)
        // Adjust logic for Mobile vs Desktop
        if(window.innerWidth <= 900) {
            // Mobile: sidebarGo means SHOWING sidebar
             hamIcon.style.display = 'none';
             crossIcon.style.display = 'inline';
        } else {
             // Desktop: sidebarGo means HIDING sidebar
             hamIcon.style.display = 'inline';
             crossIcon.style.display = 'none';
        }
    } else {
         if(window.innerWidth <= 900) {
             hamIcon.style.display = 'inline';
             crossIcon.style.display = 'none';
        } else {
             hamIcon.style.display = 'none';
             crossIcon.style.display = 'inline';
        }
    }
});

// Fix for icon state on resize
window.addEventListener('resize', () => {
    if(window.innerWidth > 900) {
        sidebar.classList.remove('sidebarGo'); // Always show sidebar on desktop reset
        hamIcon.style.display = 'none';
        crossIcon.style.display = 'inline';
    } else {
        sidebar.classList.remove('sidebarGo'); // Hide by default on mobile reset (check CSS logic)
        // Actually, let's rely on CSS media query for initial state
    }
});

// Typing Effect for Home Page
const typeTarget = document.querySelector('.type-text');
if(typeTarget) {
    const text = "Full Stack Developer & Engineer";
    let i = 0;
    function typeWriter() {
        if (i < text.length) {
            typeTarget.innerHTML += text.charAt(i);
            i++;
            setTimeout(typeWriter, 100);
        }
    }
    setTimeout(typeWriter, 1000);
}
    }
    else{
        document.querySelector('.ham').style.display='none';
        setTimeout(() => {
            document.querySelector('.cross').style.display='inline';
            
        }, 350);
    }
})