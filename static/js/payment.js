const video = document.getElementById("qr-video");
const canvasElement = document.getElementById("qr-canvas");
const canvas = canvasElement.getContext("2d");

function startScanner() {
    navigator.mediaDevices.getUserMedia({ video: { facingMode: "environment" } }).then(function(stream) {
        video.srcObject = stream;
        video.setAttribute("playsinline", true);
        video.play();
        requestAnimationFrame(tick);
    });
}

function tick() {
    if (video.readyState === video.HAVE_ENOUGH_DATA) {
        canvasElement.hidden = false;

        canvasElement.height = video.videoHeight;
        canvasElement.width = video.videoWidth;
        canvas.drawImage(video, 0, 0, canvasElement.width, canvasElement.height);

        var imageData = canvas.getImageData(0, 0, canvasElement.width, canvasElement.height);
        var code = jsQR(imageData.data, imageData.width, imageData.height, {
            inversionAttempts: "dontInvert",
        });
        if (code) {
            let qrData = code.data;
            if (qrData.startsWith("bitcoin:")) {
                let address = qrData.split("?")[0].replace("bitcoin:", "");
                document.getElementById("address").value = address;
            } else {
                alert("QR Code não contém um endereço Bitcoin válido");
            }
            stopScanner();
        }
    }
    requestAnimationFrame(tick);
}

function stopScanner() {
    let stream = video.srcObject;
    let tracks = stream.getTracks();

    tracks.forEach(function(track) {
        track.stop();
    });

    video.srcObject = null;
}
