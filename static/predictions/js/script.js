let video = document.querySelector("#video");
let canvas = document.createElement("canvas")
let image_data;

canvas.width = 640  // 350px
canvas.height = 640    // 200px

console.log("video element:", video);


const constraints = {
    video: {
      width: {
        min: 640,
        ideal: 640,
        max: 640,
      },
      height: {
        min: 640,
        ideal: 640,
        max: 640
      },
      facingMode: 'environment'
    }
  };




document.addEventListener("DOMContentLoaded", function() {
  // Move video querySelector here
  let video = document.querySelector("#video");
  
  if (video) {
      camera();
  }
});

async function camera() {
    

    try {
        let stream = await navigator.mediaDevices.getUserMedia(constraints);
        console.log("Camera stream:", stream);
        
       

        if (video) {
            video.srcObject = stream;
         
        } else {
            console.error("Video element not found.");
        }
    } catch (error) {
        console.error("Error accessing camera:", error);
    }
}


function takecamera() {

    if (!video || !canvas) {
        console.error("Video or canvas element is missing.");
        return;
    }

    let ctx = canvas.getContext('2d');
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height); // ✅ ใช้ video จากตัวแปร global

    var image_data = canvas.toDataURL("image/jpeg"); 


    document.getElementById("takemycamera").value = image_data;
    console.log('ctx',ctx)
    console.log('image_data', image_data)
}









function getCSRFToken() {
  return document.cookie.split("; ")
      .find(row => row.startsWith("csrftoken="))
      ?.split("=")[1];
}


document.getElementById("myForm").addEventListener("submit", async function(event) {
  event.preventDefault();
  
  try {
      await camera();
      console.log("Camera initialized, submitting form...");
      this.submit();  // Actually submit the form
  } catch (error) {
      console.error("Error:", error);
  }
});



document.getElementById("mineForm").addEventListener("submit", function(event) {
  event.preventDefault(); // Prevent form submission

  // Show modal
  let modal = document.getElementById("loadingModal");
  modal.style.display = "flex";

  let loadingText = document.getElementById("loadingText");
  let percentage = 0;
  
  let interval = setInterval(function() {
      percentage += 5; // Increment by 5%
      loadingText.textContent = `Loading... ${percentage}%`;

      if (percentage >= 100) {
          clearInterval(interval);
          setTimeout(() => {
              alert("Upload Complete!");
              modal.style.display = "none"; // Hide modal
          }, 500);
      }
  }, 200); // Update every 200ms
  // Automatically submit the form after taking a photo
  document.getElementById("mineForm").submit();
});









