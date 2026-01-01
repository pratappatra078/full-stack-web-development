// for fetching links from json
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

// this function is for changing name => icon in smartphone
const togglebtn =document.getElementById("theme-toggle");
const textSpan = togglebtn.querySelector(".text");
const iconSpan = togglebtn.querySelector(".icon");

function updateButton(){
    const isNight =document.body.classList.contains("night");
    if(window.innerWidth <= 768 ){
        iconSpan.textContent = isNight ? "☀️" : "🌙";
    }else{
        textSpan.textContent = isNight ? " Day Mode" : " Night Mode";
    }
}

//toggle theme
togglebtn.addEventListener("click",()=>{
    document.body.classList.toggle("night");
    updateButton();
    localStorage.setItem(
        "theme",
        document.body.classList.contains("night")? "night":"day"
    );
});
//load saved theme from browser
if(localStorage.getItem("theme")==="night"){
    document.body.classList.add("night");
}
updateButton();
window.addEventListener("resize",updateButton)