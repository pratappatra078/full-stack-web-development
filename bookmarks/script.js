fetch("links.json")
    .then(Response => Response.json())
    .then(links =>{
        document.querySelectorAll("a[data-key]").forEach(anchor => {
            const key = anchor.dataset.key;
            if(links[key]){
                anchor.href = links[key];
                anchor.target = "_blank";
            }
        });
    })
    .catch(error => console.error("Error loading links ",error));

document.querySelectorAll(".profile-item, .bookmarks-item").forEach(icon =>{
    icon.addEventListener("mouseenter",()=>{
        icon.style.transform = "scale(1.1)";
        icon.style.boxshadow = "0 6px 14px rgba(0,0,0,0.3)";
    })
    icon.addEventListener("mouseleave",()=>{
        icon.style.transform = "scale(1)";
        icon.style.boxShadow = "none";
    })
})
const togglebtn = document.getElementById("theme-toggle");
togglebtn.addEventListener("click",() =>{
    document.body.classList.toggle("night");
    if(document.body.classList.contains("night")){
        togglebtn.textContent = "☀️ Day Mode";
    }else{
        togglebtn.textContent = "🌙 Night Mode";
    }
});